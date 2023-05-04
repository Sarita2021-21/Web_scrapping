import requests
import csv
import pandas
import json



def fetchDataFromAPI(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def readCsvFile():
    data = pandas.read_csv('abn.csv')
    abnNumbers = data['ABN'].to_list()
    return abnNumbers
    
def charityAssociationWebScrapping():
    res = {}
    highest = {'name': None, 'count': 0}
    abnNumbers = readCsvFile()
    for index, abn in enumerate(abnNumbers):
        print(index, abn)
        data = fetchDataFromAPI(f"https://www.acnc.gov.au/api/dynamics/search/charity?search={abn}")
        uuid = (data['results'] and data['results'][0] and data['results'][0]['uuid']) or None
        print(uuid)
        if uuid == None:
            continue
        people = fetchDataFromAPI(f"https://www.acnc.gov.au/api/dynamics/entity/{uuid}")
        responsiblePersons = (people['data']['ResponsiblePersons']) or None
        if responsiblePersons == None:
            continue     
        for y in responsiblePersons:
            if(y['Name'] in res):
                res[y['Name']] = { 'count' : res[y['Name']]['count'] + 1 }
            else:
                res[y['Name']] = { 'count': 1 }
            if(res[y['Name']]['count'] > highest['count']):
                highest = { 'name': y['Name'], 'count' : res[y['Name']]['count']}
            
    print(highest)
                
        
    
charityAssociationWebScrapping()
    
    
    




