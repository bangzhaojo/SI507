import csv
import pandas as pd
import numpy as np


def censusdataDumping():
    """This function merge several census csv files into one csv file."""
    
    censusCounty = pd.read_csv("census_data/census_county.csv")
    censusCounty['GEOID'] = censusCounty['GEOID'].astype(str)
    censusCounty = censusCounty[['ID', 'NAME', 'GEOID']]

    censusIncome = pd.read_csv("census_data/census_income.csv")
    censusIncome['GEOID'] = censusIncome['GEOID'].astype(str)
    censusIncome = censusIncome[['GEOID', 'B19113e1']]

    censusRace = pd.read_csv("census_data/census_race.csv")
    censusRace['GEOID'] = censusRace['GEOID'].astype(str)
    censusRace = censusRace[['GEOID', 'B02001e1', 'B02001e2', 'B02001e3', 'B02001e4', 'B02001e5', 'B02001e6']]

    censusPoverty = pd.read_csv("census_data/census_poverty.csv")
    censusPoverty['GEOID'] = censusPoverty['GEOID'].astype(str)
    censusPoverty = censusPoverty[['GEOID', 'B17001e2']]

    result = censusCounty.merge(censusIncome,on="GEOID")
    print('Merge Income data successfully!')
    result = result.merge(censusRace,on="GEOID")
    print('Merge Race data successfully!')
    result = result.merge(censusPoverty,on="GEOID")
    print('Merge Poverty data successfully!')

    result.to_csv("census_all.csv")


def calculateRatio():
    censusallData = pd.read_csv("census_all.csv")
    total_pop = censusallData['B02001e1']
    white_pop = censusallData['B02001e2']
    black_pop = censusallData['B02001e3']
    asian_pop = censusallData['B02001e5']
    island_pop = censusallData['B02001e6']
    native_pop = censusallData['B02001e4']
    poverty_pop = censusallData['B17001e2']

    total_pop = list(map(float, total_pop))
    white_pop = list(map(float, white_pop))
    black_pop = list(map(float, black_pop))
    asian_pop = list(map(float, asian_pop))
    island_pop = list(map(float, island_pop))
    native_pop = list(map(float, native_pop))
    poverty_pop = list(map(float, poverty_pop))

    ratio_white = np.array(white_pop) / np.array(total_pop)
    ratio_black = np.array(black_pop) / np.array(total_pop)
    ratio_asian = np.array(asian_pop) / np.array(total_pop)
    ratio_island = np.array(island_pop) / np.array(total_pop)
    ratio_native = np.array(native_pop) / np.array(total_pop)
    ratio_poverty = np.array(poverty_pop) / np.array(total_pop)

    censusallData['ratio_white'] = ratio_white
    censusallData['ratio_black'] = ratio_black
    censusallData['ratio_asian'] = ratio_asian
    censusallData['ratio_island'] = ratio_island
    censusallData['ratio_native'] = ratio_native
    censusallData['ratio_poverty'] = ratio_poverty
    censusallData['ratio_other'] = 1 - ratio_white - ratio_black - ratio_asian - ratio_island - ratio_native

    censusallData.to_csv("census_all.csv", mode = "w")
    print("calculation Done!")
    
calculateRatio()

