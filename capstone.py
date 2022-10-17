# Mengimpor modul-modul yang dibutuhkan
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image

# Mengkonfigurasi laman web
st.set_page_config(
    page_title="Ketimpangan Listrik, Ketimpangan Kesejahteraan",
    #layout="centered",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': '''
        **Sebuah cerita pendek tentang Listrik dan Indonesia**
        https://www.linkedin.com/in/anggoro-yudho-nuswantoro-7b865010/'''
    }
)

# Pembuka artikel
st.title('Ketimpangan Listrik, Ketimpangan Kesejahteraan?')
stringHeader =  'Penulis : **Anggoro Yudho Nuswantoro**'
st.markdown(stringHeader)
image = Image.open('listrik01.jpg')
st.image(image, caption='')

# Sidebar Content
modeWarna = st.sidebar.selectbox(
    "Mode warna grafik",
    ("Indonesia", "Semua Negara")
)

stringInfo1 = '''
            ### Dataset 
            
            Dataset yang digunakan dalam artikel ini bersumber dari :
            
            1. https://ourworldindata.org/ 
            
            2. https://www.worldbank.org/en/home
            '''
st.sidebar.info(stringInfo1)

stringInfo2 = '''
            **Penyetaraan data pembangkitan dan data pemakaian**
            
            Data pemakaian / konsumsi listrik diambil dari dataset pembangkitan listrik (electricity generation). Hal ini 
            karena tidak tersedia data yang secara spesifik menunjukkan besarnya konsumsi listrik di 
            tiap negara. 
            
            Sebagai dasar, listrik adalah realtime commodity yang tidak bisa disimpan dalam waktu lama dan dalam 
            jumlah besar. Sehingga, secara praktis, dapat dikatakan bahwa seluruh energi listrik yang dibangkitkan 
            akan langsung digunakan. Di samping itu, karena jaringan listrik biasanya dibatasi oleh wilayah negara, 
            maka aliran listrik antar negara bisa diabaikan. 
            
            Dengan demikian, energi listrik yang dikonsumsi masyarakat bisa disetarakan dengan jumlah listrik yang 
            dibangkitkan.
            '''
st.sidebar.info(stringInfo2)

stringInfoAuthor = '''
            **Anggoro Yudho Nuswantoro**
            
            Memiliki prinsip: "*Terus belajar hingga usia usai*", Anggoro adalah salah seorang peserta Tetris DQLab tertua.
            Sebagai generasi tua, komputer, pemrograman dan visualisasi data adalah hal baru yang menantang baginya. Tak ingin 
            kalah dari rekan-rekan peserta yang berasal dari generasi milenial, yang bahkan dari kecil sudah terbiasa bermain 
            dengan gawai digital, Anggoro terus menantang dirinya sendiri untuk memberikan yang terbaik.             
            '''
st.sidebar.info(stringInfoAuthor)

domain = ['Indonesia','Malaysia','Singapore','Laos','Thailand','Vietnam','Philippines', 'Cambodia','Myanmar','Brunei']
range_ = ['#1CD9EF','#555555','#606060','#656565','#707070','#757575','#808080','#858585','#909090','#959595']

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
ASEANElecGen_df['Population'] = ASEANElecGen_df['Electricity consumption (TWh)']*1000000000 / ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df['Per capita electricity (kWh)'] = ASEANElecGenPerCapita_df['Per capita electricity (kWh)']
ASEANElecGen_df = ASEANElecGen_df.astype({'Population':'int64','Per capita electricity (kWh)':'int64'})

# Perbandingan pemakaian listrik
st.markdown('#### Perbandingan Pemakaian Listrik Indonesia dengan Negara ASEAN lain')

string0 = '''
        Di bawah ini disajikan grafik pemakaian listrik negara-negara ASEAN pada periode 2000 - 2020. 
        '''
st.write(string0)

col1, col2 = st.columns([1,1])

if modeWarna == "Indonesia":
    with col1:
        st.markdown('**Gambar 1.** Pemakaian Listrik di ASEAN 2000-2020')
        c = alt.Chart(ASEANElecGen_df).mark_line().encode(
            x='Year', 
            y='Electricity consumption (TWh)', 
            color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
        st.altair_chart(c, use_container_width=True)
    with col2:
        st.markdown('**Gambar 2.** Pemakaian Listrik Tahun Tertentu')
        tahun = st.slider('Tahun', min_value=2000, max_value=2020, value=2020, label_visibility="collapsed")
        c = alt.Chart(ASEANElecGen_df[ASEANElecGen_df['Year']==tahun]).mark_bar().encode(
        alt.X('Country', sort='-y'), 
        alt.Y('Electricity consumption (TWh)'),
        color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
        st.altair_chart(c, use_container_width=True)
else:
    with col1:
        st.markdown('**Gambar 1.** Pemakaian Listrik di ASEAN 2000-2020')
        c = alt.Chart(ASEANElecGen_df).mark_line().encode(
            x='Year', y='Electricity consumption (TWh)', color='Country')
        st.altair_chart(c, use_container_width=True)
    with col2:
        st.markdown('**Gambar 2.** Pemakaian Listrik Tahun Tertentu')
        tahun = st.slider('Tahun', min_value=2000, max_value=2020, value=2020, label_visibility="collapsed")
        c = alt.Chart(ASEANElecGen_df[ASEANElecGen_df['Year']==tahun]).mark_bar().encode(
        alt.X('Country', sort='-y'), 
        alt.Y('Electricity consumption (TWh)'),color='Country')
        st.altair_chart(c, use_container_width=True)

string2 = '''
        Sebagaimana terlihat dari grafik di atas (Gambar 1 dan Gambar 2), dari sisi pemakaian listrik per negara, dapat dilihat bahwa Indonesia adalah pengguna 
        listrik terbesar di wilayah Asia Tenggara (ASEAN) sejak tahun 2008. Grafik itu juga menunjukkan bahwa Indonesia dan Vietnam menjadi negara dengan penggunaan
        listrik yang terus meningkat secara signifikan dan konsisten sejak tahun 2008.
        '''
st.write(string2)

stringInfo3 = '''
        Di beberapa negara, tahun 2020 mencatat penurunan konsumsi listrik. Asumsi utamanya adalah pandemi COVID-19 yang memicu lockdown dan
        pembatasan aktivitas perkantoran dan komersial di berbagai negara. Untuk keperluan penulisan artikel ini, asumsi tersebut dirasa cukup.
        Namun, jika diperlukan, peneliti/penulis lain dapat melakukan pengujian kesahihan asumsi ini. 
        '''
st.info(stringInfo3)

string2_1 = '''
        Pemakaian listrik di tingkat agregat menjelaskan pertumbuhan kelistrikan di tingkat negara. Akan tiap negara memiliki wilayah dan 
        jumlah penduduk yang sangat bervariasi, sehingga kesepuluh negara ASEAN tersebut tidak dapat disamakan/disetarakan. 
        
        Karena kita tertarik melihat hubungan antara listrik dengan kesejahteraan penduduk, maka kita gunakan besaran populasi penduduk
        sebagai denominator. 
        '''
st.write(string2_1)

st.subheader('Populasi Penduduk Negara ASEAN')

col1, col2 = st.columns([1,1])
with col2:
    if modeWarna == "Indonesia":
        st.markdown('**Gambar 3.** Populasi Penduduk Negara ASEAN')
        c = alt.Chart(ASEANElecGen_df).mark_line().encode(
            x='Year', 
            y='Population', 
            color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
        st.altair_chart(c, use_container_width=True)
    else:
        st.markdown('**Gambar 3.** Populasi Penduduk Negara ASEAN')
        c = alt.Chart(ASEANElecGen_df).mark_line().encode(
            x='Year', y='Population', color='Country')
        st.altair_chart(c, use_container_width=True)

with col1:
    string3 = '''
            Pada Gambar 3 di samping, terlihat jelas disparitas jumlah penduduk masing-masing negara ASEAN. Indonesia 
            memiliki jumlah penduduk lebih dari dua setengah kali lipat penduduk Philippina dan kurang lebih tiga kali lipat penduduk Vietnam. 
            Sebagai catatan, Indonesia, Philippina dan Vietnam ada tiga negara dengan populasi terbesar di ASEAN. 
            
            Hal ini akan sangat berpengaruh pada besarnya listrik yang dinikmati oleh masing-masing penduduk di tiap negara, 
            yang mungkin akan jauh berbeda dibandingkan peringkat besarnya listrik secara agregat di tingkat negara. 
            '''
    st.write(string3)

st.subheader('Perbandingan Pemakaian Listrik Per Kapita Indonesia dengan Negara ASEAN lain')

string3_0 = '''
         Berdasarkan pertimbangan di atas, **pemakaian listrik per kapita**, *yang merupakan total konsumsi listrik suatu negara dibagi 
         dengan jumlah populasi negara tersebut*, adalah pendekatan yang dipilih untuk meneropong kesejahteraan penduduk berdasarkan 
         pemakaian listrik. 
         
         Gambar 4 di bawah ini menyajikan grafik pemakaian listrik per kapita negara-negara ASEAN.         
         '''
st.write(string3_0)

st.markdown('**Gambar 4.** Pemakaian Listrik Per kapita ASEAN 2000 - 2020')
if modeWarna == "Indonesia":
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', 
        y='Per capita electricity (kWh)', 
        color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
    st.altair_chart(c, use_container_width=True)
else:
    c = alt.Chart(ASEANElecGen_df).mark_line().encode(
        x='Year', y='Per capita electricity (kWh)', color='Country')
    st.altair_chart(c, use_container_width=True)

string3_1 = '''
         Sebelumnya, pada Gambar 1 dan Gambar 2 terlihat dominasi Indonesia, di mana kedua grafik tersebut menujukkan bahwa pemakaian 
         listrik Indonesia adalah yang terbesar di ASEAN. Pada chart di Gambar 4, Indosnesia justru berdada di urutan bawah. Nampak bahwa 
         secara individu atau per kapita, penggunaan listrik terbesar justru dikonsumsi oleh masyarakat Brunei dan Singapura.
         
         Kedua negara yang dari perspektif agregat pemakaian listrik nasional tidak begitu signifikan, ternyata dari
         sisi per kapita merupakan konsumen listrik yang masif.
         
         Untuk memudahkan membandingkan pemakaian listrik per kapita Indonesia terhadap negara ASEAN lainya, bar chart pada Gambar 5 di bawah ini 
         memberikan visualisasi yang lebih mudah dipahami dibandingkan line chart pada Gambar 4 di atas. 
         '''
st.write(string3_1)

st.markdown('**Gambar 5.** Perbandingan Pemakaian Listrik Per kapita ASEAN')
tahun1 = st.slider('Tahun', 2000, 2020, 2020, key='123',label_visibility="collapsed")
ASEAN2000_df = pd.DataFrame()
ASEAN2000_df[['Country','Per capita electricity (kWh)']] = ASEANElecGen_df[ASEANElecGen_df['Year']==tahun1].sort_values(by='Per capita electricity (kWh)',ascending=False)[['Country','Per capita electricity (kWh)']]
valueIndonesia = ASEAN2000_df[ASEAN2000_df['Country']=="Indonesia"]['Per capita electricity (kWh)'].values[0]
ASEAN2000_df_New = ASEAN2000_df
ASEAN2000_df_New['Per capita electricity (kWh)'] = ASEAN2000_df['Per capita electricity (kWh)']/valueIndonesia
ASEAN2000_df_New.rename(columns = {'Per capita electricity (kWh)':'Per capita electricity - relative value'}, inplace = True)

if modeWarna == "Indonesia":
    c = alt.Chart(ASEAN2000_df_New).mark_bar().encode(
            alt.X('Country', sort='-y'), 
            alt.Y('Per capita electricity - relative value'),
            color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
    st.altair_chart(c, use_container_width=True)
else:
    c = alt.Chart(ASEAN2000_df_New).mark_bar().encode(
        alt.X('Country', sort='-y'), 
        alt.Y('Per capita electricity - relative value'),
        color='Country')
    st.altair_chart(c, use_container_width=True)
    
stringInfo4 = '''
        Bar chart di atas merupakan perbandingan pemakaian listrik per kapita negara-negara ASEAN. Sebagai penyederhanaan, pemakaian listrik 
        per kapita Indonesia dinyatakan sebagai satu (1) dan pemakaian listrik per kapita negara lainnya merupakan faktor kali dari 
        Indonesia.
        '''
st.info(stringInfo4)

string4 = '''
         Dari tahun ke tahun, terlihat jelas bahwa Brunei dan Singapura meninggalkan Indonesia dan mayoritas negara ASEAN lain dalam 
         hal pemakaian listrik per kapita. Tiap penduduk Brunei menggunakan listrik lebih dari 9 (sembilan) kali lipat penggunaan 
         tiap penduduk Indonesia. Singapura? Sedikit lebih tinggi dari 8 (delapan) kali lipat Indonesia. 
         
         Kemudian Malaysia dan Laos menyusul dengan pemakaian listrik tiap penduduknya berkisar 5 (lima) dan 4 (empat) kali lipat pemakaian 
         tiap penduduk di Indonesia. Selanjutnya adalah Thailand dan Vietnam dengan pemakaian listrik per kapita per tahun berkisar 2 (dua) 
         kali lipat Indonesia. 
         
         Pada permulaan tahun 2000, Vietnam dan Laos memiliki pemakaian listrik per kapita per tahun yang setara dengan Indonesia.
         Tetapi di mulai tahun 2007, Vietnam meninggalkan Indonesia. Di tahun 2010, Laos meninggalkan Indonesia dan bahkan meninggalkan Vietnam. 
         
         Walaupun Indonesia bukan yang terendah, sangat nampak bahwa Indonesia jauh tertinggal dibanding tetangga-tetangga yang lebih makmur.
         '''
st.write(string4)

stringInfo4 = '''
        Bagaimana menggunakan ukuran pemakaian listrik sebagai *proxy* atau penanda kesejahteraan masyarakat? Walaupun tidak akurat 100%, gunakan 
        analogi atau ilustrasi sederhana berikut:
        
        Katakanlah penduduk Indonesia menggunakan satu buah pendingin ruangan (AC) di rumahnya. Dengan pemakaian listrik dua kali lipat, bisa diasumsikan 
        masyarakat Thailand menggunakan dua buah pendingin ruangan di rumahnya. Penduduk Malaysia, dengan pemakaian lima kali lipat, mungkin menggunakan
        tiga pendingin ruangan dan satu unit pemanas air listrik untuk kamar mandi. 
        
        Masyarakat Brunei dan Singapura? Mungkin mereka menggunakan pendingin ruangan di tiap ruangan dan 
        pemanas air di tiap kamar mandi dan ditambah beragam peralatan listrik lainnya. 
        
        Sebuah simplifikasi, namun bisa memberikan gambaran bagaimana tingkat kemakmuran masyarakat berdasarkan pemakaian listrik. 
        '''
st.info(stringInfo4)

st.subheader('Apakah ketimpangan listrik menunjukkan ketimpangan kesejahteraan?')

string5 = '''
         Data dan ilustrasi pada bagian di atas memberikan sedikit insight kepada kepada bagaiamana kesejahteraan masyarakat nampak
         dari pemakaian listrik. Namun, kita tentu harus memvalidasi klaim ini agar semua pihak dapat menerima bahwa klaim yang disampaikan
         di awal artikel ini tidak meleset.
         
         Kita perlu melirik berbagai ukuran yang sering dipakai oleh ekonom, ahli pembangunan ataupun pejabat pemerintah dalam memetakan 
         kesejahteraan. Ada banyak metrik yang dipakai, misalnya: GDP/Kapita (pendapatan domestik bruto per kapita), HDI (Human Development 
         Index), HCI (Human Capital Index), dan beragam ukuran lainnya.
         
         Salah satu ukuran yang mudah diperoleh datanya, dan mudah dipahami besarannya adalah GDP/Kapita. Untuk itu, metrik ini kita pilih pada 
         artikel ini. Mari kita bandingkan GDP/Kapita dari masing-masing negara di ASEAN.
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
    st.markdown('**Gambar 6.** GDP/Kapita ASEAN Periode 2000-2020')
    if modeWarna == "Indonesia":
        st.write('')
        st.write('')
        st.write('')
        c = alt.Chart(ASEANGDP_dfNew).mark_line().encode(
            x='Year', 
            y='GDP/Capita', 
            color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
        st.altair_chart(c, use_container_width=True)
    else:
        st.write('')
        st.write('')
        st.write('')
        c = alt.Chart(ASEANGDP_dfNew).mark_line().encode(
            x='Year', y='GDP/Capita', color='Country')
        st.altair_chart(c, use_container_width=True)

with col2:
    st.markdown('**Gambar 7.** GDP/Kapita ASEAN Pada Tahun Tertentu')
    tahun2 = st.slider('Tahun', 2000, 2020, 2020, key='234', label_visibility="collapsed")
    if modeWarna == "Indonesia":
        c = alt.Chart(ASEANGDP_dfNew[ASEANGDP_dfNew['Year']==tahun2]).mark_bar().encode(
                alt.X('Country', sort='-y'), 
                alt.Y('GDP/Capita'),
                color=alt.Color('Country',scale=alt.Scale(domain=domain, range=range_)))
        st.altair_chart(c, use_container_width=True)
    else:
        c = alt.Chart(ASEANGDP_dfNew[ASEANGDP_dfNew['Year']==tahun2]).mark_bar().encode(
                alt.X('Country', sort='-y'), 
                alt.Y('GDP/Capita'),
                color='Country')
        st.altair_chart(c, use_container_width=True)

string6 = '''
         Grafik GDP/Kapita juga menunjukkan adanya disparitas antar negara ASEAN. Singapura dan Brunei telah 
         jauh melampaui negara-negara ASEAN lainnya dalam hal kesejahteraan masyarakat. Malaysia dan Thailand 
         berada pada urutan berikutnya. Sedangkan Indoensia dan negara ASEAN lainnya masih mengekor di 
         belakang.
         
         Perbandingan kesejahteraan sebagaimana ditunjukkan oleh GDP/Kapita tidak 100% identik dengan pemakaian listrik
         per kapita. Vietnam dan Laos yang dari perspektif kelistrikan berada di atas Indonesia, ternyata dari segi 
         GDP/Kapita masih sedikit tertinggal dibanding Indonesia. Anomali lainnya adalah Brunei yang dalam sepuluh tahun 
         terakhir menunjukkan penurunan GDP/Kapita. Hal ini merupakan hal menarik untuk menjadi bahan kajian lebih jauh. 
         
         Walaupun demikian, kita bisa melihat dengan jelas pola umum adanya kesenjangan / ketimpangan kesejahteraan 
         di wilayah ASEAN ini. 
         
         Sebagai penutup artikel ini, disajikan grafik perbandingan pemakaian listrik per kapita dan
         GDP/Kapita dari masing-masing negara ASEAN selama periode 2000 - 2020. Grafik di bawah ini menujukkan bagaimana GDP/Capita 
         dan Pemakaian listrik per kapita mengalami pengembangan dan konstraksi dari tahun ke tahun. 
         
         Chart telah dinormalisasi dengan titik tertinggi GDP/Kapita 
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

