import streamlit as st
import plotly.express as px
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="CS & PS Traffic", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title(":chart_with_upwards_trend: Traffic Analysis")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#fl = st.file_uploader(":file_folder: upload a file", type=(["csv","txt","xlsx", "xls"]))
#if fl is not None:
    #filename = fl.name
    #st.write(filename)
    #df = pd.read_excel(filename)
#else:
    #os.chdir(r"C:\Users\r.daffa\Desktop\Dashboard Web")
    #df=pd.read_excel("traffic.xlsx")

df = pd.ExcelFile("traffic.xlsx")
df_kqi = pd.read_excel(df,'cs kqi per region')
df_cs = pd.read_excel(df,'cs per region')
df_ps = pd.read_excel(df,'ps per region')

col1, col2 = st.columns((2))
df_kqi["MYDAY"] = pd.to_datetime(df_kqi["MYDAY"])

#gettimg the min and max date 

startDate = pd.to_datetime(df_kqi["MYDAY"]).min()
endDate = pd.to_datetime(df_kqi["MYDAY"]).max() 


#filter the data based on date
with col1:
    date1 = pd.to_datetime(st.date_input("Start date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End date", endDate))

df_kqi = df_kqi[(df_kqi["MYDAY"] >= date1) & (df_kqi["MYDAY"]<= date2)].copy()


#filter the data based on region
st.sidebar.header("Please Filter Here: ")
region = st.sidebar.multiselect("Pick your Region:", options= df_kqi["Region"].unique(), default=df_kqi["Region"].unique())
technology = st.sidebar.multiselect("Pick your technology:", options= df_kqi["rat"].unique(), default=df_kqi["rat"].unique())

df_selection = df_kqi.query(
    "Region == @region & rat == @technology"
)




# --------- Main Page ---------#

#Average traffic section
average_CS = round(df_cs["Traffic_Erl"].mean(), 1)
average_PS = round(df_ps["Traffic_GB"].mean(), 1)

left_col, right_col = st.columns(2)
with left_col:
    st.subheader("Average of Voice Traffic:")
    st.subheader(f" {average_CS:,}")
with right_col:
    st.subheader("Average of Data Traffic:")
    st.subheader(f"{average_PS:,}")

st.markdown("---")


#KQIs per Regions 
regions_by_pcsr = df_selection.groupby(by=["Region"])["pcsr"].mean()
fig_pcsr_region = px.bar(
    regions_by_pcsr,
    x = regions_by_pcsr.index,
    y = "pcsr",
    title="<b>Regions per PCSSR</b>",
    color_discrete_sequence=["#0083B8"] * len(regions_by_pcsr),
    template= "plotly_white",
)
fig_pcsr_region.update_layout(
    xaxis = dict(tickmode= "linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)

regions_by_pcdr = df_selection.groupby(by=["Region"])["pcdr"].mean()
fig_pcdr_region = px.bar(
    regions_by_pcdr,
    x = regions_by_pcdr.index,
    y = "pcdr",
    title="<b>Regions per PCDR</b>",
    color_discrete_sequence=["#0083B8"] * len(regions_by_pcdr),
    template= "plotly_white",
)
fig_pcdr_region.update_layout(
    xaxis = dict(tickmode= "linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pcsr_region)
right_column.plotly_chart(fig_pcdr_region)

regions_by_e2e = (
    df_selection.groupby(by=["Region"])["e2edelayms"].mean().sort_values()
)
fig_e2e_region = px.bar(
    regions_by_e2e,
    x="e2edelayms",
    y=regions_by_e2e.index,
    orientation="h",
    title="<b>Regions per E2E Delay</b>",
    color_discrete_sequence=["#0083B8"] * len(regions_by_e2e),
    template="plotly_white",
)

st.plotly_chart(fig_e2e_region)




#if not region:
    #df2 = df.copy()
#else: 
    #df2 = df[df["Region"].isin(region)]

#creating column chart

#rat_df = df2.groupby(by = ["rat"], as_index = False)["pcsr"].sum()

#with col1:
    #st.subheader("PCSSR per technology")
    #fig = px.bar(rat_df, x = "rat", y = "Pcssr", text = ['${:,.2f}'.format(x) for x in rat_df["pcsr"]],
                #template= "seaborn " )
    #st.plotly_chart(fig, use_container_width=True, height = 200)

#creating pie chart

#with col2: 
    #st.subheader("Region per technology")
    #fig = px.pie(df2, values= "technology", names="Region", hole =0.5)
    #fig.update_traces(text = df2["Region"], textposition = "outside")
    #st.plotly_chart(fig, use_container_width=True )