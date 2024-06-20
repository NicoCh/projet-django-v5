colles = [
    ("ESH", "M. SCAFI", "Lundi", "15:30", "01:20","B 105"),
    ("ESH", "M. SCAFI", "Mercredi", "16:00", "01:20","B 105"),
    ("ESH", "M. CORPRON", "Vendredi", "16:30", "01:00","G 202"), 
    ("ESH", "M. ESCALON", "Mercredi", "14:00", "01:20","G1-105"),
    ("ESH", "M. ESCALON", "Mercredi", "15:00", "01:20","G1-105"),
    ("ESH", "M. ESCALON", "Mercredi", "16:00", "01:20","G1-105"), #1/2h
    ("ESH", "M. ESCALON", "Vendredi", "14:30", "01:20","G1-105"),

    ("Maths", "M. PECHOT", "Vendredi", "15:30", "01:00","G1-103"),
    ("Maths", "M. PECHOT", "Vendredi", "16:30", "01:00","G1-103"),
    ("Maths", "M. PECHOT", "Vendredi", "17:30", "01:00","G1-103"),#•1/2h
    ("Maths", "M. CHAUFFERT", "Vendredi", "15:30", "01:00","G1-206"),
    ("Maths", "M. CHAUFFERT", "Vendredi", "16:30", "01:00","G1-206"),
    ("Maths", "Mme GAUVIN", "Lundi", "14:30", "01:00","G1-105"),# 
    ("Maths", "Mme GAUVIN", "Lundi", "15:30", "01:00","G1-105"),# 
    
    ("Anglais", "Mme Doumerc", "Lundi", "14:00", "01:00","G1-205"), #1/2h
    ("Anglais", "Mme Malayandee", "Mercredi", "15:30", "01:00","G1-107"),
    ("Anglais", "Mme Malayandee", "Mercredi", "16:30", "01:00","G1-107"),
    ("Anglais", "Mme Ferlay", "Jeudi", "16:30", "01:00","G1-107"),
    ("Anglais", "Mme Ferlay", "Jeudi", "17:30", "01:00","G1-107"),
    ("Anglais", "Mme Boutet-Brefort", "Jeudi", "17:30", "01:00","G1-201"),
    ("Anglais", "Mme Radiguer-Hanchett", "Vendredi", "16:30", "01:20","G1-201"),
    
    ("Allemand", "Mme CHESNEAU", "Jeudi", "14:00", "01:00","CDI-202"), 

    ("Espagnol", "Mme RODRIGUES", "Mardi", "17:30", "01:20","G1-201"),
    ("Espagnol", "M LACOUR", "Lundi", "13:10", "01:20","G1-107"),
    ("Espagnol", "M LACOUR", "Lundi", "14:10", "01:20","G1-107"),
    ("Espagnol", "Mme Bellaud", "Mardi", "17:30", "01:00","CDI-202"),#1/2h
    ("Espagnol", "M Altmayer", "Mercredi", "14:00", "01:00","G1-107"),
    ("Espagnol", "M Borg", "Mercredi", "14:00", "01:00","G1-107"),
    
    ("Lettres", "Mme Gallet", "Lundi", "16:10", "01:20","G1-207"), 
    ("Lettres", "Mme Molinier", "Lundi", "17:10", "01:20","G1-201"),#s2
    ("Lettres", "Mme Molinier", "Jeudi", "14:10", "01:00","G1-201"),#s1 - >12 janvier
    ("Lettres", "Mme Slama", "Mercredi", "15:00", "01:00","G1-201"),
    ("Lettres", "Mme Slama", "Mercredi", "16:00", "01:00","G1-201"), # 1/2h

    ("Philo", "Mme Pighetti de Rivasso", "Lundi", "15:30", "01:00","G1-202"),
    ("Philo", "Mme. Courtillé", "Jeudi", "14:30", "01:00","G1-202"), 
    ("Philo", "Mme. Courtillé", "Jeudi", "15:30", "01:00","G1-202"), 
    
    ("TDinfo", "M. CHAUFFERT", "Vendredi", "13:30" , "02:00","F1-203"),

    ("TDMaths", "M. CHAUFFERT", "Lundi", "13:30" , "02:00", "G203"),
    ("TDMaths", "M. CHAUFFERT", "Lundi", "15:30" , "02:00", "G203")
]

trinomes = {
 "ALY Ibtissem" : "C",
 "AUKAULOO Zaki" : "C",
 "BARRIERE Solenn (CHI)" : "C",
 "BASHARAT Kanwal" : "D",
 "BELLANCE Enzo" : "D",
 "BENDOU Enzo" : "F",
 "BOBINEAU Chloé (ALL)" : "A",
 "BROS William" : "G",
 "CAPELLE Simon" : "E",
 "CHAID Chaïmaa" : "G",
 "CHENILCO Yena" : "G",
 "CHUNG Evan" : "H",
 "DAYIF Loubna" : "H",
 "DEVILLE--JASPARD Dyonis" : "H",
 "DHISSI Kerry Tess" : "I",
 "DUBREUIL Leo (ALL)" : "A",
 "DUGOIS Chloé" : "I",
 "DUVERNOY Quentin" : "I",
 "FOLLIN Benjamin (ALL)" : "A",
 "GORACY Lucas" : "J",
 "GUEMNE CHASSEM Sheryl Gaia" : "E",
 "HASSAN Wassim" : "J",
 "JELOUÂLI Maissa" : "J",
 "LE BRUN-JADE Chloe" : "K",
 "LETCHIMY Ïones" : "E",
 "MANDINAUD Anthony (ALL)" : "B",
 "MOUHEB Amelle" : "F",
 "NIELLINI Eloïc (ALL)" : "B",
 "NSAMBU LUMONADIO Menorah (ALL)" : "B",
 "ORGÉ Lilou" : "K",
 "PELO--TRABUC Thalya" : "K",
 "PENOT Nathan (POR)" : "D",
 "PETIT Mathilde" : "L",
 "RADJASAH Aïsha" : "L",
 "RAMASSAMY Aravindharaj" : "L",
 "TAÏBI Jalil" : "M",
 "TURLET BIABIANY Koralyne" : "M",
 "VELHO Tiago" : "F",
 "ZOUITENE Manelle" : "M",
 }

semaines=range(1,27); # 26 semaines de colles

semainesAB= ["B","A","B","A","B", #toussaint, CB
             "B","A","B","A","B","A", # Noel
             "B","A","B","A","B", #hiver + cb
             "B","A","B","A","B", #printemps
             "A","B", #pont
             "B","A","B"]

fin_semestre=12;

pause=[0,5,11,16,21,23]

lundis= ["18/09","25/09","02/10","09/10","16/10",
         "13/11","20/11","27/11","04/12","11/12","18/12",
         "08/01","15/01","22/01","29/01","05/02",
         "04/03","11/03","18/03","25/03","01/04",
         "22/04","29/04",
         "13/05","20/05","27/05"]

#semaines_sans_all=[1,3,5,7,9,11,13,15,17,19] # EC2
#semaines_sans_all=[0,2,4,7,9,11,13,15,17,19] # EC2

eleves = trinomes.keys()

groupes = sorted(list(set(trinomes.values()))) #["A", "B", "C", "D", "E", "F","G", "H"]

groupesAll = ["A","B"]
groupesEsp=list(set(groupes)-set(groupesAll))
groupesLR=["C","D"]