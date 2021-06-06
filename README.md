# Edmonds algorithm

This is an implementation of Edmonds' algorithm for finding maximum matchings on unweighted graphs.
This implementation closely follows the description of the algorithm given at https://en.wikipedia.org/wiki/Blossom_algorithm.

### Usage
Prepare your graph as a csv containing your graph's adjacency matrix (see ```example.csv``` for an example input), then run:
```
python find_maximum_matching.py --graphcsv path/to/your.csv
```
This command will output an adjacency matrix to a file at the location ```path/to/your_matching.csv``` 
(see ```example_matching.csv``` for an example output).

### Testing
The ```tests``` directory contains a fairly thorough collection of unit tests, as well
as a collection of end-to-end tests in the ```test_find_maximum_matching.py``` file.  This file contains:

  * a couple of tests for specific graphs
  * a test that generates 100 random graphs and for each one compares the result of Edmonds' algorithm with a brute 
force exponential-time algorithm
  * an invocation of ```find_maximum_matching``` on a random graph of 100 nodes to check it runs in a reasonable time 
