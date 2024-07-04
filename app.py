# Importar bibliotecas necesarias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
# Configuración de la página de Streamlit
st.set_page_config(page_title="Residuos Municipales", page_icon="🚮", initial_sidebar_state="expanded", layout='wide')
# Estilos en formato HTML para el texto
text_style = """
    <style>
        .title_text {
            font-size: 24px; font-family: "Times New Roman", Georgia, serif;
            font-weight: bold;
        }
        .desc_text {
            font-size: 24px; font-family: "Times New Roman", Georgia, serif;
            text-align: justify;
        }
    </style>
"""
st.markdown(text_style, unsafe_allow_html=True)
# Título principal de la pagina
st.markdown("<h2 class='title_text'>Residuos Municipales (2014-2021)<h3>" , unsafe_allow_html=True)


# Cargar el archivo CSV en un DataFrame
@st.cache_data
def load_data():
    file_path = 'residuos_municipales.csv'
    df = pd.read_csv(file_path, encoding="latin1", delimiter=";", index_col=0)
    df["PERIODO"] = df["PERIODO"].astype(int)
    return df

@st.cache_data
def load_tb_ubigeos():
    ubigeos_ll = 'TB_UBIGEOS.csv'
    dful = pd.read_csv(ubigeos_ll, encoding="latin1", delimiter=";", index_col=0)
    return dful

df = load_data()
dful = load_tb_ubigeos()
dfud = df

@st.cache_data
def process_data(df):
    # Group by DEPARTAMENTO and PERIODO and sum QRESIDUOS_MUN
    df_grouped = df.groupby(['PERIODO', 'DEPARTAMENTO'])['QRESIDUOS_MUN'].sum().reset_index()
    return df_grouped

# Función para generar el primer gráfico
def do_chart1():
    global df
    sum_by_periodo = df.groupby("PERIODO")["QRESIDUOS_MUN"].sum().reset_index()
    fig = go.Figure()
    # Crear un gráfico de pastel (donut chart) utilizando plotly.express
    fig.add_trace(go.Pie(
        labels=sum_by_periodo["PERIODO"],
        values=sum_by_periodo["QRESIDUOS_MUN"],
        texttemplate="%{label}<br>%{percent:.2%}",
        hole=0.6,
        showlegend=True,
        hovertemplate="<b>Año</b>: %{label}<br>"
                      "<b>Total</b>: %{value:.0f}<br>"
                      "<b>Porcentaje</b>: %{percent:.2%}<br>"
                      "<extra></extra>",
        textinfo='percent+value',
        pull=[0.1] * len(sum_by_periodo),
        marker=dict(colors=px.colors.qualitative.Set3),
    ))
    fig.add_annotation(
        text="RESIDUOS MUNICIPALES",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20)
    )
    fig.update_layout(
        title="Residuos municipales Ton/Año | 2014 - 2021",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial", size=12, color="black"),
    )
    st.plotly_chart(fig, use_container=True)


    st.markdown("*Gráfica 1: El gráfico representa la proporción expresada en porcentajes de la cantidad de residuos sólidos domiciliarios por año*")
    st.info('En la gráfica se logra observar la comparación de la cantidad de residuos sólidos domiciliarios que fueron registrados durante el periodo 2019 al 2022 y la proporción que representan respecto al 100% del total de los datos registrados, de los cuales se puede destacar que el año 2019 y 2020 tienen un porcentaje igual de distribución y lo mismo se logra observar para los años 2021 y 2022, pero es importante destacar que los 2 últimos años del periodo fueron los que mayor porcentaje de residuos sólidos domiciliarios registraron. ', icon="😀")
# Función para generar el segundo gráfico
def do_chart2():
    sum_residuos_urbanos = df.groupby("DEPARTAMENTO")["QRESIDUOS_MUN"].sum().reset_index()
    sum_residuos_urbanos.rename(columns={"QRESIDUOS_MUN": "Residuos Municipales"}, inplace=True)
    fig = px.scatter(sum_residuos_urbanos, x="DEPARTAMENTO", y="Residuos Municipales",
                    size="Residuos Municipales", color="DEPARTAMENTO",
                    hover_name="DEPARTAMENTO", title="Residuos Municipales Ton/Año por Departamento",
                    labels={"Residuos Domiciliarios": "Residuos Municipales", "DEPARTAMENTO": "Departamento"},
                    size_max=60,
                    color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_yaxes(title_text="Residuos Municipales 2014 - 2021")
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_layout(
        xaxis=dict(title='Departamento'),
        yaxis=dict(title='Residuos Municipales 2014 - 2021'),
        template="plotly_dark",
        font=dict(family="Arial", size=12, color="white"),
    )
    st.plotly_chart(fig)
    st.markdown("*Gráfica 2: El gráfico representa los residuos Municipales por departamento expresada en millones de toneladas*")
    st.warning('En el gráfico presentado podemos observar que en la capital del Perú Lima, es una de las ciudades más urbanizadas , de igual forma la más poblada del país y, por lo tanto, genera una gran cantidad de residuos sólidos domiciliarios.  ', icon="😀")
# Función para generar el tercer gráfico
def do_chart3():
    # df_grouped = process_data(df)
    # Crear el sidebar para el filtro de PERIODO
    periodos = df['PERIODO'].unique()
    selected_periodo = st.selectbox('Selecciona un PERIODO:', periodos)
    # Filtrar el dataframe por el PERIODO seleccionado
    df_filtered = df[df['PERIODO'] == selected_periodo]
    # Agrupar por DEPARTAMENTO y sumar QRESIDUOS_MUN
    df_grouped = df_filtered.groupby('DEPARTAMENTO')['QRESIDUOS_MUN'].sum().reset_index()

    # Plot with Plotly
    fig = px.line(df_grouped, x='DEPARTAMENTO', y='QRESIDUOS_MUN', title='Residuos por departamento ')

    # Add circular markers and customize the style
    fig.update_traces(
        mode='lines+markers',
        marker=dict(symbol='circle', size=10, color='red'),
        line=dict(color='blue', width=2)
    )

    # Update layout for advanced styling
    fig.update_layout(
        title=dict(
            text='Residuos por departamento - '+str(selected_periodo),
            font=dict(size=20, color='darkblue'),
            # x=0.5  # Center the title
        ),
        xaxis=dict(
            title='Departamento',
            titlefont=dict(size=16, color='darkblue'),
            tickfont=dict(size=14, color='black'),
            showgrid=True,
            gridcolor='lightgrey'
        ),
        yaxis=dict(
            title='Cantidad de Residuos',
            titlefont=dict(size=16, color='darkblue'),
            tickfont=dict(size=14, color='black'),
            showgrid=True,
            gridcolor='lightgrey'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified'
    )
    st.plotly_chart(fig)
    df_grouped.index = df_grouped.index + 1
    st.write(df_grouped)

    # # Mostrar el gráfico en Streamlit
    # st.write(f"QRESIDUOS_MUN by DEPARTAMENTO for PERIODO {selected_periodo}")
    st.markdown("*Gráfica 3: La gráfica muestra la diferencia de consumos de residuos sólidos domiciliarios por departamento con su respectiva región.*")
    st.info('Tener en cuenta que el territorio  peruano está dividido en 3 regiones naturales: costa, sierra y selva. Esta división se basa en las características topográficas y climáticas de cada región,es por ello, que en la gráfica se puede apreciar que el mismo departamento se encuentra en diferentes regiones. Por ejemplo, el departamento de Piura que se encuentra ubicado en la zona norte del país, está distribuido geográficamente en la costa y sierra, como consecuencia se pueden apreciar playas, ríos y montañas dentro de un mismo territorio.', icon="🔎")
# Función para generar el cuarto gráfico    
def do_chart4():
    # Extract the required columns
    ubigeos_distrito_selected = dfud[['UBIGEO','PERIODO', 'DEPARTAMENTO', 'PROVINCIA','DISTRITO','GPC_DOM', 'QRESIDUOS_DOM', 'QRESIDUOS_NO_DOM', 'QRESIDUOS_MUN']]

    ubigeos_ll_selected = dful[['ubigeo_inei', 'latitud', 'longitud']]

    # Reset index to avoid showing the index column
    ubigeos_distrito_selected.reset_index(drop=True, inplace=True)
    ubigeos_ll_selected.reset_index(drop=True, inplace=True)
    ubigeos_ll_selected.index = range(1, len(ubigeos_ll_selected) + 1)
    ubigeos_distrito_selected.index = range(1, len(ubigeos_distrito_selected) + 1)
    col1, col2, col3 = st.columns(3)
    distrito_filtrado = ubigeos_distrito_selected
    with col1:
    # Filter inputs
        departamento = st.selectbox('Seleccione Departamento', ubigeos_distrito_selected['DEPARTAMENTO'].unique())
        distrito_filtrado = distrito_filtrado[distrito_filtrado['DEPARTAMENTO'] == departamento]
    with col2:
        provincia = st.selectbox('Seleccione Provincia', distrito_filtrado['PROVINCIA'].unique())
        distrito_filtrado = distrito_filtrado[distrito_filtrado['PROVINCIA'] == provincia]
    with col3:
        pass
        distrito = st.selectbox('Seleccione Distrito', distrito_filtrado['DISTRITO'].unique())
        distrito_filtrado = distrito_filtrado[distrito_filtrado['DISTRITO'] == distrito]
        
    # Sum QRESIDUOS_MUN
    distrito_filtrado = distrito_filtrado.assign(QRESIDUOS_MUN_SUM=distrito_filtrado['QRESIDUOS_MUN'].sum())
    # Merge the dataframes on UBIGEO and ubigeo_reniec
    merged_df = pd.merge(distrito_filtrado, ubigeos_ll_selected, left_on='UBIGEO', right_on='ubigeo_inei')
    st.write(merged_df)
    # Plotting
    if not merged_df.empty:
        fig = px.scatter_mapbox(
            merged_df,
            hover_name="DISTRITO",
            hover_data=["DEPARTAMENTO", "PROVINCIA", "QRESIDUOS_MUN_SUM"],
            title="Total de Residuos por Distrito del 2014 al 2021",
            lat="latitud",
            lon="longitud",
            zoom=11,
            height=400,
            color="QRESIDUOS_MUN_SUM",
            size="QRESIDUOS_MUN_SUM",
            # color_continuous_scale="Viridis",  # Cute color scale
            # opacity=0.7,  # Cute opacity level
            labels={"QRESIDUOS_MUN_SUM": "Total Residuos "},
            center={"lat": merged_df["latitud"].mean(), "lon": merged_df["longitud"].mean()},
        )
        fig.update_layout(mapbox_style="open-street-map")
        # Customize map layout
        st.plotly_chart(fig)

        # Plot bar chart by PERIODO
        fig = px.bar(
        distrito_filtrado,
        x='PERIODO',
        y=['QRESIDUOS_DOM', 'QRESIDUOS_NO_DOM'],
        barmode='group',
        title='QRESIDUOS_DOM y QRESIDUOS_NO_DOM por PERIODO',
        color_discrete_map={'QRESIDUOS_DOM': 'green', 'QRESIDUOS_NO_DOM': 'gray'}
        )
        # Customize hover template
        fig.update_traces(
            hovertemplate='<b style="color:red;">Periodo</b>: %{x}<br><b style="color:blue;">Cantidad</b>: %{y:.2f} <b style="color:black;">Ton/Año</b>'
        )

        fig.update_layout(
        xaxis_title='Periodo',
        yaxis_title='Cantidad',
        yaxis_tickformat=',.2f',  # Format y-axis ticks as whole numbers
        font=dict(size=10),  # Set font size
        plot_bgcolor='rgba(0,0,0,0)', # Transparent background
        legend_title_text='TIPO DE RESIDUOS'
    )

        st.plotly_chart(fig)
    else:
        st.write("Datos no encontrado.")

# Función para mostrar información sobre el proyecto
def do_acerca():
    st.image('basura.jpg', caption="Basura en la playa", use_column_width=True)
    st.link_button("Ir a código del proyecto", "https://github.com/summermp/streamlit", type='primary')
    st.markdown("""
<p class='desc_text'> La base de datos de composición de residuos sólidos domiciliarios corresponde a la información sobre la distribución de los residuos sólidos del ámbito domiciliario generados por tipo (medido en tonelada). Dicha información, fue obtenida desde los años 2014 hasta el 2021, con respecto a todos los departamentos de nuestro país.</br></br>
La información que se toma de insumo para la estimación de esta estadística es obtenida a partir de dos fuentes de información: </br></br>
Sistema de Información para la Gestión de los Residuos Sólidos – SIGERSOL el cual es administrado por el Ministerio del Ambiente (MINAM).</br></br>
Los Estudios de caracterización de residuos sólidos municipales, que se estandarizaron desde el año 2014 en adelante, aprobada mediante Resolución Ministerial N° 457-2018-MINAM.</p>
<h4 class='title_text'>¿Qué buscamos?</h4>
<p class='desc_text'>Buscamos brindar información sobre la distribución de los residuos sólidos en el ámbito domiciliario en todos los departamentos del Perú; facilitando su uso mediante gráficas y tablas para un mejor entendimiento.</p>
<h4 class='title_text'>¿Qué son los residuos sólidos domiciliarios?</h4>
<p class='desc_text'>Residuos sólidos domiciliarios son aquellos provenientes del consumo o uso de un bien o servicio, comprenden específicamente como fuente de generación a las viviendas.</p>
<h4 class='title_text'>¿Cómo influyen los residuos sólidos en los seres vivos?</h4>
<p class='desc_text'>De acuerdo a su clasificación y aprovechamiento estos residuos domiciliarios pueden influir tanto positiva como negativamente, por ejemplo, el uso irresponsable y excesivo de plástico, pilas y/o baterías podría ser muy perjudicial para los seres vivos y al ambiente, ya que estos son residuos que podrían <b>tomarse entre 100 a 1000 años en descomponerse</b>, generando así un rastro tóxico a largo plazo en nuestro ecosistema. Por otra parte, el aprovechamiento responsable y creativo de los residuos domiciliarios, tales como la materia orgánica, el papel y el cartón permiten fomentar el reciclaje y crear nuevos productos que sean en beneficio para los seres vivos y el ambiente, por ejemplo, la descomposición de la materia orgánica podría ser fuente de compostaje para las plantas.</p>
""",  unsafe_allow_html=True)
# Función para mostrar información de nosotros
def do_nosotros():
    # st.markdown("<h4 class='title_text'>¿Quiénes somos?</h4>", unsafe_allow_html=True)
    st.markdown("<p class='desc_text'>Somos estudiantes del quinto semestre de la carrera de ingeniería ambiental de la Universidad Peruana Cayetano Heredia (UPCH). Nos apasiona el procesamiento y visualización de datos para mejorar y comprender la problemática ambiental y brindar información sobre los residuos sólidos generados en el Perú.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 2])
    with col1:
        st.image("meyli.jpeg")
    with col2:
        st.write("")
        st.markdown("""
        ## Meyli Flores Huaman
        ##### Carrera profesional de Ingeniería Ambiental
        **correo**: meyli.flores@upch.pe
        """)
        
    col1, col2 = st.columns([2, 2])
    with col1:
        st.image("lory.jpeg")
    with col2:
        st.write("")
        st.markdown("""
        ## Iory Huarca Astete
        ##### Carrera profesional de Ingeniería Ambiental
        **correo**: iory.huarca@upch.pe
        """)

# Definición de estilos para la interfaz gráfica
# Estilo del contenedor principal
styles = {
    "container": {
        "margin": "0px !important",  # Márgenes del contenedor
        "padding": "0 !important",  # Relleno del contenedor
        "align-items": "stretch",  # Alineación de los elementos dentro del contenedor
        "background-color": "#fafafa"  # Color de fondo del contenedor
    },
    # Estilo para los iconos
    "icon": {
        "color": "black",  # Color del icono
        "font-size": "20px"  # Tamaño de fuente del icono
    }, 
    # Estilo para los enlaces de navegación
    "nav-link": {
        "font-size": "20px",  # Tamaño de fuente del enlace
        "text-align": "left",  # Alineación del texto a la izquierda
        "margin": "0px",  # Márgenes del enlace
        "--hover-color": "#fafa"  # Color al pasar el mouse sobre el enlace
    },
    # Estilo para el enlace de navegación seleccionado
    "nav-link-selected": {
        "background-color": "#ff4b4b",  # Color de fondo del enlace seleccionado
        "font-size": "20px",  # Tamaño de fuente del enlace seleccionado
        "font-weight": "normal",  # Grosor de la fuente (normal en este caso)
        "color": "black",  # Color del texto del enlace seleccionado
    },
}
# Estructura del menú
menu = {
    'title': 'Menu principal',  # Título del menú principal
    'items': { 
        'Inicio' : {  # Primer elemento del menú principal
            'action': None,  # Acción a realizar al seleccionar este elemento (None indica ninguna acción)
            'item_icon': 'house',  # Ícono asociado al elemento ('house' en este caso)
            'submenu': {  # Submenú asociado al elemento 'Inicio'
                'title': None,  # Título del submenú (None indica sin título)
                'items': {  # Elementos del submenú
                    'Gráfico 1' : {'action': do_chart1, 'item_icon': 'pie-chart-fill', 'submenu': None},  # Elemento 1 del submenú
                    'Gráfico 2' : {'action': do_chart2, 'item_icon': 'bar-chart-fill', 'submenu': None},  # Elemento 2 del submenú
                    'Gráfico 3' : {'action': do_chart3, 'item_icon': 'bar-chart-line', 'submenu': None},  # Elemento 3 del submenú
                    'Gráfico 4' : {'action': do_chart4, 'item_icon': 'bar-chart-line-fill', 'submenu': None} # Elemento 4 del submenú
                },
                'menu_icon': None,  # Ícono asociado al submenú (None indica sin ícono)
                'default_index': 0,  # Índice predeterminado al cargar el submenú
                'with_view_panel': 'main',  # Indica dónde mostrar el contenido del submenú (en el área principal)
                'orientation': 'horizontal',  # Orientación del submenú (horizontal en este caso)
                'styles': styles  # Estilos del submenú
            }
        },
        'Acerca' : {  # Segundo elemento del menú principal
            'action': do_acerca,  # Acción a realizar al seleccionar este elemento (do_acerca en este caso)
            'item_icon': 'info-square',  # Ícono asociado al elemento ('info-square' en este caso)
             'submenu': {  # Submenú asociado al elemento 'Acerca'
                'title': None,  # Título del submenú (None indica sin título)
                'items': {  # Elementos del submenú
                    'Definición' : {'action': None, 'item_icon': '-', 'submenu': None},  # Elemento 1 del submenú
                },
                'menu_icon': None,  # Ícono asociado al submenú (None indica sin ícono)
                'default_index': 0,  # Índice predeterminado al cargar el submenú
                'with_view_panel': 'main',  # Indica dónde mostrar el contenido del submenú (en el área principal)
                'orientation': 'horizontal',  # Orientación del submenú (horizontal en este caso)
                'styles': styles  # Estilos del submenú
            }
        },
        'Nosotros' : {  # Tercer elemento del menú principal
            'action': None,  # Acción a realizar al seleccionar este elemento (None indica ninguna acción)
            'item_icon': 'people',  # Ícono asociado al elemento ('people' en este caso)
            'submenu': {  # Submenú asociado al elemento 'Nosotros'
                'title': None,  # Título del submenú (None indica sin título)
                'items': {  # Elementos del submenú
                    '¿Quiénes somos?' : {'action': do_nosotros, 'item_icon': '-', 'submenu': None}  # Elemento 1 del submenú
                },
                'menu_icon': None,  # Ícono asociado al submenú (None indica sin ícono)
                'default_index': 0,  # Índice predeterminado al cargar el submenú
                'with_view_panel': 'main',  # Indica dónde mostrar el contenido del submenú (en el área principal)
                'orientation': 'horizontal',  # Orientación del submenú (horizontal en este caso)
                'styles': styles  # Estilos del submenú
            }
        },
    },
    'menu_icon': 'clipboard2-check-fill',  # Ícono asociado al menú principal
    'default_index': 0,  # Índice predeterminado al cargar el menú principal
    'with_view_panel': 'sidebar',  # Indica dónde mostrar el contenido del menú principal (en la barra lateral)
    'orientation': 'vertical',  # Orientación del menú principal (vertical en este caso)
    'styles': styles  # Estilos del menú principal
}
# Definición de una función para mostrar un menú interactivo
def show_menu(menu):
    # Función interna para obtener las opciones del menú
    def _get_options(menu):
        options = list(menu['items'].keys())
        return options
    # Función interna para obtener los iconos asociados a las opciones del menú
    def _get_icons(menu):
        icons = [v['item_icon'] for _k, v in menu['items'].items()]
        return icons
    # Configuración de parámetros para la función de menú
    kwargs = {
        'menu_title': menu['title'],
        'options': _get_options(menu),
        'icons': _get_icons(menu),
        'menu_icon': menu['menu_icon'],
        'default_index': menu['default_index'],
        'orientation': menu['orientation'],
        'styles': menu['styles']
    }
    # Obtener el tipo de panel de vista (sidebar o main)
    with_view_panel = menu['with_view_panel']
    # Mostrar el menú en el panel correspondiente
    if with_view_panel == 'sidebar':
        with st.sidebar:
            menu_selection = option_menu(**kwargs)
    elif with_view_panel == 'main':
        menu_selection = option_menu(**kwargs)
    else:
        # Lanzar una excepción si el tipo de panel de vista no es reconocido
        raise ValueError(f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")
    # Lógica para manejar la selección del menú "Inicio"
    if menu_selection == 'Inicio':
        if menu['items'][menu_selection]['submenu']:
            pass
            # col1, col2 = st.columns(2)
            # selected_year = col1.slider("Seleccione año:", min(df["PERIODO"].unique()), max(df["PERIODO"].unique()))
            # st.session_state['anio_seleccionado'] = selected_year
            # filtered_year = df[df["PERIODO"] == selected_year]
            # reg_nat_values = filtered_year["REG_NAT"].unique()
            # reg_nat_values = reg_nat_values[~pd.isna(reg_nat_values)]  # Excluir valores NaN
            # selected_reg_nat = col2.radio("Seleccione región natural:", reg_nat_values, horizontal=True)
            # st.session_state['df_guardado'] = filtered_year[filtered_year["REG_NAT"] == selected_reg_nat]
            # st.toast('Seleccionaste año: '+str(selected_year)+' 📅', icon='❤')
            # st.toast('Seleccionaste región: '+selected_reg_nat+' ⛰️', icon='😍')
    # Lógica para mostrar submenú si está presente
    if menu['items'][menu_selection]['submenu']:
        show_menu(menu['items'][menu_selection]['submenu'])
    # Lógica para ejecutar la acción asociada si está presente
    if menu['items'][menu_selection]['action']:
        menu['items'][menu_selection]['action']()
# Mostrar una imagen en la barra lateral usando Streamlit
st.sidebar.image('https://www.precayetanovirtual.pe/moodle/pluginfile.php/1/theme_mb2nl/loadinglogo/1692369360/logo-cayetano.png', use_column_width=True)
# Llamar a la función para mostrar el menú interactivo
show_menu(menu)
# Crear tres columnas en la barra lateral (1:8:1 ratio)
col1, col2, col3 = st.sidebar.columns([2, 4, 2])
# Espacio en blanco en la primera y tercera columna para centrar la imagen
with col1:
    st.write("")
# Mostrar una imagen en la segunda columna, probablemente un avatar o logotipo
with col2:
    st.image('reaccion.png', use_column_width=True)
# Espacio en blanco en la tercera columna para centrar la imagen
with col3:
    st.write("")
# Mostrar un texto en la barra lateral después de las columnas y agregar efecto de nieve
st.sidebar.text("Ing. ambiental - 2024")  
