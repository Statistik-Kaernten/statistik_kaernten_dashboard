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

    #st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

   # st.image("img/logo.png", use_container_width=True)

    #with st.expander("Info"):
    #    st.write('''
    #        Infobox
    #    ''')

# # # END SIDE BAR # # #

st.write('## Tourismus - Regionen')
with st.sidebar:
    selected_monate = []
    selected_saison = False

    linieBalken = ['Zeitreihe', 'Balkendiagramm'] 
    selected_diagram = st.selectbox('Diagrammtype:', linieBalken, label_visibility='visible', index=linieBalken.index('Balkendiagramm'))
    if selected_diagram != 'Zeitreihe':
        selected_monate = st.multiselect('Monate auswählen:', getMonths()['Name'], label_visibility='visible')
        #selected_anteil_anzahl = st.radio('Anteil/Anzahl', ['Anzahl', 'Anteil'], index=0,label_visibility='hidden')
        selected_saison = st.radio('zeitliche Gruppierung auswählen:', ['Monate anzeigen', 'Tourismussaison erzeugen', 'Jahr erzeugen'], label_visibility='visible')
    selected_regionen = st.multiselect('Tourismusregionen auswählen:', getSubRegion('Tourismusregion'), label_visibility='visible')


# Tourismus nach Tourismusregione
df2 = get_data('t_tourismus1.csv', select_start_jahr-2, select_end_jahr, 'Tourismusregion', selectRegioLst=selected_regionen, selectMonatLst=selected_monate)
df = get_data('t_tourismus1.csv', select_start_jahr-2, select_end_jahr, 'Tourismusregion', selectRegioLst=selected_regionen)
df = filterJahr(df, st.session_state.start_year, st.session_state.end_year)
df2 = filterJahr(df2, st.session_state.start_year, st.session_state.end_year)



if selected_saison == 'Tourismussaison erzeugen':
    df2 = df2.groupby(['Tourismusjahr', 'Tourismusregion']).agg({'Jahr': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    x_axis_show = 'Tourismusjahr'
elif selected_saison == 'Jahr erzeugen':
    df2 = df2.groupby(['Jahr', 'Tourismusregion']).agg({'Tourismusjahr': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    x_axis_show = 'Jahr'
else: # Monate:
    #df2['Monat'] = df2['Monat'].astype(int)
    #df2 = df2.sort_values(['Jahr', 'Monat'])
    df2['Date'] = pd.to_datetime(df2[['Jahr', 'Monat']].rename(columns={'Jahr': 'year', 'Monat': 'month'}).assign(day=1))
    df2['TJahrMonat'] = df2.apply(lambda row: str(row['Jahr'])+"-"+str(row['Monat']), axis=1)
    x_axis_show = 'Date'

if df is not None:
    df['Date'] = pd.to_datetime(df[['Jahr', 'Monat']].rename(columns={'Jahr': 'year', 'Monat': 'month'}).assign(day=1))



selection = alt.selection_point(fields=selected_regionen)

chart = alt.Chart(df).mark_line().mark_line(size=2).encode(
        x=alt.X('Date:T', title='Datum', axis=alt.Axis(labelAngle=45)),
        y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', title='Anzahl'), 
        color=alt.Color(f'Tourismusregion:N', 
                        title='Tourismusregion', 
                        legend=alt.Legend(orient='bottom', 
                                          columns=4
                                          ), 
                        scale=alt.Scale(range=get_cud_palette())),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
        tooltip=[alt.Tooltip('Date:T',
                              title='Datum'), 
                 alt.Tooltip(f'Tourismusregion:N', 
                             title='Tourismusregion'),
                 alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                             title='Anzahl', 
                             format=','),
                #alt.Tooltip(f'{diff_type}:N',
                #           title=f'{diff_type}'),
                #alt.Tooltip('Durchschnittliche Verweildauer:N',
                #            title='Durchschnittliche Verweildauer')
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

selection2 = alt.selection_point(fields=['Tourismusregion'], bind='legend')

stacked_bar_chart = alt.Chart(df2).mark_bar().encode(
    x=alt.X(f'{x_axis_show}:N', 
            title='Datum', 
            axis=alt.Axis(#labelExpr="datum", 
                labelAngle=45)),
    y=alt.Y(f'{choosenAnkuenfteUebernachtungen}:Q', title='Anzahl'),
    color=alt.Color(
        'Tourismusregion:N', 
        title='Tourismusregion', 
        legend=alt.Legend(orient='bottom', 
                            columns=4
                            ), 
        scale=alt.Scale(range=get_cud_palette())
    ),
    opacity=alt.condition(selection2, alt.value(1), alt.value(0.1)),
    order=alt.Order(f'{choosenAnkuenfteUebernachtungen}:Q', sort='ascending'),
    tooltip=[
        alt.Tooltip('Date:T', 
                    title='Datum'), 
        alt.Tooltip('Tourismusregion:N', 
                    title='Tourismusregion'), 
        alt.Tooltip(f'{choosenAnkuenfteUebernachtungen}:Q', 
                    title='Anzahl', 
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


if selected_diagram == 'Zeitreihe':
    st.altair_chart(line_chart, use_container_width=True)
elif selected_diagram == 'Balkendiagramm':
    st.altair_chart(stacked_bar_chart, use_container_width=True)
else:
    st.write("Bitte Auswahl treffen")

#st.write(df)
st.write(df2)