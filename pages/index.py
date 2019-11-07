import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from plotly import graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime as dt

from app import app


df = pd.read_csv('https://raw.githubusercontent.com/bundickm/Sales-Analysis-and-Dashboard/master/sales_data_sample.csv',
                        encoding='unicode_escape')
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

sales = df[['ORDERDATE', 'SALES']]
sales.index = sales['ORDERDATE']
sales = sales.resample('M').sum().reset_index()

dispute_df = df[['ORDERNUMBER', 'STATUS', 'DEALSIZE', 
                 'CUSTOMERNAME', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 
                 'PHONE']]

def text_style(text_align='center', align_items='center', font_weight='normal', 
               font_size='150%', color='black'):
    return dict(
        textAlign = text_align,
        alignItems = align_items,
        fontWeight = font_weight,
        fontSize = font_size,
        color = color
    )


@app.callback(Output('output-graph', 'figure'),
             [Input('date-picker-single', 'date')])
def update_graph(date):
    return {'data': [go.Scatter(x=sales[sales['ORDERDATE'] > date]['ORDERDATE'], y=sales['SALES'], mode='lines')],
            'layout': go.Layout(
                xaxis={"title": "Date"}, 
                yaxis={"title": "Sales"}, 
                title='Sales per Month',
                font=dict(color="#000000"),
                titlefont=dict(size=24)
            )
    }


@app.callback(Output('sales-total', 'children'),
             [Input('date-picker-single', 'date')])
def update_sales_total(date):
    sales_total = sales[sales['ORDERDATE'] > date]['SALES'].sum()
    formatted_string = '${:0,.2f}'.format(sales_total).replace('$-', '-$')
    return formatted_string


@app.callback(Output('orders-total', 'children'),
             [Input('date-picker-single', 'date')])
def update_orders_total(date):
    orders_total = df[df['ORDERDATE'] > date]['ORDERDATE'].count()
    return str(orders_total)


@app.callback(Output('avg-sale', 'children'),
             [Input('date-picker-single', 'date')])
def update_avg_sale(date):
    sales_total = sales[sales['ORDERDATE'] > date]['SALES'].sum()
    orders_total = df[df['ORDERDATE'] > date]['ORDERDATE'].count()
    avg_sale = sales_total/orders_total

    formatted_string = '${:0,.2f}'.format(avg_sale).replace('$-', '-$')
    return formatted_string


@app.callback(Output('customer-count', 'children'),
             [Input('date-picker-single', 'date')])
def update_customer_count(date):
    customer_count = df[df['ORDERDATE'] > date]['CUSTOMERNAME'].nunique()

    return str(customer_count)


@app.callback(Output('orders-filled', 'children'),
             [Input('date-picker-single', 'date')])
def update_shipped_status(date):
    bounded_status = df[(df['ORDERDATE'] > date)]['STATUS']
    shipped = bounded_status[bounded_status == 'Shipped'].count()
    total = bounded_status.count()

    return '{:0,.2f}% Shipped'.format(shipped/total*100)


@app.callback(Output('orders-processing', 'children'),
             [Input('date-picker-single', 'date')])
def update_shipped_status(date):
    bounded_status = df[(df['ORDERDATE'] > date)]['STATUS']
    shipped = bounded_status[bounded_status == 'In Process'].count()
    total = bounded_status.count()

    return '{:0,.2f}% Processing'.format(shipped/total*100)


@app.callback(Output('orders-disputed', 'children'),
             [Input('date-picker-single', 'date')])
def update_shipped_status(date):
    bounded_status = df[(df['ORDERDATE'] > date)]['STATUS']
    shipped = bounded_status[bounded_status == 'Disputed'].count()
    total = bounded_status.count()

    return '{:0,.2f}% Disputed'.format(shipped/total*100)


sales_column = dbc.Col(
    dbc.Card([
        dbc.CardHeader('Total Sales', style=text_style(font_weight='bold')),
        dbc.CardBody('$00.00', id='sales-total', style=text_style()), 
        ]))
orders_column = dbc.Col(
    dbc.Card([
        dbc.CardHeader('Total Orders', style=text_style(font_weight='bold')),
        dbc.CardBody('000', id='orders-total', style=text_style()),
        ]))
avg_sales_column = dbc.Col(
    dbc.Card([
        dbc.CardHeader('Average Sale', style=text_style(font_weight='bold')),
        dbc.CardBody('$00.00', id='avg-sale', style=text_style()),
        ]))
customers_column = dbc.Col(
    dbc.Card([
        dbc.CardHeader('Customer Count', style=text_style(font_weight='bold')),
        dbc.CardBody('000', id='customer-count', style=text_style()),
        ]))

graph_and_datepicker = dbc.Col(
    [
        dcc.Graph
        (
            id='output-graph',
            figure=
            {
                'data': [go.Scatter(
                    x=sales['ORDERDATE'], 
                    y=sales['SALES'], 
                    mode='lines')],
            }
        ),
        
        dbc.Row
        ([
            dbc.Col
            (
                dcc.Markdown('Start Date', style=text_style(font_size='100%', font_weight='bold')),
                align='end',
                width={'size': 2,},
            ),

            dbc.Col
            (
                dcc.DatePickerSingle(
                    id='date-picker-single',
                    min_date_allowed=dt(2003, 1, 12),
                    max_date_allowed=dt(2005, 4, 30),
                    initial_visible_month=dt(2003, 1, 12),
                    date=(dt(2003, 1, 12, 0, 0, 0)),),
                width={'offset': 0},
                align='start',
            )
        ])
    ]
)

order_status = dbc.Col(
    [
        dbc.Card([
            dbc.CardHeader('Order Status', 
                style=text_style(font_weight='bold')),
            dbc.CardBody('0% Shipped', id='orders-filled',
                style=text_style(color='#5faa0a', font_weight='bold')),
            dbc.CardBody('0% Processing', id='orders-processing',
                style=text_style(color='#b7b212', font_weight='bold')),
            dbc.CardBody('0% Disputed', id='orders-disputed',
                style=text_style(color='#c62f2f', font_weight='bold')),],
            style={'margin-top': '4rem', 'width': '100%'}),
        
    #     dbc.Card('Churn Risk / Order Status',
    #         style={'margin-top': '4rem', 'textAlign': 'center', 'fontWeight': 'bold'}),
    #     daq.ToggleSwitch(id='risk-churn-switch', value=False, size=75,
    #         style={'margin-top': '1rem'}),
    ],
    md=3,
)

disputed_order_table = dash_table.DataTable(
    id='dispute-table',
    columns=[{"name": i, "id": i} for i in dispute_df.columns],
    data=dispute_df.to_dict('records'),
    style_table={'margin-top':'3rem', 'overflowX': 'scroll', 'width':'110%',},
    page_size=10,
    page_action='native',
)
@app.callback(
    dash.dependencies.Output('dispute-table', 'data'),
    [dash.dependencies.Input('date-picker-single', 'date')])
def update_table(date):
    df2 = df[((df['STATUS'] == 'Disputed') |
             (df['STATUS'] == 'On Hold')) &
             (df['ORDERDATE'] >= date)].sort_values(
                by=['ORDERDATE', 'STATUS'], ascending=False)
    df2 = df2[['ORDERNUMBER', 'STATUS', 'DEALSIZE', 
               'CUSTOMERNAME', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 
               'PHONE']]

    return df2.to_dict("records")

top_row = dbc.Row([sales_column, orders_column, avg_sales_column, customers_column])
middle_row = dbc.Row([graph_and_datepicker, order_status])
bottom_row = dbc.Row(disputed_order_table)
layout = dbc.Col([top_row, middle_row, bottom_row])