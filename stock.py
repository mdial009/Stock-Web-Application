# Description: This is a stock market dashboard to show some charts and data on some stock

# Import Libraries
import streamlit as st
import pandas as pd
import time
from PIL import Image

# Configs for streamlit
st.beta_set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Toggle for the ballons
agree = st.checkbox("Toggle Me :)")
if agree:
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Loading {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    with st.spinner("Wait for it..."):
        time.sleep(3)
        st.balloons()

# Check box for formatting of the input
option = st.sidebar.checkbox("Click me to see your input options")
if option:
    thestocksymbols = st.sidebar.selectbox("These are your options for stock symbol:", [
        "AAPL", "GOOG", "AMZN", "TSLA"])
    stocksdates = st.sidebar.markdown("Format = YEAR-MONTH-DAY")


# Add a title and an Image
st.write("""
# Stock Market Web Application
**Visually** show data on a stock!
""")

image = Image.open(
    "/Users/madanydiallo/Desktop/Python/StockMarket/Stockpic.jpeg")
st.image(image, use_column_width=True)

# Create a sidebar header
st.sidebar.header("User Input")

# Create a function to get the users input


def get_input():
    start_date = st.sidebar.text_input("Start Date", "")
    end_date = st.sidebar.text_input("End Date", "")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol

# Create a function to get a company name
def get_company_name(symbol):
    if symbol == "AMZN":
        return "Amazon"
    elif symbol == "AAPL":
        return "Apple"
    elif symbol == "TSLA":
        return "Tesla"
    elif symbol == "GOOG":
        return "Google"
    else:
        "None"

# Create a function to get the proper company data and the proper timeframe from the user start date to the user end date
def get_data(symbol, start, end):
    # Load the data
    if symbol.upper() == "AMZN":
        df = pd.read_csv(
            "/Users/madanydiallo/Desktop/Python/StockMarket/AMZN.csv")
    elif symbol.upper() == "AAPL":
        df = pd.read_csv(
            "/Users/madanydiallo/Desktop/Python/StockMarket/AAPL.csv")
    elif symbol.upper() == "GOOG":
        df = pd.read_csv(
            "/Users/madanydiallo/Desktop/Python/StockMarket/GOOG.csv")
    elif symbol.upper() == "TSLA":
        df = pd.read_csv(
            "/Users/madanydiallo/Desktop/Python/StockMarket/TSLA.csv")
    else:
        df = pd.DataFrame(
            columns=["Date", 'Close', "Open", "Volume", "Adj  Close", "High", "Low"])


# Get the date range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    # Set the start and end index rows both to 0
    start_row = 0
    end_row = 0

    # Start the date from the top of the data set and go down to see if the user start date is less then or equal to the date in the date set
    for i in range(0, len(df)):
        if start <= pd.to_datetime(df["Date"][i]):
            start_row = i
            break
        # Start from the bottom of the dataset and go up to see if the users end date is greater then or equal to the date in the date set
    for j in range(0, len(df)):
        if end >= pd.to_datetime(df["Date"][len(df)-1-j]):
            end_row = len(df) - 1 - j
            break

        # Set the index to be the date
    df = df.set_index(pd.DatetimeIndex(df["Date"].values))

    return df.iloc[start_row:end_row + 1, :]


# Get the users input
start, end, symbol = get_input()
# Get the data
df = get_data(symbol, start, end)
# Get the company name
company_name = get_company_name(symbol.upper())

# Display the close price
st.header(company_name+" Close Price\n")
st.line_chart(df["Close"])

# Display the close price
st.header(company_name+" Volume\n")
st.line_chart(df["Volume"])

# Get the statistics
st.header("Data Statistics")
st.write(df.describe())
