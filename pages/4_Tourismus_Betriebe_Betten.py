import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="Betriebe / Betten", layout="wide")

import altair as alt
from data import *
from custom import *
from style import insert_styling


insert_styling(255, 255, 255, 1, 70, 195, 159, 1)


def getPeriode(time: str):
    if (time == 'Tourismusjahr'):
        return 'Tourismusjahr'
    elif (time=='Winterhalbjahr'):
        return 'Winter'
    elif (time=='Sommerhalbjahr'):
        return 'Sommer'
    else:
        return 0
    
# CONSTANTS
START_JAHR: int = 1998
END_JAHR: int = 2023


color_palette = get_ktn_palette()

st.markdown(get_custom_css(), unsafe_allow_html=True)

# # # SIDE BAR # # # 
with st.sidebar:
    
    timePeriod = ["Tourismusjahr", "Winterhalbjahr", "Sommerhalbjahr"]
    time = st.selectbox("Zeitraum:", timePeriod, label_visibility='visible')

    values = ['Betriebe', 'Zimmer', 'Betten', 'Zusatzbetten']
    choosenArt = st.selectbox('Art', 
                              values, 
                              index=values.index('Betriebe'),
                              label_visibility='visible')
    
    options2 = getSubRegion('Tourismusregion')
    options2.append('Ganz Kärnten')
    
    region = st.selectbox("Tourismusregion", 
                            options2, 
                            index=options2.index('Ganz Kärnten'),
                            label_visibility='visible')

    
    selected_jahre: int = st.slider("Startjahr",
        min_value=START_JAHR,
        max_value=END_JAHR-1,
        value=(2014, END_JAHR),
        step=1)
    
    select_start_jahr: int = selected_jahre[0]
    select_end_jahr: int = selected_jahre[1]
    
    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png", use_container_width=True)

# # # END SIDE BAR # # #


st.write('## Betriebe / Betten')

# Tourismus nach Tourismusregionen
df = get_data('t_tourismus4.csv', select_start_jahr, select_end_jahr, 'Tourismusregion', region)

periodeDf = getPeriode(time)
if (periodeDf == 'Sommer'):
    df = df[df['Tourismushalbjahr'] == periodeDf]
elif (periodeDf == 'Winter'):
    df = df[df['Tourismushalbjahr'] == periodeDf]
elif (periodeDf == 'Tourismusjahr'):
    df = df[df['Tourismushalbjahr'] == periodeDf]

df = df[df['Art'] == choosenArt]

stacked_bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X(f'Jahr:O', 
            title='Jahr'),
    y=alt.Y(f'Anzahl:Q', 
            title='Anzahl'
            ),
    color=alt.Color(
        'Unterkunft:N', 
        scale=alt.Scale(range=color_palette),
        legend=None
    ),
    order=alt.Order('MonatId:N', sort='ascending'),
    tooltip=[
        alt.Tooltip('Jahr:O', 
                    title='Jahr'), 
        alt.Tooltip('Tourismushalbjahr:N', 
                    title='Tourismushalbjahr'), 
        alt.Tooltip('Tourismusregion:N', 
                    title='Tourismusregion'),
        alt.Tooltip('Unterkunft:N', 
                    title='Unterkunft'),
        alt.Tooltip('Art:N', 
                    title='Art'),
        alt.Tooltip(f'Anzahl:Q', 
                    title='Anzahl')

        ],
    ).properties(
        width=800,
        height=600
    )

# DISPLAY CHART
st.altair_chart(stacked_bar_chart, use_container_width=True)

# DATA AS CSV PREP
st.write(f"### Daten - {region}")
if 'Jahr' in df.columns: 
    df['Jahr'] = df['Jahr'].astype(str)
st.dataframe(df)