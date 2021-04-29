import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

players = [['James Harden', '火箭', '36.10', '44.2%', '36.8%', '87.9%'],
           ['Paul George', '快船', '28.00', '43.8%', '38.6%', '83.9%'],
           ['Giannis Antetokounmpo', '雄鹿', '27.70', '57.8%', '25.6%', '72.9%'],
           ['Joel Embiid', '76人', '27.50', '48.4%', '30%', '80.4%'],
           ['Stephen Curry', '勇士', '27.30', '47.2%', '43.7%', '91.6%'],
           ['Devin Booker', '太阳', '26.60', '46.7%', '32.6%', '86.6%'],
           ['Kawhi Leonard', '快船', '26.60', '49.6%', '37.1%', '85.4%'],
           ['Kevin Durant', '篮网', '26.00', '52.1%', '35.3%', '88.5%'],
           ['Damian Lillard', '开拓者', '25.80', '44.4%', '36.9%', '91.2%'],
           ['Kemba Walker', '凯尔特人', '25.60', '43.4%', '35.6%', '84.4%'],
           ['Bradley Beal', '奇才', '25.60', '47.5%', '35.1%', '80.8%'],
           ['Blake Griffin', '活塞', '24.50', '46.2%', '36.2%', '75.3%'],
           ['Karl-Anthony Towns', '森林狼', '24.40', '51.8%', '40%', '83.6%'],
           ['Donovan Mitchell', '爵士', '23.80', '43.2%', '36.2%', '80.6%'],
           ['Kyrie Irving', '篮网', '23.80', '48.7%', '40.1%', '87.3%'],
           ['Zach LaVine', '公牛', '23.70', '46.7%', '37.4%', '83.2%'],
           ['Russell Westbrook', '火箭', '22.90', '42.8%', '29%', '65.6%'],
           ['Klay Thompson', '勇士', '21.50', '46.7%', '40.2%', '81.6%'],
           ['Julius Randle', '尼克斯', '21.40', '52.4%', '34.4%', '73.1%'],
           ['LaMarcus Aldridge', '马刺', '21.30', '51.9%', '23.8%', '84.7%'],
           ['Jrue Holiday', '鹈鹕', '21.20', '47.2%', '32.5%', '76.8%'],
           ['Demar DeRozan', '马刺', '21.20', '48.1%', '15.6%', '83%'],
           ['Luka Dončić', '独行侠', '21.20', '42.7%', '32.7%', '71.3%'],
           ['MikeConley', '爵士', '21.10', '43.8%', '36.4%', '84.5%'],
           ["D'Angelo Russell", '勇士', '21.10', '43.4%', '36.9%', '78%'],
           ['C.J. McCollum', '开拓者', '21.00', '45.9%', '37.5%', '82.8%'],
           ['Nikola Vucevic', '魔术', '20.80', '51.8%', '36.4%', '78.9%'],
           ['Buddy Hield', '国王', '20.70', '45.8%', '42.7%', '88.6%'],
           ['Nikola Jokic', '掘金', '20.10', '51.1%', '30.7%', '82.1%'],
           ['Lou Williams', '快船', '20.00', '42.5%', '36.1%', '87.6%']
           ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
    )
])


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
