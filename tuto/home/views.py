from django.shortcuts import render
from django.http import HttpResponse


from home.exemple.fct_utiles import *
from home.exemple.colles_salles import *

#from home.global_vars import *

import ortools
import time
import csv
from itertools import combinations
from ortools.linear_solver import pywraplp
#from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
import locale
import sys


#from time import strptime
#from datetime import time, timedelta, date, datetime



# Create your views here.
def index(request):
    return render(request, 'index.html')

def colloscope(request,colloscope_id):
    data = {'colloscope_id': colloscope_id}
    PROBLEMS_ROOT = 'localhost/CollesAZ/contraintes'

    data['root'] =PROBLEMS_ROOT
    semaines = range(1,27)

    mid = len(groupes) // 2 + len(groupes) % 2 

    esh = [c for c in colles if c[0] == "ESH"]
    maths = [c for c in colles if c[0] == "Maths"]
    anglais = [c for c in colles if c[0] == "Anglais"]
    espagnol = [c for c in colles if c[0] == "Espagnol"]
    allemand = [c for c in colles if c[0] == "Allemand"]
    francais = [c for c in colles if c[0] == "Lettres"]
    philo = [c for c in colles if c[0] == "Philo"]
    td = [c for c in colles if c[0] == "TDMaths"]
    info = [c for c in colles if c[0] == "TDinfo"]




    solver = pywraplp.Solver('collotron', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    colloscope = {(c, s, g): solver.BoolVar("colloscope" + "".join(c) + "S"+str(s) + "G" + g) 
                for c in maths + esh + anglais + espagnol + allemand + francais + philo + td + info
                for s in semaines 
                for g in groupes}

    for s in semaines:
        # Nombre de colles et TP par semaine
        for g in groupes:
            solver.Add(sum(colloscope[(c, s, g)] for c in esh+maths) == 1)
            solver.Add(sum(colloscope[(c, s, g)] for c in td) == 1)
            solver.Add(sum(colloscope[(c, s, g)] for c in anglais) <= 1) #?
            solver.Add(sum(colloscope[(c, s, g)] for c in espagnol + allemand) <= 1) #?
            solver.Add(sum(colloscope[(c, s, g)] for c in francais+philo) <= 1)
            solver.Add(sum(colloscope[(c, s, g)] for c in esh+maths+anglais+espagnol+allemand+francais+philo) <= 3)

        for g in groupesAll:
            solver.Add(sum(colloscope[(c, s, g)] for c in espagnol) == 0) #inutile !
            solver.Add(sum(colloscope[(c, s, g)] for c in colles if interfere(c,("CoursAll", "", "Lundi", "13:30", "02:00","")))==0 ) #les allemands ne peuvent pas venir en TD maths le lundi matin

        for g in groupesLR:
            solver.Add(sum(colloscope[(c, s, g)] for c in esh+maths+anglais+francais+philo if interfere(c,("CoursLR", "", "Mercredi", "14:30", "05:00","")))==0 ) #les allemands ne peuvent pas venir en TD maths le lundi matin

        for g in groupesEsp:
            solver.Add(sum(colloscope[(c, s, g)] for c in allemand) == 0) # inutile !

        # nombre de groupes pour chaque créneau (au plus un pour les colles, au plus ? pour les TP d"info pas nécessaire-> ajouter TD maths)
        for c in  maths + esh + anglais + espagnol + allemand + francais + philo :
            solver.Add(sum(colloscope[(c, s, g)] for g in groupes) <= 1)
        for c in  info:
            solver.Add(sum(colloscope[(c, s, g)] for g in groupes) <= mid)
        for c in  td:
            solver.Add(sum(colloscope[(c, s, g)] for g in groupes) <= mid+1)
    
    
    # Les colles ne doivent pas se chevaucher
        for c1, c2 in combinations(colles, 2):
            if c1[0] != c2[0] and interfere(c1, c2):
                for g in groupes:
                    solver.Add(colloscope[(c1, s, g)] + colloscope[(c2, s, g)] <= 1)
            
    # imposer une heure quinzaine
    for s in semaines[:-1]:
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in maths ) == 1)
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in esh ) == 1)
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in info ) == 1)
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in francais+philo ) == 1)


    for s in semaines[2:-1]:
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in anglais ) == 1)      
        for g in groupesEsp:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in espagnol ) == 1)
        for g in groupesAll:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(2) for c in allemand ) == 1)
        for g in groupes:
            solver.Add(sum(colloscope[(c, s , g)] for c in anglais + espagnol + allemand ) == 1)

    # imposer une heure / 4semaines
    for s in semaines[:-3]:
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(4) for c in francais ) >= 1)

    # gerer alternance philo imposer une heure / 4semaines
    for s in semaines[:-5]:
        for g in groupes:
            solver.Add(sum(colloscope[(c, s + j, g)] for j in range(6) for c in philo ) >= 1)

    for s in semaines:
        if s<=fin_semestre:
            solver.Add(sum(colloscope[(c, s , g)] for g in groupes for c in colles if (c[1]=="Mme Molinier" and c[2]=="Lundi") ) == 0)
        else:
            solver.Add(sum(colloscope[(c, s , g)] for g in groupes for c in colles if c[1]=="Mme Molinier" and c[2]=="Jeudi") == 0)

    Jours=["lundi","Mardi",'Mercredi',"Jeudi",'Vendredi'];
    # gestion des alternances:
    for s in semaines:
        for c in esh:
            if (c[1]!="M. ESCALON" or c[3]!="16:00"):
                solver.Add(sum(colloscope[(c, s, g)] for g in groupes) == 1)    
        for c in anglais:
            if (c[1]!="Mme Doumerc"):
                solver.Add(sum(colloscope[(c, s, g)] for g in groupes) == 1)
        for c in maths:
            if (c[1]!="M. PECHOT" or c[3]!="17:30"):
                solver.Add(sum(colloscope[(c, s, g)] for g in groupes) == 1)     
        for c in espagnol:
            if (c[1]!="Mme Bellaud"):
                solver.Add(sum(colloscope[(c, s, g)] for g in groupes) == 1)
        
        # pas 2 colles de langue le mmême jour 
    # for j in Jours:            
    #     solver.Minimize(sum(colloscope[(c, s, g)] for g in groupes for c in anglais+allemand+espagnol if c[2]==j))
                
    for s in semaines[:-1]:
        solver.Add(sum(colloscope[(c, s+j, g)] for j in range(2) for g in groupes for c in francais if (c[1]=="Mme Slama" and c[3]=="16:00")) == 1)     
        
                

    #solver.Minimize(sum(colloscope[(c, s, g)] for c in colles if c[1]=="M. LACOUR" for g in groupesEsp for s in semaines))

    #solver.Maximize(sum(colloscope[(c, s, g)] for c in colles if (c[0]=="Espagnol" and c[1]!="M. LACOUR") for g in groupesEsp for s in semaines))

    # alternance all
    #lfor s in semainesSansAllJeudi:
    #        solver.Add(sum(colloscope[(colles[20], s, g)] for g in groupesAll) == 0)
    #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme CHESNEAU" and c[2]=="Jeudi" for s in semainesSansAllJeudi for g in groupesAll) == 0)
    #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme CHESNEAU" and c[2]=="Lundi" and c[3]=="15:30" for s in semaines for g in groupesAll) == 26)
    #solver.Minimize(sum(colloscope[(c, s, g)] for c in colles if (c[1] == "Mme CHESNEAU" and c[2]=="Lundi" and c[3]=="17:30") for s in semaines for g in groupesAll))

            
        

    #secouer
    for g in groupes:
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "M. ESCALON" for s in semaines) >= 5)
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "M. CORPRON" for s in semaines) >= 2)
        #
        solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "M. PECHOT" for s in semaines) >= 2)
        solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[0]=="Maths" and c[1] == "M. CHAUFFERT" for s in semaines) >= 2)
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme Doumerc" for s in semaines) >= 3) 
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme Agbezouhlon" for s in semaines) >= 2) 
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme Boutet-Brefort" for s in semaines) >= 2) 
    for g in groupesEsp:    
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme LASSOUED" for s in semaines) >= 1) # pas possible à cause quinzaine
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme RODRIGUES" for s in semaines) >=1) 
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "M LACOUR" for s in semaines) >= 1) 
        solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme GAUVIN" for s in semaines) >= 2) # impossible
        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "M. SCAFI" for s in semaines) >= 2)

        #solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme Slama" for s in semaines) >= 1)
        

    #for g in groupesEsp: 
    #    solver.Add(sum(colloscope[(c, s, g)] for c in colles if c[1] == "Mme Slama" for s in semaines) <=2)


    solver.Minimize(sum(colloscope[(c, s, g)] for c in colles if c[1] == "M. CHAUFFERT" and c[1]== "Lundi" and c[2] == "15:30" for s in semaines for g in groupes))
            
    #############################################
    ##### Fin des contraintes et resolution #####
    #############################################
    tic=time.time()
    #status = solver.Solve()
    toc=time.time()


    #data['status']=status
    data['temps']=toc-tic
    return render(request, 'colloscope.html',data)