import streamlit as st
import pandas as pd

df_gridlist = pd.read_csv('../runs/gridlist.txt', delimiter='\t', header=None, names=['lon', 'lat', 'Place', 'Category'])

st.title('LPJ-GUESS')
st.markdown("""
            You are viewing the results of the last run of LPJ-GUESS. Browse the different outputs in the side bar.
            """)
st.header('Gridcell locations')

st.map(df_gridlist, zoom=2)