# Mengimpor modul-modul yang dibutuhkan
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image

# Mengkonfigurasi laman web
st.set_page_config(
    page_title="Ketimpangan Listrik, Ketimpangan Kesejahteraan",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': '''
        **Sebuah cerita pendek tentang Listrik dan Indonesia**
        https://www.linkedin.com/in/anggoro-yudho-nuswantoro-7b865010/'''
    }
)

# Pembuka artikel
st.title('Ketimpangan Listrik, Ketimpangan Kesejahteraan?')
stringHeader =  '*Penulis : **Anggoro Yudho Nuswantoro** *'
st.markdown(stringHeader)
image = Image.open('listrik01.jpg')
st.image(image, caption='Saluran Transmisi Tegangan Tinggi 500KV')

string1 = '''
         Dalam kehidupan modern, energi listrik merupakan bentuk energi yang paling mudah dibangkitkan, 
         didistribusikan, dan digunakan. Penggunaan energi listrik sangat luas dan beragam dan melibatkan
         semua sektor, baik sektor rumah tangga, sektor komersial maupun sektor industri. 
         
         Sering tidak kita sadari, energi listrik telah menjadi bagian tidak terpisahkan dari kehidupan 
         manusia masa kini. Bahkan, hampir semua aspek kehidupan bergantung pada keberadaan listrik, 
         tingkat penggunaan energi listrik dapat digunakan menjadi penanda tingkat kesejahteraan suatu 
         masyarakat. 
         
         Artikel ini mencoba melihat bagaimana perbandingan penggunaan listrik di Indonesia dan di 
         negara-negara ASEAN lainnya, lalu menggunakannya untuk meneropong tingkat kesejahteraan masyarakat 
         di masing-masing negara tersebut.
         '''
st.write(string1)

# Mengimport dataset
ASEANElecGen_df = pd.read_csv('ASEANElecGen.csv',sep=';')
ASEANElecGen_df = ASEANElecGen_df[ASEANElecGen_df['Year']>=2000]
ASEANElecGen_df = ASEANElecGen_df[ASEANElecGen_df['Year']<=2020].reset_index()
ASEANElecGenPerCapita_df = pd.read_csv('ASEANElecGenPerCapita.csv',sep=';')
ASEANElecGenPerCapita_df = ASEANElecGenPerCapita_df[ASEANElecGenPerCapita_df['Year']>=2000]
ASEANElecGenPerCapita_df = ASEANElecGenPerCapita_df[ASEANElecGenPerCapita_df['Year']<=2020].reset_index()
ASEANElecGen_df['Population'] = ASEANElecGen_df['Electricity generation (TWh)']*1000000000 / ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df['Per capita electricity (kWh)'] = ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df = ASEANElecGen_df.astype({'Population':'int64','Per capita electricity (kWh)':'int64'})

# Perbandingan pemakaian listrik
st.markdown('#### Perbandingan Pemakaian Listrik Indonesia dengan Negara ASEAN lain')
col1, col2 = st.columns([1,1])
with col1:
    st.markdown('**Gambar 1.** Pemakaian Listrik di ASEAN 2000-2020')
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', y='Electricity generation (TWh)', color='Country')
    st.altair_chart(c, use_container_width=True)
with col2:
    st.markdown('**Gambar 2.** Pemakaian Listrik Tahun Tertentu')
    tahun = st.slider('Tahun', min_value=2000, max_value=2020, value=2020, label_visibility="collapsed")
    c = alt.Chart(ASEANElecGen_df[ASEANElecGen_df['Year']==tahun]).mark_bar().encode(
       alt.X('Country', sort='-y'), 
       alt.Y('Electricity generation (TWh)'),color='Country')
    st.altair_chart(c, use_container_width=True)
warna1 = st.radio(
    "Mode warna grafis",
    ('Hanya Indonesia', 'Semua Negara'))

st.markdown('Sumber: https://ourworldindata.org/ & https://www.worldbank.org/en/home')

string2 = '''
        Dari data pemakaian listrik di tingkat agregat / negara, dapat dilihat bahwa Indonesia adalah pengguna 
        listrik terbesar di wilayah Asia Tenggara (ASEAN) dari tahun ke tahun, terutama sejak tahun 2008. 
        
        Namun, tidaklah tepat jika kita hanya melihat dari besarnya pemakaian agregat satu negara, karena besarnya 
        populasi di tiap negara yang berbeda.
        '''
st.write(string2)

st.subheader('Populasi Penduduk Negara ASEAN')

col1, col2, col3 = st.columns([1,3,1])

with col2:
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', y='Population', color='Country')
    st.altair_chart(c, use_container_width=True)



string3 = '''
         Pada tampilan chart di atas, terlihat jelas bahwa jumlah penduduk masing-masing negara berbeda dan terdapat 
         perbedaan yang cukup besar antara Indonesia dan negara ASEAN lainnya. 
         
         Untuk itu, akan lebih tepat jika yang diperbandingkan adalah pemakaian listrik per kapita di masing-masing
         negara ASEAN. 
         '''
st.write(string3)

st.subheader('Perbandingan Pemakaian Listrik Per Kapita Indonesia dengan Negara ASEAN lain')

c = alt.Chart(ASEANElecGen_df).mark_line().encode(
    x='Year', y='Per capita electricity (kWh)', color='Country')
st.altair_chart(c, use_container_width=True)

string3 = '''
         Jika pada chart pertama terlihat bahwa pemakaian listrik Indonesia adalah yang terbesar, di chart ini 
         terlihat bahwa secara per kapita, penggunaan listrik terbesar adalah oleh masyarakat Brunei dan Singapura.
         Kedua negara kecil yang dari perspektif agregat pemakaian listrik tidak begitu signifikan, ternyata dari
         sisi per kapita merupakan konsumen listrik yang masif.
         
         Untuk membantu memperjelas grafik di atas, disajikan pemakaian listrik per kapita pada tahun 
         2020 di negara-negara ASEAN dalam bentuk Bar Chart di bawah ini:
         
         '''
st.write(string3)

tahun1 = st.slider('Tahun', 2000, 2020, 2020, key='123')
ASEAN2000_df = pd.DataFrame()
## ASEAN2000_df = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Entity','Per capita electricity (kWh)']].reset_index()
#ASEAN2000_df['Country'] = ASEANElecGen_df[ASEANElecGen_df['Year']==2020].sort_values(by='Per capita electricity (kWh)',ascending=False)['Country']
ASEAN2000_df[['Country','Per capita electricity (kWh)']] = ASEANElecGen_df[ASEANElecGen_df['Year']==tahun1].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Country','Per capita electricity (kWh)']]

#c = alt.Chart(ASEAN2000_df).mark_Sbar().encode(
#       alt.X('Country', sort='-y'), 
#       alt.Y('Per capita electricity (kWh)'),
#       color='Country')
#st.altair_chart(c, use_container_width=True)

domain = ['Indonesia','Malaysia','Singapore','Laos','Thailand','Vietnam','Philippines', 'Cambodia','Myanmar','Brunei']
range_ = ['#1CD9EF','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696']
#range_ = ['#F44336', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray']

c = alt.Chart(ASEAN2000_df).mark_bar().encode(
        alt.X('Country', sort='-y'), 
        alt.Y('Per capita electricity (kWh)'),
        color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
st.altair_chart(c, use_container_width=True)

string4 = '''
         Dari tahun ke tahun, terlihat jelas bahwa Brunei dan Singapura meninggalkan mayoritas negara ASEAN dalam 
         hal pemakaian listrik per kapita, dengan pemakaian berkisar 9,000 - 10.000 kWh per kapita per tahun.
         
         Kemudian Malaysia dan Laos menyusul dengan pemakaian berkisar 4.000 - 5.000 kWh per kapita per tahun. 
         Selanjutnya adalah Thailand dan Vietnam dengan pemakaian listrik per kapita per tahun berkisar 2.000 kWH. 
         
         Vietnam dan Laos awalnya memiliki pemakaian listrik per kapita per tahun yang setara dengan Indonesia.
         Tetapi di mulai tahun 2007, Vietnam meninggalkan Indonesia. Di tahun 2010, Laos meninggalkan Indonesia
         dan bahkan meninggalkan Vietnam. 
         
         Sangat nampak bahwa Indonesia jauh tertinggal dibanding tetangga-tetangga yang lebih makmur. Nampak bahwa
         Pemakaian listrik per kapita di Singapura dan di Brunei sekitar sembilan kali lipat pemakaian per kapita 
         di Indonesia, yang hanya sekitar 1000 kWH. 
         
         Indonesia hanya lebih tinggi dibandingkan Myanmar, Kamboja dan Philipina. 
         '''
st.write(string4)

st.subheader('Apakah ketimpangan listrik menunjukkan ketimpangan kesejahteraan?')

string5 = '''
         Di awal artikel, dinyatakan bahwa penggunaan energi listrik dapat digunakan sebagai penanda kesejahteraan 
         masyarakat. Bagaimana kita, secara sederhana, memastikan bahwa asumsi tersebut tepat? 
         
         Salah satu ukuran yang sering digunakan oleh ekonom adalah GDP/Kapita (yaitu pendapatan domestik bruto
         dibagi jumlah populasi). Mari kita bandingkan GDP/Kapita dari masing-masing negara di ASEAN.
         '''
st.write(string5)

ASEANGDP_df = pd.read_csv('GDP.csv',sep=';')
listYear = [str(i) for i in range(2000,2022)]
ASEANGDP_dfNew = pd.DataFrame()
for i in listYear:
    ASEANGDP_dfTemp = pd.DataFrame()
    yearSeries = pd.Series([i for x in range(10)])
    ASEANGDP_dfTemp[['Country','Code']] =ASEANGDP_df[['Country Name','Country Code']]
    ASEANGDP_dfTemp['Year'] = yearSeries
    ASEANGDP_dfTemp['GDP'] = ASEANGDP_df[i]
    ASEANGDP_dfNew = pd.concat([ASEANGDP_dfNew,ASEANGDP_dfTemp])
ASEANGDP_dfNew = ASEANGDP_dfNew.reset_index()

ASEANGDP_dfNew = ASEANGDP_dfNew.astype({'Year':'int64'})
ASEANGDP_dfNew = ASEANGDP_dfNew[ASEANGDP_dfNew['Year']<=2020]
ASEANGDP_dfNew = ASEANGDP_dfNew.sort_values(by=['Country','Year'],ignore_index=True)

ASEANGDP_dfNew['Population'] =ASEANElecGen_df['Population']
ASEANGDP_dfNew['GDP/Capita'] = ASEANGDP_dfNew['GDP']/ASEANGDP_dfNew['Population']
ASEANGDP_dfNew = ASEANGDP_dfNew.astype({'GDP/Capita':'int64'})

col1, col2 = st.columns(2)

with col1:
    st.write('')
    st.write('')
    st.write('')
    c = alt.Chart(ASEANGDP_dfNew).mark_line().encode(
        x='Year', y='GDP/Capita', color='Country')
    st.altair_chart(c, use_container_width=True)

with col2:
    tahun2 = st.slider('Tahun', 2000, 2020, 2020, key='234')
    c = alt.Chart(ASEANGDP_dfNew[ASEANGDP_dfNew['Year']==tahun2]).mark_bar().encode(
            alt.X('Country', sort='-y'), 
            alt.Y('GDP/Capita'),
            color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
    st.altair_chart(c, use_container_width=True)

string6 = '''
         Terlihat bahwa Pemakaian listrik per kapita tidak secara tepat 100% menunjukkan ketimpangan
         kesejahteraan (sebagaimana diukur melalui GDP/Kapita). Namun kita bisa merasakan adanya ketimpangan baik pada 
         chart pemakaian listrik per kapita maupun pada chart GDP/Kapita. 
         
         Singapura dan Brunei telah jauh melampaui negara-negara ASEAN lainnya dalam hal kesejahteraan masyarakat. 
         Malaysia dan Thailand berada pada urutan berikutnya. Sedangkan negara ASEAN lainnya masih mengekor di 
         belakang.
         
         Grafik di bawah ini menujukkan bagaimana perkembangan GDP/Capita dan Pemakaian listrik per kapita 
         dari tahun ke tahun untuk masing-masing negara. CHart telah dinormalisasi dengan titik tertinggi GDP/Kapita 
         dan Pemakaian Listrik per kapita, agar dapat dibandingkan pada satu grafik yang sama. 
         '''
st.write(string6)


ASEANElecGen_df['GDP/Capita'] = ASEANGDP_dfNew['GDP/Capita']

negara = st.selectbox(
    'Negara yang dipilih: ', domain)
tickerDF = pd.DataFrame()
tickerDF['Per capita electricity (kWh)'] = ASEANElecGen_df[ASEANElecGen_df['Country']==negara]['Per capita electricity (kWh)']
tickerDF['kWh/Capita (Normalized)'] = tickerDF['Per capita electricity (kWh)']/max(tickerDF['Per capita electricity (kWh)'])
tickerDF['GDP/Capita'] = ASEANElecGen_df[ASEANElecGen_df['Country']==negara]['GDP/Capita']
tickerDF['GDP/Capita (Normalized)'] = tickerDF['GDP/Capita']/max(tickerDF['GDP/Capita'])
tickerDF['Year']= ASEANElecGen_df[ASEANElecGen_df['Country']==negara]['Year']
tickerDF = tickerDF.set_index('Year')

base = alt.Chart(tickerDF.reset_index()).transform_calculate(
    elec="'kWh/Capita (Normalized)'",
    GDP="'GDP/Capita (Normalized)'",
)
scale = alt.Scale(domain=["GDP/Capita (Normalized)", "kWh/Capita (Normalized)"], range=['lightblue','red'])
elec_plot = base.mark_line().encode(
    alt.X('Year'),
    alt.Y('kWh/Capita (Normalized)', axis = None),
    color=alt.Color('elec:N', scale=scale, title=''),
)
GDP_plot = base.mark_line().encode(
  x = alt.X('Year'), 
  y = alt.Y('GDP/Capita (Normalized)'),
  color=alt.Color('GDP:N', scale=scale, title=''),
)
altair_plot = alt.layer(elec_plot, GDP_plot)
st.altair_chart(altair_plot, use_container_width=True)


stringFooter = '''
**Sumber data** :

*1. World Bank*

*2. World in Data*    
                '''
st.markdown(stringFooter)

