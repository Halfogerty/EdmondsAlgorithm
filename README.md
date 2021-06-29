# Edmonds algorithm

This is a zero-dependency implementation of Edmonds' algorithm for finding maximum matchings on unweighted graphs.
This implementation closely follows the description of the algorithm given at https://en.wikipedia.org/wiki/Blossom_algorithm.

### Usage
Prepare your graph as a csv containing your graph's adjacency matrix (see ```example.csv``` for an example input), then run:
```
python find_maximum_matching.py --graphcsv path/to/your.csv
```
This command will output an adjacency matrix to a file at the location ```path/to/your_matching.csv``` 
(see ```example_matching.csv``` for an example output).

### Testing

#### Correctness
The ```tests``` directory contains a fairly thorough collection of unit tests, as well
as a collection of end-to-end tests in the ```test_find_maximum_matching.py``` file.  This file contains:

  * a couple of tests for specific graphs
  * a test that generates 100 random graphs and for each one compares the result of Edmonds' algorithm with a brute 
force exponential-time algorithm

#### Performance

Edmonds' algorithm should at worst be linear in the number of edges and quadratic in the number of vertices.
The ```tests/test_performance.py``` contains tests for this which measure how the runtime scales as we increase the numbers of
edges and vertices.  The runtime for ```test_linear_in_edges``` does seem to be linear, but 
```test_quadratic_in_vertices``` is definitely sub-quadratic. I haven't dug into 
why this is. My first thoughts are:
    
1. I'm keeping the edges constant leading to very sparse graphs
for which ```find_maximum_matching``` scales sub-quadratically. 
    
2. Quadratic scaling only appears in the 
worst-case, but my tests  consider the average case.