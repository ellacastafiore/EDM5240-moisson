#coding: utf-8

#J'importe les modules requis pour moissonner
import csv
import requests
from bs4 import BeautifulSoup

#Je me crée une variable pour mon url donné

#Mon entête pour savoir qui va foutre son nez dans leurs affaires
entetes = {
    "User-Agent":"Je m'appelle Leïla Jolin-Dahel.",
    "From":"ellacastafiore@gmail.com"
}

urlListe = "https://lobbycanada.gc.ca/eic/site/012.nsf/fra/h_00027.html"  #le dossier parent de url
print("### " + urlListe)

#Pour trouver les liens des rapports, qui sont des html situés dans la section tab2 (rapports), en li dans le code source
srcListe = requests.get(urlListe, headers=entetes)
htmlListe = BeautifulSoup(srcListe.text,"html.parser")
ongletListe = BeautifulSoup(str(htmlListe.find("div", id="tab2")),"html.parser")
rapportsListe = BeautifulSoup(str(ongletListe.find_all("li")),"html.parser")

#Pour ouvrir les liens dans la première page (poupée russe, #lol!)
for rapport in rapportsListe.find_all("a"):
    urlRapport = "https://lobbycanada.gc.ca/eic/site/012.nsf/fra/" + rapport.get("href")
    srcRapport = requests.get(urlRapport, headers=entetes)
    htmlRapport = BeautifulSoup(srcRapport.text,"html.parser")
    tabRapport = BeautifulSoup(str(htmlRapport.find("table", class_="disclosureList")),"html.parser")
    contratsListe = tabRapport.find_all("a")
    print("\n=> " + urlRapport)
    
    #pour aller chercher les url de chaque *#&(&*(& de contrat individuellement 
    for contrat in contratsListe:
        urlContrat = "https://lobbycanada.gc.ca/eic/site/012.nsf/fra/" + contrat.get("href")
        srcContrat = requests.get(urlContrat, headers=entetes)
        htmlContrat = BeautifulSoup(srcContrat.text,"html.parser")
        tabContrat = BeautifulSoup(str(htmlContrat.find("table", class_="disclosureDetails")),"html.parser")
        detailsListe = BeautifulSoup(str(tabContrat.find_all("tr")),"html.parser")
        
        
        #Pour Touteeeeeuh les informations des lobbyeux 
        print("\n=>=>=> " + urlContrat)
        #print(detailsListe)
        
        for details in detailsListe:
            htmlDetails = BeautifulSoup(str(details),"html.parser")
            titreDetails = BeautifulSoup(str(htmlDetails.find("th")),"html.parser")
            valeurDetails = BeautifulSoup(str(htmlDetails.find("td")),"html.parser")
            
            print(str(titreDetails.text) + "\t" + str(valeurDetails.text))