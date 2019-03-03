*Seriating* a correlation matrix means re-ordering its rows and columns so that similar items end up close together. Kind of like clustering, but better. [Here is an excellent demonstration of its use](http://nicolas.kruchten.com/content/2018/02/seriation/). You can install this package with

```pip install seriate```

### Licensing

This module does not have a license currently as the underlying LKH solver - which is installed automatically with this package - is vaguely described as **'for academic and non-commercial use'** , and I'm not sure how that restricts the choice of license for this wrapper.

### Internals

Seriation reduces to solving a travelling salesman problem, and so internally this package uses the [LKH](http://www.akira.ruc.dk/~keld/research/LKH/) solver. If you'd like to extend this script, you'll probably find these references useful:
 
 - [The LKH user guide](http://www.akira.ruc.dk/~keld/research/LKH/LKH-2.0/DOC/LKH-2.0_USER_GUIDE.pdf)
 - [The TSPLIB format spec](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf)
