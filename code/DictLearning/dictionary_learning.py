"""
    @Stan
    Implementation of online dictionary learning algorithms 1 and 2

    DONE :
    - algorithm1
    - structure of algorithm2
    - mini batch
    - add a stopping criterion for while loop in algorithm2
    - test convergence criterion (cf renormalisation)
    - initial dictionary in early steps of algo1
    - Implementation with a .fit method = class ?
    - test it on scikit learn ex.
    - write test dictionary learning script


    TODO :
    - add a verbose function
    - selection of best regularization parameter or inscrease batch size
    - select option : SQN or normal where would be the access point ?
    - should I add a runtime attribute ? => maybe not yet, maybe not here
"""


import numpy as np
import math


class StochasticDictionaryLearning:
    '''
    This class implements dictionary learning

    Attributes:
    - n_components
    - option, select SQN method or normal method
    - l, regularization parameter
    - n_iter, int, number of iterations
    - eta, int, mini batch size
    - verbose, int, control verbosity of algorithm


    Methods:
    __init__ :
    fit :
    set_params :
    get_params :
    print_attributes ?

    '''

    def __init__(self, n_components=100, option=None,
                 l=0.001, n_iter=30, eta=100, verbose=0):
        self.n_components = n_components
        self.option = option  # select whether SQN method should be used
        self.l = l
        self.n_iter = n_iter
        self.eta = eta
        self.verbose = verbose

    def fit(self, X):
        '''
        This methods runs dictionary learning algorithms on data X

        INPUTS:
        - self
        - X : (n_samples, m) array like, data

        OUTPUTS:
        - D : (m, k) array like, learned dictionary
        '''

        D = algorithm1(X,
                       n_components=self.n_components,
                       l=self.l,
                       n_iter=self.n_iter,
                       eta=self.eta,
                       verbose=self.verbose)
        return D


def algorithm1(x, n_components=100, l=0.01, n_iter=30, eta=3, verbose=0):
    '''
    Online dictionary learning algorithm

    INPUTS:
    - x : (n_samples, m) array like, data
    - l, regularization parameter
    - n_components, number of components of dictionary
    - n_iter, int, number of iterations
    - eta, int, mini batch size
    - verbose, int, control verbosity of algorithm

    OUTPUTS:
    - D : (m, k) array like, learned dictionary
    '''

    n_s = len(x[:, 0])  # number of samples in x

    D = np.random.rand(len(x[0, :]), n_components)  # initial dictionary
    print D.shape

    # Dimensions of dicitonary
    [m, k] = D.shape

    # 1: initialization
    A = np.zeros((k, k))
    B = np.zeros((m, k))

    '''
    First iteration in a while loop so that matrix A in not empty
    - if empty => change l
    - if empty => change batch size

    So that we ensure that no problem occurs in algo2
    '''

    '''
    Loop
    for t in range(2, n_iter + 1):

    '''

    # 2: Loop
    for t in range(1, n_iter + 1):

        # 3: Draw xj from x
        j = np.random.randint(0, n_s, eta)
        xt = x[j, :]
        xt = np.asmatrix(xt).T

        # 4: Sparse coding with LARS
        from sklearn.linear_model import LassoLars
        lars = LassoLars(alpha=l)
        # Lars LassoLars

        lars.fit(D, xt)
        alpha = lars.coef_
        alpha = (np.asmatrix(alpha)).T

        # computing coefficient beta for step 5/6
        if t < eta:
            theta = float(t * eta)
        else:
            theta = math.pow(eta, 2) + t - eta

        beta = (theta + 1 - eta) / (theta + 1)

        # 5: Update A
        a = np.zeros((k, k))
        for i in range(0, eta):
            a = a + (alpha[:, i]).dot(alpha[:, i].T)
        A = beta * A + a

        # 6: Update B
        b = np.zeros((m, k))
        for i in range(0, eta):
            b = b + xt[:, i].dot(alpha[:, i].T)
        B = beta * B + b

        # Compute new dictionary update
        D = algorithm2(D, A, B)

    # 9 : Return learned dictionary
    return D


def algorithm2(D, A, B, c_max=3, eps=0.00001):
    '''
    Dictionary update

    INPUTS:
    - D, (m, k), input dictionary
    - A, (k, k)
    - B, (m, k)
    - c_max, int, max number of iterations
    - eps, float, stopping criterion

    OUTPUT:
    - D, updated dictionary
    '''

    m = len(D[:, 0])
    k = len(D[0, :])

    c = 0  # counter
    cv = False  # convergence or stop indicator

    # 2: loop to update each column
    while cv is not True:

        # keep a trace of previous dictionary
        D_old = np.zeros((m, k))
        for i in range(0, m):
            for j in range(0, k):
                D_old[i, j] = D[i, j]

        for j in range(0, k):

            # 3: Update the j-th column of d
            u = (1 / A[j, j]) * (B[:, j] - D.dot(A[:, j]))
            u = u + np.asmatrix(D[:, j]).T

            # renormalisation
            renorm = max(np.linalg.norm(u), 1)
            u = np.divide(u, renorm)

            for p in range(0, m):
                D[p, j] = u[p]

        # counter update
        c = c + 1

        # compute differences between two updates
        grad = D - D_old
        crit = np.linalg.norm(grad)

        # check convergence
        if crit < eps:
            cv = True
        if c > c_max:
            cv = True

    if c == c_max:
        print "Dictionary Updating Algo reached max number of iterations"
        print "Consider higher max number of interations"

    # 6: Return updated dictionary
    return D


if __name__ == "__main__":
    sdl = StochasticDictionaryLearning()
    # algorithm1(x)

    '''
    Testing is not here anymore
    '''
