# Dixon-Coles-Football-Predictor

Runs on Python 2.7

Football results predictor based on Dixon-Coles method
http://www.math.ku.dk/~rolf/teaching/thesis/DixonColes.pdf

Based on previous results, a home advantage parameter for all teams, and attack and defense parameters
 for each team are calculated. These parameters influence a distribution of potential goals scored for each team (Poisson) over
which probabilities can be summed to figure out the probability of a home win,
draw or home loss. The previous results are also weighted exponentially by their age (old results 
are less relevant to present form).

The teams are:

Arsenal    | Aston Villa | Burnley   | Chelsea     | Crystal Palace
-----------|-------------|-----------|-------------|----------------
Everton    | Hull        | Leicester | Liverpool   | Man City
Man United | Newcastle   | QPR       | Southampton | Stoke
Sunderland | Swansea     | Tottenham | West Brom   | West Ham