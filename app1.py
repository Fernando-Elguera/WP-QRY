from google.protobuf.symbol_database import Default
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import datetime
import base64
import numpy as np
import os
from pyxlsb import open_workbook as open_xlsb
import streamlit.components.v1 as components

#import gspread

#este codigo me ayuda a leer desde google
#gc = gspread.service_account(filename='wip-qry-814f60ad261d.json')

# Abrir por titulo
#sh = gc.open("Survey_Results")

# Seleccionar primera hoja
#worksheet = sh.get_worksheet(0)


#worksheet.update(ng.link')
#worksheet.update('Z3', 'fecha')'Z1', 'dominio')
#worksheet.update('Z2', 'scrapi
#worksheet.update('Z4', '22/04/2021')
#worksheet.update('Z5', 'num URLs indexadas')
#worksheet.update('Z6', '10')

st.set_page_config(page_title='WIP & QRY + Ordenes Antiguas')
st.header('WIP & QRY + Ordenes Antiguas')
#st.subheader('Fecha')

### --- LOAD DATAFRAME
today = datetime.date.today()
date = st.sidebar.date_input('Fecha a buscar', today)
excel_file = 'Wip_QRY.xlsx'

# Para bajar el archivo de excel
def get_binary_file_downloader_html(bin_file, file_label='File'):
     with open(bin_file, 'rb') as f:
         data = f.read()
     bin_str = base64.b64encode(data).decode()
     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
     return href


sheet_name = date
sheet_name = sheet_name.strftime("%Y-%m-%d")
df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:V',
                   header=3)

# arreglo_aux = df.to_numpy()
# for i in range(len(arreglo_aux.T[10])):
#     if arreglo_aux.T[10][i] == "-":
#         arreglo_aux.T[10][i] = 0
# arreglo_aux.T[10]



df_general = pd.read_excel(excel_file,
                   sheet_name='General',
                   usecols='B:V',
                   header=3)


df_participants = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols='X:Y',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION

planta = df['Planta'].unique().tolist()
ages = df['Work_Order'].unique().tolist()

work_order_selection = st.slider('Work_Order:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))

planta_selection = st.multiselect('Planta:',
                                    planta,
                                    default=planta)# Cual Planta Inicia, para aparecer todas porner planta

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Work_Order'].between(*work_order_selection)) & (df['Planta'].isin(planta_selection))
mask_general = (df_general['Work_Order'].between(*work_order_selection)) & (df_general['Planta'].isin(planta_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Ordenes disponibles: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Dias']).count()[['Work_Order']]
df_grouped = df_grouped.rename(columns={'Work_Order': 'Cantidad'})
df_grouped = df_grouped.reset_index()

df_grouped1 = df_general[mask_general].groupby(by=['Fecha']).count()[['Mayor']]
df_grouped1 = df_grouped1.rename(columns={'Mayor': 'Cantidad'})
df_grouped1 = df_grouped1.reset_index()

df_grouped2 = df_general[mask_general].groupby(by=['Fecha']).count()[['Menor']]
df_grouped2 = df_grouped2.rename(columns={'Menor': 'Cantidad'})
df_grouped2 = df_grouped2.reset_index()

# --- DISPLAY IMAGE & DATAFRAME
#col1, col2 = st.columns(2)

#image = Image.open('images/usi.jpg')
#print(image)
#col1.image(image,
#        caption='Fer Elguera 15249',
#        use_column_width=True)
#col2.dataframe(df[mask])       
df[mask]

#Codigo para escribir en HTML
# html_string = '''
# <h1>HTML string in RED</h1>
# <script language="javascript">
# document.querySelector("h1").style.color = "red";
# console.log("Streamlit runs JavaScript");
# alert("Streamlit runs JavaScript");
# </script>'''
# components.html(html_string)  # JavaScript works
# st.markdown(html_string, unsafe_allow_html=True)  # JavaScript doesn't work
#HTML

st.markdown(get_binary_file_downloader_html('Wip_QRY.xlsx', 'Excel'), unsafe_allow_html=True)

#Suma las ordenes mayores o igual a 20 dias
# df_g = (df['Antiguedad']>=20).sum()
# df_g

bar_chart = px.bar(df_grouped,
                   x='Dias',
                   y='Cantidad',
                   text='Cantidad',
                   title="<b>Rango de ordenes abiertas General B2-B3</b>",
                  #orientation="h",
                  # width=1000,
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
                    #orientation="h",
                   # width=1000,
                    color_discrete_sequence = ['#0083B8']*len(df_grouped2,),
                    template= 'plotly_white')

st.plotly_chart(bar_chart)
left_column, right_column = st.columns(2)
left_column.plotly_chart(bar_chart1, use_container_width=True)
right_column.plotly_chart(bar_chart2, use_container_width=True)


# --- PLOT PIE CHART
# pie_chart = px.pie(df_participants,
#                 title='Total No. of Participants',
#                 values='Participants',
#                 names='Departments')

# st.plotly_chart(pie_chart)
           
