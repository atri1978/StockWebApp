from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from forms import *
from models import *
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import os 
from bs4 import BeautifulSoup
from decimal import Decimal

def addDataStock(stock, shares, username):
    check_data = Stock.query.filter(Stock.username == username,
                                    Stock.stock == stock).first()
    
    if check_data:    
        org_shares = db.session.query(Stock.numShares).filter_by(stock=stock).first()   
        fixed_shares = org_shares._data[0]
        new_shares = shares+fixed_shares
        check_data.numShares = new_shares
        db.session.commit()

    else: 
        new_data = Stock(username = username, 
                        stock = stock, 
                        numShares = shares)
        db.session.add(new_data)
        db.session.commit()
    
def addDataUser(username, stock, shares):
    check_record = UserPortfolio.query.filter(UserPortfolio.username == username).first()
    
    data = getData(stock)
    current_value = dataframeAnalysis(data)["currentVal"]
    current_value = float(current_value)
    total = Decimal(shares*current_value)
    money_left = Decimal(100000-total)
    
    
    if check_record:
        check_money = db.session.query(UserPortfolio.moneyLeft).filter(UserPortfolio.username == username).first()._data[0]
        
        check_record.moneyLeft = Decimal(check_money-total)
        check_record.profit = 0    
        db.session.commit()    

    else:
        new_record = UserPortfolio(username=username, 
                                   profit = 0, 
                                   moneyLeft = money_left)
        db.session.add(new_record)
        db.session.commit()
        

def sellDataStock(stock, shares, username):
    org_stock = Stock.query.filter(Stock.username == username,
                                   Stock.stock == stock).first()
    
    org_shares = org_stock.numShares

    new_shares = org_shares-shares

    org_stock.numShares = new_shares

    db.session.commit()

def sellDataUser(username, stock, shares):
    org_record = UserPortfolio.query.filter(UserPortfolio.username == username).first()
    check_money = db.session.query(UserPortfolio.moneyLeft).filter(UserPortfolio.username == username).first()._data[0]


    data = getData(stock)
    current_value = dataframeAnalysis(data)["currentVal"]
    current_value = Decimal(current_value)
    total = Decimal(shares*current_value)
    money_left = Decimal(check_money+total)
    profit = money_left-100000

    org_record.moneyLeft = money_left
    org_record.profit = profit


    db.session.commit()
    

    


def checkUser(username):
    user = User.query.filter_by(username=username).first()
    check_user = user.username
    
    if check_user == username:
        return True
    
    else:
        return False

def addUser(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()


def authUser(username, password):
    user = User.query.filter_by(username=username,
                                password=password).first()
    return user
    

def get_news(stock_symbol = "AAPL"):
        url = "https://www.google.com/finance/quote/" + stock_symbol + ":NASDAQ?sa=X&ved=2ahUKEwjBtsnSya77AhVQtaQKHcuHCjsQ_AUoAXoECAIQAw"
        grab = requests.get(url)
        soup = BeautifulSoup(grab.text, 'lxml')
        urls = []
        for link in soup.find_all('a'):
            a = link.get('href')
            a = str(a)
            urls.append(a)

        fixed_url = []
        for i in urls:  
            if i[0] == "h":
                fixed_url.append(i)
        
        for i in fixed_url:
            if "google" in i:
                fixed_url.remove(i)

        return fixed_url[1:9]

def get_newsStock(stock_symbol = "AAPL"):
        url = "https://www.google.com/finance/quote/" + stock_symbol + ":NASDAQ?sa=X&ved=2ahUKEwjBtsnSya77AhVQtaQKHcuHCjsQ_AUoAXoECAIQAw"
        grab = requests.get(url)
        soup = BeautifulSoup(grab.text, 'lxml')
        urls = []
        for link in soup.find_all('a'):
            a = link.get('href')
            a = str(a)
            urls.append(a)

        fixed_url = []
        for i in urls:  
            if i[0] == "h":
                fixed_url.append(i)
        
        for i in fixed_url:
            if "google" in i:
                fixed_url.remove(i)

        return fixed_url[1:4]


def getData(sym):
    
    URL = "https://api.twelvedata.com/time_series?apikey=6a43140c51e34f48b80f612b22ed7c6a&interval=1min&format=JSON"
    TEST_URL = "https://api.twelvedata.com/time_series?apikey=6a43140c51e34f48b80f612b22ed7c6a&interval=1min&start_date=2023-08-11 09:00:00&end_date=2023-08-11 16:00:00&format=JSON&symbol=AAPL&exchange=NASDAQ&type=stock"

    
    # testStart = "2023-07-25 09:30:00"
    # testEnd =  "2023-07-25 15:59:00"
    start_date = str(datetime.now().date()) + " 09:30:00"
    end_date = str(datetime.now().date()) + " 15:59:00"
    current_date = str(datetime.now().date())
    current_time = datetime.now().strftime("%H:%M:%S")


    parameters = {
            "exchange": "NASDAQ",
            "symbol": sym,
            "start_date": start_date,
            "end_date": end_date,
            "type": "stock"
        }
    
    response = requests.get(url=URL, params= parameters)
    data  =  response.json()["values"]
    return data

    # TEST_response = requests.get(url=TEST_URL)
    # TEST_data = TEST_response.json()["values"]
    # return TEST_data

def weekData(sym):
    URL = "https://api.twelvedata.com/time_series?apikey=6a43140c51e34f48b80f612b22ed7c6a&interval=1min&format=JSON"
    TEST_URL = "https://api.twelvedata.com/time_series?apikey=6a43140c51e34f48b80f612b22ed7c6a&interval=1min&start_date=2023-08-11 09:00:00&end_date=2023-08-11 16:00:00&format=JSON&symbol=AAPL&exchange=NASDAQ&type=stock"
    
   

    start_date = str(timedelta(-7) + datetime.now().date())
    current_date = str(datetime.now().date())
    current_time = datetime.now().strftime("%H:%M:%S")
    end_date = current_date + " " + current_time


    parameters = {
            "exchange": "NASDAQ",
            "symbol": sym,
            "start_date": start_date,
            "end_date": end_date,
            "type": "stock"
        }
    
    response = requests.get(url=URL, params= parameters)
    data  =  response.json()["values"]

    # TEST_response = requests.get(url=TEST_URL)
    # TEST_data = TEST_response.json()["values"]

    return data


def dataframeAnalysis(data):
    df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
    firstValIndex = len(df) - 1
    max = df["open"].max()
    min = df["open"].min()
    newValIndex = df["open"][0]
    firstVal = df["open"][firstValIndex]

    change = (float(newValIndex) - float(firstVal)) / float(firstVal)

    percentChange = round(change * 100, 2)
    analysis = {"max":max, "min":min, "percentChange":percentChange,
                "currentVal": newValIndex,
                "intialVal": firstVal}
    return analysis


def createGraph(sym):
    data = getData(sym)
    df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
    time_index = df["datetime"]

    new_df = pd.DataFrame(data, index = time_index, columns=["open"])
    x = new_df.index
    y = new_df["open"]

# Create a line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))

# Add labels and title
    fig.update_layout(
    title='Line Chart',
    xaxis=dict(title='X-axis'),
    yaxis=dict(title='Y-axis')
)

# Display the chart
    if os.path.isfile("templates/dayGraph.html"):
        os.remove("templates/dayGraph.html")

    
    fig.write_html("templates/dayGraph.html")


def createGraphstock1(sym):
    data = getData(sym)
    df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
    time_index = df["datetime"]

    new_df = pd.DataFrame(data, index = time_index, columns=["open"])
    x = new_df.index
    y = new_df["open"]

# Create a line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))

# Add labels and title
    fig.update_layout(
    title='Line Chart',
    xaxis=dict(title='X-axis'),
    yaxis=dict(title='Y-axis')
)

# Display the chart
    if os.path.isfile("templates/stock1Graph.html"):
        os.remove("templates/stock1Graph.html")

    
    fig.write_html("templates/stock1Graph.html")


def createGraphstock2(sym):
    data = getData(sym)
    df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
    time_index = df["datetime"]

    new_df = pd.DataFrame(data, index = time_index, columns=["open"])
    x = new_df.index
    y = new_df["open"]

# Create a line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))

# Add labels and title
    fig.update_layout(
    title='Line Chart',
    xaxis=dict(title='X-axis'),
    yaxis=dict(title='Y-axis')
)

# Display the chart
    if os.path.isfile("templates/stock2Graph.html"):
        os.remove("templates/stock2Graph.html")

    
    fig.write_html("templates/stock2Graph.html")



def createGraphstock3(sym):
    data = getData(sym)
    df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
    time_index = df["datetime"]

    new_df = pd.DataFrame(data, index = time_index, columns=["open"])
    x = new_df.index
    y = new_df["open"]

# Create a line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))

# Add labels and title
    fig.update_layout(
    title='Line Chart',
    xaxis=dict(title='X-axis'),
    yaxis=dict(title='Y-axis')
)

# Display the chart
    if os.path.isfile("templates/stock3Graph.html"):
        os.remove("templates/stock3Graph.html")

    
    fig.write_html("templates/stock3Graph.html")

def weekGraph(sym):
    data = weekData(sym)
    df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume"])
    time_index = df["datetime"]


    new_df = pd.DataFrame(data, index = time_index, columns=["open"])
    x = new_df.index
    y = new_df["open"]

# Create a line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))

# Add labels and title
    fig.update_layout(
    title='Line Chart',
    xaxis=dict(title='X-axis'),
    yaxis=dict(title='Y-axis')
)

# Display the chart
    if os.path.isfile("templates/weekGraph.html"):
        os.remove("templates/weekGraph.html")

    
    fig.write_html("templates/weekGraph.html")


 