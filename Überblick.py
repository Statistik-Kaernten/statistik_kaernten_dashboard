# Dashboard der Landesstelle für Statistik
# Amt der Kärntner Landesregierung
# BETA-Version 0.2.0 vom 08.01.2025
# erstellt von Martin Writz, BSc.

# please report bugs to martin.writz@ktn.gv.at or
# abt1.statistik@ktn.gv.at 
# feel free to contribute or
# to commit a pull request directly

# ÜBERBLICK SEITE des Dashboards
import streamlit as st

## PAGE CONFIG
st.set_page_config(page_title="Dashboard der Landesstelle für Statistik", layout="wide")

from custom import *
from style import insert_styling
from PIL import Image, ImageOps


def colored_box(label, bgcolor, text, textcolor, bordercolor):
    # Define the CSS styles for the box
    box_style = f"""
        background-color: {bgcolor}; 
        padding: 20px; 
        border-radius: 5px; 
        border: 2px solid {bordercolor};  /* White border with a thickness of 2px */
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);  /* Optional: Adds a subtle shadow for better visibility */
        text-align: center;  /* Center-aligns the text within the box */
    """
    
    # Render the box with Streamlit
    st.markdown(f"""
        <div style="{box_style}">
            <h2 style="color: {textcolor}; margin: 0;">{label}</h2>
            <p style="margin: 0; color: {textcolor}"><font size="5">{text}</font></p>
        </div>
        """, unsafe_allow_html=True)

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
            Dashboard der Landesstelle für Statistik, Amt der Kärntner Landesregierung, BETA-Version 0.3 vom 07.02.2025, erstellt von Martin Writz, BSc.
            
            please report bugs to martin.writz@ktn.gv.at or abt1.statistik@ktn.gv.at, feel free to contribute or to commit a pull request directly
        ''')

st.markdown(f"""<h1>Dashboard der Landesstelle für Statistik</h1>""", unsafe_allow_html=True)
st.markdown(f"""<h2>Die interaktive Version des statistischen Handbuchs des Landes Kärnten</h2>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    colored_box("TOURISMUS", "#46C39F", r"Gegenüber dem Dezember des Jahres 2023 errechnet sich bei den Ankünften eine Steigerung von 5,1 % und bei den Übernachtungen ein Plus von 9,1 %. Die durchschnittliche Aufenthaltsdauer belief sich auf 3,5 Nächtigungen.", "black", "white")
