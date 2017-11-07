import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot, plot
from llxquant.utils import max_drop_down
import math
import numpy as np
from llxquant.env import RISK_FREE_RATE


def create_table(market_values):
    """market_values should be series with date index """
    daily_1p_return=market_values/market_values.shift(1)
    total_return=market_values/market_values.iloc[0]
    maxdropdown,mdd=max_drop_down(total_return)
    annualreturn = math.pow(total_return[-1], 250 / len(total_return)) - 1

    dayreturnstd = np.std(daily_1p_return, ddof=1)
    if dayreturnstd == 0:
        sharp = 0
    else:
        sharp = (annualreturn - RISK_FREE_RATE) / (dayreturnstd * np.sqrt(250))


    table = [
        (u'回测收益', str(round((total_return[-1] - 1) * 100, 2)) + '%'),
        (u'年化收益', str(round(annualreturn * 100, 2)) + '%'),
        (u'夏普比率', str(round(sharp, 3))),
        (u'最大回撤', str(round(maxdropdown * 100, 3)) + '%'),
        (u'最大回撤天数', str(mdd)),
    ]
    return total_return,table


def plot_charts(days, day_returns, table,index_returns=None, notebook_mode=True):

    fig = ff.create_table(table, height_constant=10)
    
    strategy = go.Scatter(
        name=u'策略收益',
        x=days,
        y=day_returns,
        xaxis='x2',
        yaxis='y2',
    )
    if not(index_returns is None):
        benchmark = go.Scatter(
            name=u'基准收益',
            x=days,
            y=index_returns,
            xaxis='x2',
            yaxis='y2',
        )

    layout = dict(
        xaxis={
            'rangeslider': {
                'visible': False,
            }
        },
        yaxis={
            'domain': [0.8, 1]
        },
        xaxis2={
            'side': 'bottom',
            'rangeslider': {
                'visible': False,
            }
        },
        yaxis2={
            'domain': [0, 0.75],
            'side': 'right',
            'ticksuffix': '%',
        },
        legend={
            'x': 0,
            'y': 0.8,
            'orientation': 'h'
        }
    )
    
    fig['data'].extend(go.Data([strategy]))
    fig.layout.update(layout)
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.margin.update({'t':50, 'b':50, 'l':50, 'r':80})
    fig.layout.update({'height': 400})

    if notebook_mode:
        init_notebook_mode()
        iplot(fig, validate=False, show_link=False)
    else:
        plot(fig, filename='report.html', validate=False, show_link=False)

    return fig


def plot_charts_with_market_value(market_values,notebook_mode=False):
    total_return, table =create_table(market_values)
    total_return=total_return*100-100
    return plot_charts(list(total_return.index),list(total_return),table,notebook_mode=notebook_mode)
