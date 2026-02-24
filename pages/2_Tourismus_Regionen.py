# Tourismus - Saisonen
import streamlit as st

# PAGE CONFIG
#st.set_page_config(page_title="Tourismus Regionen", layout="wide")

import altair as alt
from data import *
from custom import *

insert_styling(255, 255, 255, 1, 70, 195, 159, 1, slider_bg_color='#b7d7ce', text_color='black')

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
END_JAHR: int = 2026

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
    selected_jahre: int = st.slider("Jahre",
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
    selected_regionen = []
    selected_vorjahr_vormonat = 'Vorjahr'
    selected_order = 'Alphabetisch'

    linieBalken = ['Liniendiagramm', 'Balkendiagramm'] 
    selected_diagram = st.selectbox('Diagrammtyp:', linieBalken, label_visibility='visible', index=linieBalken.index('Balkendiagramm'))
    advanced_options = st.checkbox('Erweiterte Funktionen', False)
    if advanced_options:
        if selected_diagram != 'Liniendiagramm':
            sorting = ['Alphabetisch', 'Wert']
            selected_order = st.selectbox('Sortierung:', sorting, label_visibility='visible', index=sorting.index('Alphabetisch'))
            selected_saison = st.radio('zeitliche Gruppierung auswählen:', ['Monate anzeigen', 'Tourismussaison erzeugen', 'Jahr erzeugen'], label_visibility='visible')
            vorjahrmonat = ['Vorjahr', 'Vormonat']
            if selected_saison == 'Monate anzeigen':
                selected_vorjahr_vormonat = st.selectbox('Vergleich Vorjahr/Vormonat', vorjahrmonat, label_visibility='visible', index=vorjahrmonat.index('Vorjahr'))
            else:
                #selected_vorjahr_vormonat = st.selectbox('Vergleich Vorjahr/Vormonat', vorjahrmonat, label_visibility='visible', index=vorjahrmonat.index('Vorjahr'), disabled=True)
                selected_vorjahr_vormonat = 'Vormonat'
            selected_anteil_anzahl = st.radio('Anteil/Anzahl auswählen:', ['Anzahl', 'Anteil'], index=0,label_visibility='visible')
           
            selected_monate = st.multiselect('Monate auswählen:', getMonths()['Name'], label_visibility='visible')
        selected_regionen = st.multiselect('Tourismusregionen auswählen:', getSubRegion('Tourismusregion'), label_visibility='visible')

    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png")

    #with st.expander("Info"):
    #    st.write('''
    #        Infobox
    #    ''')

    if selected_anteil_anzahl == 'Anteil':
        diff_type = 'Veränderung Anteil'
    elif (choosenAnkuenfteUebernachtungen == 'Ankünfte'):
        diff_type = 'Veränderung Ankünfte'
    elif (choosenAnkuenfteUebernachtungen == 'Übernachtungen'):
        diff_type = 'Veränderung Übernachtungen'

    if selected_order=='Alphabetisch':
        df_sort = 'Tourismusregion:N'
    else:
        df_sort = f'{choosenAnkuenfteUebernachtungen}:Q'

# # # END SIDE BAR # # #

st.write('## Tourismus - Regionen')

# Tourismus nach Tourismusregionen
df = get_data('t_tourismus1.csv', START_JAHR, END_JAHR, 'Tourismusregion', selectRegioLst=selected_regionen)
df2 = get_data('t_tourismus1.csv', START_JAHR-1, END_JAHR, 'Tourismusregion', selectRegioLst=selected_regionen, selectMonatLst=selected_monate)
df = filterJahr(df, st.session_state.start_year, st.session_state.end_year)
df2 = filterJahr(df2, st.session_state.start_year-1, st.session_state.end_year)

if selected_saison == 'Tourismussaison erzeugen':
    if st.session_state.start_year == 2004:
        df2 = df2[((df2['Jahr'] == df2['Jahr'].min()) & (df2['Monat'].astype(int).isin([11, 12]))) | (df2['Jahr'] != df2['Jahr'].min()-1)]
    else:
        df2 = df2[((df2['Jahr'] == df2['Jahr'].min()) & (df2['Monat'].astype(int).isin([11, 12]))) | (df2['Jahr'] != df2['Jahr'].min())]
    df2 = df2.groupby(['Tourismusjahr', 'Tourismusregion']).agg({'Jahr': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    total = df2.groupby('Tourismusjahr')[f'{choosenAnkuenfteUebernachtungen}'].transform('sum')
    x_axis_show = 'Tourismusjahr'
elif selected_saison == 'Jahr erzeugen':
    #df2 = filterJahr(df2, st.session_state.start_year, st.session_state.end_year)
    df2 = df2.groupby(['Jahr', 'Tourismusregion']).agg({'Tourismusjahr': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    total = df2.groupby('Jahr')[f'{choosenAnkuenfteUebernachtungen}'].transform('sum')
    x_axis_show = 'Jahr'
else: # Monate:
    #df2 = filterJahr(df2, st.session_state.start_year, st.session_state.end_year)
    df2['Date'] = pd.to_datetime(df2[['Jahr', 'Monat']].rename(columns={'Jahr': 'year', 'Monat': 'month'}).assign(day=1))
    total = df2.groupby('Date')[f'{choosenAnkuenfteUebernachtungen}'].transform('sum')
    df2['Date'] = df2['Date'].apply(lambda x: x.strftime('%Y-%m'))
    x_axis_show = 'Date'
df2['Anzahl'] = df2[f'{choosenAnkuenfteUebernachtungen}']
df2['Anteil'] = round((df2[f'{choosenAnkuenfteUebernachtungen}'] / total) * 100, 1)

if df is not None:
    df['Date'] = pd.to_datetime(df[['Jahr', 'Monat']].rename(columns={'Jahr': 'year', 'Monat': 'month'}).assign(day=1))

if selected_vorjahr_vormonat == 'Vorjahr':
    if len(selected_regionen) == 0:
        if len(selected_monate) == 0:
            diff_factor = 12*len(df2['Tourismusregion'].unique())
        else:
            diff_factor = len(selected_monate)*len(df2['Tourismusregion'].unique())
    else:
        if len(selected_monate) == 0:
            diff_factor = 12*len(df2['Tourismusregion'].unique())
        else:
            diff_factor = len(selected_monate)*len(selected_regionen)

else:
    if len(selected_regionen) == 0:
        if len(selected_monate) == 0:
            diff_factor = len(df2['Tourismusregion'].unique())
        else:
            diff_factor = len(df2['Tourismusregion'].unique())
    else:
        if len(selected_monate) == 0:
            diff_factor = len(df2['Tourismusregion'].unique())
        else:
            diff_factor = len(selected_regionen)

if selected_anteil_anzahl == 'Anteil':
    df2 = calcDifference(df2, diff_factor, 'Anteil')
else:
    df2 = calcDifference(df2, diff_factor)

if selected_saison == 'Jahr erzeugen':
    df2 = filterJahr(df2, st.session_state.start_year, st.session_state.end_year)
else:
    df2 = filterJahr(df2, st.session_state.start_year, st.session_state.end_year)

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
    order=alt.Order(f'{df_sort}', sort='ascending'),
    tooltip=[
        alt.Tooltip(f'{x_axis_show}:N', 
                    title='Datum'), 
        alt.Tooltip('Tourismusregion:N', 
                    title='Tourismusregion'), 
        alt.Tooltip(f'{selected_anteil_anzahl}:Q', 
                    title=f'{selected_anteil_anzahl}', 
                    format=','),
        alt.Tooltip(f'{diff_type}:N',
                    title=f'{diff_type}'),
        alt.Tooltip('Durchschnittliche Verweildauer:N',
                    title='Durchschnittliche Verweildauer')
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
    st.altair_chart(line_chart)
elif selected_diagram == 'Balkendiagramm':
    st.altair_chart(stacked_bar_chart)
else:
    st.write("Bitte Auswahl treffen")
df2['Jahr'] = df2['Jahr'].astype(str)

try:    
    df2 = df2[['Jahr', 'Tourismusjahr', 'Tourismushalbjahr', 'Monat', 'Tourismusregion', 'Ankünfte', 'Übernachtungen']]
except:
    df2 = df2[['Jahr', 'Tourismusjahr', 'Tourismusregion', 'Ankünfte', 'Übernachtungen']]
st.write(f"### Gefilterte Daten")
st.write(df2)