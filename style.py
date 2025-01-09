import base64
import streamlit as st

def insert_styling(bgr: int, bgg: int, bgb: int, bgAlpha: int, sbr: int, sbg: int, sbb: int, sbAlpha: int) -> None: 

#    # # #  B A C K G R O U N D  I M A G E # # #
#    # Function to get the base64 string of the image
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

#    # Get the base64 string of your image
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