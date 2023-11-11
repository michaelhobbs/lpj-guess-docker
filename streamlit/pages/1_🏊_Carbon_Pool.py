import streamlit as st
import pandas as pd
import altair as alt

demo_df: pd.DataFrame = pd.read_csv('../out/cpool.out', delim_whitespace=True)
demo_df = demo_df.rename(columns={"Lon": "lon", "Lat": "lat"}, errors="raise")

st.title('Carbon Pool')
st.markdown("""
            The carbon pool is composed of:
            - `VegC`: Carbon contained in living vegetation
            - `LitterC`: Carbon found in litter, such as dead leaves
            - `SoilC`: Carbon found in the soil, eg: once litter has been processed by worms
            """)
st.sidebar.markdown("# 🏊 Carbon Pool")
# st.bar_chart(demo_df[['VegC', 'LitterC', 'SoilC']])
chart = (
    alt.Chart(demo_df[['Year', 'SoilC', 'LitterC', 'VegC']].melt('Year', var_name='Type', value_name='Amount'))
    .mark_area(opacity=0.3)
    .encode(
        x="Year:Q",
        y=alt.Y("Amount:Q", stack=None).title("Amount (kg/m$^{2}$)"),
        color="Type:N",
        tooltip=["Year", "Amount", "Type"]
    )
)
st.altair_chart(chart, use_container_width=True)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(demo_df)