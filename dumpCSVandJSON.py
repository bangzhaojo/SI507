import json
import csv

'''loading the census data'''
censusOri = open('census_all.csv')
censusData = csv.reader(censusOri, delimiter=',')

countyCensus = []

for county in censusData:
    if county[2] == 'ID':  # delete the first row
        continue
    countyDic = {}
    if len(county[2]) == 4:   # make sure that all the fips are in five digits
        countyDic['fip'] = '0' + county[2]
    else:
        countyDic['fip'] = county[2]
    
    countyDic['ratioWhite'] = round(float(county[13][:6]) * 100, 2)
    countyDic['ratioBlack'] = round(float(county[14][:6]) * 100, 2)
    countyDic['ratioAsian'] = round(float(county[15][:6]) * 100, 2)
    countyDic['ratioIsland'] = round(float(county[16][:6]) * 100, 2)
    countyDic['ratioNative'] = round(float(county[17][:6]) * 100, 2)
    countyDic['ratioPoverty'] = round(float(county[18][:6]) * 100, 2)
    countyDic['ratioOther'] = round(float(county[19][:6]) * 100, 2)
    countyCensus.append(countyDic)

# print(countyCensus)

'''Loading the covid JSON file'''
jsonOri = open('covid_19_api_data.json')

covid19Data = json.load(jsonOri)

for county2 in countyCensus:
    for county in covid19Data:
        if county['fips'] == county2['fip']:
            county2['state'] = county['state']
            county2['name'] = county['county']
            if county['metrics']['vaccinationsCompletedRatio']:
                county2['vacRate'] = county['metrics']['vaccinationsCompletedRatio'] * 100
            county2['population'] = county['population']
            if county['actuals']['cases'] and county['actuals']['deaths']:
                county2['caseRate'] = round(float(county['actuals']['cases']) / county['population'] * 100, 2)
                county2['deathRate'] = round(float(county['actuals']['deaths']) / county['population'] * 100, 2)
            else:
                county2['caseRate'] = None
                county2['deathRate'] = None
            break

with open('countyData.json', 'w') as f:
    json.dump(countyCensus, f, indent = 4)

print('Successfully dump ' + str(len(countyCensus)) + ' counties.')