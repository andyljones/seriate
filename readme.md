*Seriating* a correlation matrix means re-ordering its rows and columns so that similar items end up close together. Kind of like clustering, but better. [Here is an excellent demonstration of its use](http://nicolas.kruchten.com/content/2018/02/seriation/). 

This is a minimal script that uses [LKH](http://www.akira.ruc.dk/~keld/research/LKH/) to seriate matrices using TSP. It uses LKH rather than Concorde because Concorde is a pain to set up. If you'd like to extend this script, you'll probably find these references useful:
 
  - [The LKH user guide](http://www.akira.ruc.dk/~keld/research/LKH/LKH-2.0/DOC/LKH-2.0_USER_GUIDE.pdf)
 - [The TSPLIB format spec](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf)