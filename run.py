# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import index, segmentation, pareto, sales


navbar = dbc.NavbarSimple(
    brand='Sales and Customer Dashboard',
    brand_href='/', 
    children=[
        dbc.NavItem(dcc.Link('Overview', href='/', className='nav-link')),
        dbc.NavItem(dcc.Link('Customer Segmentation', href='/segmentation', className='nav-link')), 
        dbc.NavItem(dcc.Link('Pareto Analysis', href='/pareto', className='nav-link')), 
        dbc.NavItem(dcc.Link('Sales', href='/sales', className='nav-link')), 
    ],
    sticky='top',
    color='light', 
    light=True, 
    dark=False
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Michael Bundick', className='mr-2'), 
                    html.A(html.I(className='fas fa-envelope-square mr-1'), href='mailto:bundickm@gmail.com'), 
                    html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/bundickm/Sales-Analysis-and-Dashboard'), 
                    html.A(html.I(className='fab fa-linkedin mr-1'), href='https://www.linkedin.com/in/michael-bundick/'),
                ], 
                className='lead'
            )
        )
    )
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    navbar,
    dbc.Container(id='page-content', className='mt-4'),
    html.Hr(),
    footer
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/segmentation':
        return segmentation.layout
    elif pathname == '/pareto':
        return pareto.layout
    elif pathname == '/sales':
        return sales.layout
    else:
        return dcc.Markdown('## Page not found')

if __name__ == '__main__':
    app.run_server(debug=True)