# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:14:40 2022

@author: PC de Nicolas
"""
import csv
from fpdf import FPDF
from colles_salles import *

def load_data_from_csv(csv_filepath):
    headings, rows = [], []
    with open(csv_filepath, encoding="utf8") as csv_file:
        for row in csv.reader(csv_file, delimiter="\t"):
            if not headings:  # extracting column names from first row:
                headings = row
            else:
                rows.append(row)
    return headings, rows

class PDF(FPDF):
    def colored_table(self, headings, rows, pause, col_widths=(20,26,14, 8, 11, 6),col_height=4):
        # Colors, line width and bold font:
        self.set_fill_color(255)
        self.set_text_color(0)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.cell(col_widths[0], 6, 'Colloscope ECG1', border=0, align="C", fill=True)
        self.ln()
        #self.set_font(style="B")
 #       for col_width, heading in zip(col_widths, headings):
 #           self.cell(col_width, 7, heading, border=1, align="C", fill=True)
 #       self.ln()
        for line in headings:
            for i in range(5):
                self.cell(col_widths[i], 6, line[i], border=0, align="C", fill=True)
            for j in range(5,len(line)):
                if (j-5 in pause):
                    self.cell(2, 6, ' ', border='R', align="C", fill=False)
                if (len(str(line[j]))>2):
                    self.set_font("helvetica", "B", 5)
                self.cell(col_widths[5], 7, str(line[j]), border=1, align="C", fill=True)
                self.set_font("helvetica", "B", 7)
            self.ln()

#        self.ln()
        self.set_font("helvetica", "B", 7)
        # Color and font restoration:
        #self.set_fill_color(224, 235, 255)
        self.set_fill_color(120, 160, 245)
        #self.switch_bg_color()
        self.set_text_color(0)
        #self.set_font()
        fill = False
        Noir=False
        matiere=rows[0][0]
        changeMat=True
        for row in rows:
            if (matiere!=row[0]):
                changeMat=True
                matiere=row[0]
                self.switch_bg_color()
            if (changeMat):
                #self.set_line_width(0.05)
                if (matiere !='ESH'):
                    self.cell(col_widths[0], 2, '', border='T', align="L", fill=False)
                self.ln()
                changeMat=False
                self.set_line_width(0.3)
                self.cell(col_widths[0], col_height, row[0], border='LTR', align="C", fill=True)
            else:
                self.cell(col_widths[0], col_height, ' ', border='LR', align="C", fill=True)

            for i in range(1,5):
                #self.cell(col_widths[i], 5, row[i], border="LR", align="L", fill=True)
                self.cell(col_widths[i], col_height, row[i], border=1, align="L", fill=True)
            for j in range(5,len(line)):  
                if (j-5 in pause):
                    self.cell(2, col_height, ' ', border='LR', align="C", fill=False)
                if (row[j]==""):
                    Noir=True
                    self.switch_to_black();
                if (len(str(row[j]))>2):
                    self.set_font("helvetica", "B", 4)
                self.cell(col_widths[5], col_height, row[j], border=1, align="C", fill=True)
                self.set_font("helvetica", "B", 7)

                if(Noir):
                    self.switch_from_black()           
            self.ln()

                
    
            fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
    
    bg=0
    def switch_to_black(self):
        self.set_fill_color(40)
    def switch_from_black(self):
        self.bg-=1
        self.switch_bg_color()
    def switch_bg_color(self):
        self.bg+=1
        if(self.bg==1):
            self.set_fill_color(242,134, 131)
        if(self.bg==2):
            self.set_fill_color(180, 255, 120)
        if(self.bg==3):
            self.set_fill_color(255, 234, 160)
        if(self.bg==4):
            self.set_fill_color(255, 214, 120)
        if(self.bg==5):
            self.set_fill_color(87,176, 166)
        if(self.bg==6):
            self.set_fill_color(80,164, 180)
        if(self.bg==7):
            self.set_fill_color(242,134, 131)
        if(self.bg==8):
            self.set_fill_color(232,185, 143)

    def afficher_groupes(self,trinomes,nb_par_ligne=4):
        tri_tri=sorted(trinomes.items(), key=lambda t: t[1])
        #groupes=list({v:k for k,v in trinomes.items()}.keys())       
        #groupes.sort()
        self.set_fill_color(180,180, 255)
        fill_col=False
        groupe=tri_tri[0][1]
        for e in tri_tri:
            if (e[1]!=groupe):
                groupe=e[1]
                fill_col=not fill_col
            self.cell(10, 7, e[1], border=1, align="C", fill=fill_col)
            self.cell(100, 7, e[0], border=1, align="L", fill=fill_col)
            self.ln()
            


#charger les données :

h,r=load_data_from_csv('collotron_ortools_sat2022_09_14_10_45_55.csv')    
    
for row in r:
    row.pop(4)
    
line1=['','','','','']+[s for s in semaines];
line2=['','','','',''] + semainesAB
line3=['','','','',''] + lundis
headings=[line1,line2,line3]
rows=[['untel','A','B'],['autre colleur','C','D'] ]


pdf = PDF(orientation="L", unit="mm", format="A4")
pdf.set_left_margin(15)
pdf.set_top_margin(15)
pdf.set_font("helvetica", "B", 8)
pdf.add_page()
pdf.colored_table(headings,r,pause)

pdf.add_page()
pdf.afficher_groupes(trinomes)

pdf.output("colloscope_v5.pdf")

