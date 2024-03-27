
import numpy as np
from sklearn.cluster import KMeans
import tqdm

def get_centroids(data, num_centroids: int):
    kmeans = KMeans(n_clusters = num_centroids)
    kmeans.fit(data)
    centroids = kmeans.cluster_centers_
    return centroids

def get_cluster_id(data, centroids):
    closest_centroids = []
    for p in tqdm.tqdm(np.array(data)):
        ps = np.vstack(len(centroids)*[p.tolist()])
        dists = np.sqrt(np.square(ps - centroids).sum(-1))
        closest_centroid = np.argmin(dists)
        closest_centroids.append(closest_centroid)
    return closest_centroids