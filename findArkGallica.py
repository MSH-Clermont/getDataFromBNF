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

shutil.copyfile ("data/FRBnF_lot5_cinema.csv", "data/FRBnF_lot5_cinema-copy.csv")
#on ouvre le csv dans une dataFrame pour la MAJ du DOI
dataFrameCSV = pd.read_csv("data/FRBnF_lot5_cinema.csv", delimiter=",")


with open('data/FRBnF_lot5_cinema.csv', newline='') as csvfile:

    fichierlu = csv.DictReader(csvfile)

    for y, row in enumerate(fichierlu):
        payload = {}
        headers = {}
        arkGallicaFrbnf = ""
        ark_aTesterGallica = ""
        arkCatalogue = ""

        if row['FRBNF_NUM']:
            url =f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.recordid any \"{row['FRBNF_NUM']}\" and bib.digitized all \"freeAccess\""
            response = requests.request("GET", url, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            arkGallicaFrbnf = parseXMLGallica('.//mxc:subfield[@code="u"]', root)


        elif row['Author'] and row['Title']:
            # auteur sans la date de naissance
            url_titre_auteur = f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=(bib.author all \"{row['Author']}\") and (bib.title all \"{row['Title']}\") and bib.digitized all \"freeAccess\""
            response = requests.request("GET", url_titre_auteur, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            ark_aTesterGallica = parseXMLGallica('.//mxc:subfield[@code="u"]', root)

        dataFrameCSV.loc[y, 'ARK-Gallica'] = arkGallicaFrbnf
        dataFrameCSV.loc[y, 'ARK-Gallica-aTester'] = ark_aTesterGallica

dataFrameCSV.to_csv("data/FRBnF_lot5_cinema.csv", index=False)