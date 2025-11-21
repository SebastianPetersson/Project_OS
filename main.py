import dash
from dash import Input, Output
from layout import layout, df, germany
import Functions

app = dash.Dash(__name__)
app.layout = layout

@app.callback(
    [Output("age-graph", "figure"),
     Output("sport-stats-graph", "figure"),
     Output("weight-height-graph", "figure")],
    Input("sport-dropdown", "value"),
    Input("Sport-dropdown2", "value")
)

def update_graphs(selected_sport):
    fig11 = Functions.age_dist_per_sex(df, germany, "Germany", selected_sport)
    fig13, _ = Functions.stats_for_sport(df, selected_sport)
    fig14, _ = Functions.medal_distribution_weight_height(df, sport = selected_sport)
    return fig11, fig13, fig14


if __name__ == "__main__":
    app.run(debug = True)