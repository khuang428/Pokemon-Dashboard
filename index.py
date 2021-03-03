import json
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('./pkmn6v6smogon.csv')
app = dash.Dash(__name__)

TIER_ORDER = {'Uber':0, 'OU':1, 'UUBL':2, 'UU':3, 'RUBL':4, 'RU':5, 'NUBL':6, 'NU':7, 'PUBL':8, 'PU':9, 'NFE':10, 'LC':11}

def setup_graph(id): #initial graphs being brushing/linking
    if(id=='pcd'):
        data = df[['Stat Total','Sp.Atk','Sp.Def','Defense','Attack','HP','Speed']]

        fig = go.Figure(data=
            go.Parcoords(
                dimensions = list([
                    dict(range=[0,780], label='Stat Total', values=data['Stat Total'], multiselect=False),
                    dict(range=[0,255], label='Sp.Atk', values=data['Sp.Atk'], multiselect=False),
                    dict(range=[0,255], label='Sp.Def', values=data['Sp.Def'], multiselect=False),
                    dict(range=[0,255], label='Defense', values=data['Defense'], multiselect=False),
                    dict(range=[0,255], label='Attack', values=data['Attack'], multiselect=False),
                    dict(range=[0,255], label='HP', values=data['HP'], multiselect=False),
                    dict(range=[0,255], label='Speed', values=data['Speed'], multiselect=False)
                ])
            )
        )
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', transition_duration=500, clickmode='event+select')
        fig.update_traces(labelfont=dict(color='#fff'), rangefont=dict(color='#fff'), line=dict(color='#e6c339'))

        return(
            dcc.Graph(id = 'pcd', figure = fig)
        )
    if(id=='type_bar'):
        data = df['Type.1'].value_counts() #counts all the instances
        figdf = pd.DataFrame({'Type.1':data.index, 'count':data.values})
        

        fig = px.bar(figdf,x='Type.1',y='count')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fff', clickmode='event+select')
        fig.update_traces(marker_color="#e6c339")
        return(
            dcc.Graph(id = 'type_bar', figure = fig)
        )
    if(id=='tier_bar'):
        data = df['Tier'].value_counts()
        figdf = pd.DataFrame({'Tier':data.index, 'count':data.values})
        figdf = figdf.sort_values(by=['Tier'], key=lambda x: x.map(TIER_ORDER))

        fig = px.bar(figdf,x='Tier',y='count')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fff', clickmode='event+select')
        fig.update_traces(marker_color="#e6c339")
        return(
            dcc.Graph(id = 'tier_bar', figure = fig)
        )
    if(id=='gen_bar'):
        data = df['Generation'].value_counts()
        figdf = pd.DataFrame({'Generation':data.index, 'count':data.values}) 

        fig = px.bar(figdf,x='Generation',y='count')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fff', clickmode='event+select')
        fig.update_traces(marker_color="#e6c339")
        return(
            dcc.Graph(id = 'gen_bar', figure = fig)
        )

@app.callback(Output('pcd','figure'),
              Input('type_bar','selectedData'),
              Input('tier_bar','selectedData'),
              Input('gen_bar','selectedData')
)
def update_pcd(selectedTypes, selectedTiers, selectedGens):
    data = df #default data, no filters
    #filtering by types
    if selectedTypes != None:
        types=[]
        for p in selectedTypes['points']:
            types.append(p['x'])
        data = df[df['Type.1'].isin(types)]

    #filtering by tier
    if selectedTiers != None:
        tiers=[]
        for p in selectedTiers['points']:
            tiers.append(p['x'])
        data = data[data['Tier'].isin(tiers)]

    #filtering by generation
    if selectedGens != None:
        gens=[]
        for p in selectedGens['points']:
            gens.append(p['x'])
        data = data[data['Generation'].isin(gens)]

    fig = go.Figure(data=
        go.Parcoords(
            dimensions = list([
                dict(range=[0,780], label='Stat Total', values=data['Stat Total'], multiselect=False),
                dict(range=[0,255], label='Sp.Atk', values=data['Sp.Atk'], multiselect=False),
                dict(range=[0,255], label='Sp.Def', values=data['Sp.Def'], multiselect=False),
                dict(range=[0,255], label='Defense', values=data['Defense'], multiselect=False),
                dict(range=[0,255], label='Attack', values=data['Attack'], multiselect=False),
                dict(range=[0,255], label='HP', values=data['HP'], multiselect=False),
                dict(range=[0,255], label='Speed', values=data['Speed'], multiselect=False)
            ])
        )
    )

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', transition_duration=500, clickmode='event+select')
    fig.update_traces(labelfont=dict(color='#fff'), rangefont=dict(color='#fff'), line=dict(color='#e6c339'))

    return fig

@app.callback(Output('type_bar','figure'),
              Output('tier_bar','figure'),
              Output('gen_bar','figure'),
              Input('pcd', 'restyleData'),
              Input('pcd','figure'),
              Input('type_bar','selectedData'),
              Input('tier_bar','selectedData'),
              Input('gen_bar', 'selectedData')
)
def update_bars(selectedpcd, pcd, selectedTypes, selectedTiers, selectedGens):
    #used to not update the filtered bar
    type_data=df
    tier_data=df
    gen_data=df
    
    if selectedTypes != None:
        types=[]
        for p in selectedTypes['points']:
            types.append(p['x'])
        tier_data = tier_data[tier_data['Type.1'].isin(types)]
        gen_data = gen_data[gen_data['Type.1'].isin(types)]

    if selectedTiers != None:
        tiers=[]
        for p in selectedTiers['points']:
            tiers.append(p['x'])
        type_data = type_data[type_data['Tier'].isin(tiers)]
        gen_data = gen_data[gen_data['Tier'].isin(tiers)]
    
    if selectedGens != None:
        gens=[]
        for p in selectedGens['points']:
            gens.append(p['x'])
        type_data = type_data[type_data['Generation'].isin(gens)]
        tier_data = tier_data[tier_data['Generation'].isin(gens)]

    if selectedpcd != None:
        for dim in pcd['data'][0].get('dimensions', None):
            dim_range = dim.get('constraintrange') #get selected constraints, which will reset if a bar graph is filtered
            if dim_range != None:
                dim_name = dim.get('label')
                type_data = type_data[type_data[dim_name].between(int(dim_range[0]),int(dim_range[1]))]
                tier_data = tier_data[tier_data[dim_name].between(int(dim_range[0]),int(dim_range[1]))]
                gen_data = gen_data[gen_data[dim_name].between(int(dim_range[0]),int(dim_range[1]))]
    
    type_data = type_data['Type.1'].value_counts() #counts all the instances
    type_figdf = pd.DataFrame({'Type.1':type_data.index, 'count':type_data.values})    

    type_fig = px.bar(type_figdf,x='Type.1',y='count')
    type_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fff', clickmode='event+select')
    type_fig.update_xaxes(tickangle=90) #keeps the labels vertical
    type_fig.update_traces(marker_color="#e6c339")
    if selectedTypes != None:
        selected =[]
        for p in selectedTypes['points']:
            selected.append(type_fig.data[0]['x'].tolist().index(p['label']))
        type_fig.update_traces(selectedpoints=selected)

    tier_data = tier_data['Tier'].value_counts() #counts all the instances
    tier_figdf = pd.DataFrame({'Tier':tier_data.index, 'count':tier_data.values})
    tier_figdf = tier_figdf.sort_values(by=['Tier'], key=lambda x: x.map(TIER_ORDER))

    tier_fig = px.bar(tier_figdf,x='Tier',y='count')
    tier_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fff', clickmode='event+select')
    tier_fig.update_traces(marker_color="#e6c339")
    if selectedTiers != None:
        selected =[]
        for p in selectedTiers['points']:
            selected.append(tier_fig.data[0]['x'].tolist().index(p['label']))
        tier_fig.update_traces(selectedpoints=selected)

    gen_data = gen_data['Generation'].value_counts() #counts all the instances
    gen_figdf = pd.DataFrame({'Generation':gen_data.index, 'count':gen_data.values})    

    gen_fig = px.bar(gen_figdf,x='Generation',y='count')
    gen_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fff', clickmode='event+select')
    gen_fig.update_traces(marker_color="#e6c339")
    if selectedGens != None:
        selected = []
        for p in selectedGens['points']:
            selected.append(gen_fig.data[0]['x'].tolist().index(p['label']))
        gen_fig.update_traces(selectedpoints=selected)

    return [type_fig, tier_fig, gen_fig]

app.layout =  html.Div(children=[
    html.H2('Pokemon 6-vs-6 Battle Statistics', style={'text-align': 'center'}),
    html.Div(children=[
        html.Span(children = setup_graph('type_bar')),
        html.Span(children = setup_graph('tier_bar')),
        html.Span(children = setup_graph('gen_bar'))
    ], className='graph_div'),
    html.Div(children = setup_graph('pcd'), className='graph_div')
])

if __name__ == '__main__':
    app.run_server(debug=True)