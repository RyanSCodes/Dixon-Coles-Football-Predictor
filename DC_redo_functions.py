import numpy as np
import pandas as pd
import datetime as dt
import sys
import string
import random 
import math

""" Parameters obtained from optimising. Decay weights results by age, to an exponential
	function. Rho is a deviation from Poisson behaviour. Home advantage is a factor
	to alter the distribution of home teams"""
home_adv = 1.35
decay = 70.0
rho = 0.03

results_csv = 'PremierLeague14.csv'
# 20 PL teams in csv file (needs changing with seasons)
teams = ["Arsenal","Aston Villa","Burnley","Chelsea","Crystal Palace",
	"Everton","Hull","Leicester","Liverpool","Man City","Man United",
	"Newcastle","QPR","Southampton","Stoke","Sunderland","Swansea",
	"Tottenham","West Brom","West Ham"]
	
"""Calculates differences in datetimes and returns int"""
def delta_time(times) :
    now, date = times
    A = np.datetime64(date)
    B = np.datetime64(now)
    C = (B-A)/(60*60*24*10**6)
    return C.astype(int)

"""Pandas messing up datetimes..."""
def reformat_date(date_string) :
    day = date_string[:2]
    month = date_string[3:5]
    year = "20"+ date_string[6:]
    newdate = year + "-" + month + '-' + day
    return newdate
    
# Perhaps truncate records after 365 days (or other)
"""Reads previous results csv and returns numpy matrix""" 
def results_array() :
	df = pd.read_csv(results_csv, dtype={'Date': str })
	df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'] ]
	df['Date'] = df['Date'].apply(reformat_date)
	df.Date = pd.to_datetime(df.Date)
	df['Now'] = dt.datetime.now()
	df['DaysSince'] = df[['Now', 'Date']].apply(delta_time, axis=1)
	df = df[['DaysSince', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
	return df.as_matrix()

"""Initialises ability_dict with random attack and defense parameters""" 
def random_abilities() :
	ability_dict = {}
	for team in teams :
		ability_dict[team] = [random.random(), random.random()]
	return ability_dict

""" Calculates logarithm of likelihood function """
def log_likelihood(results_list, ability_dict) :
	total = 0.0
	for match in results_list :
		days = float(match[0])
#		print match[0], match[1], match[2], match[3], match[4]
		home_team = match[1]
		away_team = match[2]
		home_mean = home_adv * ability_dict[home_team][0] \
		* ability_dict[away_team][1] 
		away_mean = ability_dict[away_team][0] * ability_dict[home_team][1]
		home_goals = match[3]
		away_goals = match[4]
		home_dist = poisson(home_mean, home_goals + 1)
		away_dist = poisson(away_mean, away_goals + 1)
		tau = tau_matrix(home_mean, away_mean, home_goals, away_goals)
		total += (math.log(home_dist[home_goals]) \
		+ math.log(away_dist[away_goals]) + math.log(tau))
#		total += math.exp(- decay * days) * (math.log(home_dist[home_goals]) \
#		+ math.log(away_dist[away_goals]) + math.log(tau))
	return total
	
""" Distribution of results doesn't fit Poisson perfectly, altered slighly
	by parameter rho"""
def tau_matrix(home_mean, away_mean, home_goals, away_goals) : 
	if home_goals == 0 and away_goals == 0 :
		return 1.0 - home_mean * away_mean * rho
	elif home_goals == 0 and away_goals == 1 :
		return 1.0 + home_mean * rho
	elif home_goals == 1 and away_goals == 0 :
		return 1.0 + away_mean * rho
	elif home_goals == 1 and away_goals == 1 :
		return 1.0 - rho
	else :
		return 1.0

"""Poisson distribution for mean m, calculated up to n-1"""	
def poisson(m, n):
    p=math.exp(-m)
    r=[p]
    for i in range(1, n):
        p*=m/float(i)
        r.append(p)
    return r
# f(k) = exp(-m) * m**k / k!

""" MC routine to maximise likelihood function, convergence determined by
	'rdiff' """
def monte_carlo_opt(log_like, ability_dict, results_list) :
	delta = 0.1
	conv = []
	k = 0
	rdiff = 1.0
	while rdiff > 1e-9 :
		for key in sorted(ability_dict.keys()) :
			j = 0
			if random.random() > 0.5 : j = 1			
			disp = delta * (random.random() - 0.5)
			ability_dict[key][j] += disp
			if ability_dict[key][j] > 0 : 
				trial = log_likelihood(results_list, ability_dict)	
				if trial < log_like :
					ability_dict[key][j] -= disp
				else :
					rdiff = abs((trial - log_like)/log_like)
					log_like = trial
			else :
				ability_dict[key][j] -= disp					
		conv.append(log_like)
		k += 1
	return (ability_dict, conv, k)