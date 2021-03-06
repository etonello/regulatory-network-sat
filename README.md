## Boolean satisfiability problems for regulatory networks

The script [local_negative_circuits.py](local_negative_circuits.py) creates Boolean formulas expressing the absence of local negative circuits in the regulatory graph and a necessary condition for the existence of a cyclic attractor (or absence of fixed points with the option `-fixed`).
The formula is saved to a file in CNF DIMACS format.

Run `python local_negative_circuits.py -h` for a list of options.

Reference: E. Tonello, E. Farcot and C. Chaouiya, Local negative circuits and cyclic attractors in Boolean networks with at most five components, arXiv:1803.02095, 2018.
