import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests as r

from dash import Dash, html, dcc, callback, Output, Input, ctx
from config import Settings

# data.loc[data['test_type'] == 'SAT', 'SAT_score'] = sum(data['english_score'], data['math_score']) / 2
# data.loc[data['test_type'] == 'PSAT', 'PSAT_score'] = sum(data['english_score'], data['math_score']) / 2
# data.loc[data['test_type'] == 'ACT', 'ACT_score'] = sum(data['english_score'], data['math_score'], data['reading_score'], data['science_score']) / 4

app = Dash(__name__)

settings = Settings()

response = r.get(f'http://{settings.database_hostname}:{settings.fastapi_port}/students')
data = response.json()
df = pd.DataFrame(data)
# print(df.head())

buttons = html.Div(
    [
        # dbc.Button("Bar chart", id="btn-bar", color="secondary"),
        dbc.Button("Line chart", id="btn-line", color="secondary"),
        dbc.Button("Scatterplot", id="btn-scatter", color="secondary"),
    ],
    className="d-grid gap-2",
)

app.layout = html.Div(
    [
        html.H3("Student data plot with a selectable hover mode"),
        html.P("Select chart type:"),
        dbc.Row([buttons]),
        html.P("Select student:"),
        dcc.RadioItems(
            id="student_dropdown",
            # inline=True,
            options=["All", "Specific Student"], # TODO: figure out how to make this create s dropdown for student
        ),
        html.P("Select hovermode:"),
        dcc.RadioItems(
            id="hovermode",
            inline=True,
            options=["x", "x unified", "closest"],
            value="closest",
        ),
        dcc.Graph(id="graph"),
    ]
)

# TODO: include dbc input group here

@app.callback(
    Output("graph", "figure", allow_duplicate=True),
    Input("btn-line", "n_clicks"),
    Input("btn-scatter", "n_clicks"),
    prevent_initial_call='initial_duplicate'
)
def update_chart_type(btn_bar, btn_line):
    button_id = ctx.triggered_id
    # if button_id is "btn-bar":
    #     fig = px.bar(
    #         df,
    #         x="name",
    #         y="id",
    #         color="student",
    #         title="Hover over points to see the change",
    #     )
    if button_id == "btn-line":
        fig = px.line(
            df,
            x="name",
            y="id",
            # color="name",
            title="Hover over points to see the change",
        )
    if button_id == "btn-scatter":
        fig = px.scatter(
            df,
            x="name",
            y="id",
            # color="name",
            title="Hover over points to see the change",
        )
    
    # fig.update_traces(mode="markers+lines", hovertemplate=None)
    # fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("graph", "figure", allow_duplicate=True),
    Input("hovermode", "value"),
    prevent_initial_call='initial_duplicate'
)
def update_hovermode(mode):
    fig = px.line( # TODO: look into the types of charts
        df,
        x="name",
        y="id",
        color="student",
        title="Hover over points to see the change",
    )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode=mode)
    return fig


if __name__ == "__main__":
    app.run(debug=True)