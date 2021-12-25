from scipy.sparse.csgraph import laplacian
from sklearn.cluster import SpectralClustering
import numpy as np
import matplotlib.pyplot as plt

class SpectralCommunityDetector():
    def __init__(self):
        pass

    def get_eigenvalues(self, adj_mat):
        L = laplacian(adj_mat, normed=False)
        eigval, eighvec = np.linalg.eigh(L)
        return eigval, eighvec

if __name__ == '__main__':
    graph = np.array([
        [0, 1, 1, 0, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    ])

    obj = SpectralCommunityDetector()
    eigvals, _ = obj.get_eigenvalues(graph)
    print(f'Laplacian eigenvalues: {eigvals}')
    plt.plot(eigvals)
    plt.show()