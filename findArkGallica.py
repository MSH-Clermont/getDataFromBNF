#!/usr/bin/env python
# coding:utf-8
"""
Name : findArkGallica.py
Author : Aurelia Vasile, MSH, UCA

Created on : 28/09/2023 18:03

"""
import requests
import csv
import xml.etree.ElementTree as ET
import shutil

import pandas as pd
from scripts.parserBNFxml import parseXMLGallica

shutil.copyfile ("data/ICB_extractAlma.csv", "data/ICB_extractAlma-copy.csv")
#on ouvre le csv dans une dataFrame pour la MAJ du DOI
dataFrameCSV = pd.read_csv("data/ICB_extractAlma.csv", delimiter=",")


with open('data/ICB_extractAlma.csv', newline='') as csvfile:

    fichierlu = csv.DictReader(csvfile)

    for y, row in enumerate(fichierlu):

        url =f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.recordid any \"{row['FRBNF_NUM']}\" and bib.digitized all \"freeAccess\""

        url_titre_auteur = f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=(bib.author all \"{row['Auteur1']}\") and (bib.title all \"{row['Title']}\") and bib.digitized all \"freeAccess\""

        payload = {}
        headers = {}
        arkGallicaFrbnf = ""
        ark_aTesterGallica =""
        arkCatalogue = ""

        if row["FRBNF_oui_non"]== "vrai":
            response = requests.request("GET", url, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)

            arkGallicaFrbnf = parseXMLGallica('.//mxc:subfield[@code="u"]', root)

        else :
            response = requests.request("GET", url_titre_auteur, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            ark_aTesterGallica = parseXMLGallica('.//mxc:subfield[@code="u"]', root)


        dataFrameCSV.loc[y, 'ARK-Gallica'] = arkGallicaFrbnf
        dataFrameCSV.loc[y, 'ARK-Gallica-aTester'] = ark_aTesterGallica


dataFrameCSV.to_csv("data/ICB_extractAlma.csv", index=False)