# -*- coding: utf-8 -*-
"""
@author: bmoreira
"""
import pandas as pd
import streamlit as st
import pickle

import pybase64
from io import BytesIO


st.image('./HEADER.png')

st.write("""
# App para precificação de produtos
""")


st.sidebar.header('input de atributos pelo usuário')

st.sidebar.markdown("""[Exempo de CSV para input ](https://github.com/brunoOnm/app-precificacao/raw/main/teste_price.csv)""")

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Carregue seu arquivo XLSX", type=["xlsx"])

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='predição')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):    
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = pybase64.b64encode(val) 
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download base de dados</a>' # decode b'abc' => abc



if uploaded_file is not None:
    input_df = pd.read_excel(uploaded_file)
    # if uploaded_file.type == 'csv':
    #      input_df = pd.read_csv(uploaded_file,encoding = 'latin1', decimal =',',sep =';')
    # elif uploaded_file.type == 'xlsx':
          
else:
    
    def user_input_features():
        # Places = st.sidebar.multiselect("Quais as categorias presentes no entorno?", 
        #                  ["Saúde até 3km", "Saúde até 5km",
        #                  "ônibus influente 5 km", "ônibus influente mais que 5 km"])
        
        nome = st.sidebar.text_input('Digite o nome do produto')
        lat = st.sidebar.number_input('Digite a latitude do produto')
        long = st.sidebar.number_input('Digite a longitude do produto')
        
        st.sidebar.markdown('Quais as categorias de estabelecimentos presentes no entorno ?')
        saude_3km = st.sidebar.checkbox('Saúde até 3km')
        if saude_3km:
               saude_3km = 1
        else:
                   saude_3km = 0
                   
        saude_5km = st.sidebar.checkbox('Saúde até 5 km')
        
        if saude_5km:
               saude_5km = 1
        else:
                   saude_5km = 0
        onibus_5km = st.sidebar.checkbox('Ônibus influente 5 km')
        
        if onibus_5km:
               onibus_5km = 1
        else:
              onibus_5km = 0  
        
        onibus_mais_5km = st.sidebar.checkbox('Ônibus influente mais que 5 km')
        if onibus_mais_5km:
            onibus_mais_5km = 1
        else:
             onibus_mais_5km = 0   
        
#         Aglomerado 21	Capital	RS	Estratégia
#         Aglomerado 22	Região 1	RJ	
# 		SP	

        st.sidebar.markdown('Marque as opções relacionados ao ponto analisado ?')
        capital = st.sidebar.checkbox('capital ')
        if capital:
               capital = 1
        else:
                   capital = 0
                   
        ufSP = st.sidebar.checkbox('estado de SP ')
        if ufSP:
               ufSP = 1
        else:
                   ufSP = 0
                   
        ufRS = st.sidebar.checkbox('estado do RS ')
        if ufRS:
               ufRS = 1
        else:
                   ufRS = 0
                   
        ufRJ = st.sidebar.checkbox('estado do RJ ')
        if ufRJ:
               ufRJ = 1
        else:
                   ufRJ = 0  
                   
        aglomerado21 = st.sidebar.checkbox('aglomerado 21 ')
        if aglomerado21:
               aglomerado21 = 1
        else:
                   aglomerado21 = 0
                   
        aglomerado22 = st.sidebar.checkbox('aglomerado 22 ')
        if aglomerado22:
               aglomerado22 = 1
        else:
                   aglomerado22 = 0
                   
        rg1 = st.sidebar.checkbox('região 1  ')
        if rg1:
               rg1 = 1
        else:
                   rg1 = 0    
                   
        estrategia = st.sidebar.checkbox('produto combate  ')
        if estrategia:
               estrategia = 1
        else:
                   estrategia = 0
                   
        
        st.sidebar.markdown('Informações sociodemográficas do entorno:')
        renda_media = st.sidebar.slider('renda média do entorno', 0 , 20000)
        dens_demog = st.sidebar.slider('Densidade demográfica', 0 , 20000)
        dom_alug = st.sidebar.slider('percentual de domicílios alugados', 0.0, 1.0)
        subs_maxf2 = st.sidebar.slider('Subsídio Max F2', 0, 29000) 
        renda_c1 = st.sidebar.slider('Renda média C1', 0 , 20000)
        renda_b2 = st.sidebar.slider('Renda média B2', 0 , 20000)
        domic_a2 = st.sidebar.slider('% domicílios A2', 0.0, 1.0)        
        avaliacao = st.sidebar.slider('Avaliação', 0 , 300000)
           
        data = {'nome':nome,
                'lat': lat,
                'lon': long,
                'renda_media': renda_media,
                'pct_algd': dom_alug,
                'dens_demog': dens_demog,
                'sub_max_f2': subs_maxf2,
                'rmc1': renda_c1,
                'rmb2': renda_b2,
                'pcta2':domic_a2,
                'avaliacao': avaliacao,
                'parada de ônibus_maior_5km_influente': onibus_mais_5km,
                'parada de ônibus_ate_5km_influente':onibus_5km, 
                'Saúde_ate_5km_influente':saude_5km,
                'Saúde_ate_3km_influente':saude_3km,
                'estrategia': estrategia,
                'rg1': rg1,
                'aglomerado22': aglomerado22,
                'aglomerado21': aglomerado21,
                'ufRJ': ufRJ,
                'ufRS': ufRS,
                'ufSP': ufSP,
                'capital': capital
                }
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()

# Displays the user input features
   
st.subheader('Características capturadas:')

if uploaded_file is not None:
    st.write(input_df.head())
else:
    st.write('Aguarde o arquivo ser carregado. Por enquanto demonstrando os inputs manuais.')
    st.write(input_df.head())
    
st.subheader('Localização dos produtos:')    
st.map(input_df.loc[input_df.lat.notnull()][['lat','lon']])       

# Reads in saved classification model
clf_bojo = pickle.load(open('clf_bojo.pickle', 'rb'))
clf_cauda = pickle.load(open('clf_cauda.pickle', 'rb'))
binom_results = pickle.load(open('binom_results.pickle', 'rb'))
reg_finan = pickle.load(open('reg_finan.pickle', 'rb'))
reg_subs = pickle.load(open('reg_subs.pickle', 'rb'))

cols_finan = ['renda_media','pct_algd','capital','rg1','estrategia','sub_max_f2','avaliacao']
cols_subs = ['dens_demog','renda_media','rmc1','rmb2','pcta2', 'estimativa_financiamento','avaliacao','estrategia',
             'aglomerado21','aglomerado22','rg1','ufRS','ufRJ']
exploratorias_bojo = ['Saúde_ate_3km_influente', 'parada de ônibus_ate_5km_influente','rmb2' , 'capital','ufSP' , 'avaliacao','estimativa_subsidio']
exploratorias_cauda = ['Saúde_ate_3km_influente', 'Saúde_ate_5km_influente', 'parada de ônibus_ate_5km_influente', 'parada de ônibus_maior_5km_influente','rmb2' , 'capital','ufSP' , 'avaliacao','estimativa_subsidio']
proporção_bojo =['Predict_cauda','Predict_bojo','estimativa_subsidio', 'avaliacao', 'rmb2', 'ufSP', 'capital', 'Saúde_ate_3km_influente', 'Saúde_ate_5km_influente', 'parada de ônibus_ate_5km_influente','parada de ônibus_maior_5km_influente']


# # Apply model to make predictions

st.image('./predicoes.PNG')
st.subheader('Predições')  
try:
    input_df['estimativa_financiamento'] =  reg_finan.predict(input_df[cols_finan])
    #st.write(input_df['estimativa_financiamento'])
    input_df['estimativa_subsidio'] =  reg_subs.predict(input_df[cols_subs])
    #st.write(input_df['estimativa_subsidio'])
    input_df['Predict_bojo'] = clf_bojo.predict( input_df[exploratorias_bojo] )
    #st.write(input_df['Predict_bojo'])
    input_df['Predict_cauda'] = clf_cauda.predict(input_df[exploratorias_cauda])
    #st.write(input_df['Predict_cauda'])
    input_df['proporcao_bojo'] = binom_results.predict(input_df[proporção_bojo])
    #st.write(input_df['proporcao_bojo'])
    input_df['renda_ponderada_estimada']  = (input_df.proporcao_bojo *  input_df.Predict_bojo ) +  ((1-input_df.proporcao_bojo) *  input_df.Predict_cauda )
    #st.write(input_df['renda_ponderada_estimada'])
    st.write(input_df[['nome','renda_ponderada_estimada','estimativa_financiamento', 'estimativa_subsidio', 'Predict_bojo','Predict_cauda','proporcao_bojo']])
    


    df = input_df
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    
except:
    df = input_df


    

