# Tourismus - Saisonen
import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="Tourismus", layout="wide")

import altair as alt
from data import *
from custom import *

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

#color_palette = get_monthly_color_palette()

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
        value=(END_JAHR-10, END_JAHR),
        step=1)

    st.session_state.start_year = selected_jahre[0]
    st.session_state.end_year = selected_jahre[1]
    select_start_jahr: int = st.session_state.start_year
    select_end_jahr: int = st.session_state.end_year

    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png", use_container_width=True)

    with st.expander("Info"):
        st.write('''
            Infobox
        ''')

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


# MONATS LOGIC
#selection = alt.selection_point(fields=['Tourismusregion'], bind='legend')
selection = alt.selection_point(fields=['Tourismusregion'])

if (choosenMonatSaison == 'Monat'): 
    df = calcDifference(df, distance_for_calc_diff)
    df = df[df['Jahr'] >= select_start_jahr-1]
    df = df[~((df['Jahr'] < select_start_jahr) & (df['MonatId'] < 11))]
    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year}:O',
                axis=alt.Axis(labelAngle=45, 
                              labelExpr="substring(datum.value, 2)"), 
                title='Jahr'),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', 
                title='Anzahl'
                ),
        color=alt.Color(
            'MonatId:N', 
            title='Monat', 
            sort=monats_order,
            scale=alt.Scale(domain=monats_order, range=get_monthly_color_palette()),
            legend=None
        ),
        order=alt.Order('Jahr:N', sort='ascending'),
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
    ).configure_axis(
    labelFontSize=14,
    titleFontSize=16,
    titleFontWeight='bold'
    ).properties(
        width=800,
        height=600,
        usermeta={
                    "embedOptions": custom_locale
                }
    )

# SAISON LOGIC

else: 
    df = calcDifference(df, distance_for_calc_diff)
    df['filter'] = df['Tourismusjahr'].str[:4].astype(int)
    df = df[~(df['filter'] < select_start_jahr-1)]
    df.drop('filter', inplace=True, axis=1)
    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year}:O',
                axis=alt.Axis(labelAngle=45, 
                              labelExpr="substring(datum.value, 2)"), 
                title='Jahr'),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', 
                title='Anzahl'
                ),
        color=alt.Color(
            'Tourismusregion:N', 
            title='Tourismusregion', 
            scale=alt.Scale(range=get_monthly_color_palette()),
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
    ).configure_axis(
    labelFontSize=14,
    titleFontSize=16,
    titleFontWeight='bold'
    ).properties(
        width=800,
        height=600
    )

# DISPLAY CHART
st.altair_chart(stacked_bar_chart, use_container_width=True)

# DATA AS CSV PREP
if 'Jahr' in df.columns: 
    df['Jahr'] = df['Jahr'].astype(str)

st.write(f"## {region}")
col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.write(f"### Gefilterte Daten")
    st.dataframe(df, use_container_width=True, hide_index=True, column_order=('Jahr', 'Tourismusjahr', 'MonatId', 'Monat', 'Ankünfte', 'Übernachtungen', 'Veränderung Ankünfte', 'Veränderung Übernachtungen'))
with col2:
    st.write(f"### Gemeinden")
    gemeinden = getGemeindeListe(region)
    if(len(gemeinden) != 0):
        st.dataframe(gemeinden, hide_index=True, use_container_width=True)
    else:
        st.write(f"#### {region}")

#st.markdown("""
#    <a href="https://github.com/Statistik-Kaernten/statistik_kaernten_dashboard/blob/main/data/t_tourismus1.csv" download target="_blank">
#        <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
#            Download alle Daten
#        </button>
#    </a>
#    """, unsafe_allow_html=True)