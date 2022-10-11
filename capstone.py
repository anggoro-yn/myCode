import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title('Ketimpangan Listrik, Ketimpangan Kesejahteraan?')

string1 = '''
         Energi listrik merupakan bentuk energi yang paling mudah digunakan, baik oleh sektor rumah tangga, komersial maupun industri. 
         Karena energi listrik telah menjadi bagian tidak terpisahkan dari kehidupan manusia, energi listrik dapat digunakan menjadi 
         penanda tingkat kemakmuran suatu masyarakat. Artikel ini mencoba melihat bagaimna perbandingan pemakaian listrik di Indoensia
         dan di negara-negara ASEAN lain dan melihat sejauh apa korelasinya dengan kesejahteraan masyarakat di masing-masing negara.
         
         Setelah itu, pemakaian listrik di masing-masing provinsi di Indonesia akan dibandingkan untuk melihat bagaimana kemajuan dan 
         kesejahteraan telah dicapai di masing-masing daerah.
         '''
st.write(string1)



ASEANElecGen_df = pd.read_csv('ASEANElecGen.csv',sep=';')
ASEANElecGen_df = ASEANElecGen_df[ASEANElecGen_df['Year']>=2000]
ASEANElecGen_df = ASEANElecGen_df[ASEANElecGen_df['Year']<=2020].reset_index()

ASEANElecGenPerCapita_df = pd.read_csv('ASEANElecGenPerCapita.csv',sep=';')
ASEANElecGenPerCapita_df = ASEANElecGenPerCapita_df[ASEANElecGenPerCapita_df['Year']>=2000]
ASEANElecGenPerCapita_df = ASEANElecGenPerCapita_df[ASEANElecGenPerCapita_df['Year']<=2020].reset_index()


ASEANElecGen_df['Population'] = ASEANElecGen_df['Electricity generation (TWh)']*1000000000 / ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df['Per capita electricity (kWh)'] = ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df = ASEANElecGen_df.astype({'Population':'int64','Per capita electricity (kWh)':'int64'})

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

st.subheader('Perbandingan Pemakaian Listrik Indonesia dengan Negara ASEAN lain')

c = alt.Chart(ASEANElecGen_df).mark_line().encode(
    x='Year', y='Electricity generation (TWh)', color='Entity')

st.altair_chart(c, use_container_width=True)

string2 = '''
         Dari data pemakaian listrik secara absolut, dapat dilihat bahwa Indonesia adalah pengguna listrik terbesar di wilayah Asia Tenggara (ASEAN). 
         Namun, tidaklah pas jika kita hanya melihat dari besarnya pemakaian agregat satu negara, karena setiap negara memiliki jumlah penduduk yang
         berbeda.
         '''
st.write(string2)

st.subheader('Populasi Penduduk Negara ASEAN')

c = alt.Chart(ASEANElecGen_df).mark_line().encode(
    x='Year', y='Population', color='Entity')

st.altair_chart(c, use_container_width=True)

string3 = '''
         Terlihat jelah bahwa jumlah penduduk masing-masing negara sangat jauh perbedaannya. 
         
         Untuk itu, akan lebih tepat jika dibandingkan adalah pemakaian listrik per kapita. 
         '''
st.write(string3)

st.subheader('Perbandingan Pemakaian Listrik Per Kapita Indonesia dengan Negara ASEAN lain')

c = alt.Chart(ASEANElecGen_df).mark_line().encode(
    x='Year', y='Per capita electricity (kWh)', color='Entity')

st.altair_chart(c, use_container_width=True)

string3 = '''
         Untuk membantu memperjelas grafik di atas, disajikan data pemakaian listik per kapita pada tahun 2020 di bawah ini:
         '''
st.write(string3)

ASEANElecGen_df[ASEANElecGen_df['Year']==2020][['Entity','Per capita electricity (kWh)']]

string4 = '''
         Sangat nampak bahwa Indonesia jauh tertinggal dibanding banyak negara tetangga. Pemakaian listrik per kapita di Singapura 
         dan di Brunei sekitar semnbilan kali lipat pemakaian per kapita di Indonesia. Indonesia hanya lebih tinggi dibandingkan 
         Myanmar, Kamboja dan Philipina. 
         '''
st.write(string4)



