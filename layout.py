from dash import html, dcc
import pandas as pd
import Functions
from load_data import load_and_clean_data

olympics, germany_all, germany = load_and_clean_data()

fig1, _ = Functions.top_german_sports(germany)
fig2, _ = Functions.medals_each_year(olympics, ["GER", "FRG", "GDR"], "German Olympic Medals per Year")
fig3, _ = Functions.plot_participants(germany_all)
fig4 = Functions.plot_age_distribution(germany)
fig5, _ = Functions.summer_vs_winter(olympics)
fig6 = Functions.sex_dist_divided(germany_all, [1968, 1972, 1980, 1988])
fig7 = Functions.sex_dist_all(olympics)
fig8 = Functions.medal_e_v_ger(olympics[olympics["NOC"] == "GDR"], olympics[olympics["NOC"] == "FRG"])
fig9 = Functions.plot_efficiency(olympics, germany, "Germany", "Ski Jumping")
fig10 = Functions.medal_distribution(olympics, "Ski Jumping")
fig11 = Functions.age_dist_per_sex(olympics, germany, "Germany", "Ski Jumping")
fig12, _ = Functions.stats_for_sport(olympics, "Ski Jumping")
fig13, _ = Functions.medal_distribution_weight_height(olympics, sport = "Ski Jumping")
fig14 = Functions.sex_biat(olympics)


layout = html.Div([
    html.H1("Germany Olympic Performance Dashboard", style = {"textAlign": "center", "fontFamily": "Helvetica", "color": "black"}),

    html.H2("Uppgift 1 - Landstatistik", style = {"fontFamily": "Helvetica", "color": "black"}),

    dcc.Graph(figure = fig1),
    dcc.Graph(figure = fig2),
    dcc.Graph(figure = fig3),
    dcc.Graph(figure = fig4),
    dcc.Graph(figure = fig5),
    dcc.Graph(figure = fig6),
    dcc.Graph(figure = fig7),
    dcc.Graph(figure = fig8),

    html.H2("Uppgift 2 - Sportstatistik", style = {"fontFamily": "Helvetica", "color": "black"}),

    dcc.Dropdown(
        id = "sport-dropdown",
        options = [
            {"label": "Ski Jumping", "value": "Ski Jumping"},
            {"label": "Swimming", "value": "Swimming"},
            {"label": "Biathlon", "value": "Biathlon"},
            {"label": "Football", "value": "Football"},
        ],
        value = "Ski Jumping",
        clearable = False,
        style = {"width": "50%", "margin": "20px auto"}
    ),

    dcc.Graph(id = "efficiency-graph"),
    dcc.Graph(id = "medal-dist-graph"),
    dcc.Graph(id = "age-graph"),
    dcc.Graph(id = "sport-stats-graph"),
    dcc.Graph(id = "weight-height-graph"),
    dcc.Graph(id = "gender-and-age"),
])