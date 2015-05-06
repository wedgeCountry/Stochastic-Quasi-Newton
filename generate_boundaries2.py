"""
    @author : stan

    This script is made to generate sets of points from different
    classes and plot them and boundaries between
"""

import numpy as np
import matplotlib.pyplot as plt

n_set = 4  # number of sets / classes
n_pts = 500  # number of points per class

means = [[2, -2], [-5, 5], [3, 5], [-4, -4]]
cov0 = [[1, 0], [0, 1]]
cov1 = [[5, 3], [3, 5]]
cov2 = [[0, 1], [1, 0]]
cov3 = [[2, 1], [1, 2]]

cov = [cov0, cov1, cov2, cov3]
colors = ['r', 'b', 'y', 'g']

x = []
y = []
X = []

for i in range(0, 4):
    m0 = means[i]
    cov0 = cov[i]
    x0, y0 = np.random.multivariate_normal(m0, cov0, n_pts).T
    x.append(x0)
    y.append(y0)

for i in range(0, 4):
    x0 = x[i]
    y0 = y[i]
    plt.scatter(x0, y0, c=colors[i], edgecolors='none')

# plt.show()

X = np.zeros((n_pts * n_set, 2))
Y = np.zeros((n_pts * n_set))
for i in range(0, n_set):
    x0 = x[i]
    y0 = y[i]
    for j in range(0, n_pts):
        X[j + i * n_pts, :] = [x0[j], y0[j]]
        Y[j + i * n_pts] = i

num_subsamples = int(0.1 * n_pts)

sampled_indexes = [np.random.randint(0, X.shape[0])
                   for i in range(num_subsamples)]

X = np.asarray([X[i] for i in sampled_indexes])
Y = np.asarray([Y[i] for i in sampled_indexes])

print X.shape
print Y.shape

h = .02  # step size in the mesh
from sklearn import svm

# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 10  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C).fit(X, Y)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X, Y)
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X, Y)
lin_svc = svm.LinearSVC(C=C).fit(X, Y)

# create a mesh to plot in
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# title for the plots
titles = ['SVC with linear kernel',
          'LinearSVC (linear kernel)',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 3) kernel']


for i, clf in enumerate((svc, lin_svc, rbf_svc, poly_svc)):
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    plt.subplot(2, 2, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])

plt.show()