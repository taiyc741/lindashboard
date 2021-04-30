import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

players = [['James Harden', 'Houston Rockets', '36.10', '44.2%', '36.8%', '87.9%'],
           ['Paul George', 'Los Angeles Clippers', '28.00', '43.8%', '38.6%', '83.9%'],
           ['Giannis Antetokounmpo', 'Oklahoma city thunder', '27.70', '57.8%', '25.6%', '72.9%'],
           ['Joel Embiid', 'Philadelphia 76ers', '27.50', '48.4%', '30%', '80.4%'],
           ['Stephen Curry', 'Golden State Warriors', '27.30', '47.2%', '43.7%', '91.6%'],
           ['Devin Booker', 'Phoenix Suns', '26.60', '46.7%', '32.6%', '86.6%'],
           ['Kawhi Leonard', 'Los Angeles Clippers', '26.60', '49.6%', '37.1%', '85.4%'],
           ['Kevin Durant', 'Brooklyn Nets', '26.00', '52.1%', '35.3%', '88.5%'],
           ['Damian Lillard', 'Portland Trail Blazers', '25.80', '44.4%', '36.9%', '91.2%'],
           ['Kemba Walker', 'Karate', '25.60', '43.4%', '35.6%', '84.4%'],
           ['Bradley Beal', 'Washington Wizards', '25.60', '47.5%', '35.1%', '80.8%'],
           ['Blake Griffin', 'Detroit Pistons', '24.50', '46.2%', '36.2%', '75.3%'],
           ['Karl-Anthony Towns', 'Minnesota Timberwolves', '24.40', '51.8%', '40%', '83.6%'],
           ['Donovan Mitchell', 'Utah Jazz', '23.80', '43.2%', '36.2%', '80.6%'],
           ['Kyrie Irving', 'Brooklyn Nets', '23.80', '48.7%', '40.1%', '87.3%'],
           ['Zach LaVine', 'Cleveland Cavaliers', '23.70', '46.7%', '37.4%', '83.2%'],
           ['Russell Westbrook', 'Houston Rockets', '22.90', '42.8%', '29%', '65.6%'],
           ['Klay Thompson', 'Golden State Warriors', '21.50', '46.7%', '40.2%', '81.6%'],
           ['Julius Randle', 'New York Knicks', '21.40', '52.4%', '34.4%', '73.1%'],
           ['LaMarcus Aldridge', 'San Antonio Spurs', '21.30', '51.9%', '23.8%', '84.7%'],
           ['Jrue Holiday', 'New Orleans Pelicans', '21.20', '47.2%', '32.5%', '76.8%'],
           ['Demar DeRozan', 'San Antonio Spurs', '21.20', '48.1%', '15.6%', '83%'],
           ['Luka Dončić', 'Dallas Mavericks', '21.20', '42.7%', '32.7%', '71.3%'],
           ['MikeConley', 'Utah Jazz', '21.10', '43.8%', '36.4%', '84.5%'],
           ["D'Angelo Russell", 'Golden State Warriors', '21.10', '43.4%', '36.9%', '78%'],
           ['C.J. McCollum', 'Portland Trail Blazers', '21.00', '45.9%', '37.5%', '82.8%'],
           ['Nikola Vucevic', 'Orlando Magic', '20.80', '51.8%', '36.4%', '78.9%'],
           ['Buddy Hield', 'Sacramento Kings', '20.70', '45.8%', '42.7%', '88.6%'],
           ['Nikola Jokic', 'Denver Nuggets', '20.10', '51.1%', '30.7%', '82.1%'],
           ['Lou Williams', 'Los Angeles Clippers', '20.00', '42.5%', '36.1%', '87.6%']
           ]
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
app.layout = html.Div([
    # 指定图的id
    dcc.Graph(id='graph-with-slider'),
    # 定义滑块的各项属性
    dcc.Slider(
        id='class-slider',
        min=1,
        max=4,
        value=2,
        marks={'1': 'Score bar chart', '2': 'Hit rate bar chart', '3': 'Score line chart',
               '4': 'Scatter plot of three point hit rate'},
        step=None
    ),
    html.Div([html.H4('Player to Display:'),
              dcc.Checklist(
                  # options=[{'label': 'Houston Rockets', 'value': 'Houston Rockets'},
                  #          {'label': 'Boston', 'value': 'Boston'},
                  #          {'label': 'Chestnut Hill', 'value': 'Chestnut Hill'},
                  #          {'label': 'Cambridge', 'value': 'Cambridge'}],
                  options=[{'label': item[0], 'value': item[0]} for item in players],
                  value=[item[0] for item in players],
                  id='player_list')],
             style={'width': '49%', 'float': 'right'}),
    html.Div(id='table_div')
])


def generate_table(player_data):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in ['player', 'team', 'score']])
        ),
        html.Tbody([
            html.Tr([
                html.Td(p) for p in player_data[i][:3]
            ]) for i in range(len(player_data))
        ])
    ])


@app.callback(
    Output(component_id="table_div", component_property="children"),
    [Input(component_id="player_list", component_property="value")]
)

def update_table(player_list):
    x = []
    for items in players:
        if items[0] in player_list:
            x.append(items)
    return generate_table(x)
# 定义回调函数，使用‘@app.callback()'参数装饰器来装饰该回调函数，输出绑定图id，输入绑定滑块值
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('class-slider', 'value')]
)
def update_output_div(input_value):
    # 当滑块滑至1时，即输入值为1，返回得分条形图
    if input_value == 1:
        fig1 = dict(
            data=[{'x': [i + 1], 'y': [float(players[i][2])], 'type': 'bar', 'name': '{}'.format(players[i][0])} for i
                  in range(len(players))],
            layout=dict(title='NBA2018-2019 season regular season scoring top 10 data comparison')
        )
        return fig1
    # 当滑块滑至3，即输入值为3时，返回球员得分折线图
    if input_value == 3:
        x = []
        y = []
        for player in players:
            x.append(player[0])
            y.append(player[2])
        fig2 = dict(
            data=[
                {'x': x, 'y': y, 'type': 'Scatter', 'name': 'Core'}
            ],
            layout={
                'title': 'Player score line chart'
            }
        )
        return fig2
    # 当滑块滑至2时，即输入值为2，返回命中率条形图
    if input_value == 2:
        fig3 = dict(
            data=[

                {'x': [players[i][0]], 'y': [float(players[i][3][0:4])], 'type': 'bar',
                 'name': '{}'.format(players[i][0])} for i in range(len(players))

            ],
            layout=dict(title='Bar chart of player hit rate')
        )
        return fig3
    # 当滑块滑至4时，即输入值为4，返回得分命中率与三命中率散点图
    if input_value == 4:
        x = []
        y = []
        team = []
        for player in players:
            x.append(float(player[3][0:4]))
            if len(player[4]) == 5:
                y.append(float(player[4][0:3]))
            else:
                y.append(float(player[4][0:2]))
            team.append(player[1])
        fig4 = dict(
            data=[
                go.Scatter(
                    x=[x[i]],
                    y=[y[i]],
                    text=team,
                    name=players[i][0],
                    mode='markers',
                    opacity=0.8,
                    marker=dict(size=15, line=dict(width=0.5, color='white'))
                ) for i in range(len(players))
            ],
            layout=go.Layout(

                xaxis=dict(type='log', title='Scoring percentage'),
                yaxis=dict(title='Three point percentage', range=[10, 50]),
                margin=dict(l=40, b=40, t=100, r=10),
                hovermode='closest',
                title="Player's scoring percentage and three-point percentage",
            )
        )

        return fig4


if __name__ == '__main__':
    # 开启服务，指定端口号为7000
    app.run_server()
