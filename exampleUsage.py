import sys
from numpy.linalg import norm
from numpy import dot

from syntheticDataMaker import SyntheticDataMaker
from frequentDirections import FrequentDirections

n = 500
d = 100
ell = 20
k = 5

# this is only needed for generating input vectors
dataMaker = SyntheticDataMaker()
dataMaker.initBeforeMake(d, k, signal_to_noise_ratio=10.0)                                                                                                                                                                                                                                                                                                                         

# This is where the sketching actually happens
sketcher = FrequentDirections(d,ell)
for i in xrange(n):
    row = dataMaker.makeRow()
    sketcher.append(row)
sketch = sketcher.get()

# Here is where you do something with the sketch.
# The sketch is an ell by d matrix 
# For example, you can compute an approximate covariance of the input 
# matrix like this:

approxCovarianceMatrix = dot(sketch.transpose(),sketch)
print approxCovarianceMatrix
 





