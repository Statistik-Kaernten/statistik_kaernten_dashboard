import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="Betriebe / Betten", layout="wide")

import altair as alt
from data import *
from custom import *

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
START_JAHR: int = 2008
END_JAHR: int = 2024

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

    selected_unterkunftsart = st.multiselect('Unterkunftsart auswählen:', getList(None, 'Unterkunftsarten'), label_visibility='visible')
    
    selected_jahre: int = st.slider("Startjahr",
        min_value=START_JAHR,
        max_value=END_JAHR-1,
        value=(2014, END_JAHR),
        step=1)
    
    select_start_jahr: int = selected_jahre[0]
    select_end_jahr: int = selected_jahre[1]
    
    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png", use_container_width=True)

    with st.expander("Info"):
        st.write('''
            Infobox
        ''')

# # # END SIDE BAR # # #


st.write(f'## {choosenArt}')

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

if selected_unterkunftsart is not None and len(selected_unterkunftsart) != 0:
    df = df[df['Unterkunft'].isin(selected_unterkunftsart)]

df = df.sort_values(['Jahr', 'Unterkunft'])
df['Veränderung Vorjahr'] =  round(df['Anzahl'].pct_change(len(df[df['Jahr'] == END_JAHR])).fillna(0) * 100, 2)
df['Veränderung Vorjahr'] = df['Veränderung Vorjahr'].apply(
                                lambda x: f"+{x:.2f}%" if x >= 0 else f"{x:.2f}%" if x < 0 else "N/A")

color_map = get_color_map_all_unterkunftsarten()

stacked_bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X(f'Jahr:O', 
            axis=alt.Axis(labelAngle=45),
            title='Jahr'),
    y=alt.Y(f'Anzahl:Q', 
            title='Anzahl'
            ),
    color=alt.Color(
        'Unterkunft:N', 
        scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values())),
        #scale=alt.Scale(range=get_cud_palette()),
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
        #alt.Tooltip('Veränderung Vorjahr:N', 
        #            title='Veränderung Vorjahr'),
        alt.Tooltip('Art:N', 
                    title='Art'),
        alt.Tooltip(f'Anzahl:Q', 
                    title='Anzahl')
        ],
    ).configure_axis(
    labelFontSize=14,
    titleFontSize=16,
    titleFontWeight='bold'
    ).properties(
        width=800,
        height=600
    )

# DISPLAY CHART
if (df['Anzahl'].sum() == 0):
    st.write('Nichts zu visualisieren.')
else:
    st.altair_chart(stacked_bar_chart, use_container_width=True)

if 'Jahr' in df.columns: 
    df['Jahr'] = df['Jahr'].astype(str)

# DATA AS CSV PREP
st.write(f"## {region}")

col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.write(f"### Gefilterte Daten")
    df.drop('Veränderung Vorjahr', axis=1, inplace=True)
    st.dataframe(df, use_container_width=True, hide_index=True)#, column_order=('Jahr', 'Tourismusjahr', 'MonatId', 'Monat', 'Ankünfte', 'Übernachtungen', 'Veränderung Ankünfte', 'Veränderung Übernachtungen'))
with col2:
    st.write(f"### Gemeinden")
    gemeinden = getGemeindeListe(region)
    if(len(gemeinden) != 0):
        st.dataframe(gemeinden, hide_index=True, use_container_width=True)
    else:
        st.write(f"#### {region}")

#st.markdown("""
#    <a href="https://github.com/Statistik-Kaernten/statistik_kaernten_dashboard/blob/main/data/t_tourismus2.csv" download target="_blank">
#        <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
#            Download alle Daten
#        </button>
#    </a>
#    """, unsafe_allow_html=True)