import dash
from dash import Input, Output
from layout import layout, olympics, germany
import Functions

app = dash.Dash(__name__)
server = app.server
app.layout = layout

@app.callback(
    [Output("efficiency-graph", "figure"),
     Output("medal-dist-graph", "figure"),
     Output("age-graph", "figure"),
     Output("sport-stats-graph", "figure"),
     Output("weight-height-graph", "figure"),
     Output("gender-and-age", "figure")],
    Input("sport-dropdown", "value"),
)

def update_graphs(selected_sport):
    fig9 = Functions.medal_distribution(olympics, selected_sport)
    fig10 = Functions.age_dist_per_sex(olympics, germany, "Germany", selected_sport)
    fig11 = Functions.plot_efficiency(olympics, germany, "Germany", selected_sport)
    fig12, _ = Functions.stats_for_sport(olympics, selected_sport)
    fig13, _ = Functions.medal_distribution_weight_height(olympics, sport = selected_sport)
    fig14 = Functions.sex_biat(olympics, selected_sport)
    return fig9, fig10, fig11, fig12, fig13, fig14


if __name__ == "__main__":
    app.run(debug = True)