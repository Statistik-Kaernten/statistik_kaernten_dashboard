# PREPARE DATA FOR DASHBOARD
import pandas as pd
from streamlit import cache_data
import itertools
import numpy as np

#PANDAS SETTING
pd.options.mode.copy_on_write = True

def fillEmptyFields(df: pd.DataFrame, startingYear: int, endYear: int) -> pd.DataFrame: 

    regions = df['Tourismusregion'].unique()
    combi = getAllCombinations(startingYear, endYear, regions)

    merged_df = pd.merge(combi, df, left_on=['Jahr', 'MonatId', 'Tourismusregion'], right_on=['Jahr', 'MonatId', 'Tourismusregion'], how='left')
    
    merged_df['Ankünfte'] = merged_df['Ankünfte'].fillna(0)
    merged_df['Übernachtungen'] = merged_df['Übernachtungen'].fillna(0)

    return merged_df

def getFullDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    df['Tourismusjahr'] = np.where(
        (df['MonatId'].astype(int) < 11),
       (df['Jahr'] -1).astype(str) + "/" + df['Jahr'].astype(str).str[-2:],
        (df['Jahr']).astype(str) + "/" + (df['Jahr'] + 1).astype(str).str[-2:]
    )
    df['Tourismushalbjahr'] = df['MonatId'].apply(lambda x: 'SHJ' if x >= 5 and x < 11 else 'WHJ')
    df['Date'] = pd.to_datetime(df[['Jahr', 'MonatId']].rename(columns={'Jahr': 'year', 'MonatId': 'month'}).assign(day=1))
    df['Ankünfte'] = 0
    df['Übernachtungen'] = 0
    return df

def getAllCombinations(df: pd.DataFrame) -> pd.DataFrame:
    if 'Herkunft' in df.columns:
        var_col = 'Herkunft'
    elif 'Unterkunft' in df.columns:
        var_col = 'Unterkunft'
    cols = ['Jahr', 'MonatId', 'Tourismusregion', var_col]

    combinations = list(itertools.product(
    df['Jahr'].unique(),
    df['MonatId'].unique(),
    df['Tourismusregion'].unique(),
    df[f'{var_col}'].unique()))

    full_combinations = pd.DataFrame(combinations, columns=cols)

    full_combinations = full_combinations[(full_combinations['Jahr'].astype(int) > 2003) |
    ((full_combinations['Jahr'].astype(int) == 2003) & (full_combinations['MonatId'].astype(int) >= 11))]

    full_combinations = getFullDataFrame(full_combinations)
    monats_df = getMonths()
    new_df = pd.merge(full_combinations, monats_df, how='left', left_on='MonatId', right_on='Id')
    new_df.rename(columns={'Monat': 'MonatId', 'Name': 'Monat'}, inplace=True)
    new_df.drop(columns=['Id'], inplace=True)
    return cols, new_df

def calcDifference(df: pd.DataFrame, distance_for_calc_diff: int) -> pd.DataFrame:
    def sorting(df: pd.DataFrame) -> pd.DataFrame:
        if 'Tourismusregion' in df.columns:      
            if (len(df['Tourismusregion']) != 1):
                if 'Herkunft' in df.columns:
                    df = df.sort_values(['Date', 'Herkunft', 'Tourismusregion'])
                elif 'Unterkunft' in df.columns:
                    df = df.sort_values(['Date', 'Unterkunft', 'Tourismusregion'])
                else:
                    if 'MonatId' in df.columns:
                        df = df.sort_values(['Jahr', 'MonatId', 'Tourismusregion'])
                    elif 'Jahr' in df.columns:
                        df = df.sort_values(['Jahr', 'Tourismusregion'])
                    else:
                        df = df.sort_values(['Tourismusjahr', 'Tourismusregion'])
            else:
                if 'Herkunft' in df.columns:
                    df = df.sort_values(['Date', 'Herkunft'])
                elif 'Unterkunft' in df.columns:
                    df = df.sort_values(['Date', 'Unterkunft'])
                else:
                    if 'MonatId' in df.columns:
                        df = df.sort_values(['Jahr', 'MonatId'])
                    elif 'Jahr' in df.columns:
                        df = df.sort_values(['Jahr'])
                    else:
                        df = df.sort_values(['Tourismusjahr'])
        else:
            if 'Herkunft' in df.columns:
                df = df.sort_values(['Date', 'Herkunft'])
            elif 'Unterkunft' in df.columns:
                df = df.sort_values(['Date', 'Unterkunft'])
            else:
                if 'MonatId' in df.columns:
                    df = df.sort_values(['Jahr', 'MonatId'])
                elif 'Jahr' in df.columns:
                    df = df.sort_values(['Jahr'])
                else:
                    df = df.sort_values(['Tourismusjahr'])
        return df
    
    try:
        max_year = df['Jahr'].max()
        max_month = df[df['Jahr'] == max_year]['MonatId'].max()
    except:
        pass
    # get all combinations and set ankünfte und übernachtungen to zero
    if 'Herkunft' in df.columns or 'Unterkunft' in df.columns:
        cols, all_combinations = getAllCombinations(df)
        existing_combinations = df[cols]
        missing_combinations = all_combinations.merge(existing_combinations, on=cols, how='left', indicator=True)
        missing_combinations = missing_combinations[missing_combinations['_merge'] == 'left_only'].drop('_merge', axis=1)
        df = pd.concat([df, missing_combinations], ignore_index=True)

    #Delte all rows that are larger than MAX(YYYY/MM) in OG df 
    try:
        df = df[
        (df['Jahr'] < max_year) |
        ((df['Jahr'] == max_year) & (df['MonatId'] <= max_month))]
    except:
        pass
    df = sorting(df)
   
    df['Veränderung Ankünfte'] =  round(df['Ankünfte'].pct_change(distance_for_calc_diff).fillna(0) * 100, 2)
    df['Veränderung Ankünfte'] = df['Veränderung Ankünfte'].apply(
                                lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%" if x < 0 else "N/A")

    df['Veränderung Übernachtungen'] = round(df['Übernachtungen'].pct_change(distance_for_calc_diff).fillna(0) * 100, 2)
    df['Veränderung Übernachtungen']  = df['Veränderung Übernachtungen'].apply(
                                lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%" if x < 0 else "N/A")
    
    df['Durchschnittliche Verweildauer'] = round(df['Übernachtungen']/df['Ankünfte'], 2)
    df['Durchschnittliche Verweildauer'] = df['Durchschnittliche Verweildauer'].apply(lambda x: "N/A" if not isinstance(x, float) else x)

    maxTourismusjahr = '2024/25'

    if 'Monat' in df.columns:
        pass
    else:
        df['Veränderung Ankünfte'] = df.apply(lambda row: 'lfd.' if row['Tourismusjahr'] == maxTourismusjahr else row['Veränderung Ankünfte'], axis=1)
        df['Veränderung Übernachtungen'] = df.apply(lambda row: 'lfd.' if row['Tourismusjahr'] == maxTourismusjahr else row['Veränderung Übernachtungen'], axis=1)
        df['Durchschnittliche Verweildauer'] = df.apply(lambda row: 0 if row['Tourismusjahr'] == maxTourismusjahr else row['Durchschnittliche Verweildauer'], axis=1)
    return df

@cache_data                        
def load_data(fileName) -> pd.DataFrame:
    df = pd.read_csv(f'data/{fileName}', sep=';', decimal=',', thousands='.')
    df.rename(columns={'jahr': 'Jahr', 'monat': 'Monat', 'tourismusregion': 'Tourismusregion', 'tourismusjahr': 'Tourismusjahr',
                       'tourismushalbjahr': 'Tourismushalbjahr', 'ankuenfte': 'Ankünfte', 'uebernachtungen': 'Übernachtungen',
                       'unterkunft_6': 'Unterkunft', 'herkunft_1': 'Herkunft', 'id': 'Gkz', 'gemeinde': 'Gemeinde',
                       'bezirk': 'Bezirk', 'nuts3': 'Nuts3', 'bundesland': 'Bundesland', 'geschlecht': 'Geschlecht', 'alter': 'Alter',
                       'pop': 'Anzahl'}, inplace=True)
    return df

def getSelectionItems() -> pd.DataFrame:
    df = load_data('l_gkz.csv')
    df = df[df['Gkz'] != 99999]
    return df

def getGkz(col: str, region: str) -> list[str]:
    df = getSelectionItems()
    df = df[df[col]==region]
    return df['Gkz'].tolist()

def filter_gkz(df: pd.DataFrame, first_choice: str, second_choice: str) -> pd.DataFrame:
    try:
        return df[df['Gkz'].isin(getGkz(first_choice, second_choice))]
    except:
        return df
    
def getMonths() -> pd.DataFrame:
    monats_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    monats_name = ['Jänner', 'Feber', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    data = {'Id': monats_order, 'Name': monats_name}
    monats_df = pd.DataFrame(data)
    return monats_df
    
def addMonthNames(df: pd.DataFrame) -> pd.DataFrame:
    monats_df = getMonths()
    new_df = pd.merge(df, monats_df, how='left', left_on='Monat', right_on='Id')
    new_df.rename(columns={'Monat': 'MonatId', 'Name': 'Monat'}, inplace=True)
    new_df.drop(columns=['Id'], inplace=True)
    return new_df

def getSubRegion(columnName: str) -> list[str]:
    df = getSelectionItems()
    reList: list[str] = df[columnName].tolist()
    reList = list(set(reList))
    reList = sorted(reList)
    return reList

def getList(df: pd.DataFrame, param: str) -> list[str]:
    if df is None:
        if (param == 'Unterkunftsarten'):
            df = load_data('t_tourismus4.csv')
            return_list = sorted(list(set(df['Unterkunft'])))
            return_list.remove('Gewerbl. Beherb.betriebe 5*/4*/4* Superior')
            return return_list
    else:
        if (param == 'Herkunftsländern'):
            return sorted(list(set(df['Herkunft'])))
        elif (param == 'Unterkunftsarten'):
            return sorted(list(set(df['Unterkunft'])))
        else:
            return list(-1)

def sep_regions(df: pd.DataFrame, second_choice: str) -> pd.DataFrame:
    if (second_choice == 'Alle Tourismusregionen'):
        df = df
    elif (second_choice != 'Ganz Kärnten'):
        df = df[df['Tourismusregion'] == second_choice]
    return df

def filterTourismusjahr(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    start2 = str(start+1)[2:]
    end2 = str(end-1)
    end = str(end)[2:]
    df = df[df['Tourismusjahr'] >= f'{start}/{start2}']
    df = df[df['Tourismusjahr'] <= f'{end2}/{end}']
    return df

def filterJahr(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    df = df[df['Jahr'].astype(int) >= start]
    df = df[df['Jahr'].astype(int) <= end]
    return df

def getGemeindeListe(select: str):
    gkz = getSelectionItems()
    return gkz[gkz['Tourismusregion'] == select]['Gemeinde']

def get_data(param: str, start: int, end: int, first_choice: str, second_choice: str = 'Kärnten-Mitte', zaehlstelle: str = None, selectRegioLst: list = None, selectMonatLst: list = None) -> pd.DataFrame:
    df: pd.DataFrame = load_data(param)
    if selectRegioLst is not None and len(selectRegioLst) == 0:
        if selectMonatLst is not None and len(selectMonatLst) > 0:
            month = getMonths()
            month = month[month['Name'].isin(selectMonatLst)]['Id'].astype(int).tolist()
            df = df[df['Monat'].isin(month)]
    elif selectRegioLst is not None and len(selectRegioLst) != 0:
        df = df[df['Tourismusregion'].isin(selectRegioLst)]
        if selectMonatLst is not None and len(selectMonatLst) > 0:
            month = getMonths()
            month = month[month['Name'].isin(selectMonatLst)]['Id'].astype(int).tolist()
            df = df[df['Monat'].isin(month)]

    else:
        if (param == 't_tourismus1.csv'):
            df = sep_regions(df, second_choice)
            df = addMonthNames(df)
            df = filterTourismusjahr(df, start, end)

        elif (param == 't_tourismus2.csv' or param == 't_tourismus3.csv'):
            df = sep_regions(df, second_choice)
            df = addMonthNames(df)
            df['Date'] = pd.to_datetime(df[['Jahr', 'MonatId']].rename(columns={'Jahr': 'year', 'MonatId': 'month'}).assign(day=1))
            
            df = df[df['Jahr'] >= start]
            df = df[df['Jahr'] <= end]
            if (second_choice == 'Ganz Kärnten' and param == 't_tourismus2.csv'):
                df = df[['Jahr', 'Monat', 'MonatId', 'Date', 'Tourismusjahr', 'Tourismushalbjahr', 'Herkunft', 'Ankünfte', 'Übernachtungen']]
                df = df.groupby(['Jahr', 'Monat', 'MonatId', 'Date', 'Tourismusjahr', 'Tourismushalbjahr', 'Herkunft']).sum().reset_index() 
                df['Tourismusregion'] = 'Ganz Kärnten'
            elif (second_choice == 'Ganz Kärnten' and param == 't_tourismus3.csv'):
                df = df[['Jahr', 'Monat', 'MonatId', 'Date', 'Tourismusjahr', 'Tourismushalbjahr', 'Unterkunft', 'Ankünfte', 'Übernachtungen']]
                df = df.groupby(['Jahr', 'Monat', 'MonatId', 'Date', 'Tourismusjahr', 'Tourismushalbjahr', 'Unterkunft']).sum().reset_index() 
                df['Tourismusregion'] = 'Ganz Kärnten'
            df = df.sort_values('Date')

        if (param == 't_tourismus4.csv'):
            df = filterJahr(df, start, end)
            df = sep_regions(df, second_choice)
            if (second_choice == 'Ganz Kärnten'):
                df['Tourismusregion'] = 'Ganz Kärnten'
                df = df[['Jahr', 'Tourismusregion', 'Tourismushalbjahr', 'Unterkunft', 'Art', 'Anzahl']]
                df = df.groupby(['Jahr', 'Tourismusregion', 'Tourismushalbjahr', 'Unterkunft', 'Art']).sum().reset_index() 
        
        if (param == 't_bev1.csv'):
            df = filterJahr(df, start, end)

    return df

def get_data_with_gkz_list(param: str, start: int, end: int, gkz_list = list[str]) -> pd.DataFrame:
    df: pd.DataFrame = load_data(param)
    if (param == 't_bev1.csv'):
        df = filterJahr(df, start, end)
        df['Altersgruppe'] = df.apply(lambda row: 'A' if row['Alter'] < 15 else 'C' if row['Alter'] > 64 else 'B', axis=1)
    return df

if __name__ == '__main__':
    print(getList(None, 'Unterkunftsarten'))
    pass