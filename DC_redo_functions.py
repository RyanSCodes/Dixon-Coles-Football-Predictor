import numpy as np
import pandas as pd
import datetime as dt
import sys
import string 

results_csv = 'PremierLeague14.csv'

def delta_time(times) :
    now, date = times
    A = np.datetime64(date)
    B = np.datetime64(now)
    C = (B-A)/(60*60*24*10**6)
    return C.astype(int)
    
def results_array() :
	df = pd.read_csv(results_csv)
	df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'] ]
	df.Date = pd.to_datetime(df.Date)
	df['Now'] = dt.datetime.now()
	df['DaysSince'] = df[['Now', 'Date']].apply(delta_time, axis=1)
	df = df[['DaysSince', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
	return df.as_matrix()