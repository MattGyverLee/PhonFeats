#from Levenshtein import distance

#better?
## https://stackoverflow.com/questions/35171710/how-to-group-words-whose-levenshtein-distance-is-more-than-80-percent-in-python 

# Current
# https://stackoverflow.com/questions/38720283/python-string-clustering-with-scikit-learns-dbscan-using-levenshtein-distance

#https://stackoverflow.com/questions/13769242/clustering-words-into-groups

#https://online.stat.psu.edu/stat555/node/86/#:~:text=Clustering%20starts%20by%20computing%20a,is%20distance%20zero%20from%20itself).
#https://www.w3schools.com/python/python_ml_hierarchial_clustering.asp#:~:text=Hierarchical%20clustering%20is%20an%20unsupervised,need%20a%20%22target%22%20variable.
#https://stackoverflow.com/questions/36949795/string-clustering-in-python
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage
#https://stackoverflow.com/questions/66884270/text-data-clustering-with-python
#https://pypi.org/project/fuzzup/
#https://stackoverflow.com/questions/38720283/python-string-clustering-with-scikit-learns-dbscan-using-levenshtein-distance
#https://stackoverflow.com/questions/35171710/how-to-group-words-whose-levenshtein-distance-is-more-than-80-percent-in-python
#https://scikit-learn-extra.readthedocs.io/en/stable/auto_examples/plot_kmedoids.html#sphx-glr-auto-examples-plot-kmedoids-py
#https://www.kaggle.com/code/leomauro/text-clustering-grouping-texts
from panphon import distance
import numpy as np
import matplotlib.pyplot as plt
from sklearn_extra.cluster import KMedoids
import numpy as np

data = ["dfa", "dfe", "dfo", "lfm", "lfn", "bo"]
dst = distance.Distance()
def lev_metric(x, y):
    i, j = int(x[0]), int(y[0])     # extract indices
    return dst.weighted_feature_edit_distance(data[i], data[j])

X = np.arange(len(data)).reshape(-1, 1)
kmedoids = KMedoids(n_clusters=3, random_state=0, metric=lev_metric).fit(X)
labels = kmedoids.labels_
print(kmedoids.cluster_centers_)
unique_labels = set(labels)
colors = [
    plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))
]
for k, col in zip(unique_labels, colors):

    class_member_mask = labels == k

    xy = X[class_member_mask]
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=6,
    )

plt.plot(
    kmedoids.cluster_centers_[:, 0],
    kmedoids.cluster_centers_[:, 1],
    "o",
    markerfacecolor="cyan",
    markeredgecolor="k",
    markersize=6,
)

plt.title("KMedoids clustering. Medoids are represented in cyan.")

#The labels/centers are in

#kmedoids.labels_
#kmedoids.cluster_centers_