

import os
import sys
import json
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import streamlit as st

# Import Modules
parent_dir = os.path.join(os.getcwd(),"..")
sys.path.insert(0, parent_dir)
from semi_utils import sql_queries as sqlq
from semi_utils import backtests as bkt

engine = sqlq.get_sql_engine(os.path.join(os.getcwd(), '..', '..','data', 'semi.db'))
soxx = pd.read_sql('SELECT * FROM soxx', engine)

# Clean Up the Columns
soxx.columns = soxx.columns.str.lower()
soxx.drop(columns = ['high', 'low', 'dividends', 'stock splits', 'capital gains', 'volume'], inplace = True)
soxx['date'] = pd.to_datetime(soxx['date']).dt.strftime('%Y-%m-%d')
soxx['date'] = pd.to_datetime(soxx['date'])

soxx = bkt.get_returns(soxx)





### KEY SECTION
# Run the streamlit part
# Streamlit app layout
st.title("MACD, Signal Line, and Total Return Dashboard")

# Date Range Slider
start_idx, end_idx = st.slider(
    "Select Date Range:",
    0, len(soxx) - 1, (0, len(soxx) - 1)
)

# Convert index selection to date filtering
filtered_soxx = soxx.iloc[start_idx:end_idx].copy()
filtered_soxx = bkt.get_returns(filtered_soxx)

# Series Toggle Checkboxes
show_macd = st.checkbox('Show MACD', value=True)
show_signal = st.checkbox('Show Signal Line', value=True)
show_raw_return = st.checkbox('Show Raw Total Return', value=True)
show_vol_control = st.checkbox('Show Vol Control Total Return', value=True)
show_vertical_lines = st.checkbox('Show Vertical Lines', value=True)

# Plotting the chart
# Plotting the chart
fig = go.Figure()

# Add traces based on checkboxes (same as before)
if show_macd:
    fig.add_trace(go.Scatter(
        x=filtered_soxx['date'], 
        y=filtered_soxx['macd'], 
        mode='lines', 
        name='MACD'
    ))

if show_signal:
    fig.add_trace(go.Scatter(
        x=filtered_soxx['date'], 
        y=filtered_soxx['signal'], 
        mode='lines', 
        name='Signal Line'
    ))

if show_raw_return:
    total_return_last = filtered_soxx['total_return'].iloc[-1]
    total_days = (filtered_soxx['date'].iloc[-1] - filtered_soxx['date'].iloc[0]).days
    years = total_days / 365.25 if total_days > 0 else 1
    tr_annualized = (total_return_last ** (1 / years) - 1) * 100
    
    fig.add_trace(go.Scatter(
        x=filtered_soxx['date'], 
        y=filtered_soxx['total_return'], 
        mode='lines', 
        name=f'Raw Total Return (Annualized: {tr_annualized:.2f}%)'
    ))

if show_vol_control:
    strategy_1_return_last = filtered_soxx['strategy_1_total_return'].iloc[-1]
    strategy_1_tr_annualized = (strategy_1_return_last ** (1 / years) - 1) * 100
    
    fig.add_trace(go.Scatter(
        x=filtered_soxx['date'], 
        y=filtered_soxx['strategy_1_total_return'], 
        mode='lines', 
        name=f'Vol Control Total Return (Annualized: {strategy_1_tr_annualized:.2f}%)'
    ))

# Add vertical lines based on checkbox (same as before)
if show_vertical_lines:
    trigger_changes = filtered_soxx['trigger'].diff().fillna(0)
    for i in range(1, len(filtered_soxx)):
        if trigger_changes.iloc[i] == -1:
            fig.add_shape(type='line', x0=filtered_soxx['date'].iloc[i], x1=filtered_soxx['date'].iloc[i],
                          y0=0, y1=1, yref='paper', line=dict(color='green', dash='dash'))
        elif trigger_changes.iloc[i] == 1:
            fig.add_shape(type='line', x0=filtered_soxx['date'].iloc[i], x1=filtered_soxx['date'].iloc[i],
                          y0=0, y1=1, yref='paper', line=dict(color='red', dash='dash'))

# Update the layout for a wider figure and move the legend below or above
fig.update_layout(
    title='MACD, Signal Line, and Total Return with Interactive Features',
    xaxis=dict(title='Date', rangeslider=dict(visible=True), type='date'),
    yaxis=dict(title='MACD / Signal Line'),
    yaxis2=dict(title='Total Return (%)', overlaying='y', side='right', tickformat='.0%'),
    
    # Increase the size of the figure (width and height)
    width=1200,  # Adjust this as per your preference
    height=600,

    # Move the legend below the chart
    legend=dict(
        orientation="h",  # Horizontal legend
        x=0,  # Align legend to the left
        y=1.6,  # Place legend below the chart (or set y=1.2 for above the chart)
        xanchor='left',
        yanchor='bottom',
        traceorder='normal'  # Keep traces in the order they are defined
    )
)

# Display Plotly chart in Streamlit
st.plotly_chart(fig)

