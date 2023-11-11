import streamlit as st
import pandas as pd

demo_df: pd.DataFrame = pd.read_csv('../out/cpool.out', delim_whitespace=True)
demo_df = demo_df.rename(columns={"Lon": "lon", "Lat": "lat"}, errors="raise")

st.title('LPJ-GUESS')
st.markdown("""
            You are viewing the results of the last run of LPJ-GUESS. Browse the different outputs in the side bar.

            The grid cell locations used in the last run of LPJ-GUESS:
            """)
# st.sidebar.title("Home")
st.map(demo_df, zoom=3)