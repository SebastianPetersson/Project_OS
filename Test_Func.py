import pandas as pd
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Anonymisera namn
def hashed_names(olympics_df):
    germany_all = olympics_df[olympics_df["NOC"].isin(["GER", "GDR", "FRG"])].copy()
    germany_all["Name"] = germany_all["Name"].apply(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())
    germany_all = germany_all.rename(columns={"Name": "Hash_Names"}).reset_index(drop=True)
    germany = germany_all[germany_all["NOC"] == "GER"]
    return germany, germany_all

# Topp-sporter
def top_german_sports(germany_df, top_n=10):
    german_medals = germany_df[germany_df["Medal"].notna()].copy()
    medals_per_sport = german_medals.groupby("Sport")["Medal"].count().reset_index()
    top_sports = medals_per_sport.sort_values(by="Medal", ascending=False).head(top_n)
    fig = px.bar(top_sports, x="Sport", y="Medal", color="Sport",
                 color_discrete_sequence=px.colors.sequential.Viridis,
                 title=f"Top {top_n} German Sports by Medal Count")
    return fig, top_sports

# Medaljer per år
def medals_each_year(olympics_df, noc_list, title):
    df = olympics_df[(olympics_df["NOC"].isin(noc_list)) & (olympics_df["Medal"].notna())].copy()
    df = df.drop_duplicates(subset=["Year", "Event", "Medal", "NOC"])
    medals_breakdown = df.groupby(["Year", "NOC"])["Medal"].count().reset_index()
    fig = px.bar(medals_breakdown, x="Year", y="Medal", color="NOC", barmode="group", title=title)
    return fig, medals_breakdown

# Åldersfördelning
def plot_age_distribution(germany):
    germany_age = germany[germany['Age'].notna()]
    male = germany_age[germany_age['Sex'] == 'M']
    female = germany_age[germany_age['Sex'] == 'F']
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Male athletes", "Female athletes"))
    fig.add_trace(go.Histogram(x=male['Age'], nbinsx=20, marker_color='steelblue'), row=1, col=1)
    fig.add_trace(go.Histogram(x=female['Age'], nbinsx=20, marker_color='hotpink'), row=1, col=2)
    fig.update_layout(title_text="Age distribution", showlegend=False)
    return fig

# Summer vs Winter
def summer_vs_winter(olympics_df, noc_list=["GER", "GDR", "FRG"]):
    df = olympics_df[(olympics_df["NOC"].isin(noc_list)) & (olympics_df["Medal"].notna())].copy()
    season_medals = df.groupby("Season")["Medal"].count().reset_index()
    fig = px.bar(season_medals, x="Season", y="Medal", color="Season", title="Summer vs Winter Medals")
    return fig, season_medals

# Könsfördelning FRG vs GDR
def sex_dist_divided(df1, df2, years):
    fig = make_subplots(rows=2, cols=len(years),
                        specs=[[{'type':'domain'}]*len(years)]*2,
                        subplot_titles=[f'FRG {y}' for y in years] + [f'GDR {y}' for y in years])
    for i, year in enumerate(years):
        west = df1[df1['Year']==year]['Sex'].value_counts().reindex(['M','F'], fill_value=0)
        east = df2[df2['Year']==year]['Sex'].value_counts().reindex(['M','F'], fill_value=0)
        fig.add_trace(go.Pie(labels=west.index, values=west.values), row=1, col=i+1)
        fig.add_trace(go.Pie(labels=east.index, values=east.values), row=2, col=i+1)
    return fig

# Könsfördelning alla
def sex_dist_all(df):
    df_west = df[(df['NOC']=='FRG') & (df['Year'].between(1968,1988))]
    df_east = df[(df['NOC']=='GDR') & (df['Year'].between(1968,1988))]
    df_unified = df[(df['NOC']=='GER') & (df['Year'].between(1956,1996))]
    sex_data = {
        'West Germany': df_west['Sex'].value_counts().reindex(['M','F'], fill_value=0),
        'East Germany': df_east['Sex'].value_counts().reindex(['M','F'], fill_value=0),
        'Unified Germany': df_unified['Sex'].value_counts().reindex(['M','F'], fill_value=0)
    }
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}]*3], subplot_titles=list(sex_data.keys()))
    for i,(title,counts) in enumerate(sex_data.items()):
        fig.add_trace(go.Pie(labels=counts.index, values=counts.values), row=1, col=i+1)
    return fig

# Medal distribution weight/height
def medal_distribution_weight_height(df, sport="Ski Jumping"):
    df = df[(df["Sport"]==sport) & (df["Medal"].notna())]
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Weight","Height"))
    fig.add_trace(go.Histogram(x=df["Weight"], nbinsx=15), row=1, col=1)
    fig.add_trace(go.Histogram(x=df["Height"], nbinsx=15), row=1, col=2)
    return fig, df

# Age dist per sex
def age_dist_per_sex(global_df, germany_df, country, sport):
    german_men = germany_df[(germany_df['Sport']==sport)&(germany_df['Sex']=='M')]
    german_women = germany_df[(germany_df['Sport']==sport)&(germany_df['Sex']=='F')]
    global_df = global_df[global_df['Sport']==sport]
    fig = make_subplots(rows=1, cols=2, subplot_titles=[f"{country} {sport}", f"Global {sport}"])
    fig.add_trace(go.Histogram(x=german_men['Age'], name='Men'), row=1, col=1)
    fig.add_trace(go.Histogram(x=german_women['Age'], name='Women'), row=1, col=1)
    fig.add_trace(go.Histogram(x=global_df['Age'], name='Global'), row=1, col=2)
    return fig

# Efficiency
def plot_efficiency(global_df, germany_df, country, sport):
    global_df = global_df[global_df['Sport']==sport]
    german_men = germany_df[(germany_df['Sport']==sport)&(germany_df['Sex']=='M')]
    german_women = germany_df[(germany_df['Sport']==sport)&(germany_df['Sex']=='F')]
    global_eff = global_df['Medal'].notna().sum()/len(global_df)*100
    male_eff = german_men['Medal'].notna().sum()/len(german_men)*100
    female_eff = german_women['Medal'].notna().sum()/len(german_women)*100
    df = pd.DataFrame({'Group':['Men','Women','Global'],
                       'Efficiency':[male_eff,female_eff,global_eff]})
    fig = px.bar(df, x='Group', y='Efficiency', text=df['Efficiency'].round(1))
    return fig

# Medal distribution by country
def medal_distribution(df, sport):
    df = df[(df['Sport']==sport)&(df['Medal'].notna())]
    medals = df.groupby(['NOC','Medal']).size().reset_index(name='Count')
    fig = px.bar(medals, x='NOC', y='Count', color='Medal', barmode='stack')
    return fig, medals

# Stats for country
def stats_for_country(df, country):
    country_data = df[df["Team"]==country]
    medal_data = country_data[country_data["Medal"].notna()]
    medal_counts = medal_data.groupby("Sport")["Medal"].count().sort_values(ascending=False).head(10)
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Top sports","Age distribution"))
    fig.add_trace(go.Histogram(x=country_data["Age"].dropna(), nbinsx=20), row=1, col=2)
    return fig, medal_counts

# Stats for sport
def stats_for_sport(df, sport, top_n=10):
    sport_data = df[df["Sport"]==sport]
    medal_data = sport_data[sport_data["Medal"].notna()]
    medal_counts = medal_data.groupby("Team")["Medal"].count().sort_values(ascending=False).head(top_n)
    fig = make_subplots(rows=1, cols=2, subplot_titles=(f"Top {top_n} countries in {sport}", f"Age distribution in {sport}"))
    fig.add_trace(go.Bar(x=medal_counts.values, y=medal_counts.index, orientation='h'), row=1, col=1)
    fig.add_trace(go.Histogram(x=sport_data["Age"].dropna(), nbinsx=20), row=1, col=2)
    return fig, medal_counts

# Participants over time
def plot_participants(df):
    participants = df.groupby(["Year","NOC","Season"])["Hash_Names"].nunique().reset_index(name="Participants")
    fig = px.line(participants, x="Year", y="Participants", color="NOC", line_dash="Season",
                  title="German participants through the years")
    return fig, participants
