from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df=pd.read_csv('D:/data analyst/Books.csv')
df.drop_duplicates(inplace=True)
df['Revenue']=round(df['Stock']*df['Price'],2)

app=Dash(__name__)
app.layout=html.Div([
    html.H1("Book Analysis Dashboard", style={'textAlign':'center'}),
    dcc.Dropdown(
        id='genre',options=df['Genre'].unique(),value='',
        multi=True,style={'width':'50%'},
        placeholder='select Genre'),
    
    html.Div([
        dcc.Graph(id='graph', style={'width': '48%'}),
        dcc.Graph(id='graph2', style={'width': '48%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    html.Div([
        dcc.Graph(id='graph3', style={'width': '48%'}),
        dcc.Graph(id='graph4', style={'width': '48%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'})
])

@app.callback(
    Output('graph4','figure'),
    Output('graph','figure'),
    Output('graph2','figure'),
    Output('graph3','figure'),
    Input('genre','value')
)

def update_dash(selected_genre):
  filtered_df=df[df['Genre'].isin(selected_genre)]
  df3=filtered_df.groupby('Genre')['Revenue'].sum().reset_index()
  df1=filtered_df.groupby('Genre')['Stock'].sum().reset_index()
  df2=filtered_df.groupby('Genre')['Price'].sum().reset_index()
  bar=px.bar(df1,x='Genre',y='Stock',title="Genre vs Stock",text_auto=True)
  pie=px.bar(df2,x='Genre',y='Price',title="Genre vs Price", text_auto=True)
  bar1=px.bar(df3,x='Genre',y='Revenue',title="Genre vs Revenue", text_auto=True)
  sc=px.scatter(filtered_df,x='Book_ID',y='Published_Year',title="Book_ID vs Published_year", size='Price', color='Genre')
  return bar,pie,bar1,sc

app.run(debug=True)