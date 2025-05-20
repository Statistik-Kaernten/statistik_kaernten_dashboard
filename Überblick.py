# Dashboard der Landesstelle für Statistik
# Amt der Kärntner Landesregierung
# created by Martin Writz, BSc.

# please report bugs to martin.writz@ktn.gv.at or
# abt1.statistik@ktn.gv.at 
# feel free to contribute or
# to commit a pull request directly

# Dashboard-Overview page 
import streamlit as st
from data import *

## PAGE CONFIG
st.set_page_config(page_title="Dashboard der Landesstelle für Statistik", layout="wide")

from custom import *
from PIL import Image, ImageOps

## CUSTOM CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

insert_styling(250, 191, 116, 1, 255, 255, 255, 1)

with st.sidebar:
    cover_img = ImageOps.expand(Image.open("img/cover_hb.PNG"), border=4, fill='white')
    cover_img = cover_img.resize((289, 429))
    st.image(cover_img)
               
    st.markdown("""
    <a href="https://www.ktn.gv.at/DE/repos/files/ktn.gv.at/Abteilungen/Abt1/Dateien/PDF/Statistik/Publikationen%5fStat/Statistisches%5fHandbuch/2024%5f12%5f19%5fHandbuch%5fv2%5fverlinkt%5fcomp.pdf?exp=1584214&fps=6bd0ae5d72df8a699ee88fe30fff59bc9ec9d39e" target="_blank">
        <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
            Download
        </button>
    </a>
    """, unsafe_allow_html=True)


    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.image("img/logo.png", width=300, use_container_width=False)

    with st.expander("Info"):
        st.write('''
            Dashboard der Landesstelle für Statistik, Amt der Kärntner Landesregierung, BETA-Version 2.0 vom 20.05.2025, erstellt von Martin Writz, BSc.
            
            please report bugs to martin.writz@ktn.gv.at or abt1.statistik@ktn.gv.at, feel free to contribute or commit a pull request directly
        ''')

st.markdown(f"""<h1>Dashboard der Landesstelle für Statistik</h1>""", unsafe_allow_html=True)
st.markdown(f"""<h2>Die interaktive Version des statistischen Handbuchs des Landes Kärnten</h2>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    tourismus_box()
