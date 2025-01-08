# COLOR PALETTE LAND KAERNTEN

def get_custom_css():
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

def get_ktn_palette():
    return ['#FFDC00', '#E3000F', '#DADADA', '#B2C8DA', '#A9B84A', '#757070', '#FF851B', '#0074D9', '#2ECC40', '#F012BE', '#7FDBFF']
