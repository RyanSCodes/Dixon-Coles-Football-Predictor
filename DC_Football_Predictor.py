#!/Users/ryanshiz/anaconda/bin/python

""" Runs on Python 2.7
 	Football results predictor based on Dixon-Coles method
 	http://www.math.ku.dk/~rolf/teaching/thesis/DixonColes.pdf 
 	"""

""" Each team is given 2 parameters (and a home advantage home_adv) fitted to previous
	results in order to predict the probabilities of future results. These parameters
	influence a distribution of potential goals scored for each team (Poisson) over
	which probabilities can be summed to figure out the probability of a home win,
	draw or home loss. The previous results are also weighted by their age (old results 
	are less relevant to present form).
	"""
from DC_Functions import * 

""" Use openpyxl to read spreadsheet of last seasons results """
from openpyxl import load_workbook
wb = load_workbook('PremierLeague14.xlsx', data_only = True)
#print wb.get_sheet_names()
ws1 = wb["Results"]
	
def main() :

	match_list = read_excel(ws1)

""" Read input (teams) from command line 
	"""
	args = sys.argv[1:]
	if not args:
		print "usage: [team 1 (home)] [team2 (away)] use underscores and caps";
		sys.exit(1)
	
	if len(args) == 2 :
		home_pred = args[0]
		away_pred = args[1]
	elif len(args) == 3 :
		if args[1] in ('Villa', 'Palace', 'United', 'City', 'Brom', 'Ham') : 
			home_pred = args[0] + " " + args[1]
			away_pred = args[2]
		else :
			home_pred = args[0]
			away_pred = args[1] + " " + args[2]
	elif len(args) == 4 :
			home_pred = args[0] + " " + args[1]
			away_pred = args[2] + " " + args[3]
	else :
		sys.exit("Wrong names")					

	print " " 
	print "Predicting..."
	print home_pred, 'vs.', away_pred
	print " " 	

""" Assign each team an attacking parameter and a defensive parameter (randomly) 
	"""
	ability_dict = random_abilities()
#	rho = 0.03

""" The likelihood function is maximised to determine the most likely parameters that
	lead to a given set of results (from the spreadsheet). The optimisation
	is a crude Monte Carlo routine  
	"""
	like = log_likelihood(match_list, ability_dict)	
	print 'Random log likelihood = ', like
# rho optimisation	
#	for i in range(0,10) :
#		rho = float(i) * 0.12 / 10.0
	(ability_list, conv, k) = monte_carlo_opt(like, ability_dict, match_list)
	like = log_likelihood(match_list, ability_dict)	
#		print rho, like
		
	print 'After ', k, ' cycles:'
	print 'Minimised log likelihood = ', like	
	
#	print_ability_table(ability_dict)
	
""" Prints convergence of likelihood function 
	"""
	f = open("Converge.txt", "w")
	for i in range(1, k) :
		f.write(str(i) + " " + str(conv[i]) + "\n")
	f.close()		

""" Prints table of teams' abilities 
	"""
	rank_dict = {}
	g = open("Stats.txt", "w")
	g.write('%-15s %-12s %-10s \n' % ('Team', 'Attack', 'Defense'))
	for key in sorted(ability_dict.keys()) :
		a = key
		b = ability_dict[key][0]
		c = ability_dict[key][1]
		bb = format(float(b), '.2f')
		cc = format(float(c), '.2f')
		g.write('%-15s %-12s %-10s \n' % (a, bb, cc))
	g.close()

""" Calculates probabilities of outcomes 
	"""
	home_mean = home_adv * ability_dict[home_pred][0] \
	* ability_dict[away_pred][1] 
	away_mean = ability_dict[home_pred][0] * ability_dict[away_pred][1]
	home_dist = poisson(home_mean, 10)
	away_dist = poisson(away_mean, 10)
	
""" Creates matrix of possible scores 'c'
	"""
	a = np.array(home_dist)
	b = np.array(away_dist)	
	c = np.outer(a,b)
	print_probs(c)

""" Poisson Test (debugging goals distribution) 
	"""

#	f = open("Poisson.txt", "w")
#	for j in range(10) :
#		tring = str(j) + " " 
#		for trace in SamplePoissonTraces :
#			item = format(trace[j], '.3f')
#			tring += str(item) + " "
#		f.write(tring + "\n")
#	f.close()


if __name__ == '__main__':
	main()