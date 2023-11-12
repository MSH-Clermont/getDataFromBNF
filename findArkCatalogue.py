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

shutil.copyfile ("data/ICB_extractAlma.csv", "data/ICB_extractAlma-copy.csv")
#on ouvre le csv dans une dataFrame pour la MAJ du DOI
dataFrameCSV = pd.read_csv("data/ICB_extractAlma.csv", delimiter=",")


with open('data/ICB_extractAlma.csv', newline='') as csvfile:

    fichierlu = csv.DictReader(csvfile)

    for y, row in enumerate(fichierlu):

        url_for_catalog_fromFrbnf = f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.recordid any \"{row['FRBNF_NUM']}\""

        url_for_catalog_fromtitle_author = f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=(bib.author all \"{row['Auteur1']}\") and (bib.title all \"{row['Title']}\")"

        payload = {}
        headers = {}

        arkCatalogue = ""

        if row["FRBNF_oui_non"]== "vrai":

            response = requests.request("GET", url_for_catalog_fromFrbnf, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            arkCatalogue = parseXMLGallica('.//mxc:controlfield[@tag="003"]', root)

        else :
            response = requests.request("GET", url_for_catalog_fromtitle_author, headers=headers, data=payload)
            root = ET.fromstringlist(response.text)
            arkCatalogue = parseXMLGallica('.//mxc:controlfield[@tag="003"]', root)

        dataFrameCSV.loc[y, 'ARK-Catalogue'] = arkCatalogue


dataFrameCSV.to_csv("data/ICB_extractAlma.csv", index=False)