import pandas as pd
import hashlib

def load_and_clean_data():
    olympics = pd.read_csv("athlete_events.csv")
    noc = pd.read_csv("noc_regions.csv")
    olympics = olympics.merge(noc, on = "NOC", how = "left")

    olympics = olympics.dropna(subset=['NOC', 'region', 'Name']) #Tar bort alla rader där någon av NOC, region eller name saknas. SE ÖVER DATARENSNING! //Seb

    olympics['Hash_Names'] = olympics['Name'].apply(lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest())

    germany_all = olympics[olympics['NOC'].isin(['GER', 'FRG', 'GDR'])].copy()
    germany = germany_all[germany_all['NOC'] == 'GER'].copy()

    return olympics, germany_all, germany