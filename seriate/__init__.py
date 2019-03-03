import scipy as sp
import re
from tempfile import NamedTemporaryFile
from subprocess import Popen, STDOUT, PIPE
from pathlib import Path
import pandas as pd

PROBLEM = """NAME : python-tsp
TYPE : TSP
DIMENSION : {dimension}
EDGE_WEIGHT_TYPE : EXPLICIT
EDGE_WEIGHT_FORMAT : FULL_MATRIX
EDGE_WEIGHT_SECTION 
{edges}
EOF"""

PARAMS = """PROBLEM_FILE = {problem_filepath}
TOUR_FILE = {output_filepath}"""

def problem(distances, precision=3):
    assert distances.ge(0).all().all()
    integral = (10**precision * distances.round(precision)).astype(int).values
    width = len(str(integral.max()))
    
    formatter = '{:' + str(width) + 'd}'
    rows = [' '.join(map(formatter.format, r)) for r in integral]
    edges = '\n'.join(rows)   
    
    return PROBLEM.format(dimension=len(distances), edges=edges)

def params(problem, output, **kwargs):
    return PARAMS.format(problem_filepath=problem.name, output_filepath=output.name)
    
def output(output):
    raw = Path(output.name).read_text()
    tour = re.findall(r'TOUR_SECTION([\d\n]*)', raw)[0]
    return sp.array([int(i) for i in re.findall(r'\d+', tour)])

def cycle(distances, verbose=False):
    pd.testing.assert_index_equal(distances.index, distances.columns)
    try:
        files = {n: NamedTemporaryFile('w', delete=False) for n in ['params', 'problem', 'output']}
        
        # Write out the problem specification
        files['problem'].write(problem(distances))        
        files['params'].write(params(**files))

        # Release the file handles
        for f in files.values():
            f.close()

        # Run LKH
        p = Popen(['LKH', files['params'].name], stdout=PIPE, stderr=STDOUT)
        for line in iter(p.stdout.readline, b''):
            if verbose:
                print(line.decode())
        returncode = p.wait()
        if returncode != 0:
            raise IOError('Error while interacting with LKH')
        
        # Fetch the result
        return distances.index[output(files['output']) - 1]
    finally:
        for f in files.values():
            Path(f.name).unlink()
        
def tour(distances, **kwargs):
    augmented = distances.copy()
    augmented = augmented.append(pd.Series(0, augmented.columns, name='dummy'))
    augmented = augmented.T.append(pd.Series(0, augmented.index, name='dummy')).T
    
    t = cycle(augmented, **kwargs)
    
    dummy = sp.nonzero(t == 'dummy')[0][0]   
    c = sp.concatenate([t[dummy+1:], t[:dummy]])
    
    return pd.Index(c)

def seriate(corr):
    """Seriates a correlation matrix.
    
    Args:
        corr: a square dataframe of pairwise correlations
        
    Returns:
        A seriated correlation matrix"""
    
    order = tour(1 - corr)
    return corr.loc[order].loc[:, order]
