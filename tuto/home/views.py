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

    solver = pywraplp.Solver('collotron', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    colloscope = {var: solver.BoolVar(str(var)) for var in contraintes['binaries']}

    #d=data['subjectTo'][0]
    for d in contraintes['subjectTo']:
        if (d['bnds']['ub']!="INT_MAX"):
            solver.Add(sum([colloscope[var['name']]*var['coef'] for var in d['vars']]) <= float(d['bnds']['ub']))
        if (d['bnds']['lb']!="INT_MIN"):
            solver.Add(sum([colloscope[var['name']]*var['coef'] for var in d['vars']]) >= float(d['bnds']['lb']))
        
    tic=time.time()
    status = solver.Solve()
    toc=time.time()

    #print(pywraplp.Solver.OPTIMAL)
    resultats = {}
    for c in colloscope:
        resultats[c]=colloscope[c].solution_value()

    """
    resultats = []
    for c in colloscope:
        if (colloscope[c].solution_value()):
            resultats.append(c)
        #print(c, colloscope[c].solution_value())
    """  
    # Obtenir la date actuelle
    current_date = datetime.now()
    # Préparation des données à écrire dans le fichier JSON
    dataW = {
        'status': status,
        'temps': toc - tic,
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