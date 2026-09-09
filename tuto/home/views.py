from django.shortcuts import render
from django.http import HttpResponse


#from home.exemple.fct_utiles import *
#from home.exemple.colles_salles import *

from home.global_vars import *

import json
import ortools
import time
import csv
from itertools import combinations
from ortools.linear_solver import pywraplp
#from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
import locale
import sys
import os

from datetime import datetime

from django.http import JsonResponse, HttpResponse
import requests

def create_date_directory(base_path='results'):
    # Obtenir la date du jour au format aammdd
    today = datetime.now().strftime('%y%m%d')
    # Chemin complet du dossier
    dir_path = os.path.join(base_path, today)
    # Créer le dossier s'il n'existe pas
    os.makedirs(dir_path, exist_ok=True)
    return dir_path
#from time import strptime
#from datetime import time, timedelta, date, datetime



# Create your views here.
def index(request):
    return render(request, 'index.html')


def results(request,id):
    data={'id':id}
    res = os.path.join('media', 'colloscope', 'resultats', f'{id}.json')
    
    # Vérifier si le fichier existe
    if os.path.exists(res):
        # Ouvrir et lire le fichier JSON
        with open(res, 'r') as file:
            data = json.load(file)
        return JsonResponse(data)
    else:
        # Si le fichier n'existe pas, renvoyer une réponse JSON avec un message d'erreur
        return JsonResponse({'error': 'json de résultats non trouvé', 'path': res}, status=404)
    


def colloscope(request,colloscope_id):

    data = {'colloscope_id': colloscope_id}

    # Combiner la base URL avec les paramètres GET
    full_url = f"{PROBLEMS_ROOT}/{colloscope_id}.json"

    """

    with open(full_url, 'r') as file:
        contraintes = json.load(file)

    file.close()
    """    
    response = requests.get(full_url)
    response.raise_for_status()  # Vérifiez les erreurs HTTP
    contraintes = response.json()
    data = {'colloscope_id': full_url}
    #PROBLEMS_ROOT = 'localhost/CollesAZ/contraintes'

    # Chronométré séparément de la résolution (tic/toc plus bas) : SetTimeLimit() ne borne QUE
    # solver.Solve(), pas la construction du modèle ci-dessous (création des variables + boucle
    # d'ajout des contraintes, en pur Python) — sur un problème réel de grande taille, cette
    # construction peut elle-même devenir longue, sans qu'aucune limite ne s'applique. On sépare
    # les deux temps pour savoir lequel domine réellement (voir dataW plus bas).
    tic_construction=time.time()

    solver = pywraplp.Solver('collotron', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    colloscope = {var: solver.BoolVar(str(var)) for var in contraintes['binaries']}

    #d=data['subjectTo'][0]
    for d in contraintes['subjectTo']:
        if (d['bnds']['ub']!="INT_MAX"):
            solver.Add(sum([colloscope[var['name']]*var['coef'] for var in d['vars']]) <= float(d['bnds']['ub']))
        if (d['bnds']['lb']!="INT_MIN"):
            solver.Add(sum([colloscope[var['name']]*var['coef'] for var in d['vars']]) >= float(d['bnds']['lb']))

    toc_construction=time.time()

    # Limite de temps : sans ça, CBC cherche à PROUVER l'optimalité, ce qui peut prendre un temps
    # arbitrairement long sur un problème de cette taille (variables/contraintes binaires) — il
    # vaut largement mieux une bonne solution trouvée en quelques dizaines de secondes qu'une
    # solution "optimale prouvée" après une attente interminable. En millisecondes ; à ajuster
    # selon la patience voulue. Si la limite est atteinte, solver.Solve() renvoie FEASIBLE (1) au
    # lieu de OPTIMAL (0) — déjà géré côté site (js/make_colloscopePythonv3.js) comme "faisable"
    # avec la mention "non prouvé optimal".
    solver.SetTimeLimit(30000)  # 30 secondes

    # Tolérance d'écart (gap) : accepte une solution à 2% maximum de l'optimum théorique plutôt que
    # d'exiger une preuve d'optimalité stricte — sur un problème de cette taille, les derniers % de
    # preuve sont souvent ce qui coûte le plus cher en temps, pour un gain quasi nul en pratique.
    # Testé en local : solver.SetSolverSpecificParametersAsString("ratioGap=...") ne fonctionne PAS
    # avec la version de Cbc installée ici (2.10.7 — message "not supported by Cbc 2.10.7", ignoré
    # silencieusement). MPSolverParameters est l'API portable d'OR-Tools (indépendante du solveur
    # sous-jacent) : testée en local, aucun avertissement.
    # (SetNumThreads(4) a aussi été essayé, mais produit "No match for threads/4" avec cette version
    # de Cbc — effet réel incertain malgré un retour "True", et peu de chances d'aider de toute façon
    # sur un plan PythonAnywhere à un seul cœur : retiré.)
    solver_params = pywraplp.MPSolverParameters()
    solver_params.SetDoubleParam(pywraplp.MPSolverParameters.RELATIVE_MIP_GAP, 0.02)

    tic=time.time()
    status = solver.Solve(solver_params)
    toc=time.time()

    #print(pywraplp.Solver.OPTIMAL)
    """
    resultats = {}
    for c in colloscope:
        resultats[c]=colloscope[c].solution_value()

    """
    resultats = []
    for c in colloscope:
        if (colloscope[c].solution_value()):
            resultats.append(c)
        #print(c, colloscope[c].solution_value())
    
    # Obtenir la date actuelle
    current_date = datetime.now()
    # Préparation des données à écrire dans le fichier JSON
    dataW = {
        'status': status,
        'temps': toc - tic,
        'temps_construction': toc_construction - tic_construction,
        'resultats': resultats,
        'date' : current_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Chemin de base pour les résultats
    base_path = 'media/colloscope/resultats'

    # Créer le dossier pour la date du jour et obtenir le chemin complet
    dir_path = create_date_directory(base_path)

    # Nom du fichier JSON
    file_name = f'{colloscope_id}.json'

    # Chemin complet du fichier JSON
    file_path = os.path.join(base_path, file_name)

    # Écriture des données dans le fichier JSON
    with open(file_path, 'w') as json_file:
        json.dump(dataW, json_file, indent=4)

    data['status']=status
    data['temps']=toc-tic
    data['solver']=solver
    data['dataW']=dataW
    data['path']=file_path

    return render(request, 'colloscope.html',data)