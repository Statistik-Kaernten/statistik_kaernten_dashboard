import streamlit as st

st.set_page_config(page_title="Tourismus - Herkunftsländer Vergleich", layout="wide")

import altair as alt
from data import *
from custom import *
from create_charts import *

insert_styling(255, 255, 255, 1, 70, 195, 159, 1)

# CONSTANTS
START_JAHR: int = 2003
END_JAHR: int = 2025

bdl_at: list[str] = ['Kärnten', 'Wien', 'Tirol', 'Vorarlberg', 'Steiermark', 'Oberösterreich', 'Niederösterreich', 'Salzburg', 'Burgenland']
bdl_de: list[str] = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Mitteldeutschland', 'Norddeutschland', 'Nordrhein-Westfalen', 'Ostdeutschland']

def getPeriode(time: str):
    if (time == 'Kalenderjahr'):
        return 'Jahr'
    elif (time=='Winterhalbjahr'):
        return 'WHJ'
    elif (time=='Sommerhalbjahr'):
        return 'SHJ'
    else:
        return 0

st.markdown(get_custom_css(), unsafe_allow_html=True)

# # # BEGIN REGIONS-AUSWAHL # # # 
with st.sidebar:
    ankuenfteUebernachtungen = ['Ankünfte', 'Übernachtungen']
    choosenAnkuenfteUebernachtungen = st.selectbox('Ankünfte/Übernachtungen', ankuenfteUebernachtungen, label_visibility='visible',  index=ankuenfteUebernachtungen.index('Übernachtungen'))
    if (choosenAnkuenfteUebernachtungen == 'Ankünfte'):
        diff_type = 'Veränderung Ankünfte'
    elif (choosenAnkuenfteUebernachtungen == 'Übernachtungen'):
        diff_type = 'Veränderung Übernachtungen'
    choosenHerkunftUnterkunft = st.selectbox('nach', ['Herkunftsländern', 'Unterkunftsarten'], label_visibility='visible')
    time = 'Kalenderjahr'

    first_choice = 'Tourismusregion' 

    options2 = getSubRegion(first_choice)
    options2.append('Ganz Kärnten')
    #options2.append('Alle Tourismusregionen') #???
    second_choice = 'Ganz Kärnten'
    second_choice = st.selectbox("Tourismusregion:", 
                                    options2, 
                                    label_visibility='visible',
                                    index=options2.index(second_choice) 
                                    if second_choice in options2 else 0)
    
    selected_jahre: int = st.slider("Startjahr",
        min_value=START_JAHR,
        max_value=END_JAHR-1,
        value=(2014, END_JAHR),
        step=1)
    
    select_start_jahr: int = selected_jahre[0]
    select_end_jahr: int = selected_jahre[1]

    #####   
    linieBalken = ['Liniendiagramm', 'Balkendiagramm'] 
    choosenDiagram = st.selectbox('Grafik', linieBalken, label_visibility='collapsed',  index=linieBalken.index('Balkendiagramm'))
    if (choosenHerkunftUnterkunft == 'Herkunftsländern'):
        df = get_data('t_tourismus2.csv', select_start_jahr-1, select_end_jahr, first_choice, second_choice)
        type: str = 'Herkunft'
        waehlenSie = 'Bitte wählen Sie ein Land aus.'
    elif(choosenHerkunftUnterkunft == 'Unterkunftsarten'):
        df = get_data('t_tourismus3.csv', select_start_jahr-1, select_end_jahr, first_choice, second_choice)
        type: str = 'Unterkunft'
        waehlenSie = 'Bitte wählen Sie eine Unterkunftsart aus.'
    displayList: list[str] = getList(df, choosenHerkunftUnterkunft)
    if (choosenHerkunftUnterkunft == 'Herkunftsländern'):
        laender: list[str] = ['Bundesländer Österreichs', 'Regionen Deutschlands', 'Alle Herkunftsländer', 'Auswahl']

        selectLaender = st.selectbox('Märkte nach Regionen:', laender)
        bdl: list[str] = bdl_at + bdl_de
        allLaenderList = [item for item in displayList if item not in bdl]

        if (selectLaender == 'Bundesländer Österreichs'):
            selected = bdl_at
        elif (selectLaender == 'Regionen Deutschlands'):
            selected = bdl_de
        elif (selectLaender == 'Alle Herkunftsländer'):
            selected = allLaenderList
        else:
            selected = []
    elif (choosenHerkunftUnterkunft == 'Unterkunftsarten'):
        selected = displayList
    options = st.multiselect(
            "# Auswahl:",
            displayList,
            selected, 
            placeholder=waehlenSie
            )
    #####


    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png", use_container_width=True)

    with st.expander("Info"):
        st.write('''
            Infobox
        ''')

# # # END REGIONS-AUSWAHL # # #


st.write(f'## Tourismus nach {choosenHerkunftUnterkunft}')
st.write(f"### Anzahl der {choosenAnkuenfteUebernachtungen} - {second_choice}")

# # # #  GET THE DATA
#if (choosenHerkunftUnterkunft == 'Herkunftsländern'):
#    df = get_data('t_tourismus2.csv', select_start_jahr-1, select_end_jahr, first_choice, second_choice)
#    type: str = 'Herkunft'
#    waehlenSie = 'Bitte wählen Sie ein Land aus.'
#elif(choosenHerkunftUnterkunft == 'Unterkunftsarten'):
#    df = get_data('t_tourismus3.csv', select_start_jahr-1, select_end_jahr, first_choice, second_choice)
#    type: str = 'Unterkunft'
#    waehlenSie = 'Bitte wählen Sie eine Unterkunftsart aus.'

# # #  BEGIN - SELECTION SECTION  # # #
#displayList: list[str] = getList(df, choosenHerkunftUnterkunft)

#if (choosenHerkunftUnterkunft == 'Herkunftsländern'):
#    laender: list[str] = ['Bundesländer Österreichs', 'Regionen Deutschlands', 'Alle Herkunftsländer', 'Auswahl']

#    selectLaender = st.selectbox('Märkte nach Regionen:', laender)
#    bdl: list[str] = bdl_at + bdl_de
#    allLaenderList = [item for item in displayList if item not in bdl]

#    if (selectLaender == 'Bundesländer Österreichs'):
#        selected = bdl_at
#    elif (selectLaender == 'Regionen Deutschlands'):
#        selected = bdl_de
#    elif (selectLaender == 'Alle Herkunftsländer'):
#        selected = allLaenderList
#    else:
#        selected = []
#elif (choosenHerkunftUnterkunft == 'Unterkunftsarten'):
#    selected = displayList
#options = st.multiselect(
#        "# Auswahl:",
#        displayList,
#        selected, 
#        placeholder=waehlenSie
#        )



#### SYMBOL LIMIT
def getSymbolLimit():
    return (len(options))

def getColumnLength():
    if (getSymbolLimit() > 26):
        return 2
    else: 
        return 1
    
df = df[df[type].isin(options)]

# # #  END - SELECT LÄNDER SECTION  # # #
if choosenHerkunftUnterkunft == 'Unterkunftsarten':
    color_map_keys = list(get_color_map_unterkunftsarten(displayList).keys())
    color_map_values = list(get_color_map_unterkunftsarten(displayList).values())
else:
    color_map_keys = options
    color_map_values = get_cud_palette()


periodeDf = getPeriode(time)
if (periodeDf == 'SHJ'):
    df = df[df['Tourismushalbjahr'] == periodeDf]
elif (periodeDf == 'WHJ'):
    df = df[df['Tourismushalbjahr'] == periodeDf]
selection = alt.selection_point(fields=[type], bind='legend')

df = calcDifference(df, 12*getSymbolLimit())
df = df[df['Jahr'] >= select_start_jahr]

chart = alt.Chart(df).mark_line().mark_line(size=2).encode(
        x=alt.X('Date:T', title='Datum', axis=alt.Axis(labelAngle=45)),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', title='Anzahl'), 
        color=alt.Color(f'{type}:N', 
                        title=f'{type}', 
                        legend=alt.Legend(orient='right', 
                                          columns=getColumnLength(),
                                          symbolLimit=getSymbolLimit(),
                                          titleFontWeight='bold'), 
                        scale=alt.Scale(domain=color_map_keys, range=color_map_values)),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
        tooltip=[alt.Tooltip('Date:T',
                              title='Datum'), 
                 alt.Tooltip(f'{type}:N', 
                             title=f'{type}'),
                 alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                             title='Anzahl', 
                             format=','),
                alt.Tooltip(f'{diff_type}:N',
                            title=f'{diff_type}'),
                alt.Tooltip('Durchschnittliche Verweildauer:N',
                            title='Durchschnittliche Verweildauer')
                             ],
    ).add_params(
    selection).properties(
    width=800,
    height=600
)
line = chart.mark_line()
points = chart.mark_point(filled=True, size=30)
line_chart = (chart + points).configure_axis(
    labelFontSize=14,
    titleFontSize=16,
    titleFontWeight='bold'
    )

selection2 = alt.selection_point(fields=[f'{type}'], bind='legend')
stacked_bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Date:T', title='Datum', axis=alt.Axis(labelAngle=45)),
    y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', title='Anzahl'),
    color=alt.Color(
        f'{type}:N', 
        title=f'{type}', 
        legend=alt.Legend(orient='right', 
                            columns=getColumnLength(),
                            symbolLimit=getSymbolLimit(),
                            titleFontWeight='bold'), 
        scale=alt.Scale(domain=color_map_keys, range=color_map_values)
    ),
    opacity=alt.condition(selection2, alt.value(1), alt.value(0.1)),
    order=alt.Order(f'{choosenAnkuenfteUebernachtungen}:Q', sort='ascending'),
    tooltip=[
        alt.Tooltip('Date:T', 
                    title='Datum'), 
        alt.Tooltip(f'{type}:N', 
                    title=f'{type}'), 
        alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                    title='Anzahl', 
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

if (options!=[]):
#    linieBalken = ['Liniendiagramm', 'Balkendiagramm'] 
#    choosenDiagram = st.selectbox('Grafik', linieBalken, label_visibility='collapsed',  index=linieBalken.index('Balkendiagramm'))
    if (choosenDiagram == 'Liniendiagramm'):
        st.altair_chart(line_chart, use_container_width=True)
    elif (choosenDiagram == 'Balkendiagramm'):
        st.altair_chart(stacked_bar_chart, use_container_width=True)

if (options!=[]):
    st.write(f"### Gefilterte Daten - {second_choice} nach {choosenHerkunftUnterkunft}")
    df.drop(columns=['Date'], inplace=True)
    if 'Jahr' in df.columns: 
        df['Jahr'] = df['Jahr'].astype(str)
    st.dataframe(df, hide_index=True)

#st.markdown("""
#    <a href="https://github.com/Statistik-Kaernten/statistik_kaernten_dashboard/blob/main/data/t_tourismus2.csv" download target="_blank">
#        <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
#            Download alle Daten Herkunftsländer
#        </button>
#    </a>
#    """, unsafe_allow_html=True)

#st.markdown("""
#    <a href="https://github.com/Statistik-Kaernten/statistik_kaernten_dashboard/blob/main/data/t_tourismus3.csv" download target="_blank">
#        <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
#            Download alle Daten Unterkunftsarten
#        </button>
#    </a>
#    """, unsafe_allow_html=True)