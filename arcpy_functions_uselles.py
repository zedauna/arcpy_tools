# -*- coding: cp1252 -*-
"""
# ---------------------------------------------------------------------------
# Name : arcpy_functions_uselles.py
# Created on: 04/12/2021
# Author: VIGAN Jéros
# Usage: 
# Description: 
#https://desktop.arcgis.com/fr/arcmap/10.3/tools/data-management-toolbox/an-overview-of-the-data-management-toolbox.htm
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

#Fonction d'affichage des champs d'une couche
def affiche_champ(feature_classe_or_table):
    list_champ=arcpy.ListFields(feature_classe_or_table)
    print(" ...Liste des champs de cette classe entité : "+ str(feature_classe_or_table)+"\n")
    for champ in list_champ:
        print(champ.name+ " ------ " + champ.type+"\n")

#Fonction de gestion de workspace
def verif_repertoire(chemin):
    rep = input('Dans quel répertoire  travailleras tu ?')
    while not os.path.exists(chemin+rep):
        return verif_repertoire(chemin)
    else : 
        print("ce dossier de travail est bien pris en compte. Merci.\n")
        return chemin+rep 

#choix de la couche
def verif_couche():
    liste_couches=arcpy.ListFeatureClasses()
    entite_classe = input('Entre le nom de la classe avec laquelle tu travailleras')
    while entite_classe  not in liste_couches:
        return verif_couche()
    else:
        return entite_classe

#choix de champ de travailler
def verif_champ(entite_classe):
    list_champ=arcpy.ListFields(entite_classe)
    choix_champ = input('Entre le nom du champ avec laquelle tu travailleras')
    while len(arcpy.ListFields(entite_classe,choix_champ))<0:
        return verif_champ(entite_classe)
    else:
        return choix_champ

#ajouter un champ à une couche choisie
def ajout_champ(entite_classe,champ,typ):
    arcpy.AddField_management(entite_classe,champ,typ)
    print(arcpy.GetMessages(0))
    print('\n')
    print (' le champ '+champ + ' a été rajouté dans la classe ' +entite_classe+"\n")

#supprimer un champ d'une couche choisie
def supprime_champ(entite_classe,champ):
    arcpy.DeleteField_management(entite_classe,champ)
    print(arcpy.GetMessages(0))
    print('\n')
    print (' le champ '+champ + ' a été supprimé de la classe ' +entite_classe+"\n")

#calcul des valeurs d'un champ d'une couche choisie
def calcul_champ(entite_classe,champ,formule):
    arcpy.CalculateField_management(entite_classe,champ,formule,"PYTHON")
    print(arcpy.GetMessages(0))
    print('\n')
    print (' le champ '+champ + ' a été modifié avec la formule' + formule+"\n")

#Fonction d'affichage d'une liste
def affiche_singe(list_signe):
    print(" ...Liste des singes de comparaison.... \n")
    for signe in list_signe:
        print("signe ... :"+ signe +"\n")

def verif_signe(list_signe):
    choix_signe = input('Entre votre signe de comparaison')
    while choix_signe  not in list_signe:
        return verif_signe(list_signe)
    else:
        return choix_signe

#Fonction d'affichage  d'une liste
def affiche_selection(list_sellection):
    print(" ...Liste des selections disponibles.... \n")
    for selection in list_sellection:
        print("selection ... :"+ selection+"\n")

def verif_selection(list_sellection):
    choix_selection = input('Entre votre signe de comparaison')
    while choix_selection  not in list_sellection:
        return verif_selection(list_sellection)
    else:
        return choix_selection

#Fonction d'affichage d'un document mxd
def affiche_bloc_mxd():
    mxdSelf = arcpy.mapping.MapDocument("CURRENT")
    blocs = arcpy.mapping.ListDataFrames(mxdSelf)
    nb = len(blocs)
    print(" ...Liste des blocs disponibles.... \n")
    for bloc in blocs:
        print(bloc.name," ",bloc.spatialReference.name+"\n")

def affiche_couche_mxd():
    mxdSelf =  arcpy.mapping.MapDocument("CURRENT")
    couches = arcpy.mapping.ListLayers(mxdSelf)
    print(" ...Liste des couches ouvertes.... \n")
    for couche in couches:
        print(couche.name)
        print(arcpy.Describe(couche).spatialReference.name+"\n")

def affiche_couche_bloc_mxd(n):
    mxdSelf = arcpy.mapping.MapDocument("CURRENT")
    blocs=arcpy.mapping.ListDataFrames(mxdSelf)
    couches = arcpy.mapping.ListLayers(mxdSelf,"",blocs[n])
    print(" ...Liste des couches ouvertes.... \n")
    for couche in couches:
        print(couche.name+"\n")
        print(arcpy.Describe(couche).spatialReference.name+"\n")

def affiche_table_mxd():
    mxdSelf =  arcpy.mapping.MapDocument("CURRENT")
    tables = arcpy.mapping.ListTableViews(mxdSelf)
    print(" ...Liste des couches ouvertes....\n ")
    for table in tables:
        print(table+"\n")

#chaque blocs , affiche les leurs contenus
def affiche_bloc_hierrachie_mxd():
    mxdSelf =  arcpy.mapping.MapDocument("CURRENT")
    blocs = arcpy.mapping.ListDataFrames(mxdSelf)
    nb = len(blocs)
    for i in range(nb):
          mesCouches = arcpy.mapping.ListLayers(mxdSelf,"",blocs[i])
          print("Dans ce bloc :" +blocs[i].name+"\n")
          print("il a  "+str(len( mesCouches))+ " couches \n")
          for couche in mesCouches:
                print(couche.name+"\n")

#nombre de couches vecteur et raster
def affiche_bloc_nombre_mxd():
    mxdSelf =  arcpy.mapping.MapDocument("CURRENT")
    blocs = arcpy.mapping.ListDataFrames(mxdSelf)
    tables = arcpy.mapping.ListTableViews(mxdSelf)

    nb = len(blocs)
    cpt_layer=0
    cpt_raster=0
    cpt_table=0

    for i in range(nb):
        mesCouches = arcpy.mapping.ListLayers(mxdSelf,"",blocs[i])
        print("Dans ce bloc :" +blocs[i].name+"\n")
        print("il a  "+str(len( mesCouches))+ " couches \n")
        for couche in mesCouches:
            if couche.isFeatureLayer:
                cpt_layer+=1
                print(couche.name+"\n")
            if couche.isRasterLayer:
                cpt_raster+=1
            print(couche.datasetName+"\n")

def aff_elements():
    mxdSelf =  arcpy.mapping.MapDocument("CURRENT")
    elts = arcpy.mapping.ListLayoutElements(mxdSelf) 
    for elt in elts: 
        print(elt.name+" -- "+elt.type+"\n")

#Fonction d r des champs d'une couche
def reorder_fields(table, out_table, field_order, add_missing=True):
    """
    Reorders fields in input featureclass/table
    :table:         input table (fc, table, layer, etc)
    :out_table:     output table (fc, table, layer, etc)
    :field_order:   order of fields (objectid, shape not necessary)
    :add_missing:   add missing fields to end if True (leave out if False)
    -> path to output table
    """
    existing_fields = arcpy.ListFields(table)
    existing_field_names = [field.name for field in existing_fields]

    existing_mapping = arcpy.FieldMappings()
    existing_mapping.addTable(table)
    new_mapping = arcpy.FieldMappings()

    def add_mapping(field_name):
        mapping_index = existing_mapping.findFieldMapIndex(field_name)
        # required fields (OBJECTID, etc) will not be in existing mappings
        # they are added automatically
        if mapping_index != -1:
            field_map = existing_mapping.fieldMappings[mapping_index]
            new_mapping.addFieldMap(field_map)

    # add user fields from field_order
    for field_name in field_order:
        if field_name not in existing_field_names:
            raise Exception("Field: {0} not in {1}".format(field_name, table))

        add_mapping(field_name)

    # add missing fields at end
    if add_missing:
        missing_fields = [f for f in existing_field_names if f not in field_order]
        for field_name in missing_fields:
            add_mapping(field_name)
            
    # use merge with single input just to use new field_mappings
    arcpy.Merge_management(table, out_table, new_mapping)
    print(arcpy.GetMessages(0))
    print('\n')
    return out_table

#Fonction de travail
def selectByAttribute1(source,intermediaire,critere,destination):
    arcpy.MakeFeatureLayer_management(source,intermediaire)
    arcpy.SelectLayerByAttribute_management(intermediaire,"NEW_SELECTION",critere)
    arcpy.CopyFeatures_management(intermediaire,destination)
    arcpy.SelectLayerByAttribute_management(intermediaire,"CLEAR_SELECTION")
    print(arcpy.GetMessages(0))
    print('\n')
    print("la couche : "+destination+ " selon votre critere de selection est bien effectuée\n")

def selectByAttribute2(source,critere,destination='ville41_bis'):
    arcpy.Select_analysis(source,destination,critere)
    print(arcpy.GetMessages(0))
    print('\n')
    print("la couche : "+destination+ " selon votre critere de selection est bien effectuée\n")


def selectByLocation(couche1,couche2,intermediaire,destination,condition="WITHIN"):
    arcpy.MakeFeatureLayer_management(couche1,intermediaire)
    arcpy.SelectLayerByLocation_management(intermediaire,condition,couche2)
    arcpy.CopyFeatures_management(intermediaire,destination)
    arcpy.SelectLayerByAttribute_management(intermediaire,"CLEAR_SELECTION")
    print(arcpy.GetMessages(0))
    print('\n')
    print("la couche : "+destination+ " selon votre critere de selection est bien effectuée \n")

def selectByAttribute3(couche,intermediaire,destination,critere1,critere2):
    arcpy.MakeFeatureLayer_management(couche,intermediaire)
    arcpy.SelectLayerByAttribute_management(intermediaire,"NEW_SELECTION",critere1)
    arcpy.SelectLayerByAttribute_management(intermediaire,"SUBSET_SELECTION",critere2)
    arcpy.CopyFeatures_management(intermediaire,destination)
    arcpy.SelectLayerByAttribute_management(intermediaire,"CLEAR_SELECTION")
    print(arcpy.GetMessages(0))
    print('\n')
    print("la couche : "+destination+ " selon votre critere de selection est bien effectuée \n")

#liste des selections existantes 
list_sellection=["WITHIN","INTERSECT","WITHIN_A_DISTANCE","CONTAINS","SHARE_A_LINE_SEGMENT_WITH","HAVE_THEIR_CENTER_IN"]

def verif_selection(list_sellection):
    choix_selection = input('Entre votre signe de comparaison')
    while choix_selection  not in list_sellection:
        return verif_selection(list_sellection)
    else:
        return choix_selection

def jointurePermanente(source,joint_field_1,joint_field_2,table_joint):
    arcpy.MakeFeatureLayer_management(source,source+"_joint")
    arcpy.AddJoin_management(source+"_joint",joint_field_1,table_joint,joint_field_2)
    #arcpy.AddJoin_management(base1, champ 1, base2, champ 2, "KEEP_ALL")
    print(arcpy.GetMessages(0))
    print('\n')
    print("la couche : "+source+"_joint est prête\n")

#https://pro.arcgis.com/fr/pro-app/latest/tool-reference/analysis/spatial-join.htm
def jointureSpatial(target_features, join_features, out_feature_class):
    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class)
    print(arcpy.GetMessages(0))
    print('\n')
    print("la couche : "+source+"_joint est prête\n")
    
#fonction modification
def modif(classe_entite,cible,champ,valeur):
    c1=arcpy.UpdateCursor(classe_entite,cible,None,champ)
    ligne=c1.next()
    ligne.getValue(champ)
    ligne.setValue(champ,valeur)
    c1.updateRow(ligne)
    print("la modification du champ",champ,"doont la cible est :",cible,"dans la classe entité",classe_entite,"a été un succès")

#fonction d'ajouter
def ajout(classe_entite,champ,valeur):
    c1=arcpy.InsertCursor(classe_entite)
    ligne=c1.newRow()
    ligne.setValue(champ,valeur)
    c1.insertRow(ligne) 
    print("l'ajout de la ligne dans le champ",champ,"dans la classe entité",classe_entite,"a été un succès")

#fonction de suppression
def supp(classe_entite,cible):
    c1=arcpy.UpdateCursor(classe_entite)
    ligne=c1.next()
    c1.deleteRow(ligne)
    print("la suppression de la ligne",cible, "dans la classe entité ",classe_entite,"a été un succès")

#fonction recherche
def rech(classe_entite,champ):
    c1=arcpy.SearchCursor(classe_entite)
    for ligne in c1:
        valeur=ligne.getValue(champ)
    print("la recherche du champ",champ, "dans la classe entité ",classe_entite,"a pour valeur",str(valeur))

#----------------------------------------------
# Declaration du dossier de travail (wokspace)
#----------------------------------------------
repertoire
arcpy.env.workspace=repertoire
