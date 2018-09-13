# -*- coding: utf-8 -*-
# Demo file for Spyder Tutorial
# Hans Fangohr, University of Southampton, UK

import re
import urllib
from bs4 import BeautifulSoup
import csv



def calcMaxPag(nrC, cartier):
    

    url='https://www.imobiliare.ro/vanzare-apartamente/cluj-napoca/'+str(cartier)+'?nrcamere='+str(nrC)
    global maxim
    maxim = 0
    print(url)
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    
    for link in soup.findAll('a', attrs={'data-pagina': re.compile("")}): 
        s = link["data-pagina"]
        if int(s) > maxim:  maxim=int(s)
   
    return maxim



def ApartamenteVanzare(nrC,nrP,cartier):
    
   # nrP = nr paginii in URL
   # nrC = nr de camere din URL
    #if nrP==1: nrP=''
    #else: nrP ='&pagina='+ str(nrP)
    
    url='https://www.imobiliare.ro/vanzare-apartamente/cluj-napoca/'+str(cartier)+'?nrcamere='+str(nrC)+'&pagina='+str(nrP)
    global maxim    
    print(url)
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    #print(soup.prettify())
    
   
    return soup
    

def scrapApartDate(nrC:int, nrP:int, cartier:str):

    soup = ApartamenteVanzare(nrC,cartier)
    i=0 
    for link in soup.findAll('ul', attrs={'class': re.compile("^caracteristici")}): 
        i+=1
        s = str(link)
        for r in (("<li>", ","), ("<ul>", ","),("<span>", ""),
              ("</li>", ""),("</ul>", ""),("</span>", ""),("mp utili", ","),("<ul class=\"caracteristici\">", "")):
            s = s.replace(*r)
        print (i,s)
    
'''
def pret(nrC:int,nrP:int,cartier:str):
    i=0
    soup = ApartamenteVanzare(nrC,nrP,cartier)
    for link in soup.findAll('span', attrs={'class': re.compile("^pret-mare")}):
        i +=1
        pret=link.string
        print (i,pret)
'''


def generateAnuntId(nrC:int, nrP:int, cartier:str):
    
    global maxim
    global j
    j=0
    soup = ApartamenteVanzare(nrC,nrP,cartier)
    print(maxim)
    #print(soup.prettify)
    fisierCSV = 'Id-'+str(nrC)+str(cartier)+'.csv'
    with open(fisierCSV, 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',' , quoting=csv.QUOTE_MINIMAL)
        for link in soup.findAll("div", attrs={'class':re.compile("box-anunt"),'id':re.compile('anunt-')}):
            anId=(link['id'])[6:]
            j +=1
            spamwriter.writerow([j,anId])
            print (j,anId)
        #print (listaAnunturi)  
    return anId
      

def anuntDetailPage(anuntId:str, cartier:str, nrC:int):
    
    global link1
    global link2
    global final

    link1 = ''
    link2 = ''
    final = ''
    
    url= 'https://www.imobiliare.ro/vanzare-apartamente/cluj-napoca/'+cartier+'/apartament-de-vanzare-'+str(nrC)+'-camere-'+str(anuntId)
    #print(url)
    
    r_det = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r_det, "lxml")
    
    
    for link in soup.findAll('div', attrs={'class':'pret first blue'}):
        pret = link.contents[1]
    
    
    final = str(anuntId)+','+str(pret)+','+str(cartier)+','
    
    
    link1 = soup.find("ul", { "class" : "lista-tabelara" })
    link1 = link1.findChildren()
    #print(type(link1))
    
    link2 = soup.find("ul", { "class" : "lista-tabelara mobile-list" })
    link2 = link2.findChildren()
    #print(link2)
    
    
    listR1 = ('Nr. camere:','Suprafaţă utilă:','Suprafaţă construită:',
            'Compartimentare:','Confort:','Etaj:','Nr. bucătării:','Nr. băi:')
    
    listR2 = ('An construcţie:','Structură rezistenţă:','Tip imobil:',
              'Regim înălţime:','Nr. locuri parcare:','Nr. balcoane:')
      
    l1= len(listR1)-1
    l2= len(listR2)-1
    
    
    one = concatColoane(listR1,l1,link1)
    complet = concatColoane(listR2,l2,link2)
    complet = complet.replace('[', '').replace(']', '').replace("'", "").replace('mp', '').replace('(in constructie)', '')
    print(complet)
    
    with open('propertyDetails.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',' , quoting=csv.QUOTE_MINIMAL, quotechar= ' ' 	)
        spamwriter.writerow([complet])

def concatColoane(listR:str, l:int, link:BeautifulSoup):    
    global final
    q = 0
    b = False
    k = 0
    
    while k <= l: 
        if (q <= l):
            for i in link:
                if listR[k] in str(i):
                    value=str(i.next.next.contents)
                    value = value.replace(",", ".")
                    final = final + value + ','
                    b = True
                    q = q + 1
        if (b == False):
            final = final+','  
        k = k + 1
        b = False  
    return final
    
       

def listaParametrii(cartier:str,nrC:int):
    
     fisierCSV = 'Id-'+str(nrC)+str(cartier)+'.csv'    
     with open(fisierCSV, newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',')
         for row in spamreader:
             anunt=str(row[1])
             anuntDetailPage(anunt,cartier,nrC)
             #print(', '.join(row))


def total(nrC:int, cartier:str):

    maxim = 0
    maxim = calcMaxPag(nrC,cartier)
    if maxim != 0:
        print(maxim,cartier)
        for x in range(1, maxim+1):
            generateAnuntId(nrC,x,cartier)
      
        listaParametrii(cartier,nrC)
    

def finalRun():
    
    listaCartiere = ('aeroport','andrei-muresanu','apahida','aurel-vlaicu','baciu','becas',
                     'borhanci','bulgaria','buna-ziua','calea-turzii','campului',
                     'central','cordos','dambul-rotund','europa','faget','gara',
                     'gheorgheni','grigorescu','gruia','hasdeu','horea','industrial',
                     'intre-lacuri','iris','manastur','marasti','p-ta-mihai-viteazul',
                     'periferie','plopilor','semicentral','someseni','sopor','ultracentral','zorilor')
    
    
    for m in range (0,len(listaCartiere)):
       for no in range(1,5):
         total(no, listaCartiere[m])

if __name__ == "__main__":
# main program starts here
    global j
    global final
    global maxim
    
    finalRun()
    
    
    
    #nrP=1
    #curatareLista()
    #ApartamenteVanzare(2,'grigorescu')
    #scrapApartDate(nrC,max,'grigorescu')
    #pret(nrC,nrP,'grigorescu')
    #generateAnuntId(nrC,'grigorescu')
    #anuntDetailPage('XA3510003','grigorescu',4)
    
