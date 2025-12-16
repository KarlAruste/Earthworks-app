import streamlit as st

st.set_page_config(
    page_title="Earthworks App",
    layout="wide"
)

st.title("Earthworks App")
st.subheader("Kaevetööde ja masinate kalkulatsioonid")

st.markdown("""
Tere tulemast!

See veebirakendus on mõeldud:
- kaevetööde mahtude arvutamiseks
- masinate tootlikkuse ja hindade võrdlemiseks
- erinevate tööstsenaariumite analüüsiks

🚧 Rakendus on arenduses.
Siia lisanduvad peagi:
- projektide üleslaadimine
- LandXML mahuarvutused
- masinate hinnakirjad
- aruannete eksport
""")

st.divider()

st.info("See on avaleht. Funktsioonid lisanduvad järk-järgult.")
