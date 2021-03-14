import numpy as np
import pandas as pd

from data import sate_variables_names 

def nutrient_matrix_to_dataframe(matrix):
    ''' convert a nutrient matrix with the nutrient state variables as columns to a DF'''
    return pd.DataFrame(matrix, columns=[variable['name'] for variable in sate_variables_names['STATE_VARIABLES'] if variable['location'] == 'pond'])