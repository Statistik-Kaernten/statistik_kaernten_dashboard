import streamlit as st
from data import addMonthNames, load_data
import base64

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
            '#56B4E9', 
            '#009E73', 
            '#F0E442', 
            '#0072B2', 
            '#D55E00',
            '#999999', 
            '#F28500', 
            '#A2CD5A', 
            '#AD6F3B', 
            '#5D9C9A', 
            '#D3A4A4'
            ]
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
        text-align: center;  /* Center-aligns the text within the box */
    """
    # Render the box with Streamlit
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

def insert_styling(bgr: int, bgg: int, bgb: int, bgAlpha: int, sbr: int, sbg: int, sbb: int, sbAlpha: int) -> None: 
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
            background-size: 100%; /* Zoom in on the image */
            background-position: top;
            background-repeat: no-repeat;
            background-attachment: fixed;
            /*background-color: rgba(255, 255, 255, 1);*/ /* White color with 70% opacity */
            background-blend-mode: normal; /* Overlay to mix background color and image */
          /*  z-index: -1;*/ /* causing issues with random table in the top left corner */
        }}
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

    # # # FIXED SIEBAR WIDTH # # #
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
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