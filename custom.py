import streamlit as st
from data import addMonthNames, load_data, getList
import base64
from data import getSubRegion
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import altair as alt

custom_locale = {
                "formatLocale": {
                                "decimal": ",",
                                "thousands": ".",
                                "grouping": [3],
                                "currency": ["", "\u00a0€"]
                                },

                "timeFormatLocale": {
                                "dateTime": "%A, der %e. %B %Y, %X",
                                "date": "%d.%m.%Y",
                                "time": "%H:%M:%S",
                                "periods": ["AM", "PM"],
                                "days": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
                                "shortDays": ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
                                "months": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
                                "shortMonths": ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
                                    }
                }

zaehlstellen_dict = {
                '7140': 'A11: Karawankentunnel',
                '632': 'A11: St. Martin', 
                '70': 'A11: St. Ulrich', 

                '54': 'A02: Velden',
                '530': 'A02: Packsattel',
                '534': 'A02: Gräberntunnel',
                '542': 'A02: St. Andrä im Lavanttal',
                '558': 'A02: Völkermarkt',
                '563': 'A02: Grafenstein',
                '212': 'A02: Klagenfurt Nord',
                '569': 'A02: Krumpendorf',
                '576': 'A02: Pörtschach Ost',
                '581': 'A02: Villach',

                '165': 'S37: Zollfeld'
                }

def get_custom_css() -> str:
    """
    Custom CSS for streamlit app  
    Slider Color (#FFDC00)  
    Watermark Params
    """
    custom_css = """
        <style>
        
        div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
            background-color: #FFDC00 !important; }

       .watermark {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 200px;
                color: rgba(0, 0, 0, 0.5);
                transform: translate(-50%, -50%) rotate(-20deg); 
                white-space: nowrap;
                z-index: 1000;
                pointer-events: none;
                }
        #vg-tooltip-element{z-index: 1000051}
        </style>
        """
    return custom_css

def get_cud_palette() -> list[str]:
    """
    Color Universal Design Color Palette

    :return: cud_color_palette: List of hex colors
    """
    
    cud_colors = [
            '#003B5C', 
            '#FFB81C', 
            '#55B0B9', 
            '#F56D8D', 
            '#9E2A2F', 
            '#5B8C5A', 
            '#CC79A7',
            '#E69F00', 
            '#b3dbf5',#'#56B4E9',  
            '#009E73', 
            #'#F0E442', 
            #'#0072B2', 
            #'#D55E00',
            #'#999999', 
            #'#F28500', 
            #'#A2CD5A', 
            #'#AD6F3B', 
            #'#5D9C9A', 
            #'#D3A4A4'
            ]
    '''
    cud_colors = [
            '#e69d00', 
            '#56b3e9', 
            '#009e74', 
            '#f0e442', 
            '#0071b2', 
            '#d55c00', 
            '#cc79a7',
            '#000000', 
            '#999999'
            ]
    '''
    return cud_colors

def get_monthly_color_palette() -> list[str]:
    """
    Color Palette for monthly representation, blueish colors for winter, redish colors for summer
    
    :return: monthly_color_palette: List of 12 hex colors (6 blueish, 6 redish)

    """
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
    return color_palette

def colored_box(label, bgcolor, text, textcolor, bordercolor):
    # Define the CSS styles for the box
    box_style = f"""
        background-color: {bgcolor}; 
        padding: 20px; 
        border-radius: 5px; 
        border: 2px solid {bordercolor};  /* White border with a thickness of 2px */
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);  /* Optional: Adds a subtle shadow for better visibility */
        text-align: left;  /* Center-aligns the text within the box */
    """
    # Render the box with Streamlit#<h2 style="color: {textcolor}; margin: 0;">{label}</h2>
    st.markdown(f"""
        <div style="{box_style}">
            <h2 style="color: {textcolor}; margin: 0;">{label}</h2>
            <p style="margin: 0; color: {textcolor}"><font size="5">{text}</font></p>
        </div>
        """, unsafe_allow_html=True)

def format_prozent(value: float) -> str:
    sign = '-' if value < 0 else '+'
    value  = f"{abs(value):.1f}".replace('.', ',')
    return f"{sign}{value} %"

def anstiegrueckgang(value: float) -> list[str]:
    if (value >= 0):
        lst = ['Anstieg', 'Plus']
    else: 
        lst = ['Rückgang', 'Minus']
    return lst

def insert_styling(bgr: int, bgg: int, bgb: int, bgAlpha: int, sbr: int, sbg: int, sbb: int, sbAlpha: int, slider_bg_color: str = '#ffffff', text_color: str = 'black') -> None: 
    """
    Inject CSS for the streamlit app, background image, background color, sidebarcolor

    :param: bgr: Background red (0-255)
    :param: bgg: Background green (0-255)
    :param: bgb: Background blue (0-255) 
    :param: bgAlpha: Background Alpha - transparency (0-1)

    :param: bgr: Sidebar red (0-255)
    :param: bgg: Sidebar green (0-255)
    :param: bgb: Sidebar blue (0-255)
    :param: bgAlpha: Sidebar Alpha - transparency (0-1)

    """
    # # #  B A C K G R O U N D  I M A G E # # #
    # Function to get the base64 string of the image
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Get the base64 string of your image
    image_base64 = get_base64_image("img/top_background_mid.PNG")

    # Inject CSS with the image as the background
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{image_base64}");
            background-size: 100%;                                          /* Zoom in on the image */
            background-position: top;
            background-repeat: no-repeat;
            background-attachment: fixed;
            /*background-color: rgba(255, 255, 255, 1);*/                   /* White color with 70% opacity */
            background-blend-mode: normal;                                  /* Overlay to mix background color and image */
          /*  z-index: -1;*/                                                /* causing issues with random table in the top left corner */
        }}
            /* Change sidebar text color to white*/
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        div[data-baseweb="select"] > div {{
            background-color: {slider_bg_color}}};
        </style>
        """,
        unsafe_allow_html=True
    )
    # # #  END BG-Image # # #

    # # # BACK GROUND COLOR # # # 
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: rgba({bgr}, {bgg}, {bgb}, {bgAlpha});
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <style>
        [data-testid=stSidebar] {{
            background-color: rgba({sbr}, {sbg}, {sbb}, {sbAlpha});
            /*z-index: 9999;*/  /* Ensures the sidebar stays on top */
        }}
    </style>
    """, unsafe_allow_html=True)
    # # # END BACK GROUND COLOR  # # # 

    # # # FIXED SIDEBAR WIDTH # # #
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    
def tourismus_box() -> any:
    """
    colored_box for "Tourismus"

    :return: colored_box with monthly "Tourismus" information
    """
    df = addMonthNames(load_data('t_tourismus1.csv'))
    df = df[df['Jahr'] >= df['Jahr'].max()-1] 
    df = df.groupby(['Jahr', 'MonatId']).agg({'Monat': 'max', 'Ankünfte': 'sum', 'Übernachtungen': 'sum'}).reset_index()
    monthDf = df.groupby(['MonatId']).agg({'Monat': 'max'}).reset_index()
    current_month_int = df[df['Jahr'] == df['Jahr'].max()]['MonatId'].max()

    current_month_str = monthDf.loc[monthDf['MonatId'] == df[df['Jahr'] == df['Jahr'].max()]['MonatId'].max(),'Monat'].values[0]
    veraenderung_ankuenfte = 100/df.loc[(df['Jahr'] == int(df['Jahr'].max()-1)) & (df['MonatId'] == current_month_int)]['Ankünfte'].values[0]*df.loc[(df['Jahr'] == int(df['Jahr'].max())) & (df['MonatId'] == current_month_int)]['Ankünfte'].values[0]-100
    veraenderung_uebernachtungen = 100/df.loc[(df['Jahr'] == int(df['Jahr'].max()-1)) & (df['MonatId'] == current_month_int)]['Übernachtungen'].values[0]*df.loc[(df['Jahr'] == int(df['Jahr'].max())) & (df['MonatId'] == current_month_int)]['Übernachtungen'].values[0]-100
    durchschnittliche_verweildauer = f"{round(df.loc[(df['Jahr'] == int(df['Jahr'].max())) & (df['MonatId'] == current_month_int)]['Übernachtungen'].values[0]/df.loc[(df['Jahr'] == int(df['Jahr'].max())) & (df['MonatId'] == current_month_int)]['Ankünfte'].values[0],1):.1f}".replace('.', ',')

    tourismus_box = colored_box("TOURISMUS", "#46C39F", f"Gegenüber dem {current_month_str} des Vorjahres errechnet sich bei den Ankünften ein {anstiegrueckgang(veraenderung_ankuenfte)[0]} von {format_prozent(veraenderung_ankuenfte)} und bei den Übernachtungen ein {anstiegrueckgang(veraenderung_uebernachtungen)[1]} von {format_prozent(veraenderung_uebernachtungen)}. Die durchschnittliche Aufenthaltsdauer belief sich auf {durchschnittliche_verweildauer} Nächtigungen.", "black", "white")
    return tourismus_box

def bevoelkerung_box() -> any:
    """
    colored_box for "Bevölkerung"

    :return: colored_box with yearly "Bevölkerung" information
    """
    df = load_data('t_bev1.csv')
    df = df.groupby(['Jahr']).agg({'Anzahl': 'sum'}).reset_index()
    max_year = 2025
    last_year = max_year - 1

    pop_this_year = df.loc[df['Jahr']==max_year]['Anzahl'].values[0]
    pop_last_year = df.loc[df['Jahr']==last_year]['Anzahl'].values[0]

    diff = round(100/pop_last_year*pop_this_year - 100, 2)

    geb_df = load_data('t_bev2.csv')
    geb_df = geb_df.groupby(['Jahr']).agg({'Anzahl': 'sum'}).reset_index()

    geb_jahr_max = geb_df['Jahr'].max()
    geb_jahr_vorjahr = geb_df['Jahr'].max() - 1

    geburten_max_jahr = geb_df.loc[geb_df['Jahr'] == geb_jahr_max]['Anzahl'].values[0]
    geburten_vorjahr = geb_df.loc[geb_df['Jahr'] == geb_jahr_vorjahr]['Anzahl'].values[0]
    geb_diff = round(100/geburten_vorjahr*geburten_max_jahr - 100, 2)

    df_gest = load_data('t_bev4_gestorbene.csv')
    df_gest = df_gest.groupby(['Jahr']).agg({'Anzahl': 'sum'}).reset_index()
    gest_jahr_max = df_gest['Jahr'].max()
    gest_jahr_vorjahr = df_gest['Jahr'].max() - 1

    gest_max_jahr = df_gest.loc[df_gest['Jahr'] == gest_jahr_max]['Anzahl'].values[0]
    gest_vorjahr = df_gest.loc[df_gest['Jahr'] == gest_jahr_vorjahr]['Anzahl'].values[0]

    gest_diff = round(100/gest_vorjahr*gest_max_jahr - 100, 2)

    wanderungssaldo = '+2.403'

    bevoelkerung_box = colored_box("BEVÖLKERUNG", "#8f44a3", f"Per 1.1.{max_year} hatte Kärnten {add_thousand_dot(str(pop_this_year))} Einwohner. Im Vergleich zum Vorjahr gab es somit einen {anstiegrueckgang(diff)[0]} von {format_prozent(diff)}. Im Jahr {geb_jahr_max} gab es {add_thousand_dot(str(geburten_max_jahr))} Geburten (ein {anstiegrueckgang(geb_diff)[1]} von {format_prozent(geb_diff)}) und {add_thousand_dot(str(gest_max_jahr))} Todesfälle ({format_prozent(gest_diff)}). Das Wanderungssaldo betrug {wanderungssaldo}.", "white", "white")
    return bevoelkerung_box

def get_color_map_regionen() -> dict[str: str]:
    """
    Fixed Colors for Tourismusregionen, to prevent color"jumping" when adding or removing items from multiselect
    """
    tourismusregionen = getSubRegion('Tourismusregion')
    palette = get_cud_palette()

    color_map_regionen = {
        tourismusregionen[0]: palette[0], 
        tourismusregionen[1]: palette[1],
        tourismusregionen[2]: palette[2],
        tourismusregionen[3]: palette[3],
        tourismusregionen[4]: palette[4],
        tourismusregionen[5]: palette[5],
        tourismusregionen[6]: palette[6],
        tourismusregionen[7]: palette[7],
        tourismusregionen[8]: palette[8]
    }
    return color_map_regionen

def get_color_map_all_unterkunftsarten() -> dict[str: str]:
    palette = get_cud_palette()
    displayList = getList(None, 'Unterkunftsarten')
    color_map_all_unterkunftsarten = {
        displayList[0]: palette[0], 
        displayList[1]: palette[1],
        displayList[2]: palette[2],
        displayList[3]: palette[3],
        displayList[4]: palette[4],
        displayList[5]: palette[5],
        displayList[6]: palette[6],
        displayList[7]: palette[7],
        displayList[8]: palette[8],
        displayList[9]: palette[0], 
        displayList[10]: palette[1],
        displayList[11]: palette[2],
        displayList[12]: palette[3],
        displayList[13]: palette[4],
        displayList[14]: palette[5],
        displayList[15]: palette[6],
        displayList[16]: palette[7]
    }
    return color_map_all_unterkunftsarten

def get_color_map_unterkunftsarten(displayList: list[str]) -> dict[str: str]:
    palette = get_cud_palette()
    color_map_unterkunftsarten = {
        displayList[0]: palette[0], 
        displayList[1]: palette[1],
        displayList[2]: palette[2],
        displayList[3]: palette[3],
        displayList[4]: palette[4],
        displayList[5]: palette[5],
        displayList[6]: palette[6]
    }
    return color_map_unterkunftsarten

def round_to_nearest_10_step(n):
    # Find the power of 10 just below the number
    power = 10 ** (len(str(n)) - 1)
    # Calculate the lower and upper bounds
    lower = (n // power) * power
    upper = lower + power
    # Return the closer of the two
    return lower if n - lower < upper - n else upper

def pop_chart(df: pd.DataFrame, gkz_list: list[str], animate: bool = False):  
    df['gkz'] = df['gkz'].astype(str)
    df = df[df['gkz'].isin(gkz_list)]
    df.drop(columns=['gkz'], inplace=True)
    df = df.groupby(['Jahr', 'Geschlecht', 'Alter']).sum().reset_index()
    max_val = max(abs(df["Anzahl"])) 
    df = df.pivot(index=['Jahr', 'Alter'], columns=['Geschlecht'], values=['Anzahl']).reset_index()
    min_jahr = df['Jahr'].unique().min()
    max_jahr = df['Jahr'].unique().max()
    
    if animate:
        base_df = df[df['Jahr'] == min_jahr]
    else:
        base_df = df[df['Jahr'] == max_jahr]

    step = int(round_to_nearest_10_step(int(round(max_val/4, 0))))

    # Round up to nearest step
    tick_max = int(np.ceil(max_val / step)) * step

    # Generate symmetric tick values
    tickvals = list(range(-tick_max, tick_max + step, step))
    ticktext = [f"{abs(val):,.0f}".replace(",", ".") for val in tickvals]

    # Base Data
    #df = df[df['Jahr'] == df['Jahr'].unique().min()]
    #yr = df["jahr"]
    max_x = max(df['Anzahl']['männlich'].max(), df['Anzahl']['weiblich'].max())
    y = base_df['Alter']
    x1 = base_df['Anzahl']['männlich'] * -1
    x2 = base_df['Anzahl']['weiblich']
    if base_df['Jahr'].max() > 2025:
        opac = 0.75
    else:
        opac = 1

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=y,
            x=x1,
            name="Männer",
            orientation="h",
            showlegend=True,
            marker=dict(
                color="#B9CFDF",
                line=dict(color="#9CBCD2", width=1),
            ),
            opacity=opac
        )
    )

    fig.add_trace(
        go.Bar(
            y=y,
            x=x2,
            name="Frauen",
            orientation="h",
            showlegend=True,
            marker=dict(
                color="#EAD6D6",
                line=dict(color="#DDBBBB", width=1),
            ),
            opacity=opac
        )
    )

    if animate:
        frames = []
        for year in range(min_jahr, max_jahr+1):
            if year > 2025:
                opac = 0.5
            else:
                opac = 1
            year_df = df[df['Jahr'] == year]
            frames.append(go.Frame(
                data=[
                    go.Bar(x=-year_df['Anzahl']['männlich'], y=year_df['Alter'], opacity=opac),
                    go.Bar(x=year_df['Anzahl']['weiblich'], y=year_df['Alter'], opacity=opac)
                ],
                name=str(year), 
                layout=go.Layout(title_text=f"<b>Bevölkerungspyramide – {year}</b>")
            ))

        fig.frames = frames

        fig.update_layout(
            title={
                'text': f"<b>Bevölkerungspyramide – {min_jahr}</b>",
                'x': 0.5,          # Horizontal center
                'xanchor': 'center',
                'yanchor': 'top'
            },
                title_font=dict(size=24, color='black'),
            margin=dict(
                l=25,
                r=25,
                b=25,
                t=25,
            ),
            #paper_bgcolor="#363845",
            #plot_bgcolor="#363845",
            yaxis=dict(
                title="Alter",
                title_font_size=15,
                tickfont_size=12,
                showgrid=True,
                #titlefont_color="#FFFFFF",
                #tickfont_color="#FFFFFF",
                range=[-1, 115],
                autorange=False
            ),
            xaxis=dict(
                title="Bevölkerung",
                title_font_size=15,
                tickfont_size=12,
                showgrid=True,
                #titlefont_color="#FFFFFF",
                #tickfont_color="#FFFFFF",
                tickvals = tickvals,
                ticktext = ticktext,
                #tickvals=[-4000,-3000,-2000,-1000,0,1000,2000,3000,4000,],
                #ticktext=["4.000", "3.000", "2.000", "1.000", 0, "1.000", "2.000", "3.000", "4.000"],
                range=[-max_x-1, max_x+1],
                autorange=False
            ),
            legend=dict(
                x=0,
                y=1,
                #bgcolor="#363845",
                #bordercolor="#363845",
            ),
            barmode="relative",
            bargap=0,
            bargroupgap=0,
            width=800,  # Set the width of the graph
            height=600,  # Set the height of the graph
            dragmode=False,  # Disable panning and box-select dragging
            xaxis_fixedrange=True,  # Disable zoom on x-axis
            yaxis_fixedrange=True, 
            font=dict(family="Roboto, sans-serif"),
            updatemenus=[{
                'type': 'buttons',
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 250, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 0},
                        'mode': 'immediate'
                    }]
                }],
                #'visible': False
            }]
        )
    else:
    #fig.add_trace(
    #    go.Scatter(
    #        y=y,
    #        x=x1,
    #        name="Männer",
    #        showlegend=False,
    #        mode="markers",
    #        marker_color="#81A9C5",
    #        marker_size=8,
    #    )
    #)

    #fig.add_trace(
    #    go.Scatter(
    #        y=y,
    #        x=x2,
    #        name="Frauen",
    #        showlegend=False,
    #        mode="markers",
    #        marker_color="#CFA0A0",
    #        marker_size=8,
    #    )
    #)

        fig.update_layout(
            title={
                'text': f"<b>Bevölkerungspyramide – {max_jahr}</b>",
                'x': 0.5,          # Horizontal center
                'xanchor': 'center',
                'yanchor': 'top'
            },
                title_font=dict(size=24, color='black'),
            margin=dict(
                l=25,
                r=25,
                b=25,
                t=25,
            ),
            #paper_bgcolor="#363845",
            #plot_bgcolor="#363845",
            yaxis=dict(
                title="Alter",
                title_font_size=15,
                tickfont_size=12,
                showgrid=True,
                #titlefont_color="#FFFFFF",
                #tickfont_color="#FFFFFF",
                range=[-1, 115],
                autorange=False
            ),
            xaxis=dict(
                title="Bevölkerung",
                title_font_size=15,
                tickfont_size=12,
                showgrid=True,
                #titlefont_color="#FFFFFF",
                #tickfont_color="#FFFFFF",
                tickvals = tickvals,
                ticktext = ticktext,
                #tickvals=[-4000,-3000,-2000,-1000,0,1000,2000,3000,4000,],
                #ticktext=["4.000", "3.000", "2.000", "1.000", 0, "1.000", "2.000", "3.000", "4.000"],
                range=[-max_x-1, max_x+1],
                autorange=False
            ),
            legend=dict(
                x=0,
                y=1,
                #bgcolor="#363845",
                #bordercolor="#363845",
            ),
            barmode="relative",
            bargap=0,
            bargroupgap=0,
            width=800,  # Set the width of the graph
            height=600,  # Set the height of the graph
            dragmode=False,  # Disable panning and box-select dragging
            xaxis_fixedrange=True,  # Disable zoom on x-axis
            yaxis_fixedrange=True, 
            font=dict(family="Roboto, sans-serif")
        )
    
    return fig

def handle_comma(input: float) -> str:
    input = str(input).replace('.', ',')
    return input

def add_thousand_dot(txt: str) -> str:
    if(txt[0] == '-'):
        if(len(txt) > 7):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:6] + '.' + txt[6:]
            txt = txt[::-1]
        elif(len(txt) > 4):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:]
            txt = txt[::-1]
    else:
        if(len(txt) > 6):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:6] + '.' + txt[6:]
            txt = txt[::-1]
        elif(len(txt) > 3):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:]
            txt = txt[::-1]
    return txt

def get_age_order(altersgruppe: str) -> list[str]:
    if altersgruppe == 'erwerbsalter':
        age_order = ['unter 15 Jahre', '15 bis 64 Jahre', '65 Jahre und älter']
    elif altersgruppe == 'gruppe_5':
        age_order = [
            'unter 5 Jahre',
            '5 bis 9 Jahre',
            '10 bis 14 Jahre',
            '15 bis 19 Jahre',
            '20 bis 24 Jahre',
            '25 bis 29 Jahre',
            '30 bis 34 Jahre',
            '35 bis 39 Jahre',
            '40 bis 44 Jahre',
            '45 bis 49 Jahre',
            '50 bis 54 Jahre',
            '55 bis 59 Jahre',
            '60 bis 64 Jahre',
            '65 bis 69 Jahre',
            '70 bis 74 Jahre',
            '75 bis 79 Jahre',
            '80 bis 84 Jahre',
            '85 bis 89 Jahre',
            '90 bis 94 Jahre',
            '95 bis 99 Jahre',
            '100 Jahre und älter'
        ]
    elif altersgruppe == 'gruppe_15':
        age_order = ['unter 15 Jahre', '15 bis 29 Jahre', '30 bis 49 Jahre', '50 bis 64 Jahre', '65 bis 84 Jahre', '85 Jahre und älter']
    return age_order

def select_messstelle(values: str) -> str:
    key = [key for key, value in zaehlstellen_dict.items() if value == values]
    if key:
        return key[0]
    else:
        return None
    
def create_linechart(df: pd.DataFrame, reg: int) -> pd.DataFrame:
    palette = get_cud_palette()
    y_min = min(df['ANZAHL'].astype(float).min(), df['REGRESSION'].astype(float).min())
    y_max = max(df['ANZAHL'].astype(float).max(), df['REGRESSION'].astype(float).max())
    df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(int(round(x, 0)))))

    chart = alt.Chart(df).mark_line(color=palette[1], size=4).encode(
        x=alt.X('DATUM:T', title='Datum', axis=alt.Axis(format='%Y-%m', labelAngle=45)),
        y=alt.Y('ANZAHL:Q', title='Anzahl', scale=alt.Scale(domain=(y_min, y_max))),
        tooltip=[alt.Tooltip('DATUM:T', title='Datum'), 
             #alt.Tooltip('TYPE:N', title='Arbeitsstätte'),
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')]

    )

    hover_points = alt.Chart(df).mark_circle(size=250, opacity=0).encode(
    x=alt.X('DATUM:T', title='Datum'),
    y=alt.Y('ANZAHL:Q', title='Anzahl'),
    tooltip=[alt.Tooltip('DATUM:T', title='Jahr'), 
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')]
    )

    df['REG_FORMATTED'] = df['REGRESSION'].apply(lambda x: add_thousand_dot(str(int(round(x, 0)))))
    regression_line = alt.Chart(df).mark_line(color=palette[6], size=2).encode(
            x=alt.X('DATUM:T'),
            y=alt.Y('REGRESSION:Q', title="Trend"),
            tooltip=alt.value(None)
            #[alt.Tooltip('DATUM:T', title='Datum'),
            #         alt.Tooltip('REG_FORMATTED:O', title='Trend')]
        )

    if(reg == False):
        combined_chart = (chart + hover_points).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )
    else:
        combined_chart = (chart + hover_points + regression_line).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )

    return combined_chart

def LinearRegression(df: pd.DataFrame) -> pd.DataFrame:

    df['DATUM'] = pd.to_datetime(df['DATUM'])
    df['DAYS_NUMERIC'] = (df['DATUM'] - df['DATUM'].min()).dt.days

    x_mean = np.mean(df['DAYS_NUMERIC'])
    df['ANZAHL'] = df['ANZAHL'].astype(float)
    y_mean = np.mean(df['ANZAHL'])

    numerator = np.sum((df['DAYS_NUMERIC'] - x_mean) * (df['ANZAHL'] - y_mean))
    denominator = np.sum((df['DAYS_NUMERIC'] - x_mean) ** 2)
    m = numerator / denominator
    b = y_mean - m * x_mean

    df['REGRESSION'] = m * df['DAYS_NUMERIC'] + b
    return df

def verkehr_anpassen(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(['JAHR', 'MONAT'])
    df['DAYS'] = (df['DATUM'] - df['DATUM'].min()).dt.days
    df = LinearRegression(df)
    df.drop(columns=['JAHR', 'MONAT', 'DAYS'], inplace=True, axis=1)
    return df

def convert_hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format. Use #RRGGBB or #RGB.")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return [r, g, b, 255]

def set_colors(df: pd.DataFrame, gkz_list: list[str]):
    UNSELECTED = convert_hex_to_rgba(get_cud_palette()[8])
    SELECTED = convert_hex_to_rgba(get_cud_palette()[3])
    df['Color'] = df['GKZ'].apply(lambda x: SELECTED if x in gkz_list else UNSELECTED)
    return df

if __name__ == '__main__':
    pass
