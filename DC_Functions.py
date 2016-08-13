
import sys
import re
import random
import math
import numpy as np

""" Parameters obtained from optimising. Decay weights results by age, to an exponential
	function. Rho is a deviation from Poisson behaviour. Home advantage is a factor
	to alter the distribution of home teams.
	"""
home_adv = 1.35
decay = 70.0
rho = 0.03

""" Reads spreadsheet and returns list of results and age in days since most 
	recent game 
	"""
def read_excel(wsx) :
	res_list = []	
	for k in range(2,382):
		mini_list = []
		d = str(wsx.cell(row = k, column = 2).value)
		end = d.find(" ")
		dd = d[:end]
		match = re.search(r'(\d\d\d\d)-(\d\d)-(\d\d)', dd)
		if match : 
			year = match.group(1)
			month = match.group(2)
			day = int(match.group(3))
		total = 0
		if year == '2015' :
			total += 137
		if month == '09' :
			total += 15
		elif month == '10' :
			total += 15 + 30
		elif month == '11' :
			total += 15 + 30 + 31
		elif month == '12' :
			total += 15 + 30 + 31 + 30
		elif month == '02' :
			total += 31
		elif month == '03' :
			total += 31	+ 28	
		elif month == '04' :
			total += 31 + 28 + 31
		elif month == '05' :
			total += 31 + 28 + 31 + 30
		total += day - 16	
		total = 265 - total
		mini_list.append(total)
		for j in range(3,5) :
			a = str(wsx.cell(row = k, column = j).value)
			mini_list.append(a)
		for j in range(5,7) :
			a = int(wsx.cell(row = k, column = j).value)
			mini_list.append(a)
		res_list.append(mini_list)
	return res_list	

""" Initialises ability dict with random parameters 
	"""
def random_abilities() :
	ability_dict = {}
	ability_dict["Arsenal"] = [random.random(), random.random()]
	ability_dict["Aston Villa"] = [random.random(), random.random()]
	ability_dict["Burnley"] = [random.random(), random.random()]
	ability_dict["Chelsea"] = [random.random(), random.random()]
	ability_dict["Crystal Palace"] = [random.random(), random.random()]
	ability_dict["Everton"] = [random.random(), random.random()]
	ability_dict["Hull"] = [random.random(), random.random()]
	ability_dict["Leicester"] = [random.random(), random.random()]
	ability_dict["Liverpool"] = [random.random(), random.random()]
	ability_dict["Man City"] = [random.random(), random.random()]
	ability_dict["Man United"] = [random.random(), random.random()]
	ability_dict["Newcastle"] = [random.random(), random.random()]
	ability_dict["QPR"] = [random.random(), random.random()]
	ability_dict["Southampton"] = [random.random(), random.random()]
	ability_dict["Stoke"] = [random.random(), random.random()]
	ability_dict["Sunderland"] = [random.random(), random.random()]
	ability_dict["Swansea"] = [random.random(), random.random()]
	ability_dict["Tottenham"] = [random.random(), random.random()]
	ability_dict["West Brom"] = [random.random(), random.random()]
	ability_dict["West Ham"] = [random.random(), random.random()]
	return ability_dict

""" Distribution of results doesn't fit Poisson perfectly, altered slighly
	by parameter rho
	"""
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

""" Calculates logarithm of likelihood function 
	"""
def log_likelihood(match_list, ability_dict) :
	total = 0.0
	for match in match_list :
		days = float(match[0])
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
		total += math.exp(- decay * days) * (math.log(home_dist[home_goals]) \
		+ math.log(away_dist[away_goals]) + math.log(tau))
	return total

""" MC routine to maximise likelihood function, convergence determined by
	'rdiff' 
	"""
def monte_carlo_opt(like, ability_dict, match_list) :
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
				trial = log_likelihood(match_list, ability_dict)	
				if trial < like :
					ability_dict[key][j] -= disp
				else :
					rdiff = abs((trial - like)/like)
					like = trial
			else :
				ability_dict[key][j] -= disp					
		conv.append(like)
		k += 1
	return (ability_dict, conv, k)
	
def poisson(m, n):
    p=math.exp(-m)
    r=[p]
    for i in range(1, n):
        p*=m/float(i)
        r.append(p)
    return r
# f(k) = exp(-m) * m**k / k!

""" Sum of all outcomes where home goals > away goals
	"""
def home_win(matrix) :
	return sum([matrix[i][j]                    
    	for i in range(matrix.shape[0])
        for j in range(matrix.shape[1])
        if i > j])
""" Sum of all outcomes where home goals = away goals
	"""
def draw(matrix) :
	return sum([matrix[i][j]                    
    	for i in range(matrix.shape[0])
        for j in range(matrix.shape[1])
        if i == j])
""" Sum of all outcomes where home goals < away goals
	"""   
def away_win(matrix) :
	return sum([matrix[i][j]                    
    	for i in range(matrix.shape[0])
        for j in range(matrix.shape[1])
        if i < j])

""" Print results to command line
	"""
def print_probs(matrix) :
	print " "
	print "Probabilities calculated as..."
	print " "
	a = float(home_win(matrix))
	b = float(draw(matrix))
	c = float(away_win(matrix))
	print '%-10s %-12s %-10s' % ('Outcome', 'Probability', 'Odds (Bet Multiplier)')	
	print '%10s %-12f %-10f' % ('Home win :', a, 1.0/a)
	print '%10s %-12f %-10f' % ('Draw :', b, 1.0/b)
	print '%10s %-12f %-10f' % ('Away win :', c, 1.0/c)
	print "Check... ", a + b + c
	print " "
	
""" Prints teams and their ability parameters 
	"""
def print_ability_table(ability_dict) :
	rank_dict = {}
	print " "
	print '%-15s %-12s %-10s' % ('Team', 'Attack', 'Defense')
	for key in sorted(ability_dict.keys()) :
		a = key
		b = ability_dict[key][0]
		c = ability_dict[key][1]
		d = b - c
		rank_dict[key] = d
		bb = format(float(b), '.2f')
		cc = format(float(c), '.2f')
		print '%-15s %-12s %-10s' % (a, bb, cc)
		
""" Difference Rankings (Generates table which should correspond to ranking of teams 
	for debugging)
	"""
#	rank_list = []
#	for key in rank_dict :
#		rank_tuple = (key, rank_dict[key])
#		rank_list.append(rank_tuple)
#	sort_list = sorted(rank_list, key=lambda tup: tup[1])
#	for team in reversed(sort_list) : 
#		print team
#	print " "