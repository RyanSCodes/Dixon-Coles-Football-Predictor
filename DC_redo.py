#!/Users/ryanshiz/anaconda/bin/python

""" previous results csv from http://www.football-data.co.uk/englandm.php"""

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
#print ability_dict
	
	log_like = log_likelihood(results_list, ability_dict)	
	print 'Random log likelihood = ', log_like

	(ability_list, conv, k) = monte_carlo_opt(log_like, ability_dict, results_list)
	log_like = log_likelihood(results_list, ability_dict)
	
	print 'After ', k, ' cycles:'
	print 'Minimised log likelihood = ', log_like
	
if __name__ == '__main__':
	main()