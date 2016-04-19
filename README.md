# frequent-directions
This repo was created by [Edo Liberty](www.edoliberty.com) and [Mina Ghashami](http://www.cs.utah.edu/~ghashami/).
It contains the simplest version of the frequent directions algorithm for matrix sketching in Python. 
It is developed for academic use only and for reproducibility of the results in the following papers:
* [Simple and Deterministic Matrix Sketches](http://www.cs.yale.edu/homes/el327/papers/simpleMatrixSketching.pdf) Edo Liberty
* [Relative Errors for Deterministic Low-Rank Matrix Approximations](http://www.cs.utah.edu/~ghashami/papers/relative_err_soda.pdf) Mina Ghashami, and Jeff M. Phillips
* [Frequent Directions: Simple and Deterministic Matrix Sketching](http://www.cs.utah.edu/~ghashami/papers/fd_journal.pdf) Mina Ghashami, Edo Liberty, Jeff M. Phillips, and David P. Woodruff


### Creating an example matrix

Run this command to create a matrix to work with
    
    $ ./syntheticDataMaker.py -n=1000 -d=50 > matrix.csv
    
This will create a csv file containing a matrix with n rows and d columns.
 
### Running FD

You can use the file created above or any other csv file containing a matrix

    cat matrix.csv | ./frequentDirections.py -d=50 -ell=15 > sketch.csv
    
The main in `frequentDirections.py` will only use rows in `matrix.csv` that contain exactly `-d=50` comma separated floats.  
The file `sketch.csv` will contain a sketch matrix in csv format.
It will consist of `-ell=15` rows of dimension `-d=50` as comma separated floats.


You can also look at `exampleUsage.py` for an example on how to import and use frequent directions.   
    
