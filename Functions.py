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

#Funktion för uppgift 1: De sporter landet fått flest medaljer i.
def top_german_sports(germany_df, top_n = 10, palette = "Blues_d"):
    """Makes a barplot showing which sports that Germany has won the most medals in. It filters the DataFrame
    to include only rows with non-null medals and groups the data by sport. And selects the top N sports."""
    german_medals = germany_df[germany_df["Medal"].notna()].copy()
    medals_per_sport = german_medals.groupby("Sport")["Medal"].count().reset_index()
    top_sports = medals_per_sport.sort_values(by = "Medal", ascending = False).reset_index(drop = True).head(top_n)

    plt.figure(figsize = (12, 6))
    sns.barplot(data = top_sports, x = "Sport", y = "Medal", hue = "Sport", palette = palette, dodge = False)
    plt.title(f"Top {top_n} German Sports by Medal Count")
    plt.ylabel("Number of Medals")
    plt.xlabel("Sport")
    plt.xticks(rotation = 45)
    plt.legend([],[], frameon=False)
    plt.tight_layout()
    plt.show()
    return top_sports

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

#Funktion för Uppgift 1: Skapa fler plots...
def plot_summer_vs_winter(olympics_df, noc_list=["GER", "GDR", "FRG"]):
    """Plots a bar chart comparing summer vs winter olympic medals for given NOC code."""
    df = olympics_df[(olympics_df["NOC"].isin(noc_list)) & (olympics_df["Medal"].notna())].copy()

    season_medals = df.groupby("Season")["Medal"].count().reset_index()

    plt.figure(figsize=(8,4))
    sns.barplot(data = season_medals, x = "Season", y = "Medal", edgecolor = "black", hue = "Season", palette = "tab10")
    plt.title("GER, GDR, FRG - Summer vs Winter Olympic Medals")
    plt.xlabel("Season")
    plt.ylabel("Number of Medals")
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

#Funktion för Uppgift 2: Skapa fler plots...
def medal_distribution_weight_height(olympics_df, sport = "Ski Jumping"):
    """Plots histogram of medal winning athletes based on their weight and height."""
    df = olympics_df[(olympics_df["Sport"] == sport) & (olympics_df["Medal"].notna())].copy()
    fig, axes = plt.subplots(1, 2, figsize = (14, 6))

    sns.histplot(data = df, x = "Weight", bins = 15, ax = axes[0], color = "skyblue")
    axes[0].set_title(f"Medals vs. Weight in {sport}")
    axes[0].set_xlabel("Weight (kg)")
    axes[0].set_ylabel("Number of Medals")

    sns.histplot(data = df, x = "Height", bins = 15, ax = axes[1], color = "lightgreen")
    axes[1].set_title(f"Medals vs. Height in {sport}")
    axes[1].set_xlabel("Height (cm)")
    axes[1].set_ylabel("Number of Medals")

    plt.tight_layout()
    plt.show()