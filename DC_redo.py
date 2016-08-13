#!/Users/ryanshiz/anaconda/bin/python

""" csv from http://www.football-data.co.uk/englandm.php"""

from DC_redo_functions import *

def main() :

	"""Read previous season's results"""
	results_list = results_array()

	""" Read input (teams) from command line """
	args = sys.argv[1:]
	if not args:
		print "usage: [team 1 (home)] [team2 (away)] use underscores and caps";
		sys.exit(1)
	args[0] = args[0].replace('_', ' ')
	args[1] = args[1].replace('_', ' ')
	
	
	
	
	
if __name__ == '__main__':
	main()