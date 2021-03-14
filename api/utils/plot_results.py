import numpy as np
import matplotlib.pyplot as plt

from data import metric_constants, biological_constants

def plot_nitrogen_components(nutrient_matrix, xlabel, ylabels, isConcentrationData=False):
    x_values = np.array([x + 1 for x in range(nutrient_matrix.shape[0])])

    tan = nutrient_matrix[:, 0]
    nox = nutrient_matrix[:, 1]
    micro = nutrient_matrix[:, 2]
    don = nutrient_matrix[:, 4]

    microalgae_nitrogen = micro * biological_constants['MICROALGAE_N_TO_CHL_RATIO']

    ax = plt.subplot(111)
    ax.stackplot(x_values, tan, nox, don, microalgae_nitrogen, labels=['TAN', 'NOx', 'DON', 'Microalgae'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabels[0])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.legend(loc=2)

    return ax

def plot_phosphorous_components(nutrient_matrix, xlabel, ylabels, isConcentrationData=False):
    x_values = np.array([x + 1 for x in range(nutrient_matrix.shape[0])])

    phosphorous = nutrient_matrix[:, 5]
    micro = nutrient_matrix[:, 2]

    microalgae_phosphorous = (micro * biological_constants['MICROALGAE_N_TO_CHL_RATIO']) / biological_constants['MICROALGAE_N_TO_P_RATIO']

    ax = plt.subplot(111)
    ax.stackplot(x_values, phosphorous, microalgae_phosphorous, labels=['dissolved P', 'Microalgae'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabels[1])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.legend(loc=2)

    return ax


def plot_total_suspended_solids(nutrient_matrix, xlabel, ylabels, isConcentrationData=False):
    x_values = np.array([x + 1 for x in range(nutrient_matrix.shape[0])])

    ts = nutrient_matrix[:, 6]

    if isConcentrationData == True:
        TSS_conversion = 1
    else:
        nutrient_matrix = nutrient_matrix / metric_constants['MILLIGRAMS_IN_KG']
        TSS_conversion = 1 / metric_constants['KG_IN_TONNES']

    ax = plt.subplot(111)
    ax.plot(x_values, ts * TSS_conversion, label='total solids', color='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabels[3])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return ax