# Residential HVAC

## Single-speed air conditioners

To calculate COP:
```
$ python air_conditioner.py SEER
````

Example w/ results:
```
$ python air_conditioner.py 13
COP_cooling: 4.0
```

## Single-speed heat pumps

To calculate COP:
```
$ python heat_pump.py SEER HSPF
```

Example w/results:
```
$ python heat_pump.py 13 7.7
COP_cooling: 4.04
COP_heating: 3.09
```

## Tests

Tests provide expected COPs for a given set of SEER/HSPF values.

To run all tests:
```
$ python tests.py

Testing ACs:
SEER = 8...
SEER = 10...
SEER = 13...
SEER = 14...
SEER = 15...
.
Testing HPs:
SEER = 8, HSPF=6.0...
SEER = 10, HSPF=6.2...
SEER = 13, HSPF=7.7...
SEER = 14, HSPF=8.2...
SEER = 15, HSPF=8.5...
.
----------------------------------------------------------------------
Ran 2 tests in 0.008s

OK
```
