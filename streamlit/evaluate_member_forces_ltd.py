import streamlit as st
import pandas as pd

''' 
# Evaluate Load Take Down
This App enables you to evaluate column and wall forces exported from an analysis with
SOFiSTiK in Revit. The *.csv file to be uploaded should contain at least the following columns:
["Member", "Level", "Load Case", "Normal Force"]
'''

# read data
uploaded_file = st.file_uploader("Upload *.csv file:")
if uploaded_file is None:
    quit()

df = pd.read_csv(uploaded_file, sep=';')

# print imported data
st.write("Imported Data:")
st.dataframe(df,height=300)


'''
### Sum of Forces per Level
As a first check we calculate the sum of the resulting normal forces for each level and for
a selected load case.
'''

load_cases = df["Load Case"].drop_duplicates().values
lc_selected = st.selectbox("Select Load Case:", load_cases)

normal_forces_grouped = df[df["Load Case"]==lc_selected].groupby(["Level"])["Normal Force"].sum()
st.dataframe(normal_forces_grouped)

st.bar_chart(normal_forces_grouped, y="Normal Force", height=300)

'''
### Development of Member Forces along Levels
Using Pivot-Tables in Pandas, we now re-organize the data, that for each member the development
of the forces is displayed along the levels. This requires, that in the given *.csv file, vertically
staggered members should have received the same member name. Though multiple members may share
the same name then, they are still uniquely identifiable using their level.
'''

lc_selected = st.selectbox("Select Load Case:", load_cases, key="Second Selection")

df_selected = df[df["Load Case"]==lc_selected] # filter lc 1
members_per_level = df_selected.pivot(index="Member",columns="Level",values="Normal Force")

st.dataframe(members_per_level)
st.write(f"Development of member forces along levels. Load case: {lc_selected}")
