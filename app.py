#Building the Python charts in python file
from js import Plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyodide.http import open_url
from pyscript import display, document
import warnings
warnings.filterwarnings("ignore") 

#Serve the data through an external server (Github), use open_url method 
#provided by Pyodide
url = "https://raw.githubusercontent.com/DisephD/Pyscript-Dashboad/main/data/water_data_processed%20(1).csv"

water_data = pd.read_csv(open_url(url), parse_dates=["Date"])

#create a html representation of a plotly graph
#using Plotly method from the JS module
def plotly_to_json (fig, target_id): 
    chart_json = fig.to_json()
    Plotly.newPlot (target_id, JSON.parse(chart_json))

#creating line chart python graph
def line_chart (filtered_df):

    daily_total = filtered_df.groupby("Day")["Score"].sum().reset_index()
    
    fig = px.line(daily_total, x="Day", y="Score", height=270, width= 670, markers=True)
    fig.update_traces (marker_size = 6, texttemplate='%{text:.2s}', line_color= "#4587D9")
    fig.update_layout(plot_bgcolor="rgb(254,254,254)", margin=dict(t=50,l=10,b=5,r=10), 
                      title= "Daily Trend", title_font_family ="Times New Roman Black", 
                      title_font_size = 17, title_x = 0.01, xaxis_tickfont_size=11,
                      yaxis=dict( title=None, titlefont_size=14, tickfont_size=11, tickfont_color= "#A9A9AB", ),
                      xaxis = dict(title=None, tickfont_size =11,  tickfont_color= "#A9A9AB"),
                      )
    
    fig.add_hline(y=2000, line_width=1,  line_dash="dash", line_color="#bbd9fe")
    plotly_to_json (fig, "line_chart")

#creating bar chart template/outline 
def table_chart (filtered_df):

    table_daily_total = filtered_df.groupby("Date")["Water(ml)"].sum().reset_index()
    table_daily_total["Daily_Change"] = table_daily_total["Water(ml)"].pct_change().mul(100).round(1).fillna(0).apply(lambda x: f"+{x}" if x > 0 else str(x)) + "%"
    table_daily_total["Daily_Change"] = table_daily_total["Daily_Change"].astype("category")
    
    font_color = ["#333131", "#333131",
                  ["#8DE28D" if "+" in x else "#FE5555" if "-" in x else "#333131" for x in list(table_daily_total["Daily_Change"])]]
    table_daily_total["Date"] = table_daily_total["Date"].astype("str")
    fig= go.Figure(data=[go.Table (columnwidth = [12, 10, 10],
                                    header=dict(values=list(table_daily_total.columns, ),
                                                 fill_color='white', align=['left', "left", "left"], 
                                                height=45,font=dict(size=17, color= "black"),
                                                line_color= "rgb(231, 239, 250)",), 
                                    cells=dict(values=[table_daily_total["Date"], table_daily_total["Water(ml)"],
                                                        table_daily_total["Daily_Change"]],
                                                fill_color='white', line_color= "rgb(231, 239, 250)", 
                                                align=['left',"left","left"],
                                                height=45, font=dict(size=15, color= font_color)))
                                    ])
    fig.layout.width= 670
    fig.update_layout(plot_bgcolor="rgb(254,254,254)",height= 270, margin=dict(t=5,l=10,b=10,r=10),)
    plotly_to_json (fig, "table")
    return table_daily_total