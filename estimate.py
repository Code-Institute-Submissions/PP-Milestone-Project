## Assign specific estimators to the given scores

def estimate_score(score):

    if score in (11111, 11121):
        result = ['Naive Bayes', 'LinearSVC']
    elif score in (11112, 11122):
        result = ['KNeighbors Classifier', 'Kernel SVC', 'RandomForest Classifier']
    elif score in (11211, 11222, 11221, 11212):
        result = ["SGD Classifier", "Kernel Approximation"]
    elif score in (12112, 12111):
        result =  ["KMeans-Classifier", "GMM"]
    elif score in (12212, 12211):
        result = ["MiniBatch KMeans"]
    elif score in (12121, 12122):
        result = ["Get more data"]
    elif score in (12221, 12222):
        result = ["MeanShift", "VBGMM"]
    elif score in (21212,	21221,	21222,	21211,  22211,	22212,	22221,  22222):
        result = ["SGD Regressor"]
    elif score in (21112,	21121, 	21122,	21111,  22111,	22112,	22121,  22122):
        result = ["ElasticNet", "Kernel SVR", "RandomForest Regressor"]
    elif score in (31111, 31112,  31122,  31121,  32111,  32112,  32122,  32121):
        result = ["Kernel PCA", "Linear Discriminant Analysis"]
    elif score in (31211, 31212,  31222,  31221,  32211,  32212,  32222,  32221):
        result = ["Isomap", "Spectral Embedding"]
    else:
        result = ["Please answer all the questions"]
    return result    