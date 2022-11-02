import plotly.express as px
import plotly.graph_objects as go
import plotly
import matplotlib.pyplot as plt
import os 


class plots:
    FOLDER = '../images'

    def visualize_corr_matrix(self, corr_matrix):
        return corr_matrix.style.background_gradient(cmap='coolwarm').format(precision=2)

    def plot_daily_returns_of(self, df, company):
        fig = px.line(df, x='date', y=company,title='Daily Returns')
        fig.update_traces(opacity=0.5)
        return fig

    def plot_all_daily_returns(self, df):
        fig = px.line(df, x='date', y=df.columns[1:],title='Daily Returns')
        fig.update_traces(opacity=0.5)
        return fig

    def scatter_plot_portfolios(self, ports_summary, main_ports, filename="portfolios_scatter_plot.png", format="png"):
        fig = go.Figure()
        scatter_plot = go.Scatter(
            x = ports_summary['risk'],
            y = ports_summary['return'],
            mode='markers', opacity=0.8,
            marker=dict(line=dict(width=0.3, color='white'))
        )
        fig.add_trace(scatter_plot)
        fig.add_trace(go.Scatter(
            x=main_ports['risk'],
            y=main_ports['return'],
            mode="markers+text", marker=dict(color='yellow', size=13, line=dict(width=2, color='red')),
            text=['MAX SHARPE-RATIO', 'MIN RISK', 'EQUAL ALLOCATIONS'],
            textposition='bottom center',
            textfont=dict(color='red', size=13)
        ))
        fig.update_layout(
                        margin=dict(t=30, b=10),
                        showlegend=False,
                        xaxis = dict(
                            showgrid=False,tickangle = -45,
                            categoryorder='total descending',title_text='Risk'),
                        yaxis = dict(title_text='Return'),
                        title=dict(text = '10001 Portfolios Risk-Return',
                                    font=dict(size=18, 
                                            color='black'),
                                    x=0.5,
                                    y=1,
                                    xanchor='center',
                                    yanchor='top'),
                        )
        return fig

    