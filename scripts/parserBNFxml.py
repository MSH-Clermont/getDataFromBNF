#!/usr/bin/env python
# coding:utf-8
"""
Name : parserBNFxml.py
Author : Aurelia Vasile, MSH, UCA

Created on : 05/10/2023 18:49

"""

NAMESPACES = {
            "srw":"http://www.loc.gov/zing/srw/",
            "xmlns":"http://catalogue.bnf.fr/namespaces/InterXMarc",
            "ixm":"http://catalogue.bnf.fr/namespaces/InterXMarc",
            "mn":"http://catalogue.bnf.fr/namespaces/motsnotices",
            "sd":"http://www.loc.gov/zing/srw/diagnostic/",
            "mxc":"info:lc/xmlns/marcxchange-v2"
        }

def parseXMLGallica(path, root):
    global element, arkGallica
    try:
        element = root.find(path, namespaces=NAMESPACES)
        arkGallica = element.text
        return arkGallica
    except :
        print("La ressource n'a pas de lien Gallica ou BNF-Catalogue")
