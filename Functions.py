import pandas as pd
import hashlib
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#Funktion för Uppgift 1: Anonymisera kolumnen med idrottarnas namn.
def hashed_names(olympics_df):
    """Anonymizes the column named 'Names' in the selected column. Input your dataframe as is."""
    germany_all = olympics_df[olympics_df["NOC"].isin(["GER", "GDR", "FRG"])].copy()
    germany_all["Name"] = germany_all["Name"].apply(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())
    germany_all = germany_all.rename(columns = {"Name": "Hash_Names"}).reset_index(drop = True)
    germany = germany_all[germany_all["NOC"] == "GER"]
    return germany, germany_all

def top_german_sports(germany_df, top_n = 10):
    """Makes a barplot showing which sports that Germany has won the most medals in. It filters the DataFrame
    to include only rows with non-null medals and groups the data by sport. And selects the top N sports."""

    german_medals = germany_df[germany_df["Medal"].notna()].copy()
    medals_per_sport = german_medals.groupby("Sport")["Medal"].count().reset_index()
    top_sports = medals_per_sport.sort_values(by = "Medal", ascending = False).reset_index(drop = True).head(top_n)

    fig = px.bar(
        top_sports,
        x = "Sport",
        y = "Medal",
        color = "Sport",
        color_discrete_sequence = px.colors.sequential.Viridis,
        title = f"Top {top_n} German Sports by Medal Count")
    
    fig.update_layout(xaxis_title = "Sport", yaxis_title = "Number of Medals", legend_title = "", xaxis_tickangle = -45)
    
    return fig, top_sports

#Samuel
def medals_each_year(olympics_df, noc_list, title):
    """Makes a barplot over medals won each year. Takes input for dataframe, list of NOC's, and title. """

    df = olympics_df[(olympics_df["NOC"].isin(noc_list)) & (olympics_df["Medal"].notna())].copy()
    df = df.drop_duplicates(subset = ["Year", "Event", "Medal", "NOC"])

    medals_breakdown = df.groupby(["Year", "NOC"])["Medal"].count().reset_index()

    fig = px.bar(medals_breakdown, x = "Year", y = "Medal", color = "NOC", barmode = "group", title = title, labels = {"Year": "Year", "Medal": "Number of Medals", "NOC": "Country Code"})
    
    fig.update_layout(xaxis_tickangle = -45, legend_title = "Country Code")
    return fig, medals_breakdown

# Funktion för uppgift 1: Histogram över åldrar
def plot_age_distribution(germany):
    df = germany[germany["Age"].notna()]

    male = df[df["Sex"] == "M"]
    female = df[df["Sex"] == "F"]

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Male athletes", "Female athletes"])
    male_fig = px.histogram(male, x="Age", nbins=20, opacity=0.75, color_discrete_sequence=["steelblue"])
    female_fig = px.histogram(female, x="Age", nbins=20, opacity=0.75, color_discrete_sequence=["hotpink"])

    for trace in male_fig.data:
        fig.add_trace(trace, row=1, col=1)

    for trace in female_fig.data:
        fig.add_trace(trace, row=1, col=2)

    fig.update_layout(title="Age distribution", showlegend=False, height=500, width=1000)
    fig.update_xaxes(title="Age")
    fig.update_yaxes(title="Number of athletes", row=1, col=1)

    return fig

#Samuel
def summer_vs_winter(olympics_df, noc_list = ["GER", "GDR", "FRG"]):

    df = olympics_df[(olympics_df["NOC"].isin(noc_list)) & (olympics_df["Medal"].notna())].copy()

    season_medals = df.groupby("Season")["Medal"].count().reset_index()

    fig = px.bar(
        season_medals,
        x = "Season",
        y = "Medal",
        color = "Season",
        color_discrete_sequence = px.colors.qualitative.Set1,
        title="GER, GDR, FRG - Summer vs Winter Olympic Medals",
        labels={"Season": "Season", "Medal": "Number of Medals"}
    )

    fig.update_layout(
        xaxis_title = "Season",
        yaxis_title = "Number of Medals",
        showlegend = False,
        width = 700,
        height = 400)
    return fig, season_medals

#Sebastian
def sex_dist_all(df):
    df_west = df[(df['NOC'] == 'FRG') & (df['Year'].between(1968, 1988))]
    df_east = df[(df['NOC'] == 'GDR') & (df['Year'].between(1968, 1988))]
    df_unified = df[(df['NOC'] == 'GER') & (df['Year'].between(1956, 1996))]

    sex_data = {
        'West Germany (FRG, 1968-1988)': df_west['Sex'].value_counts().reindex(['M', 'F'], fill_value=0),
        'East Germany (GDR, 1968-1988)': df_east['Sex'].value_counts().reindex(['M', 'F'], fill_value=0),
        'Germany (1956-1996)': df_unified['Sex'].value_counts().reindex(['M', 'F'], fill_value=0)
    }

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'domain'}]*3],
        subplot_titles=list(sex_data.keys())
    )
    
    for i, (title, counts) in enumerate(sex_data.items()):
        fig.add_trace(go.Pie(
            labels=counts.index,
            values=counts.values,
            marker_colors=['grey', 'orange'],
            name=title,
            showlegend=True
        ), row=1, col=i+1)

    fig.update_layout(title_text='Gender Distribution Comparison: East (GDR), West (FRG), and Unified Germany.',
                      title_x = 0.5)
    return fig

#Sebastian
def sex_dist_divided(df, years):
    """Creates a 2-row subplot of pie charts showing gender distribution for selected Olympic years. More or less years can be selected."""

    east_germany = df[df['NOC'] == 'GDR'].copy()
    west_germany = df[df['NOC'] == 'FRG'].copy()

    fig = make_subplots(
        rows=2, cols=len(years),
        specs=[[{'type': 'domain'}]*len(years)]*2,
        subplot_titles=[f'FRG {year}' for year in years] + [f'GDR {year}' for year in years]
    )

    for i, year in enumerate(years):
        west_data = west_germany[west_germany['Year'] == year]['Sex'].value_counts().reindex(['M', 'F'], fill_value=0)
        fig.add_trace(go.Pie(
            labels=west_data.index,
            values=west_data.values,
            marker_colors=['grey', 'orange'],
            name=f'FRG {year}',
            showlegend=False
        ), row=1, col=i+1)

        east_data = east_germany[east_germany['Year'] == year]['Sex'].value_counts().reindex(['M', 'F'], fill_value=0)
        fig.add_trace(go.Pie(
            labels=east_data.index,
            values=east_data.values,
            marker_colors=['grey', 'orange'],
            name=f'GDR {year}',
            showlegend=False
        ), row=2, col=i+1)

    fig.update_layout(
        height=600,
        width=300 * len(years),
        title_text="Gender Distribution in Olympic Teams During Germany's Division: East (GDR) vs West (FRG)",
        title_x=0.5
    )
    return fig

#Samuel
def medal_distribution_weight_height(olympics_df, sport="Ski Jumping"):
    """Plots histogram of medal winning athletes based on their weight and height."""

    df = olympics_df[(olympics_df["Sport"] == sport) & (olympics_df["Medal"].notna())].copy()

    fig = make_subplots(rows = 1, cols = 2, subplot_titles = (f"Medals vs. Weight in {sport}",
                                                        f"Medals vs. Height in {sport}"))
    
    weight_hist = go.Histogram(x = df["Weight"], nbinsx = 15, marker_color = "skyblue")
    fig.add_trace(weight_hist, row = 1, col = 1)
    
    height_hist = go.Histogram(x = df["Height"], nbinsx = 15, marker_color="lightgreen")
    fig.add_trace(height_hist, row = 1, col = 2)
    
    fig.update_layout(
        title_text = f"Medal Distribution by Weight and Height in {sport}",
        xaxis_title = "Weight (kg)",
        yaxis_title = "Number of Medals",
        xaxis2_title = "Height (cm)",
        yaxis2_title = "Number of Medals",
        bargap = 0.1,
        showlegend = False,
        width = 1000,
        height = 500
    )
    return fig, df

#Sebastian
def age_dist_per_sex(global_df, germany_df, country, sport):
    """Makes a histplot over the chosen sports agespan, one for the chosen countrys male and female contenders, and one for the sports global agespan. \n
    Input a global dataframe, the dataframe for your selected country, the country name, and the chosen sport."""

    german_men = germany_df[(germany_df['Sport'] == sport) & (germany_df['Sex'] == 'M')]
    german_women = germany_df[(germany_df['Sport'] == sport) & (germany_df['Sex'] == 'F')]
    global_df = global_df[global_df['Sport'] == sport]
    men_mean = german_men['Age'].mean()
    women_mean = german_women['Age'].mean()
    global_mean = global_df['Age'].mean()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            f"{country} – Age Distribution in {sport}",
            f"Global Age Distribution in {sport}"
        ],
        shared_yaxes=True
    )

    fig.add_trace(go.Histogram(x=german_men['Age'], name='Men', nbinsx=20, histnorm='percent', marker_color='black', opacity=0.5,
        hovertemplate='Group=Men<br>Age=%{x}<br>percent=%{y}<extra></extra>'
    ), row=1, col=1)

    fig.add_trace(go.Histogram(x=german_women['Age'], name='Women', nbinsx=20, histnorm='percent', marker_color='orange', opacity=0.5,
        hovertemplate='Group=Women<br>Age=%{x}<br>percent=%{y}<extra></extra>'
    ), row=1, col=1)

    fig.add_trace(go.Histogram(x=global_df['Age'], name='Global', nbinsx=20, histnorm='percent', marker_color='skyblue',
        hovertemplate='Age=%{x}<br>percent=%{y}<extra></extra>'
    ), row=1, col=2)

    #Linjer som visar mean.
    fig.add_vline(x=men_mean, line_dash='dash', line_color='black',
                  annotation_text=f"Men mean: {men_mean:.1f}", annotation_position="top right", row=1, col=1)
    fig.add_vline(x=women_mean, line_dash='dash', line_color='orange',
                  annotation_text=f"Women mean: {women_mean:.1f}", annotation_position="top left", row=1, col=1)
    fig.add_vline(x=global_mean, line_dash='dash', line_color='blue',
                  annotation_text=f"Global mean: {global_mean:.1f}", annotation_position="top right", row=1, col=2)

    fig.update_layout(barmode='overlay', title_text=f"{country} - Age Distribution in {sport}", 
        title_x=0.5,
        height=500,
        width=1000,
        legend_title_text='Group',
        xaxis_title='Age',
        xaxis2_title='Age',
        yaxis_title='Contenders (percent)'
    )

    return fig

#Sebastian #Note: Något skevt händer. Gör en temporär fix längst ned.
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
    return fig

#Sebastian #Note: Något skevt händer även här. Gör en temporät fix längst ned.
def medal_distribution(df, sport): #EGEN note: denna ska göras till dropdown-meny, så att användaren kan välja olika länder!
    """Creates an interactive bar chart of medal counts per country for a given sport using Plotly."""
    palette = {
        'Gold': "#DABE1E",
        'Silver': '#C0C0C0',
        'Bronze': '#CD7F32'
    }

    df = df[(df['Sport'] == sport) & (df['Medal'].notna())].copy()
    total_medals = df.groupby('NOC').size().sort_values(ascending=False)

    top_nocs = total_medals.head(10).index.tolist()
    if 'GER' not in top_nocs:
        top_nocs.append('GER')

    medals = df[df['NOC'].isin(top_nocs)]
    medals = medals.groupby(['NOC', 'Medal']).size().reset_index(name='Count')

    fig = px.bar(
        medals,
        x='NOC',
        y='Count',
        color='Medal',
        color_discrete_map=palette,
        title=f"Medal Distribution in {sport} by Country (Olympic History)",
        labels={'NOC': 'Country (NOC)', 'Count': 'Number of Medals'}
    )

    fig.update_layout(barmode='stack', xaxis_tickangle=-45)
    return fig

#Samuel
def stats_for_country(df, country):

    country_data = df[df["Team"] == country].copy()

    medal_data = country_data[country_data["Medal"].notna()]
    medal_counts = (
        medal_data.groupby("Sport")["Medal"]
        .count()
        .sort_values(ascending = False)
        .head(10))

    fig = make_subplots(
        rows = 1, cols = 2,
        subplot_titles = (f"Topp 10 sporter - medaljfördelning ({country})", 
        f"Åldersfördelning bland idrottare - {country}"))
    
    bar_trace = go.Bar(
        x = medal_counts.values,
        y = medal_counts.index,
        orientation = "h",
        marker_color = "steelblue")
    
    fig.add_trace(bar_trace, row = 1, col = 1)
    
    age_trace = go.Histogram(
        x = country_data["Age"].dropna(),
        nbinsx = 20,
        marker_color = "skyblue")
    
    fig.add_trace(age_trace, row = 1, col = 2)

    fig.update_layout(
        title_text = f"Olympic Stats for {country}",
        xaxis_title = "Antal medaljer",
        yaxis_title = "Sport",
        xaxis2_title = "Ålder",
        yaxis2_title = "Antal idrottare",
        bargap = 0.1,
        showlegend = False,
        width = 1000,
        height = 500)
    
    return fig, medal_counts

#Samuel
def stats_for_sport(df, sport, top_n = 10):

    sport_data = df[df["Sport"] == sport].copy()
 
    medal_data = sport_data[sport_data["Medal"].notna()]
    medal_counts = (
        medal_data.groupby("Team")["Medal"]
        .count()
        .sort_values(ascending = False)
        .head(top_n))
    
    fig = make_subplots(
        rows = 1, cols = 2,
        subplot_titles = (f"Topp {top_n} länder - medaljfördelning ({sport})",
        f"Åldersfördelning bland idrottare - {sport}"))
    
    bar_trace = go.Bar(
        x = medal_counts.values,
        y = medal_counts.index,
        orientation = "h",
        marker_color = "steelblue")
    fig.add_trace(bar_trace, row = 1, col = 1)
    
    age_trace = go.Histogram(
        x = sport_data["Age"].dropna(),
        nbinsx = 20,
        marker_color = "skyblue")
    
    fig.add_trace(age_trace, row = 1, col = 2)

    fig.update_layout(
        title_text = f"Olympic Stats for {sport}",
        xaxis_title = "Antal medaljer",
        yaxis_title = "Land",
        xaxis2_title = "Ålder",
        yaxis2_title = "Antal idrottare",
        bargap = 0.1,
        showlegend = False,
        width = 1000,
        height = 500)
    
    return fig, medal_counts

#Sebastian
def plot_participants(df):
    participants = df.groupby(["Year", "NOC", "Season"])["Hash_Names"].nunique().reset_index(name='Participants')

    fig = px.line(
        participants,
        x='Year',
        y='Participants',
        color='NOC',
        line_dash='Season',
        title='Participants over the years'
    )

    fig.update_layout(
        title={'text': 'German participants through the years', 'x':0.5, 'xanchor':'center'},
        xaxis_title='År',
        yaxis_title='Antal deltagare',
        legend_title='Nation'
    )

    return fig, participants

#Mattias
def medal_e_v_ger(east_germany, west_germany):

    east = east_germany[['Year', 'Medal']].dropna(subset=['Medal'])
    east_medals = east.groupby(['Year','Medal']).size().unstack(fill_value = 0)

    west = west_germany[['Year','Medal']].dropna(subset=['Medal'])
    west_medals = west.groupby(['Year','Medal']).size().unstack(fill_value = 0)

    fallen_years = sorted(set(west_medals.index).union(set(east_medals.index)))
    Dif_medals = ['Gold','Silver','Bronze']

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=[f"{m} Medals" for m in Dif_medals])

    colors = {"East Germany":"green","West Germany":"red"}

    for i, medal in enumerate(Dif_medals):
        plotting = pd.DataFrame({
            "Year": fallen_years,
            "East Germany": east_medals.reindex(fallen_years).get(medal, pd.Series(0, index = fallen_years)).values,
            "West Germany": west_medals.reindex(fallen_years).get(medal, pd.Series(0, index = fallen_years)).values
        })

        medal_molten = plotting.melt(id_vars = "Year", var_name = "Country", value_name = "Number of medals")

        for country in ["East Germany","West Germany"]:
            subset = medal_molten[medal_molten["Country"]==country]
            fig.add_trace(
                go.Bar(x = subset["Year"], y = subset["Number of medals"],
                       name=country, marker_color = colors[country],
                       showlegend=(i == 0)),
                row=1, col=i+1
            )

    fig.update_layout(
        height = 500, width = 1200,
        title_text = "East vs West Germany Medal Comparison",
        barmode = "group",
        xaxis = dict(tickangle = 45),
        xaxis2 = dict(tickangle = 45),
        xaxis3 = dict(tickangle = 45)
    )
    return fig