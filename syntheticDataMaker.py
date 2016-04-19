#!/usr/bin/python
import sys
from numpy.random import randn
from numpy.linalg import qr
from numpy import exp, ones, dot, zeros, array
        
class SyntheticDataMaker:

    def __init__(self):
        self.wasInitForMake = False
        
    def initBeforeMake(self, dimension, \
                       signal_dimension=0, \
                       signal_to_noise_ratio=0,\
                       signal_singular_value_decay_factor=0, \
                       signal_singular_value_decay_type='exp'):
        
        self.dimension = dimension
        self.signal_dimension = signal_dimension
        self.signal_to_noise_ratio = signal_to_noise_ratio
        self.signal_singular_value_decay_factor = signal_singular_value_decay_factor
        self.signal_singular_value_decay_type = signal_singular_value_decay_type
    
        # setting a random singular space    
        [Q,R] = qr( randn(self.dimension, self.signal_dimension) )
        self.signal_row_space = Q.transpose()
        del Q,R
        
        # setting the singular values  
        eta = self.signal_singular_value_decay_factor
        if self.signal_singular_value_decay_type == 'exp':
            self.signal_singular_values = [exp(-10*eta*i/self.signal_dimension) for i in xrange(self.signal_dimension)] 
        elif self.signal_singular_value_decay_type == 'lin':
            self.signal_singular_values = [max(1.0 - eta*float(i)/self.signal_dimension,0.0) for i in xrange(self.signal_dimension)]
        else:
            self.signal_singular_values = ones(self.signal_dimension)
        # done initializing 
        self.wasInitForMake = True


    def makeRow(self):
        if not self.wasInitForMake:
            sys.stderr.write('ERROR: must run initBeforeMake(...) before makeRow()')
            return
        noise = randn(self.dimension)
        signal_coeffs = randn(self.signal_dimension)
        signal = dot(self.signal_singular_values * signal_coeffs, self.signal_row_space)
        return signal + noise/self.signal_to_noise_ratio

    def makeMatrix(self, n):
        matrix = zeros((n, self.dimension))
        for i in xrange(n):
            matrix[i,:] = self.makeRow()
        return matrix
            
    def getSignalRowSpace(self):
        return self.signal_row_space

    def __vector_to_string__(self,v):
        s = '%s\n'%(','.join('%.2E'%x for x in v.flatten()))
        return s
    
    def __vector_from_string(self,s):
        v = array([float(x) for x in s.strip('\n').split(',')])
        return v
    
        
    def readFromFileIter(self,f=sys.stdin):
        for line in f:
            yield self.__vector_from_string(line)
    
    def writeToFile(self, v, f=sys.stdout):
        f.write(self.__vector_to_string__(v))
            
    def writeToFileIter(self, vs, f=sys.stdout):
        for v in vs:
            f.write(self.__vector_to_string__(v))


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=100, help='number of rows in matrix')
    parser.add_argument('-d', type=int, default=10, help='dimension of row vectors (number of columns in matrix)')
    parser.add_argument('-k', type=int, default=5, help='the rank of the signal')
    parser.add_argument('-snr', type=float, default=10.0, help='signal to noise ratio')
    args = parser.parse_args()
    
    sdn = SyntheticDataMaker()
    sdn.initBeforeMake(args.d, args.k, args.snr)
    
    for i in xrange(args.n):
        row  = sdn.makeRow()
        sdn.writeToFile(row)

    