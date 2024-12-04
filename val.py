# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Yahoo Finance에서 제공하는 US Treasury rates의 티커
tickers = {
    '3M': '^IRX',       # 3개월
    '6M': '^FVX',       # 6개월
    '1Y': '^IR1TIBOR',  # 1년
    '2Y': '^IR2TIBOR',  # 2년
    '5Y': '^FVX',       # 5년
    '10Y': '^TNX',      # 10년
    '30Y': '^TYX'       # 30년
}

# 각 티커에 대해 최신 금리 데이터를 가져옴
rates = {}
for maturity, ticker in tickers.items():
    data = yf.Ticker(ticker).history(period='1d')
    if not data.empty:
        rates[maturity] = data['Close'].iloc[-1]
    else:
        print(f"데이터를 가져올 수 없습니다: {ticker}")

# 데이터프레임으로 변환
df = pd.DataFrame(list(rates.items()), columns=['Maturity', 'Rate'])
df['Rate'] = df['Rate'].astype(float)

# 만기 순서에 따라 정렬
maturity_order = ['3M', '6M', '1Y', '2Y', '5Y', '10Y', '30Y']
df['Maturity'] = pd.Categorical(df['Maturity'], categories=maturity_order, ordered=True)
df = df.sort_values('Maturity')

# Term Structure 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(df['Maturity'], df['Rate'], marker='o', linestyle='-', color='b')
plt.title('US Treasury Rates Term Structure')
plt.xlabel('Maturity')
plt.ylabel('Rate (%)')
plt.grid(True)
plt.show()
