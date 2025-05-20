# Tourismus - Saisonen
#import streamlit as st
from data import getMonths
from custom import *

# PAGE CONFIG
st.set_page_config(page_title="Tourismus Regionen", layout="wide")

import altair as alt
from data import *
from custom import *
#from style import insert_styling

insert_styling(255, 255, 255, 1, 70, 195, 159, 1)

color_map = get_color_map_regionen()

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

st.markdown(get_custom_css(), unsafe_allow_html=True)

# # # SIDE BAR # # # 
with st.sidebar:
    values = ['Ankünfte', 'Übernachtungen']
    choosenAnkuenfteUebernachtungen = st.selectbox('Ankünfte/Übernachtungen', 
                                                   values, 
                                                   index=values.index('Übernachtungen'),
                                                   label_visibility='visible')
    
    #timePeriod = ["Tourismusjahr", "Winterhalbjahr", "Sommerhalbjahr"]
    #time = st.selectbox("Zeitraum:", timePeriod, label_visibility='visible')

    #options2 = getSubRegion('Tourismusregion')
    #options2.append('Ganz Kärnten')
    #options2.append('Alle Tourismusregionen')
    
    #region = st.selectbox("Tourismusregion", 
    #                        options2, 
    #                        index=options2.index('Ganz Kärnten'),
    #                        label_visibility='visible')
    selected_jahre: int = st.slider("Startjahr",
        min_value=START_JAHR,
        max_value=END_JAHR-1,
        value=(END_JAHR-10, END_JAHR),
        step=1)

    st.session_state.start_year = selected_jahre[0]
    st.session_state.end_year = selected_jahre[1]
    select_start_jahr: int = st.session_state.start_year
    select_end_jahr: int = st.session_state.end_year

    selected_monate = []
    selected_saison = False
    selected_anteil_anzahl = 'Anzahl'
    
    linieBalken = ['Liniendiagramm', 'Balkendiagramm'] 
    selected_diagram = st.selectbox('Diagrammtyp:', linieBalken, label_visibility='visible', index=linieBalken.index('Balkendiagramm'))
    if selected_diagram != 'Liniendiagramm':
        selected_anteil_anzahl = st.radio('Anteil/Anzahl auswählen:', ['Anzahl', 'Anteil'], index=0,label_visibility='visible')
        selected_monate = st.multiselect('Monate auswählen:', getMonths()['Name'], label_visibility='visible')
        selected_saison = st.radio('zeitliche Gruppierung auswählen:', ['Monate anzeigen', 'Tourismussaison erzeugen', 'Jahr erzeugen'], label_visibility='visible')
    selected_regionen = st.multiselect('Tourismusregionen auswählen:', getSubRegion('Tourismusregion'), label_visibility='visible')

    
    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png", use_container_width=True)

    with st.expander("Info"):
        st.write('''
            Infobox
        ''')

# # # END SIDE BAR # # #

st.write('## Tourismus - Regionen')

    

# Tourismus nach Tourismusregione
df2 = get_data('t_tourismus1.csv', select_start_jahr-2, select_end_jahr, 'Tourismusregion', selectRegioLst=selected_regionen, selectMonatLst=selected_monate)
df = get_data('t_tourismus1.csv', select_start_jahr-2, select_end_jahr, 'Tourismusregion', selectRegioLst=selected_regionen)
df = filterJahr(df, st.session_state.start_year, st.session_state.end_year)
df2 = filterJahr(df2, st.session_state.start_year, st.session_state.end_year)

if selected_saison == 'Tourismussaison erzeugen':
    df2 = df2.groupby(['Tourismusjahr', 'Tourismusregion']).agg({'Jahr': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    total = df2.groupby('Tourismusjahr')[f'{choosenAnkuenfteUebernachtungen}'].transform('sum')
    x_axis_show = 'Tourismusjahr'
elif selected_saison == 'Jahr erzeugen':
    df2 = df2.groupby(['Jahr', 'Tourismusregion']).agg({'Tourismusjahr': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    total = df2.groupby('Jahr')[f'{choosenAnkuenfteUebernachtungen}'].transform('sum')
    x_axis_show = 'Jahr'
else: # Monate:
    df2['Date'] = pd.to_datetime(df2[['Jahr', 'Monat']].rename(columns={'Jahr': 'year', 'Monat': 'month'}).assign(day=1))
    total = df2.groupby('Date')[f'{choosenAnkuenfteUebernachtungen}'].transform('sum')
    df2['Date'] = df2['Date'].apply(lambda x: x.strftime('%Y-%m'))
    x_axis_show = 'Date'
df2['Anzahl'] = df2[f'{choosenAnkuenfteUebernachtungen}']
df2['Anteil'] = round((df2[f'{choosenAnkuenfteUebernachtungen}'] / total) * 100, 1)

if df is not None:
    df['Date'] = pd.to_datetime(df[['Jahr', 'Monat']].rename(columns={'Jahr': 'year', 'Monat': 'month'}).assign(day=1))

selection = alt.selection_point(fields=['Tourismusregion'], bind='legend')

chart = alt.Chart(df).mark_line().mark_line(size=2).encode(
        x=alt.X('Date:T', title='Datum', axis=alt.Axis(labelAngle=45)),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', title='Anzahl'), 
        color=alt.Color(f'Tourismusregion:N', 
                        title='Tourismusregion', 
                        legend=alt.Legend(orient='bottom', 
                                          columns=4,
                                          titleFontWeight='bold'
                                          ), 
                        scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values()))),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    ).add_params(
    selection).properties(
    width=800,
    height=600
)

hover_points = alt.Chart(df).mark_circle(size=100, opacity=0).encode(
    x='Date:T',
    y=f'{choosenAnkuenfteUebernachtungen}:Q',
    tooltip=[alt.Tooltip('Date:T',
                              title='Datum'), 
                 alt.Tooltip(f'Tourismusregion:N', 
                             title='Tourismusregion'),
                 alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                             title='Anzahl', 
                             format=',')] 
)

line_chart = (chart + hover_points).configure_axis(
    labelFontSize=14,
    titleFontSize=16,
    titleFontWeight='bold'
    )

selection2 = alt.selection_point(fields=['Tourismusregion'], bind='legend')

stacked_bar_chart = alt.Chart(df2).mark_bar().encode(
    x=alt.X(f'{x_axis_show}:N', 
            title='Datum', 
            axis=alt.Axis(labelExpr="datum.value", 
                labelAngle=45)),
    y=alt.Y(f'{selected_anteil_anzahl}:Q', title=f'{selected_anteil_anzahl}'),
    color=alt.Color(
        'Tourismusregion:N', 
        title='Tourismusregion', 
        legend=alt.Legend(orient='bottom', 
                            columns=4,
                            titleFontWeight='bold'
                            ), 
        scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values()))
    ),
    opacity=alt.condition(selection2, alt.value(1), alt.value(0.1)),
    order=alt.Order(f'{choosenAnkuenfteUebernachtungen}:Q', sort='ascending'),
    tooltip=[
        alt.Tooltip(f'{x_axis_show}:N', 
                    title='Datum'), 
        alt.Tooltip('Tourismusregion:N', 
                    title='Tourismusregion'), 
        alt.Tooltip(f'{selected_anteil_anzahl}:Q', 
                    title=f'{selected_anteil_anzahl}', 
                    format=','),
        #alt.Tooltip(f'{diff_type}:N',
        #            title=f'{diff_type}'),
        #alt.Tooltip('Durchschnittliche Verweildauer:N',
        #            title='Durchschnittliche Verweildauer')
    ],
).configure_axis(
    labelFontSize=14,
    titleFontSize=16,
    titleFontWeight='bold'
    ).add_params(
    selection2).properties(
    width=800,
    height=600
)


if selected_diagram == 'Liniendiagramm':
    st.altair_chart(line_chart, use_container_width=True)
elif selected_diagram == 'Balkendiagramm':
    st.altair_chart(stacked_bar_chart, use_container_width=True)
else:
    st.write("Bitte Auswahl treffen")

#st.write(df)
st.write(df2)