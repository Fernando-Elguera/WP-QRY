from google.protobuf.symbol_database import Default
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import datetime
import base64
import numpy as np
import os
# from pyxlsb import open_workbook as open_xlsb
import streamlit.components.v1 as components


st.set_page_config(page_title='WIP & QRY + Ordenes Antiguas')
st.header('WIP & QRY + Ordenes Antiguas')
#st.subheader('Fecha')

### --- LOAD DATAFRAME
today = datetime.date.today()
date = st.sidebar.date_input('Fecha a buscar', today)
excel_file = 'Wip_QRY.csv'

# Para bajar el archivo de excel
# def get_binary_file_downloader_html(bin_file, file_label='File'):
#      with open(bin_file, 'rb') as f:
#         data = f.read()
#      bin_str = base64.b64encode(data).decode()
#      href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
#      return href

# Para cambiar cadena de fecha
Fecha_buscada= date
Fecha_buscada = Fecha_buscada.strftime("%Y-%m-%d")

df = pd.read_csv('WIP_QRY.csv',
                  usecols=['Planta','Work_Order','P/N','Modelo','BU','W/O Qty','W/O GR Qty','W/O Scrap Qty','Balance',  'W/O WIP Amount','Aging -B0','Aging','Shortage','Dias','Aging rank_1','Dashboard_0','Dashboard_1','Rank','Mayor','Menor','Fecha'],)

df_general = pd.read_csv('WIP_QRY.csv',
                  usecols=['Planta','Work_Order','P/N','Modelo','BU','W/O Qty','W/O GR Qty','W/O Scrap Qty','Balance',  'W/O WIP Amount','Aging -B0','Aging','Shortage','Dias','Aging rank_1','Dashboard_0','Dashboard_1','Rank','Mayor','Menor','Fecha'],)

# df_general = pd.read_excel(excel_file,
#                    sheet_name='General',
#                    usecols='B:V',
#                    header=3)

df_participants = pd.read_csv('WIP_QRY.csv',
                 usecols=['Planta','Work_Order','P/N','Modelo','BU','W/O Qty','W/O GR Qty','W/O Scrap Qty','Balance',  'W/O WIP Amount','Aging -B0','Aging','Shortage','Dias','Aging rank_1','Dashboard_0','Dashboard_1','Rank','Mayor','Menor','Fecha'],)

df_participants.dropna(inplace=True)

# df_participants = pd.read_excel(excel_file,
#                                 sheet_name=sheet_name,
#                                 usecols='X:Y',
#                                 header=3)
# df_participants.dropna(inplace=True)


df_fecha = df['Fecha']==Fecha_buscada
filtered_df1 = df[df_fecha]

# # --- STREAMLIT SELECTION

planta = filtered_df1['Planta'].unique().tolist()
ages = filtered_df1['Work_Order'].unique().tolist()

work_order_selection = st.slider('Work_Order:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))



planta_selection = st.sidebar.multiselect('Planta:',
                                    planta,
                                    default=planta)# Cual Planta Inicia, para aparecer todas porner planta

# # --- FILTER DATAFRAME BASED ON SELECTION
# mask = (df['Work_Order'].between(*work_order_selection)) & (df['Planta'].isin(planta_selection))
mask = (filtered_df1['Work_Order'].between(*work_order_selection)) & (filtered_df1['Planta'].isin(planta_selection))
mask_general = (df_general['Work_Order'].between(*work_order_selection)) & (df_general['Planta'].isin(planta_selection))
# number_of_result = df[mask].shape[0]
number_of_result = filtered_df1[mask].shape[0]
st.markdown(f'*Ordenes disponibles: {number_of_result}*')



# # --- GROUP DATAFRAME AFTER SELECTION 
df_grouped = filtered_df1[mask].groupby(by=['Dias']).count()[['Work_Order']]
df_grouped = df_grouped.rename(columns={'Work_Order': 'Cantidad'})
df_grouped = df_grouped.reset_index()

df_grouped1 = df_general[mask_general].groupby(by=['Fecha']).count()[['Mayor']]
df_grouped1 = df_grouped1.rename(columns={'Mayor': 'Cantidad'})
df_grouped1 = df_grouped1.reset_index()

df_grouped2 = df_general[mask_general].groupby(by=['Fecha']).count()[['Menor']]
df_grouped2 = df_grouped2.rename(columns={'Menor': 'Cantidad'})
df_grouped2 = df_grouped2.reset_index()

    

# Para filtrar por columna 

# df_2310 = df['Planta']==2310
# filtered_df = df[df_2310]


filtered_df1[mask]

# Fecha_buscada
# filtered_df


# if Fecha_buscada == filtered_df1:

#     filtered_df1



# df[mask]

# Para filtrar por columna 
# df_2310 = df['Planta']==2310
# filtered_df = df[df_2310]
# filtered_df

# st.markdown(get_binary_file_downloader_html('Wip_QRY.csv', 'Excel'), unsafe_allow_html=True)


bar_chart = px.bar(df_grouped,
                   x='Dias',
                   y='Cantidad',
                   text='Cantidad',
                   title="<b>Rango de ordenes abiertas General B2-B3</b>",
#                   #orientation="h",
#                   # width=1000,
                   color_discrete_sequence = ['#0083B8']*len(df_grouped,),
                   template= 'plotly_white')


bar_chart1 = px.bar(df_grouped1,                    
                    x= 'Fecha',
                    y='Cantidad',
                    text='Cantidad',
                    title="<b>Ordenes abiertas > 20 dias</b>",
                    #orientation="h",
                    # width=1000,
                    color_discrete_sequence = ['#0083B8']*len(df_grouped1,),
                    template= 'plotly_white')



bar_chart2 = px.bar(df_grouped2,                    
                    x= 'Fecha',
                    y='Cantidad',
                    text='Cantidad',
                    title="<b>Ordenes abiertas < 20 dias</b>",                                      
#                     #orientation="h",
#                    # width=1000,
                    color_discrete_sequence = ['#0083B8']*len(df_grouped2,),
                    template= 'plotly_white')

st.plotly_chart(bar_chart)
left_column, right_column = st.columns(2)
left_column.plotly_chart(bar_chart1, use_container_width=True)
right_column.plotly_chart(bar_chart2, use_container_width=True)




           
