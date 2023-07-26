import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
import csv


data = pd.read_csv(r'C:\Users\Suman\Desktop\TCS.csv')

data.drop(data[data['Series'] == 'BL'].index, inplace = True) 

ind  = data.index[-1]-90

for i in range(ind,data.index[-1],1):
    max_p = data['Close Price'].max()
    min_p = data['Close Price'].min()
    mean_p = data['Close Price'].mean()
print('Max price for the last 90 Days: ',max_p)
print('Min price for the last 90 Days:', min_p)
print('Mean price for the last 90 Days: ', mean_p)
print("\n")


data['Date'] = pd.to_datetime(data['Date'])

data['Month'] = data['Date'].dt.strftime('%B') 

data['Year'] = pd.DatetimeIndex(data['Date']).year


#Pandas default index is int64 and to use groupby or resample we need to change the index
data.set_index(data['Date'], inplace = True)


group = data.groupby(['Month', 'Year'])


VWAP = []

for i,j in group:
    VWAP = np.sum(data['Close Price']* data['Total Traded Quantity'])/ np.sum(data['Total Traded Quantity'])
    #print(i, VWAP) 


def avg_price():
    N = int(input("Enter a number: "))
    mean = np.mean(data['Close Price'].tail(N))  
    print("The Average Price for last " + str(N) + " days: " + str(mean))
    print("\n")
    
avg_price() # N =7, 14, 30, 90, 180, 365


def percentage():
    N = int(input("Enter a number: "))
    difference = data.iloc[-1]['Close Price'] - data.iloc[-N]['Close Price']
    if difference < 0:
        loss = -(difference/data.iloc[-1]['Close Price'])*100
        print("The loss for last " + str(N) + " days: " + str(loss))
        print("\n")
    else:
        profit = (difference/data.iloc[-1]['Close Price'])*100
        print("The profit for last " + str(N) + " days: " + str(profit))
        print("\n")
        
percentage()  # N =7, 14, 30, 90, 180, 365


data['Day_Perc_Change'] = data['Close Price'].pct_change()
data = data.dropna()


def conditions(s):
    if (s['Day_Perc_Change'] > -0.5) and (s['Day_Perc_Change'] < 0.5) :
        return ('Slight or No Change')
    elif (s['Day_Perc_Change']> 0.5) and (s['Day_Perc_Change']<1) :
        return ('Slight Positive')
    elif (s['Day_Perc_Change'] < -0.5) and (s['Day_Perc_Change']>-1):
        return ('Slight Negative')
    elif (s['Day_Perc_Change']) in range(1,3):
        return ('Postive')
    elif (s['Day_Perc_Change']) in range(-1,-3):
        return ('Negative')
    elif (s['Day_Perc_Change']) in range(3,7):
        return ('Among Top Gainers')
    elif (s['Day_Perc_Change']) in range(-3,-7):
        return ('Among Top Losers')
    elif (s['Day_Perc_Change']) > 7:
        return('Bull Run')
    elif (s['Day_Perc_Change']) <- 7:
        return ('Bear Drop')
    
data['Trend'] =  data.apply(conditions, axis=1)

group1 = data.groupby('Trend')

# print j you will understand that j is the column values for each trend (i) which are SLight Negative and Slight or no change
# for each i(trend) you access the Total Traded Quantity column amongst all the columns using j ['total traded quantity'] 
# and finf mean and median of the columns 

for i,j in group1:
    print("Average of Total Traded Quantity for: ")
    print(i, j['Total Traded Quantity'].mean())
    print("\n")
    print("Median of Total Traded Quantity for: ")
    print(i, j['Total Traded Quantity'].median())
    print("\n")


data.set_index('Date')

register_matplotlib_converters
plt.plot(data['Date'], data["Close Price"])
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.xticks(rotation = 60)
plt.title('TCS Close Price')
plt.grid()
plt.show()


plt.stem(data['Date'],data['Day_Perc_Change'])
plt.xlabel('Date')
plt.ylabel('Day_Perc_Change')
plt.xticks(rotation = 60)
plt.title('Stem Plot for Day_Perc_Change of TCS')
plt.grid()
plt.show()

plt.stem(data['Date'],data['No. of Trades'])  #Volumes
plt.xlabel('Date')
plt.ylabel('NO. of Trades')
plt.xticks(rotation = 60)
plt.title('Stem Plot for Daily Volumes of TCS') 
plt.grid()
plt.show()


# PIE Chart

def conditions(s):
    if s['Day_Perc_Change'] > -0.5 and s['Day_Perc_Change'] < 0.5 :
        return (1)
    elif s['Day_Perc_Change']> 0.5 and s['Day_Perc_Change']<1:
        return (2)
    elif s['Day_Perc_Change'] >-0.5 and s['Day_Perc_Change']<-1:
        return (3)
    elif s['Day_Perc_Change'] in range(1,3):
        return (4)
    elif s['Day_Perc_Change'] in range(-1,-3):
        return (5)
    elif s['Day_Perc_Change'] in range(3,7):
        return (6)
    elif s['Day_Perc_Change'] in range(-3,-7):
        return (7)
    elif s['Day_Perc_Change'] > 7:
        return(8)
    else:
        return (9)
    
data['Trend'] =  data.apply(conditions, axis=1)
colors = ['Blue', 'red']
group1 = data.groupby('Trend')
plt.pie(data['Trend'], colors = colors)
plt.show()


# BAR GRAPH

group1 = data.groupby('Trend')

list = []

for i,j in group1:
    trade1 = j['Total Traded Quantity'].mean()
    plot = plt.bar(data['Total Traded Quantity'], trade1)

plt.xticks(range(min(data['Total Traded Quantity']), max(data['Total Traded Quantity'])+1))
#plt.xticks(data['Total Traded Quantity'])    
plt.grid()
plt.title('Mean')
plt.ylabel('Trade_Average')
plt.xlabel('Total Trade Quantity')
plt.show()


# HISTOGRAM

plt.hist(data['Day_Perc_Change'], bins =92)
plt.ylabel('Daily Return Percentage')
plt.show()


data1 = pd.read_csv(r'C:\Users\Suman\Desktop\AICTE Internship\Mid_Cap\TATAPOWER.csv')
data2 = pd.read_csv(r'C:\Users\Suman\Desktop\AICTE Internship\Mid_Cap\VOLTAS.csv')
data3 = pd.read_csv(r'C:\Users\Suman\Desktop\AICTE Internship\Mid_Cap\APOLLOTYRE.csv')
data4 = pd.read_csv(r'C:\Users\Suman\Desktop\AICTE Internship\Mid_Cap\BERGEPAINT.csv')
data5 = pd.read_csv(r'C:\Users\Suman\Desktop\AICTE Internship\Mid_Cap\RBLBANK.csv')
nifty_index = pd.read_csv(r'C:\Users\Suman\Desktop\AICTE Internship\Nifty50\Nifty50.csv')


data1.drop(data1[data1['Series'] !='EQ'].index , inplace =True)
data2.drop(data2[data2['Series'] !='EQ'].index , inplace =True)
data3.drop(data3[data3['Series'] !='EQ'].index , inplace =True)
data4.drop(data4[data4['Series'] !='EQ'].index , inplace =True)
data5.drop(data5[data5['Series'] !='EQ'].index , inplace =True)


Data_CP = pd.concat([data1['Close Price'],
                     data2['Close Price'],
                     data3['Close Price'],
                     data4['Close Price'],
                     data5['Close Price']], axis=1)

# Rename the column names
Data_CP.columns = ['TATAPOWER_CP', 'VOLTAS_CP', 'APOLLOTYRE_CP', 'BERGEPAINT_CP', 'RBLBANK_CP']


Data_CP_Perc_Change = pd.concat([Data_CP['TATAPOWER_CP'].pct_change(),
                                 Data_CP['VOLTAS_CP'].pct_change(),
                                 Data_CP['APOLLOTYRE_CP'].pct_change(),
                                 Data_CP['BERGEPAINT_CP'].pct_change(),
                                 Data_CP['RBLBANK_CP'].pct_change()], axis=1)

Data_CP_Perc_Change.columns = ['TATAPOWER_PERC_CHANGE', 
                   'VOLTAS_PERC_CHANGE',
                   'APOLLOTYRE_PERC_CHANGE', 
                   'BERGEPAINT_PERC_CHANGE', 
                   'RBLBANK_PERC_CHANGE']


Data_CP_Perc_Change = Data_CP_Perc_Change.dropna()


#finding the correlation between the percentage change i.e the correlation matrix
correlation = Data_CP_Perc_Change.corr()


# add a column for percentage in the daily closing prices in the nifty index
nifty_index['Nifty_Perc_Change'] = nifty_index['Close'].pct_change()
nifty_index = nifty_index.dropna()


sns.pairplot(Data_CP_Perc_Change)
plt.show()

# 7 day rolling average of the percentage change of the TATAPOWER stock price

Data_CP_Perc_Change['TATAPOWER_PERC_CHANGE'].rolling(7).mean().plot()


# Standard Deviation for the percentage changes of each stock

std1 = Data_CP_Perc_Change['TATAPOWER_PERC_CHANGE'].rolling(7).std(ddof = 0)

std2 = Data_CP_Perc_Change['VOLTAS_PERC_CHANGE'].rolling(7).std(ddof = 0)
std3 = Data_CP_Perc_Change['APOLLOTYRE_PERC_CHANGE'].rolling(7).std(ddof = 0)
std4 = Data_CP_Perc_Change['BERGEPAINT_PERC_CHANGE'].rolling(7).std(ddof = 0)
std5 = Data_CP_Perc_Change['RBLBANK_PERC_CHANGE'].rolling(7).std(ddof = 0) 

#print(" Standard Deviation for TATAPOWER_PERC_CHANGE is:  ", std1)
#print(" Standard Deviation for VOLTAS_PERC_CHANGE is:     ", std2)
#print(" Standard Deviation for APOLLOTYRE_PERC_CHANGE is: ", std3)
#print(" Standard Deviation for BERGEPAINT_PERC_CHANGE is: ",std4 )
#print(" Standard Deviation for RBLBANK_PERC_CHANGE is:    ",std5 )

#stds = [std1,std2,std3,std4,std5]

plt.plot(std1)
plt.title('Voliatlity for TATAPOWER')
plt.show()


nifty_std = nifty_index['Nifty_Perc_Change'].rolling(7).std(ddof = 0)
plt.plot(nifty_std)
plt.title('Volitality for Nifty')
plt.show()


plt.plot(std1)
plt.plot(nifty_std)
plt.title('Volitalities of TATAPOWER and Nifty')
plt.show()


# Using TATAPOWER  close price to calculate moving averages

data1['Date'] = pd.to_datetime(data1['Date'])
moving_averages1 = []
moving_averages2 = []


# 21 days to group : 7 *3 = 21 so 7 groups ....CHECK , NOT SURE
#moving_averages1 = data1['Close Price'].head(21).rolling(window = 3).mean()


moving_averages1 = data1['Close Price'].rolling(window = 21).mean()
moving_averages2 = data1['Close Price'].rolling(window = 34 ).mean()

moving_averages_list1 = moving_averages1.tolist()
moving_averages_list2 = moving_averages2.tolist()

plt.grid(True)
#plt.plot(data1['Date'], data1['Close Price'], label ='Price')
plt.plot(data1['Date'],moving_averages1, label = 'For 21 days')
plt.plot(data1['Date'],moving_averages2, label = 'For 34 days')
plt.xticks(rotation = 40)
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Trade Calls using SMA for TATAPOWER')
plt.legend()
plt.show()



#Using TATAPOWER dataframe close price to calc the following


window = 14
no_of_std = 2

#Calculate rolling mean and standard deviation using number of days set above
rolling_mean = data1['Close Price'].rolling(window).mean()
rolling_std = data1['Close Price'].rolling(window).std()


dict  = {'Date' : Bands_for_TATAPOWER['Date'] ,
         'Close Price' :Bands_for_TATAPOWER['Close Price'],
         'Rolling Mean' : Bands_for_TATAPOWER['Rolling Mean'],
          'Bollinger High' : Bands_for_TATAPOWER['Bollinger High'],
          'Bollinger Low' : Bands_for_TATAPOWER['Bollinger Low']}

Bands_for_TATAPOWER = pd.DataFrame(dict)
Bands_for_TATAPOWER.to_csv("./Bollinger for TATAPOWER.csv", sep=',',index=False)

#create two new DataFrame columns to hold values of upper and lower Bollinger bands
Bands_for_TATAPOWER['Date'] = data1['Date']
Bands_for_TATAPOWER['Close Price'] = data1['Close Price']
Bands_for_TATAPOWER['Rolling Mean'] = rolling_mean
Bands_for_TATAPOWER['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
Bands_for_TATAPOWER['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)

Bands_for_TATAPOWER[['Close Price','Bollinger High','Bollinger Low']].plot()



plt.grid(True)
plt.title('Trade Calls using Bollinger Bands for TATAPOWER')
plt.legend()
plt.show()


    
    
