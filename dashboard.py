import streamlit as st
import plotly.express as px
import pandas as pd 
import numpy as np
from streamlit_extras.app_logo import add_logo
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_folium import st_folium
import folium
import pydeck as pdk
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="CS & PS Traffic", page_icon=":chart_with_upwards_trend:", layout="wide")
st.header(":chart_with_upwards_trend: Traffic Analysis")

st.markdown('<style>div.block-container{padding-top:4rem;}</style>',unsafe_allow_html=True)

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
df_metrics = pd.read_excel(df,'Metrics')


#------  Beggining of the side bar section -------#
#--- sidebar logo ----
st.sidebar.image("image/zain.png", use_column_width=True)

#filter the data based on region
st.sidebar.header("Please Filter Here: ")
region = st.sidebar.multiselect("Pick your Region:", options= df_kqi["Region"].unique(), default=df_kqi["Region"].unique())
technology = st.sidebar.multiselect("Pick your technology:", options= df_kqi["rat"].unique(), default=df_kqi["rat"].unique())

df_selection = df_kqi.query(
    "Region == @region & rat == @technology"
)

#----- The End of the sidebar section -------

#------ Begining of the metrics section -------
st.subheader("KQI & QOE Metrics")
QOE1New = df_metrics['Global'].tail(7).mean()
QOE1Previous = df_metrics['Global'].head(7).mean()
QOE1Delta = "{:.2%}".format((QOE1New - QOE1Previous)/QOE1Previous)

QOE2New = df_metrics['Data'].tail(7).mean()
QOE2Previous = df_metrics['Data'].head(7).mean()
QOE2Delta = "{:.2%}".format((QOE2New - QOE2Previous)/QOE2Previous)

KQI1New = df_metrics['PCSSR'].tail(7).mean()
KQI1Previous = df_metrics['PCSSR'].head(7).mean()
KQI1Delta = "{:.2%}".format((KQI1New - KQI1Previous)/KQI1Previous)

KQI2New = df_metrics['PCDR'].tail(7).mean()
KQI2Previous = df_metrics['PCDR'].head(7).mean()
KQI2Delta = "{:.2%}".format((KQI2New - KQI2Previous)/KQI2Previous)

KQI3New = df_metrics['E2E'].tail(7).mean()
KQI3Previous = df_metrics['E2E'].head(7).mean()
KQI3Delta = "{:.2%}".format((KQI3New - KQI3Previous)/KQI3Previous)

QOE1 , QOE2, KQI1, KQI2, KQI3 = st.columns(5)
QOE1.metric(
    label= "**Global QOE**",
    value= round(QOE1New, 2),
    delta= QOE1Delta,
    delta_color="normal")

QOE2.metric(
    label= "**Data QOE**",
    value= round(QOE2New, 2),
    delta= QOE2Delta,
    delta_color="normal")


KQI1.metric(
    label= "**PCSSR %**",
    value= round(KQI1New, 2),
    delta= KQI1Delta,
    delta_color="normal")

KQI2.metric(
    label= "**PCDR %**",
    value= round(KQI2New, 2),
    delta= KQI2Delta,
    delta_color="inverse")

KQI3.metric(
    label= "**E2E Delay**",
    value= round(KQI3New, 2),
    delta= KQI3Delta,
    delta_color="inverse")

#styling metrics
style_metric_cards(background_color="#0b0217", border_left_color="#d8d3e0",border_color="#c8d7f7")
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 29px;
}
</style>
""",
    unsafe_allow_html=True,
)

#------ End of the metrics section -------

# -----  Beginning of KQIs per region section ------
st.subheader("KQI Analysis per Region", divider='violet')
col1, col2 = st.columns((2))
df_kqi["MYDAY"] = pd.to_datetime(df_kqi["MYDAY"])

#getting the min and max date 
startDate = pd.to_datetime(df_kqi["MYDAY"]).min()
endDate = pd.to_datetime(df_kqi["MYDAY"]).max() 
#filter the data based on date
with col1:
    date1 = pd.to_datetime(st.date_input("Start date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End date", endDate))

df_kqi = df_kqi[(df_kqi["MYDAY"] >= date1) & (df_kqi["MYDAY"]<= date2)].copy()

st.markdown("---")


#KQIs per Regions bar graph 
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

st.markdown("---")
# ----- Ending of KQI Analysis Per Region Section ------


#-----Beginning of Voice Traffic Analysis Section -------
st.header("Voice & Data Traffic per Region", divider='violet')

st.subheader("Please Filter Here: ")
#Date Filter
CScol1, CScol2 = st.columns((2))
df_cs["Day_time"] = pd.to_datetime(df_cs["Day_time"])
#getting the min and max date 
startDateCS = pd.to_datetime(df_cs["Day_time"]).min()
endDateCS = pd.to_datetime(df_cs["Day_time"]).max() 
#filter the data based on date
with CScol1:
    CSdate1 = pd.to_datetime(st.date_input("Start date", startDateCS, key="CSStart"))
with CScol2:
    CSdate2 = pd.to_datetime(st.date_input("End date", endDateCS, key="CSEnd"))

df_cs = df_cs[(df_cs["Day_time"] >= date1) & (df_cs["Day_time"]<= date2)].copy()


#filter the data based on region and rat

region_CS = st.multiselect("Pick your Region:", options= df_cs["Region"].unique(), default=df_cs["Region"].unique(), key="CSRegion")
technology_CS = st.multiselect("Pick your technology:", options= df_cs["accesstype"].unique(), default=df_cs["accesstype"].unique(), key="CSRat")

df_selection_CS = df_cs.query(
    "Region == @region_CS & accesstype == @technology_CS"
)
st.markdown("---")

#Average traffic
average_CS = round(df_selection_CS["Traffic_Erl"].mean(), 1)
st.subheader("Average of Voice Traffic:")
st.subheader(f" {average_CS:,}")
st.markdown('##')
st.markdown('##')


#Trend through time analysis
df_selection_CS["Month_Day"] = df_selection_CS["Day_time"].dt.to_period("D")
st.subheader("Voice Traffic Trend")

linechart_CS = pd.DataFrame(df_selection_CS.groupby(df_selection_CS["Month_Day"].dt.strftime("%D : %b"))["Traffic_Erl"].sum()).reset_index()
CS_trend_fig = px.line(linechart_CS, x="Month_Day", y="Traffic_Erl", labels = {"Traffic_Erl": "Amount"}, height=500, width=1000, template="gridon")
st.plotly_chart(CS_trend_fig, use_container_width=True)

st.markdown('##')
st.markdown('##')
#Graphs Section
left_column_CS, right_column_CS = st.columns((2))
#Voice per Regions bar graph 
with left_column_CS:
    regions_by_CS = df_selection_CS.groupby(by=["Region"])["Traffic_Erl"].sum()
    fig_CS_region = px.bar(
        regions_by_CS,
        x = regions_by_CS.index,
        y = "Traffic_Erl",
        title="<b>Voice Traffic per Regions</b>",
        color_discrete_sequence=["#0083B8"] * len(regions_by_CS),
        template= "plotly_white",
        )
    fig_CS_region.update_layout(
        xaxis = dict(tickmode= "linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False)
        )
    st.plotly_chart(fig_CS_region,use_container_width=True)

#Voice traffic per rat
with right_column_CS:
    fig_Voice_rat = px.pie(df_selection_CS, values="Traffic_Erl", names="accesstype", hole=0.5, title="<b>Voice Traffic per technology</b>")
    fig_Voice_rat.update_traces(text= df_selection_CS["accesstype"], textposition = "outside")
    st.plotly_chart(fig_Voice_rat, use_container_width=True)

#Map Section
#fig = px.scatter_geo(
 #   data_frame=df_selection_CS,
  #  color="Region",
   # lon="longitude",
    #lat="latitude",
    #scope= "africa",
    #fitbounds='locations',
    #hover_name="Region",
    #size="Traffic_Erl",  # <-- Set the column name for size
    #height=800,
#)

#st.plotly_chart(fig, use_container_width=True)


#another map

#map_df = pd.read_excel(df,'cs per region',usecols=['Region','latitude','longitude'])
#point_size = df_selection_CS.groupby(by=['Region'])['Traffic_Erl'].sum().round(10)
#map_df["point_size"]=point_size
#st.map(map_df, color="#800080", size="point_size", use_container_width=True)
#print(point_size)
#----- Ending of Voice Traffic Analysis Section -------