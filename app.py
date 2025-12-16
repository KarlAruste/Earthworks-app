import streamlit as st

st.set_page_config(page_title="Earthworks App", layout="wide")

# --- Sidebar menu ---
st.sidebar.title("Earthworks App")
page = st.sidebar.radio(
    "Menüü",
    ["Avaleht", "Mahukalkulaator", "Masinad", "Seaded"],
    index=0
)

st.sidebar.divider()
st.sidebar.caption("Versioon: 0.1 (arenduses)")

# --- Pages ---
if page == "Avaleht":
    st.title("Earthworks App")
    st.subheader("Kaevetööde ja masinate kalkulatsioonid")

    st.markdown("""
Tere tulemast!

See veebirakendus on mõeldud:
- kaevetööde mahtude arvutamiseks
- masinate tootlikkuse ja hindade võrdlemiseks
- erinevate tööstsenaariumite analüüsiks

🚧 Rakendus on arenduses. Siia lisanduvad peagi:
- projektide üleslaadimine
- LandXML mahuarvutused
- masinate hinnakirjad
- aruannete eksport
""")

    st.info("Vali vasakult menüüst järgmine moodul.")

elif page == "Mahukalkulaator":
    st.title("Mahukalkulaator")
    st.write("Siia tuleb mahu ja aja/hinna kalkulaator (Excel/CSV/LandXML upload).")
    st.warning("Placeholder – lisame funktsiooni järgmisena.")

elif page == "Masinad":
    st.title("Masinad")
    st.write("Siia tuleb masinate nimekiri, tunnihinnad, tootlikkused ja koefitsiendid.")
    st.warning("Placeholder – lisame funktsiooni järgmisena.")

elif page == "Seaded":
    st.title("Seaded")
    st.write("Siia saab hiljem panna ühikud, vaikimisi koefitsiendid, tööpäeva pikkuse jne.")
    st.warning("Placeholder – lisame funktsiooni järgmisena.")
