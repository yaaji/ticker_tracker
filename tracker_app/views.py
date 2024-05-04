from django.shortcuts import render, HttpResponse
import  yfinance as yf
import pandas as pd
from datetime import date, timedelta
import plotly.graph_objects as go
import json

def home(request):
    ticker = request.GET.get('ticker')    
    start = request.GET.get('start')
    end = request.GET.get('end')

    if ticker:
        
        if start == "":
            start = (date.today() - timedelta(days=360)).strftime("%Y-%m-%d")
            end = date.today().strftime("%Y-%m-%d")

        df = yf.download(tickers=ticker, interval='1d', start=start, end=end)

        data = []
        for index, row in df.iterrows():
            record = {}
            record['Date'] = index
            record['Open'] = row['Open']
            record['Close'] = row['Close']
            record['High'] = row['High']
            record['Low'] = row['Low']
            record['Volume'] = row['Volume']
            data.append(record)

        ticker_info =  yf.Ticker(ticker).info

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Open'], mode='lines',name='Open'))
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines',name='Close'))

        fig.update_xaxes(type='date')

        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(label='1y',step='year',count=1,stepmode='backward'),
                        dict(label='YTD',step='year',count=1,stepmode='todate'),
                        dict(label='6m',step='month',count=6,stepmode='backward'),
                        dict(label='1m',step='month',count=1,stepmode='backward'),
                        dict(label='1w',step='day',count=7,stepmode='backward')
                    ])
                ),
                rangeslider=dict(visible=True),
                type='date'
            )
        )

        json_string = json.dumps( fig.to_json() )

        return render(request=request, template_name='home.html', context={
            'ticker': ticker_info, 
            'data':data, 
            'start':start, 
            'end':end, 
            'graph':json_string})
    
    else:
        return render(request=request, template_name='home.html')
    