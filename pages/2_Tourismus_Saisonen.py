# Tourismus - Saisonen
import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="Tourismus", layout="wide")

import altair as alt
from data import *
from custom import *
from style import insert_styling

insert_styling(255, 255, 255, 1, 70, 195, 159, 1)

# # # SESSION STATES # # #
if 'start_year' not in st.session_state:
    st.session_state.start_year=2015
if 'end_year' not in st.session_state:
    st.session_state.end_year=2025

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
    options2.append('Alle Tourismusregionen')
    
    region = st.selectbox("Tourismusregion", 
                            options2, 
                            index=options2.index('Ganz Kärnten'),
                            label_visibility='visible')
    selected_jahre: int = st.slider("Startjahr",
        min_value=START_JAHR,
        max_value=END_JAHR-1,
        value=(END_JAHR-10, END_JAHR),
        step=1)

    st.session_state.start_year = selected_jahre[0]
    st.session_state.end_year = selected_jahre[1]
    select_start_jahr: int = st.session_state.start_year
    select_end_jahr: int = st.session_state.end_year

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

# YEAR AND DIFF LOGIC
if (periodeDf == 'SHJ'):
    df = df[df['Tourismushalbjahr'] == periodeDf]
    year = 'Tourismusjahr'
    if (region == 'Alle Tourismusregionen'):
        distance_for_calc_diff = 6*9
    else:
        distance_for_calc_diff = 6

elif (periodeDf == 'WHJ' or periodeDf == 'Jahr'):
    if (region == 'Alle Tourismusregionen'):
        distance_for_calc_diff = 12*9
    else: 
        distance_for_calc_diff = 12
    if (periodeDf == 'WHJ'):
        if (region == 'Alle Tourismusregionen'):
            distance_for_calc_diff = 6*9
        else:
            distance_for_calc_diff = 6
        df = df[df['Tourismushalbjahr'] == periodeDf]
    year = 'Tourismusjahr'

if (choosenMonatSaison == 'Saison'):
    if (region == 'Alle Tourismusregionen'):
        distance_for_calc_diff = 9
    else:
        distance_for_calc_diff = 1

elif (choosenMonatSaison == 'Saison'):
    if(region == 'Ganz Kärnten'):
        distance_for_calc_diff = 1
    elif (len(df['Tourismusregion'].unique() != 1)):
        distance_for_calc_diff = 9
    else:
        distance_for_calc_diff = 1

year = 'Tourismusjahr'
# DATAFRAME LOGIC
if ((choosenMonatSaison == 'Saison') and (time != 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Tourismusjahr', 'Tourismushalbjahr', 'Tourismusregion']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Tourismusjahr', 'Tourismushalbjahr']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
        df['Tourismusregion'] = 'Ganz Kärnten'

elif((choosenMonatSaison == 'Saison') and (time == 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Tourismusjahr', 'Tourismusregion']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Tourismusjahr']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
        df['Tourismusregion'] = 'Ganz Kärnten'

elif ((choosenMonatSaison == 'Monat') and (time != 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Tourismushalbjahr', 'Tourismusregion', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Tourismushalbjahr', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
        df['Tourismusregion'] = 'Ganz Kärnten'
        

elif((choosenMonatSaison == 'Monat') and (time == 'Tourismusjahr')):
    if(region != 'Ganz Kärnten'):
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Tourismusregion', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    else:
        df = df.groupby(['Jahr', 'MonatId', 'Tourismusjahr', 'Monat']).agg({'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
        df['Tourismusregion'] = 'Ganz Kärnten'

monats_order = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monats_order_n = ['Jänner', 'Feber', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
t_region_palette = ['#3a5487', '#5c8c9c', '#c0c4c9', '#eb7e24', '#ca1e32', '#C8602A', '#8C4C22', '#A95C6D', '#F2C278']
#t_region_palette = ['#D66E30', '#A75E24', '#C55D44', '#F1A54C', '#F49D2D', '#9B5D2B', '#E0A56A', '#9A5736', '#D77A3C']
#t_region_palette = ['#8C4C22', '#B45F30', '#F19C42', '#F5A623', '#DA5C21', '#B94E0E', '#FF6F26', '#D45C21', '#C8602A']
#t_region_palette = ['#FF5733', '#FF8D1A', '#FFB84D', '#FF6F61', '#FF7E2D', '#FF9B3D', '#F28D24', '#F47A3C', '#F15C3C']
#t_region_palette = ['#D4A29C', '#A95C6D', '#C08497', '#F1D0B1', '#F2C8B3', '#8C4D4D', '#D88F88', '#9C4D40', '#D8B4A0']
#t_region_palette = ['#C0392B', '#F39C12', '#E74C3C', '#F1C40F', '#D35400', '#E67E22', '#C67C47', '#F39C12', '#F47C4D']
#t_region_palette = ['#FF8C42', '#FF5E13', '#FF6A13', '#F8C21C', '#F49D4B', '#FFB74D', '#D3551F', '#E07A35', '#F58F41']
#t_region_palette = ['#F4C542', '#F1A54C', '#F1B748', '#F2C65C', '#F29F28', '#F4A625', '#F1B14B', '#F5C759', '#F49E21']
#t_region_palette = ['#D36B1F', '#F29257', '#E86A42', '#D2491E', '#D78E55', '#F3A642', '#D55D1E', '#FF7D2A', '#F15A3A']
#t_region_palette = ['#9E2A2F', '#B84B2B', '#DC5422', '#E94B3C', '#F1C40F', '#F39C12', '#FF6B2D', '#D35400', '#F2C278']
#t_region_palette = ['#3288bd', '#f46d43', '#66c2a5', '#fee08b', '#e6f598', '#abdda4', '#f46d43', '#ffffbf', '#d53e4f']
#t_region_palette = ['#30b0e0', '#d2d2cb', '#4d695d', '#83a79d', '#dae8e5', '#a1cde5', '#bfdeee', '#bc252d', '#abdda4']


# MONATS LOGIC
if (choosenMonatSaison == 'Monat'): 
    df = calcDifference(df, distance_for_calc_diff)
    df = df[df['Jahr'] >= select_start_jahr-1]
    df = df[~((df['Jahr'] < select_start_jahr) & (df['MonatId'] < 11))]
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
            alt.Tooltip('Tourismusregion:N', 
                        title='Tourismusregion'),
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
    df['filter'] = df['Tourismusjahr'].str[:4].astype(int)
    df = df[~(df['filter'] < select_start_jahr-1)]
    df.drop('filter', inplace=True, axis=1)
    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year}:O', 
                title='Jahr'),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', 
                title='Anzahl'
                ),
        color=alt.Color(
            'Tourismusregion:N', 
            title='Tourismusregion', 
            scale=alt.Scale(range=t_region_palette),
            legend=None
        ),
        tooltip=[
            alt.Tooltip('Tourismusjahr:O', 
                        title='Tourismusjahr'), 
            alt.Tooltip('Tourismusregion:N', 
                        title='Tourismusregion'),
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