#!/usr/bin/env python
# coding:utf-8
"""
Name : findArkCatalogue.py
Author : Aurelia Vasile, MSH, UCA

Created on : 05/10/2023 18:45

"""

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

            url_for_catalog_fromFrbnf = f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.recordid any \"{row['FRBNF_NUM']}\""
            response = requests.request("GET", url_for_catalog_fromFrbnf, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            arkCatalogue = parseXMLGallica('.//mxc:controlfield[@tag="003"]', root)


        elif row['Author'] and row['Title']:
            url_for_catalog_fromtitle_author = f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=(bib.author all \"{row['Author']}\") and (bib.title all \"{row['Title']}\")"
            response = requests.request("GET", url_for_catalog_fromtitle_author, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            arkCatalogue = parseXMLGallica('.//mxc:controlfield[@tag="003"]', root)

        dataFrameCSV.loc[y, 'ARK-Catalogue'] = arkCatalogue


dataFrameCSV.to_csv("data/FRBnF_lot5_cinema.csv", index=False)