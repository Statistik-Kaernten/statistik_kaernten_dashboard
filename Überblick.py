# Dashboard der Landesstelle für Statistik
# Amt der Kärntner Landesregierung
# created by Martin Writz, BSc.

# please report bugs to martin.writz@ktn.gv.at or
# abt1.statistik@ktn.gv.at 
# feel free to contribute or
# to commit a pull request directly

# Dashboard-Overview page 
from data import *
from custom import *
from PIL import Image, ImageOps

## PAGE CONFIG
st.set_page_config(page_title="Dashboard der Landesstelle für Statistik", layout="wide", initial_sidebar_state='expanded')


## CUSTOM CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

insert_styling(226, 226, 226, 1, 255, 255, 255, 1)

with st.sidebar:
    cover_img = ImageOps.expand(Image.open("img/cover_hb25.png"), border=4, fill='white')
    cover_img = cover_img.resize((289, 429))
    st.image(cover_img)
               
    st.markdown("""
    <a href="https://www.ktn.gv.at/DE/repos/files/ktn.gv.at/Abteilungen/Abt1/Dateien/PDF/Statistik/Publikationen%5fStat/Statistisches%5fHandbuch/Handbuch2025%5f2.pdf" target="_blank">
        <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
            Download
        </button>
    </a>
    """, unsafe_allow_html=True)


    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.image("img/logo.png", width='stretch')

    with st.expander("Info"):
        st.write('''
            Dashboard der Landesstelle für Statistik, Amt der Kärntner Landesregierung, aktualisiert am 20.01.2026, erstellt von Martin Writz, BSc.
            
            please report bugs to martin.writz@ktn.gv.at or statistik@ktn.gv.at, feel free to contribute or commit a pull request directly
        ''')

st.markdown(f"""<h1>Dashboard der Landesstelle für Statistik</h1>""", unsafe_allow_html=True)
st.markdown(f"""<h2>Die interaktive Version des statistischen Handbuchs des Landes Kärnten</h2>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    tourismus_box()
