# Tourismus - Saisonen

import streamlit as st
# PAGE CONFIG
st.set_page_config(page_title="Tourismus", layout="wide")

import altair as alt
from data import *
from custom import *

from style import insert_styling

insert_styling(255, 255, 255, 1, 70, 195, 159, 1)

def getPeriode(time: str):
    if (time == 'Tourismusjahr'):
        return 'Jahr'
    elif (time=='Winterhalbjahr'):
        return 'WHJ'
    elif (time=='Sommerhalbjahr'):
        return 'SHJ'
    else:
        return 0
    
# CONSTANTS
START_JAHR: int = 2004
END_JAHR: int = 2025

color_palette = ['#003783', 
                 '#00076d',
                 '#7586ff', 
                 '#98a9ff', 
                 '#c8d9ff',  
                 '#afe1f4', 
                 '#ffc556', 
                 '#ffbf00', 
                 '#f6977a',
                 '#fa8072',
                 '#f9cb9c', 
                 '#feeece']

st.markdown(get_custom_css(), unsafe_allow_html=True)

# # # SIDE BAR # # # 
with st.sidebar:
    values = ['Ankünfte', 'Übernachtungen']
    choosenAnkuenfteUebernachtungen = st.selectbox('Ankünfte/Übernachtungen', 
                                                   values, 
                                                   index=values.index('Übernachtungen'),
                                                   label_visibility='visible')
    
    timePeriod = ["Tourismusjahr", "Winterhalbjahr", "Sommerhalbjahr"]
    time = st.selectbox("Zeitraum:", timePeriod, label_visibility='visible')

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

st.write('## Tourismus - Saisonen')

# Tourismus nach Tourismusregionen
df = get_data('t_tourismus1.csv', select_start_jahr-2, select_end_jahr, 'Tourismusregion', region)

st.write(f"### Anzahl der {choosenAnkuenfteUebernachtungen} - {region} - {time}")

monatsaisonvalues = ['Saison', 'Monat']
choosenMonatSaison = st.selectbox("Saison/Monat", 
                                  monatsaisonvalues, 
                                  index=monatsaisonvalues.index('Monat'),
                                  label_visibility='visible')


periodeDf = getPeriode(time)

if (choosenAnkuenfteUebernachtungen == 'Ankünfte'):
    diff: str = 'Veränderung Ankünfte'
elif(choosenAnkuenfteUebernachtungen == 'Übernachtungen'):
    diff: str = 'Veränderung Übernachtungen'

if (periodeDf == 'SHJ'):
    df = df[df['Tourismushalbjahr'] == periodeDf]
    year = 'Tourismusjahr'
    distance_for_calc_diff = 6
elif (periodeDf == 'WHJ' or periodeDf == 'Jahr'):
    distance_for_calc_diff = 12
    if (periodeDf == 'WHJ'):
        distance_for_calc_diff = 6
        df = df[df['Tourismushalbjahr'] == periodeDf]
    year = 'Tourismusjahr'
if (choosenMonatSaison == 'Saison'):
    distance_for_calc_diff = 1

if ((choosenMonatSaison == 'Saison') and (time != 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Tourismusjahr', 'Tourismushalbjahr', 'Tourismusregion']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Tourismusjahr', 'Tourismushalbjahr']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
elif((choosenMonatSaison == 'Saison') and (time == 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Tourismusjahr', 'Tourismusregion']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Tourismusjahr']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
elif ((choosenMonatSaison == 'Monat') and (time != 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Tourismushalbjahr', 'Tourismusregion', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Tourismushalbjahr', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
elif((choosenMonatSaison == 'Monat') and (time == 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Tourismusregion', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()

monats_order = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monats_order_n = ['Jänner', 'Feber', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

# MONATS LOGIC
if (choosenMonatSaison == 'Monat'): 
    df = calcDifference(df, distance_for_calc_diff)
    df = df[df['Jahr'] >= select_start_jahr-1]
    df =  df[~((df['Jahr'] < select_start_jahr) & (df['MonatId'] < 11))]
    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year}:O', 
                title='Jahr'),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', 
                title='Anzahl'
                ),
        color=alt.Color(
            'MonatId:N', 
            title='Monat', 
            sort=monats_order,
            scale=alt.Scale(domain=monats_order, range=color_palette),
            legend=None
        ),
        order=alt.Order('MonatId:N', sort='ascending'),
        tooltip=[
            alt.Tooltip('Jahr:O', 
                        title='Jahr'), 
            alt.Tooltip('Monat:N', 
                        title='Monat'), 
            alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                        title='Anzahl', 
                        format=','),
            alt.Tooltip(f'{diff}:O', 
                        title='Veränderung zum Vorjahr'),
            alt.Tooltip(f'Durchschnittliche Verweildauer:O', 
                        title='Durchschnittliche Verweildauer')


        ],
    ).properties(
        width=800,
        height=600
    )

# SAISON LOGIC
else: 
    df = calcDifference(df, distance_for_calc_diff)
    df = df[1:]
    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year}:O', 
                title='Jahr'),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', 
                title='Anzahl', 
                sort=monats_order
                ),
        tooltip=[
            alt.Tooltip('Tourismusjahr:O', 
                        title='Tourismusjahr'), 
            alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                        title='Anzahl', 
                        format=','),
            alt.Tooltip(f'{diff}:O', 
                        title='Veränderung zum Vorjahr'),
            alt.Tooltip(f'Durchschnittliche Verweildauer:O', 
                        title='Durchschnittliche Verweildauer')

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