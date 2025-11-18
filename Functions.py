import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import hashlib

#Funtion för Uppgift 1: Anonymisera kolumnen med idrottarnas namn.
def hashed_names(olympics_df):
    """Anonymizes the column named 'Names' in the selected column. Input your dataframe as is."""
    germany_all = olympics_df[olympics_df["NOC"].isin(["GER", "GDR", "FRG"])].copy()
    germany_all["Name"] = germany_all["Name"].apply(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())
    germany_all = germany_all.rename(columns = {"Name": "Hash_Names"}).reset_index(drop = True)
    germany = germany_all[germany_all["NOC"] == "GER"]
    return germany, germany_all


#Funktion för Uppgift 1: Antal medaljer per OS.
def medals_each_year(olympics_df, noc_list, title):
    """Makes a barplot over medals won each year. Takes input for dataframe, list of NOC's, and title. """
    df = olympics_df[(olympics_df["NOC"].isin(noc_list)) & (olympics_df["Medal"].notna())].copy()
    medals_breakdown = df.groupby(["Year", "NOC"])["Medal"].count().reset_index()
    
    plt.figure(figsize=(14,7))
    sns.barplot(data = medals_breakdown, x = "Year", y = "Medal", hue = "NOC")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Number of Medals")
    plt.xticks(rotation = 45)
    plt.legend(title = "Country Code")
    plt.show()

#Funktion för Uppgift 2: Medaljfördelning mellan länder i sporterna (Luge).
def medals_per_column(olympics_df, sport, palette = "Set2"):
    """Makes a barplot for medals won per country. Takes input for dataframe, selected sport, and palette."""
    df = olympics_df[(olympics_df["Sport"] == sport) & (olympics_df["Medal"].notna())].copy()
    medals = df.groupby(["NOC", "Medal"]).size().reset_index(name = "Count")
    
    plt.figure(figsize = (12, 6))
    sns.barplot(data = medals, x = "NOC", y = "Count", hue = "Medal", palette = palette)
    plt.title(f"Medal Distribution in {sport} by Country (Olympic History)")
    plt.ylabel("Number of Medals")
    plt.xlabel("Country (NOC)")
    plt.xticks(rotation = 45)
    plt.legend(title = "Medal")
    plt.show()
