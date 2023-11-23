from dash import Dash, html,dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash_bootstrap_components import Alert
import dash_table
import random

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Base de datos
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://cagomezj:1234@cluster0.lg8bsx8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.sensores.sensor_1
result = 0

# Declarar data_dist fuera de la función para evitar el UnboundLocalError
data_dist = []

# App layout
app.layout = dbc.Container([
    html.H1("Asentamiento Tuneladora", className='display-4 text-center text-primary', style={'margin-top': '20px'}),
    html.Hr(className='my-4', style={'border-top': '2px solid #4285F4'}),
    html.H5("Natalia Ximena Tovar 20222579057 - Juan David Torres 20222579045", style={'font-style': 'italic', 'text-align': 'center', 'color': 'blue'}),

    html.H4("Distancia Actual", id='distancia-actual', style={'text-align': 'center', 'color': '#333', 'margin-bottom': '20px'}),

    dcc.Graph(id='asentamiento', style={'width': '100%'}),

    dcc.Interval(
        id='interval-component',
        interval=1 * 500,  # en milisegundos, actualiza cada 1 segundo
        n_intervals=0
    ),

    html.Div(id='alerta-texto', className='text-center mt-4', style={'color': 'red', 'font-size': '18px'}),

    dash_table.DataTable(
        id='tabla-datos',
        columns=[
            {'name': 'Tiempo', 'id': 'tiempo'},
            {'name': 'Asentamiento (cm)', 'id': 'asentamiento'},
            {'name': 'Alerta', 'id': 'alerta'}
        ],
        style_table={'maxHeight': '300px', 'overflowY': 'scroll'},
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
    ),
    
    html.Div(style={'height': '50px'}),  # Ajusta la altura según tus preferencias
    html.P("Simulación en tiempo real realizado en la Universidad Distrital Francisco José de Caldas - Facultad Tecnológica - Programación II - Ingeniería Civil",
           style={'text-align': 'center', 'font-size': '12px', 'color': '#777'})

], style={'max-width': '800px', 'margin': 'auto'})

@app.callback(
    [Output('asentamiento', 'figure'),
     Output('distancia-actual', 'children'),
     Output('alerta-texto', 'children'),
     Output('tabla-datos', 'data')],
    [Input('interval-component', 'n_intervals')]
)
def consultar(n):
    global data_dist, result, db
    #----------------------------------------------------------- ACTIVAR ACÁ EL SENSOR
    #result = db.find_one(sort=[('updated_at', -1)])
    #distancia = int(result['distancia'])
    #data_dist.append(distancia)
    
    distancia = random.randint(0, 30) # Números aleatorios de 0 a 30 para verificar gráfica y tabla
    data_dist.append(distancia)
    # --------------------------------------------------------------------------------
    
    # Crear el objeto de figura de Plotly
    fig = go.Figure(data=[go.Scatter(y=data_dist, mode='lines+markers')])
    
    # Agregar una línea punteada para el límite 
    
    limite = 25 # Modificar acá el límite que se quiere
    
    
    fig.add_shape(type='line',
                  x0=0, x1=len(data_dist) - 1, y0=limite, y1=limite,
                  line=dict(color='red', width=2, dash='dash'))
    
    # Agregar texto como leyenda dentro del gráfico
    fig.add_annotation(
        x=len(data_dist) - 1, y=limite,
        text=f'Límite: {limite} cm',
        showarrow=True,
        arrowhead=2,
        arrowcolor='red',
        arrowsize=1,
        arrowwidth=2,
        ax=-30,
        ay=-30,
        font=dict(color='red')
    )

    fig.update_layout(
        title='Asentamiento a lo largo del tiempo',
        xaxis_title='Tiempo',
        yaxis_title='Asentamiento (cm)',
        xaxis=dict(showline=True, showgrid=False),
        yaxis=dict(showline=True, showgrid=False),
        hovermode='x',
    )

    # Agregar un texto según la condición
    if distancia >= limite:
        alerta_texto = Alert("!ALERTA!, se está superando el límite establecido", color='danger', className='mt-3', style={'font-size': '24px'})
    else:
        alerta_texto = Alert("El dato no supera el límite establecido", color='success', className='mt-3', style={'font-size': '24px'})

    # Formatear la distancia para mostrarla en el H1
    distancia_texto = f"El asentamiento fue: {distancia} cm"

    # Actualizar la tabla con los últimos 15 datos
    tabla_datos = [{'tiempo': i, 'asentamiento': data, 'alerta': '!ALERTA!, se está superando el límite establecido' if data >= limite else 'El dato no supera el límite establecido'}
                for i, data in enumerate(data_dist[-15:], start=len(data_dist)-14)]


    return fig, distancia_texto, alerta_texto, tabla_datos



if __name__ == "__main__":
    app.run_server(debug=True)