# python-labelpropagation

Python implementation of label propagation

Inspired by smly's [java-labelpropagation](https://github.com/smly/java-labelpropagation), and implemented in pure python code.

## Install

    python setup.py install

or 

    pip install labelprop


## Usage

initialize labelprop

    from labelprop import LabelProp

    lp = LabelProp()


load data from file

    lp.load_data_from_file('<FILE_NAME>')

load data from memory

    lp.load_data_from_mem('<LOADED_DATA_IN_MEMORY>')

conduct label propagation
    
    """ template

    lp.run(<EPS>, <MAX_ITER>, show_log=<True/False>, clean_result=<True/False>)
        <EPS>: threshold
        <MAX_ITER>: max interation
        show_log: show report
        clean_result: if clean data

    """
    
    # sample
    ans = lp.run(0.00001, 100, show_log=True, clean_result=True) 

## Data Format

### Input Data Format

each line is in list format, c contains

- list[0]: node id
- list[1]: label, use 0 if unknown
- list[2]: list of neighbor nodes with weight

Example

    [1, 0, [[2, 1.0], [3, 1.0]]]
    [2, 1, [[1, 1.0], [3, 1.0]]]
    [3, 0, [[1, 1.0], [2, 1.0], [4, 1.0]]]
    [4, 0, [[3, 1.0], [5, 1.0], [8, 1.0]]]
    [5, 0, [[4, 1.0], [6, 1.0], [7, 1.0]]]
    [6, 2, [[5, 1.0], [7, 1.0]]]
    [7, 0, [[5, 1.0], [6, 1.0]]]
    [8, 0, [[4, 1.0], [9, 1.0]]]
    [9, 2, [[8, 1.0]]]

### Log Information

set show_log as True (default Fasle), like
    
    lp.run(0.00001, 100, show_log=True) 

Example

    Number of vertices:             0
    Number of class labels:         2
    Number of unlabeled vertices:   -3
    Numebr of labeled vertices:     3
    eps:                            1e-05
    max iteration                   100

    iter =  100 , eps =  8.58306884771e-06

### Normal Output Data Format

set clean_result as False, like
    
    lp.run(0.00001, 100, clean_result=False) 

each line is in list format, which contains

- list[0]: node id
- list[1]: predicted label
- list[2:]: list of labels with weight

Example

    [1, 1, [1, 0.8705872816197973], [2, 0.12941033419441167]]
    [2, 1, [1, 1.0], [2, 0.0]]
    [3, 1, [1, 0.7411750400767577], [2, 0.2588211452259766]]
    [4, 2, [1, 0.35293926912195533], [2, 0.6470559625064625]]
    [5, 2, [1, 0.14117504007676362], [2, 0.8588211452259706]]
    [6, 2, [1, 0.0], [2, 1.0]]
    [7, 2, [1, 0.07058728161980515], [2, 0.9294103341944038]]
    [8, 2, [1, 0.1764691577238195], [2, 0.8235270275789148]]
    [9, 2, [1, 0.0], [2, 1.0]]

### Cleaned Output Data Format

set clean_result as True, like
    
    lp.run(0.00001, 100, clean_result=True) 

each line is in list format, which contains

- list[0]: node id
- list[1]: predicted label
- list[2:]: weight for label

Example

    [1, 1, 0.999997615814209]
    [2, 1, 1.0]
    [3, 1, 0.9999961853027344]
    [4, 2, 0.9999952316284177]
    [5, 2, 0.9999961853027343]
    [6, 2, 1.0]
    [7, 2, 0.999997615814209]
    [8, 2, 0.9999961853027344]
    [9, 2, 1.0]







