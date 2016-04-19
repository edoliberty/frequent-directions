from numpy import zeros, max, sqrt, isnan, isinf, dot, diag, count_nonzero
from numpy.linalg import svd, linalg
from scipy.linalg import svd as scipy_svd
from scipy.sparse.linalg import svds as scipy_svds

from matrixSketcherBase import MatrixSketcherBase

class FrequentDirections:

    def __init__(self , d, ell):
        self.class_name = 'FrequentDirections'
        self.d = d
        self.ell = ell
        self.m = 2*self.ell
        self._sketch = zeros( (self.m, self.d) ) 
        self.nextZeroRow = 0
                 
    def append(self,vector):     
        if count_nonzero(vector) == 0:
            return

    	if self.nextZeroRow >= self.m:
            self.__rotate__()

        self._sketch[self.nextZeroRow,:] = vector 
        self.nextZeroRow += 1
        
    def __rotate__(self):
        try:
            [_,s,Vt] = svd(self._sketch , full_matrices=False)
        except linalg.LinAlgError as err:
            [_,s,Vt] = scipy_svd(self._sketch, full_matrices = False)
        #[_,s,Vt] = scipy_svds(self._sketch, k = self.ell)

        
        if len(s) >= self.ell:
            sShrunk = sqrt(s[:self.ell]**2 - s[self.ell-1]**2)
            self._sketch[:self.ell:,:] = dot(diag(sShrunk), Vt[:self.ell,:])
            self._sketch[self.ell:,:] = 0
            self.nextZeroRow = self.ell
        else:
            self._sketch[:len(s),:] = dot(diag(s), Vt[:len(s),:])
            self._sketch[len(s):,:] = 0
            self.nextZeroRow = len(s)

         
    def get(self):
        return self._sketch[:self.ell,:]
    
