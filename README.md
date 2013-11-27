pulsar_planet
=============

Pulsar Planet Monte Carlo (python)


This code simulates the probabistic orbital changes wrought upon a two-body system when one of the bodies (a gas giant) undergoes supernova. This simulation is a re-written version of my undergraduate thesis code, originally written in Mathematica.

I rewrote this for several reasons: I needed to make many small tweaks to the simulation and, now that I'm out of college, Mathematica is very expensive and not very accessible to many people. Python is free and its syntax is easy to read. This rewrite has also been a great reason to learn about using Numpy, Scipy, and Matplotlib. 

To run a single monte carlo simulation, run 
>$ python function_unit_test.py

This will simulate the probability that the Earth would remain orbitally bound to the Sun, should the Sun explode in supernova. Such an outcome, of course, won't happen, as the Sun not massive enough.


