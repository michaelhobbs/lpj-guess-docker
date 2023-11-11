#%% imports
import streamlit as st
import pandas as pd
import altair as alt

#%% loading data
# Load the data from the files into pandas dataframes
df_cpool = pd.read_csv('../out/cpool.out', delim_whitespace=True)
df_gridlist = pd.read_csv('../runs/gridlist.txt', delimiter='\t', header=None, names=['Lon', 'Lat', 'Place', 'Category'])

# Creating a dictionary for mapping from gridlist.txt
mapping_dict = {(row['Lon'], row['Lat']): row['Place'] for index, row in df_gridlist.iterrows()}

# Function to map category based on Lon and Lat
def map_category(row):
    return mapping_dict.get((row['Lon'], row['Lat']))

# Applying the function to cpool dataframe
df_cpool['Place'] = df_cpool.apply(map_category, axis=1)

#%% creating page
st.title('Carbon Pool')
st.markdown("""
            The carbon pool is composed of:
            - `VegC`: Carbon contained in living vegetation
            - `LitterC`: Carbon found in litter, such as dead leaves
            - `SoilC`: Carbon found in the soil, eg: once litter has been processed by worms

            When comparing several gridcells, we use the `Total` carbon pool, sum of `VegC`, `LitterC` and `SoilC`.
            """)


st.header('Single Gridcell')
single = st.selectbox(
    'Gridcell to view composition',
    df_cpool['Place'].unique(),
    0)

single_df = df_cpool[df_cpool['Place'] == single]
chart = (
    alt.Chart(single_df[['Year', 'SoilC', 'LitterC', 'VegC']].melt('Year', var_name='Type', value_name='Amount'))
    .mark_area(opacity=0.3)
    .encode(
        x="Year:Q",
        y=alt.Y("Amount:Q", stack=None).title("Amount (kg/m$^{2}$)"),
        color="Type:N",
        tooltip=["Year", "Amount", "Type"]
    )
)
st.altair_chart(chart, use_container_width=True)


st.header('Multiple Gridcells')
#%% selection of gridcells to vizualize
options = st.multiselect(
    'Gridcells to view',
    df_cpool['Place'].unique(),
    None)


#%% lasagna plot
color_condition = alt.condition(
    'datum.value % 10 == 0',
    alt.value("white"),
    alt.value(None),
)
selected = df_cpool
if len(options) != 0:
    selected = df_cpool[df_cpool['Place'].isin(options)]
df_cpool = selected
lasagna = alt.Chart(df_cpool).mark_rect().encode(
    alt.X("Year:O").axis(
            labelAngle=0,
            labelOverlap=False,
            labelColor=color_condition,
            tickColor=color_condition,
        ),
    alt.Y("Place:N").title(None),
    alt.Color("Total:Q")
)
st.altair_chart(lasagna, use_container_width=True, theme=None)

#%% Plotting Total Cpool by place per year
# Create a common chart object
chart = alt.Chart(df_cpool, height=600).encode(
    alt.Color("Place").legend(orient='bottom', direction='vertical')
)

# Draw the line
line = chart.mark_line().encode(
    x="Year:Q",
    y="Total:Q"
)

# Use the `argmax` aggregate to limit the dataset to the final value
label = chart.encode(
    x='max(Year):Q',
    y=alt.Y('Total:Q').aggregate(argmax='Year'),
    text='Place'
)

# Create a text label
text = label.mark_text(align='left', dx=4)

# Create a circle annotation
circle = label.mark_circle()

# Draw the chart with all the layers combined
st.altair_chart(line + circle + text, use_container_width=True)

#%% Raw data
with st.expander('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df_cpool)