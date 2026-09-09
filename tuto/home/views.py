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
from ortools.sat.python import cp_model
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

    # Chronométré séparément de la résolution (tic/toc plus bas) : SetTimeLimit()/max_time_in_seconds
    # ne borne QUE solver.Solve(), pas la construction du modèle ci-dessous (création des variables +
    # boucle d'ajout des contraintes, en pur Python) — sur un problème réel de grande taille, cette
    # construction peut elle-même devenir longue, sans qu'aucune limite ne s'applique. On sépare les
    # deux temps pour savoir lequel domine réellement (voir dataW plus bas).
    tic_construction=time.time()

    # Passé de CBC (pywraplp) à CP-SAT (cp_model) : CP-SAT est le solveur de contraintes/MIP hybride
    # d'OR-Tools, spécifiquement réputé (et généralement bien plus rapide que CBC en pratique) sur ce
    # genre de problème — affectation/emploi du temps avec beaucoup de variables binaires et de
    # contraintes de capacité/égalité. Toujours dans le même paquet ortools déjà installé, rien à
    # ajouter. Le format du modèle reçu de PHP (subjectTo/binaries) est INCHANGÉ — seule cette
    # fonction change, rien côté PHP/JS à adapter pour ce point.
    #
    # to_int_bound() : CP-SAT exige des bornes ENTIÈRES (contrairement à CBC/LP qui acceptait du
    # flottant) — le PHP envoie parfois une borne en chaîne ("1") ou avec un petit ajustement flottant
    # hérité de l'ancien solveur LP (ex: valeur+0.05 pour éviter un souci de précision qui ne
    # concernait que les solveurs continus) : round() récupère la valeur entière voulue dans les deux
    # cas, sans avoir besoin de toucher au PHP.
    def to_int_bound(valeur):
        return int(round(float(valeur)))

    model = cp_model.CpModel()
    colloscope = {var: model.NewBoolVar(str(var)) for var in contraintes['binaries']}

    for d in contraintes['subjectTo']:
        expr = sum(colloscope[var['name']] * var['coef'] for var in d['vars'])
        if (d['bnds']['ub']!="INT_MAX"):
            model.Add(expr <= to_int_bound(d['bnds']['ub']))
        if (d['bnds']['lb']!="INT_MIN"):
            model.Add(expr >= to_int_bound(d['bnds']['lb']))

    toc_construction=time.time()

    solver = cp_model.CpSolver()

    # Limite de temps : sans ça, le solveur cherche à PROUVER l'optimalité, ce qui peut prendre un
    # temps arbitrairement long sur un problème de cette taille — il vaut largement mieux une bonne
    # solution trouvée en quelques minutes qu'une solution "optimale prouvée" après une attente
    # interminable. En secondes (pas millisecondes, contrairement à pywraplp.SetTimeLimit) ; à
    # ajuster selon la patience voulue.
    solver.parameters.max_time_in_seconds = 300  # 5 minutes

    # Tolérance d'écart (gap) : accepte une solution à 2% maximum de l'optimum théorique plutôt que
    # d'exiger une preuve d'optimalité stricte — sur un problème de cette taille, les derniers % de
    # preuve sont souvent ce qui coûte le plus cher en temps, pour un gain quasi nul en pratique.
    # Nativement supporté par CP-SAT (contrairement à SetSolverSpecificParametersAsString qui ne
    # fonctionnait pas avec la version de Cbc utilisée avant).
    solver.parameters.relative_gap_limit = 0.02

    # Recherche en parallèle : contrairement à SetNumThreads() côté CBC (qui produisait des erreurs
    # de parsing avec la version installée), num_search_workers est un paramètre CP-SAT natif et
    # fiable. N'aide que si le plan PythonAnywhere alloue plus d'un cœur CPU ; sans effet néfaste
    # sinon.
    solver.parameters.num_search_workers = 4

    tic=time.time()
    status_brut = solver.Solve(model)
    toc=time.time()

    # Traduit le statut CP-SAT (OPTIMAL=4, FEASIBLE=2, INFEASIBLE=3, MODEL_INVALID=1, UNKNOWN=0) vers
    # la même convention numérique que l'ancien solveur pywraplp (OPTIMAL=0, FEASIBLE=1, INFEASIBLE=2,
    # ...) — déjà comprise partout ailleurs (fichier de résultats, js/make_colloscopePythonv3.js) :
    # aucun changement nécessaire côté site pour ce point non plus.
    STATUT_CPSAT_VERS_PYWRAPLP = {
        cp_model.OPTIMAL: 0,
        cp_model.FEASIBLE: 1,
        cp_model.INFEASIBLE: 2,
        cp_model.MODEL_INVALID: 5,
        cp_model.UNKNOWN: 6,
    }
    status = STATUT_CPSAT_VERS_PYWRAPLP.get(status_brut, 6)

    resultats = []
    for c in colloscope:
        if (solver.Value(colloscope[c])):
            resultats.append(c)

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