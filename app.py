import streamlit as st

st.set_page_config(
    page_title="Earthworks App",
    layout="wide"
)

# ----------- GLOBAL DARK THEME CSS -----------
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #0f1117;
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #141821;
    border-right: 1px solid #1f2937;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

/* Remove radio circle */
div[role="radiogroup"] > label > div:first-child {
    display: none;
}

/* Sidebar menu items */
div[role="radiogroup"] label {
    background-color: transparent;
    padding: 10px 12px;
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
}

div[role="radiogroup"] label:hover {
    background-color: #1b1f2a;
}

/* Active item (Streamlit hack – first checked) */
div[role="radiogroup"] label:has(input:checked) {
    background-color: #ff8a00;
    color: #000;
}

/* Headings */
h1, h2, h3 {
    color: #f9fafb;
}

/* Info box */
div[data-testid="stAlert"] {
    background-color: #1b1f2a;
    border: 1px solid #ff8a00;
}

/* Buttons */
.stButton>button {
    background-color: #ff8a00;
    color: #000;
    border-radius: 8px;
    border: none;
    padding: 8px 16px;
}

.stButton>button:hover {
    background-color: #ffa733;
}

</style>
""", unsafe_allow_html=True)

# ----------- SIDEBAR -----------
st.sidebar.markdown("## 🏗 Earthworks")
st.sidebar.caption("Kaevetööde kalkulaator")
st.sidebar.divider()

page = st.sidebar.radio(
    "",
    [
        "📁 Projects",
        "📐 Volumes",
        "🚜 Machines",
        "👷‍♂️ Workers",
        "📊 Reports",
        "⚙️ Settings"
    ]
)

st.sidebar.divider()
st.sidebar.caption("v0.1 • arenduses")

# ----------- PAGES -----------
if page == "📁 Projects":
    st.title("Projects")
    st.write("Projektide loetelu ja haldus.")
    st.info("Siia tulevad projektid ja objektid.")

elif page == "📐 Volumes":
    st.title("Volumes")
    st.write("Kaevemahtude arvutused (Excel / LandXML).")
    st.warning("Lisame järgmise sammuna.")

elif page == "🚜 Machines":
    st.title("Machines")
    st.write("Masinate tunnihinnad ja tootlikkused.")
    st.warning("Lisame järgmise sammuna.")

elif page == "👷‍♂️ Workers":
    st.title("Workers")
    st.write("Tööjõu planeerimine.")
    st.warning("Lisame järgmise sammuna.")
    
elif page == "📊 Reports":
    st.title("Reports")
    st.write("Aruanded ja ekspordid (Excel / PDF).")
    st.warning("Lisame järgmise sammuna.")

elif page == "⚙️ Settings":
    st.title("Settings")
    st.write("Rakenduse seaded ja vaikimisi koefitsiendid.")
