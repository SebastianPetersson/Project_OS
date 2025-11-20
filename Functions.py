import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import hashlib
import plotly
import plotly.express as px

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
    df = df.drop_duplicates(subset=["Year", "Event", "Medal", "NOC"])

    medals_breakdown = df.groupby(["Year", "NOC"])["Medal"].count().reset_index()
    
    plt.figure(figsize=(14,7))
    sns.barplot(data = medals_breakdown, x = "Year", y = "Medal", hue = "NOC")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Number of Medals")
    plt.xticks(rotation = 45)
    plt.legend(title = "Country Code")
    plt.show()

# Funktion för uppgift 1: Histogram över åldrar
def plot_age_distribution(germany):
    germany_age = germany[germany['Age'].notna()]
    male = germany_age[germany_age['Sex'] == 'M']
    female = germany_age[germany_age['Sex'] == 'F']

    fig, axes = plt.subplots(1, 2, figsize=(12,6), sharey=True)

    sns.histplot(male['Age'], bins=20, kde=True, color='steelblue', ax=axes[0])
    axes[0].set_title('Male athletes')

    sns.histplot(female['Age'], bins=20, kde=True, color='hotpink', ax=axes[1])
    axes[1].set_title('Female athletes')

    for ax in axes:
        ax.set_xlabel('Age')
        ax.set_ylabel('Number of athletes')

    plt.suptitle('Age distribution', fontsize=18)
    plt.tight_layout()

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

def sex_distribution(df1, df2, years):
    """Plots pie charts showing gender distribution for selected Olympic years. Takes 2 dataframes, in this case one for West Germany and one for East Germany."""

    fig, ax = plt.subplots(2, len(years), figsize=(16, 5))
    fig.suptitle("Gender Distribution in Olympic Teams During Germany's Division: East(GDR) vs West(FRG)", fontsize=15, weight = 'bold')

    for i, year in enumerate(years):
        west_data = df1[df1['Year'] == year]['Sex'].value_counts().reindex(['M', 'F'], fill_value=0)
        ax[0, i].pie(west_data, labels=west_data.index, autopct='%1.1f%%',startangle=90, colors=['grey', 'orange'])
        ax[0, i].set_title(f'FRG {year}')

        east_data = df2[df2['Year'] == year]['Sex'].value_counts().reindex(['M', 'F'], fill_value=0)
        ax[1, i].pie(east_data, labels=east_data.index, autopct='%1.1f%%', startangle=90, colors=['grey', 'orange'])
        ax[1, i].set_title(f'GDR {year}')

def sex_dist_all(df1, df2, df3):
    east_sex = df1['Sex'].value_counts()
    west_sex = df2['Sex'].value_counts()
    germany_sex_compare = df3[df3['Year'].between(1956, 1996)] #Tre OS innan och efter splittringen för någorlunda värdig jämförelse

    fig, axes = plt.subplots(1, 3, figsize=(10, 5))
    fig.suptitle('Sex distribution comparison', fontsize=20)
    axes[0].pie(east_sex, labels = west_sex.index, autopct='%1.1f%%', startangle=90, colors = ['grey', 'orange'])
    axes[0].set_title('West Germany (FRG, 1968-1988)')
    axes[1].pie(west_sex, labels = east_sex.index, autopct='%1.1f%%', startangle=90, colors = ['grey', 'orange'])
    axes[1].set_title('East Germany (GDR, 1968-1988)')
    axes[2].pie(germany_sex_compare['Sex'].value_counts(), autopct = '%1.1f%%', startangle=90, colors = ['grey', 'orange'])
    axes[2].set_title('Germany (1956-1996)')
    plt.tight_layout()
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

def age_dist_per_sex(global_df, germany_df, country, sport):
    """Makes a histplot over the chosen sports agespan, one for the chosen countrys male and female contenders, and one for the sports global agespan. \n
    Input a global dataframe, the dataframe for your selected country, the country name, and the chosen sport."""
    
    german_men = germany_df[(germany_df['Sport'] == sport) & (germany_df['Sex'] == 'M')]
    german_females = germany_df[(germany_df['Sport'] == sport) & (germany_df['Sex'] == 'F')]
    global_df = global_df[global_df['Sport'] == sport]
    men_mean = german_men['Age'].mean()
    female_mean = german_females['Age'].mean()
    global_mean = global_df['Age'].mean()

    fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharex=True)
    fig.suptitle(f'{country} - age distribution in {sport}', fontsize=20)

    sns.histplot(data=german_men, x = 'Age', kde=True, stat='percent', bins = 20, color='black', alpha = 0.8, label = 'men', ax = ax[0])
    sns.histplot(data=german_females, x = 'Age', kde=True, stat='percent', bins = 20, color='orange', alpha = 0.5, label = 'women', ax = ax[0])
    ax[0].set(title=f'Agespan for {country} in {sport} - men and females', xlabel='Age',  ylabel='Contenders (percent)')
    ax[0].axvline(men_mean, color = 'black', linestyle = '--', label = f'men mean age: {men_mean:.1f}')
    ax[0].axvline(female_mean, color = 'orange', linestyle = '--', label = f'female mean age: {female_mean:.1f}')
    ax[0].grid(True)
    ax[0].legend()

    sns.histplot(data=global_df, x = 'Age', bins=20, kde=True, stat='percent', color='skyblue', label = 'global age', alpha=0.7, ax=ax[1])
    ax[1].set(title=f'Agespan globally in {sport}', xlabel='Age', ylabel='Contenders (percent)')
    ax[1].axvline(global_mean, color = 'blue', linestyle = '--', label = f'mean age: {global_mean:.1f}')
    ax[1].grid(True)
    ax[1].legend()
    plt.show()

def plot_efficiency(global_df, germany_df, country, sport):
    """Plots the efficiency of the selected countrys contenders in the selected sport, and gives a comparison to the global efficiency. \n
    Input one global dataframe, one dataframe for the country and the selected sport."""

    global_df = global_df[global_df['Sport'] == sport]
    german_men = germany_df[(germany_df['Sport'] == sport) & (germany_df['Sex'] == 'M')]
    german_females = germany_df[(germany_df['Sport'] == sport) & (germany_df['Sex'] == 'F')]

    global_eff = global_df['Medal'].notna().sum() / len(global_df) * 100
    male_eff = german_men['Medal'].notna().sum() / len(german_men) * 100
    female_eff = german_females['Medal'].notna().sum() / len(german_females) * 100

    grouped = pd.DataFrame({
        'Group': ['Germany - Men', 'Germany - Women', 'Global'],
        'Efficiency': [male_eff, female_eff, global_eff]
        })
    fig = px.bar(grouped, x='Group', y='Efficiency', color='Group',
                 text=grouped['Efficiency'].round(1),
                 title=f'{country} - Medal Efficiency in {sport}',
                 labels={'Efficiency': 'Medaljer per 100 deltagare'},
                 color_discrete_sequence=['black', 'orange', 'skyblue'])
    
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[0, max(grouped['Efficiency']) * 1.2])
    fig.show()

def medal_distribution(olympics_df, sport):
    """Makes a barplot for medals, and types of medals, per country for the top 10 countrys in the sport. Includes Germany regardless of performance. \n
     Takes input for dataframe and selected sport."""

    palette = {
        'Gold': "#DABE1E",
        'Silver': '#C0C0C0',
        'Bronze': '#CD7F32'
    }

    df = olympics_df[(olympics_df['Sport'] == sport) & (olympics_df['Medal'].notna())].copy()
    total_medals = df.groupby('NOC').size().sort_values(ascending=False)

    top_nocs = total_medals.head(10).index.tolist()
    if 'GER' not in top_nocs:
        top_nocs.append('GER')
    
    medals = df[df['NOC'].isin(top_nocs)]
    medals = medals.groupby(['NOC', 'Medal']).size().reset_index(name='Count')

    plt.figure(figsize = (12, 6))
    sns.barplot(data = medals, x = 'NOC', y = 'Count', hue = 'Medal', palette = palette)
    plt.title(f"Medal Distribution in {sport} by Country (Olympic History)")
    plt.ylabel("Number of Medals")
    plt.xlabel("Country (NOC)")
    plt.xticks(rotation = 45)
    plt.legend(title = "Medal")
    plt.show()

def visualize_country_stats(df, country):

    country_data = df[df["Team"] == country].copy()

    medal_data = country_data[country_data["Medal"].notna()]
    medal_counts = (
        medal_data.groupby("Sport")["Medal"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize = (14, 6))

    plt.subplot(1, 2, 1)
    sns.barplot(x = medal_counts.values, y = medal_counts.index, color = "steelblue")
    plt.title(f"Topp 10 sporter - medaljfördelning ({country})")
    plt.xlabel("Antal medaljer")
    plt.ylabel("Sport")

    plt.subplot(1, 2, 2)
    sns.histplot(country_data["Age"].dropna(), kde = True, bins = 20, color = "skyblue")
    plt.title(f"Åldersfördelning bland idrottare - {country}")
    plt.xlabel("Ålder")
    plt.ylabel("Antal idrottare")

    plt.tight_layout()
    plt.show()

def visualize_sport_stats(df, sport, top_n = 10):

    sport_data = df[df["Sport"] == sport].copy()

    medal_data = sport_data[sport_data["Medal"].notna()]
    medal_counts = (
        medal_data.groupby("Team")["Medal"]
        .count()
        .sort_values(ascending=False)
        .head(top_n)
    )

    plt.figure(figsize = (14, 6))

    plt.subplot(1, 2, 1)
    sns.barplot(x = medal_counts.values, y = medal_counts.index, color = "steelblue")
    plt.title(f"Topp {top_n} länder - medaljfördelning ({sport})")
    plt.xlabel("Antal medaljer")
    plt.ylabel("Land")

    plt.subplot(1, 2, 2)
    sns.histplot(sport_data["Age"].dropna(), kde = True, bins = 20, color = "skyblue")
    plt.title(f"Åldersfördelning bland idrottare - {sport}")
    plt.xlabel("Ålder")
    plt.ylabel("Antal idrottare")

    plt.tight_layout()
    plt.show()

def plot_participants(df):
    participants = df.groupby(["Year", "NOC", "Season"])["Hash_Names"].nunique().reset_index(name='Participants')

    fig = px.line(participants,
              x = 'Year', 
              y = 'Participants', 
              color = 'NOC', 
              line_dash='Season',
              title='Participants over the years')

    fig.update_layout(
        title={'text' : 'German participants through the years','x':0.5,'xanchor':'center'},
        xaxis_title='År', yaxis_title='Antal deltagare', legend_title='Nation'
    )
    fig.show()