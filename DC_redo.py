#!/Users/ryanshiz/anaconda/bin/python

from DC_redo_functions import *

def main() :

	"""Read previous season's results"""
	results_list = results_array()

	"""Read input (teams) from command line """
	args = sys.argv[1:]
	if not args:
		print "usage: [team 1 (home)] [team2 (away)] use underscores and caps";
		sys.exit(1)
	home_pred = args[0].replace('_', ' ')
	away_pred = args[1].replace('_', ' ')
	
	print " " 
	print "Predicting..."
	print home_pred, 'vs.', away_pred
	print " "
	
	""" Assign each team an attacking parameter and a defensive parameter (randomly)"""
	ability_dict = random_abilities()
	
	log_like = log_likelihood(results_list, ability_dict)	
	print 'Random log likelihood = ', log_like

	(ability_list, conv, k) = monte_carlo_opt(log_like, ability_dict, results_list)
	log_like = log_likelihood(results_list, ability_dict)
	
	print 'After ', k, ' cycles:'
	print 'Minimised log likelihood = ', log_like
	
	"""Prints convergence of likelihood function """
	f = open("Converge.txt", "w")
	for i in range(1, k) :
		f.write(str(i) + " " + str(conv[i]) + "\n")
	f.close()
	
	""" Prints table of teams' abilities """
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
	
	""" Calculates probabilities of outcomes """
	home_mean = home_adv * ability_dict[home_pred][0] \
	* ability_dict[away_pred][1] 
	away_mean = ability_dict[home_pred][0] * ability_dict[away_pred][1]
	home_dist = poisson(home_mean, 10)
	away_dist = poisson(away_mean, 10)
	
	""" Creates matrix of possible scores 'c' """
	a = np.array(home_dist)
	b = np.array(away_dist)	
	c = np.outer(a,b)
	print_probs(c)
	
	
if __name__ == '__main__':
	main()