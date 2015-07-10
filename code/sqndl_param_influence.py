# -*- coding: utf-8 -*-
"""
Created on Tuesday 9 July

@author: Stanislas Chambon

This scripts implements function to compute dictionaries in parallel
"""

from sqndict import SqnDictionaryLearning
import matplotlib.pyplot as plt
from scipy.misc import lena
from dictionary_learning_test import preprocess_data
from dictionary_learning_test import plot_dictionary
from joblib import Parallel, delayed
import numpy as np


def inner_sqndl(data, params):
    '''
    Performs dictionary learning on data with parameters params

    INPUTS;
    - data
    - params

    OUTPUTS:
    - dictionary learned
    '''

    sdl = SqnDictionaryLearning(n_components=params['n_components'],
                                option=params['option'],
                                alpha=params['alpha'],
                                n_iter=params['n_iter'],
                                max_iter=params['max_iter'],
                                batch_size=params['batch_size'],
                                verbose=params['verbose'])

    print "dictionary attributes"
    sdl.print_attributes()

    print "dictionary learning"
    sdl.fit(data)

    return sdl.components


def parallel_sqndl(data, l_params, n_jobs=1):
    '''
    Performans dictionary learning in parallel

    INPUTS:
    - data
    - l_params : list of params sets to use
    - n_jobs : number of jobs to run in parallel

    OUTPUTS:
    - l_dict : list of dictionary learned
    '''

    l_dict = Parallel(n_jobs=n_jobs)(delayed(inner_sqndl)(data, p)
                                     for p in l_params)

    return l_dict


if __name__ == "__main__":

    # loads data
    data, lena, distorted = preprocess_data(lena)

    # define a list of params sets
    l_params = []
    for n in [1, 5, 10, 15, 20]:
        params = dict(n_components=100,
                      option=None,
                      alpha=0.01,
                      n_iter=n,
                      max_iter=20,
                      batch_size=50,
                      verbose=0)

        l_params.append(params)

    # run parallel dict learning
    l_dict = parallel_sqndl(data, l_params, n_jobs=5)

    # store parameters and dictionaries
    influence = []
    influence.append(l_params)
    influence.append(l_dict)
    np.save('influence_n_iter', influence)

    # plot dictionaries for fun
    for d in l_dict:
        plot_dictionary(d)

    plt.show()
