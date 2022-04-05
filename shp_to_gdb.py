# -*- coding: cp1252 -*-
"""
# ---------------------------------------------------------------------------
# Name : shp_to_gdb
# Created on: 05/04/2022
# Author: VIGAN Jéros
# Usage: 
# Description: Ce script permet de convertir mutliples classe d'entités vers géodatabase
# ---------------------------------------------------------------------------
"""

#------------------------------
# Importation des packages de travail
#------------------------------
import arcpy
import os, re
import time , datetime

#------------------------------
# Fonctions
#------------------------------

#Fonction d'affichage des couches dans un dossier ou geodatabase
def affiche_couches():
    liste_couches=arcpy.ListFeatureClasses()
    print(" ...Liste des couches presents dans ce workspace....\n ")
    c=0
    for couche in liste_couches:
        c+=1
        print(" la classe entite  numero :  "+ str(c)+" est :.... ",couche + "\n" )

#Fonction d'affichage des couches dans un dossier
def affiche_couches_v2(path):
    arcpy.env.workspace=path
    liste_couches=arcpy.ListFeatureClasses('*')
    print("\n...Liste des couches presents dans ce workpsace ....\n ")
    print("\n workspace : "+str(path)+" \n")
    c=0
    for couche in liste_couches:
        c+=1
        print(" la classe entite  numero :  "+ str(c)+" est :.... ",couche + "\n" )
         
#Fonction d'affichage des champs d'une couche
def affiche_champ(feature_classe_or_table):
    list_champ=arcpy.ListFields(feature_classe_or_table)
    print(" ...Liste des champs de cette classe entité : "+ str(feature_classe_or_table)+"\n")
    for champ in list_champ:
        print(champ.name+ " ------ " + champ.type+"\n")
        
#Créer une File GDB
def createFileGDB(path,FileGDB):
    if not arcpy.Exists(os.path.join(path,FileGDB)):
        arcpy.CreateFileGDB_management(path,FileGDB)
        print(arcpy.GetMessages(0))
        print('\n')

#Supprimer une table ou geodatabase
def deleteEntity(path,entity):
    if arcpy.Exists(os.path.join(path,entity)):
        arcpy.Delete_management(os.path.join(path,entity))
        print(arcpy.GetMessages(0))
        print('\n')

#Defintion de la projection
def defineProjetction(path,entity,projection=2145):
    arcpy.DefineProjection_management(os.path.join(path,entity),arcpy.SpatialReference(projection))
    print(arcpy.GetMessages(0))
    print('\n Réference définie est : {}'.format(arcpy.Describe(os.path.join(path,entity)).spatialReference))
    print('\n')

#Fonction d'affichage des couches dans un dossier
def shp_to_gdb(path,outWorkspace):
    arcpy.env.workspace=path
    inFeatures=arcpy.ListFeatureClasses('*')
    arcpy.FeatureClassToGeodatabase_conversion(inFeatures, outWorkspace)
    print(arcpy.GetMessages(0))
    print('\n')
        
#----------------------------------------------
# Declaration du dossier output
#----------------------------------------------
path=r'D:\Navigation\Téléchargements\CoursDistance\13_Arcgis\Arcgis_python\Tp6\out'
deleteEntity(path,'occitanie.gdb')
createFileGDB(path,'occitanie.gdb')
#defineProjetction(path,entity='occitanie.gdb')
outWorkspace=os.path.join(path,'occitanie.gdb')

#----------------------------------------------
# Main (Classe d'entités vers géodatabase)
#----------------------------------------------
#https://desktop.arcgis.com/fr/arcmap/10.3/tools/conversion-toolbox/feature-class-to-geodatabase.htm
repertoire=r'D:\Navigation\Téléchargements\CoursDistance\13_Arcgis\Arcgis_python\Tp6\in'
for path in os.listdir(repertoire):
          affiche_couches_v2(os.path.join(repertoire,path))
          shp_to_gdb(os.path.join(repertoire,path),outWorkspace)
