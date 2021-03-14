import numpy as np

sate_variables_names = {
    'STATE_VARIABLES': [
        {'name': 'tan', 'type': 'nitrogen', 'location': 'pond'},
        {'name': 'nox', 'type': 'nitrogen', 'location': 'pond'},
        {'name': 'micro_chl_n', 'type': 'chlorophyl', 'location': 'pond'},
        {'name': 'sediment_n', 'type': 'solids', 'location': 'pond'},
        {'name': 'don', 'type': 'nitrogen', 'location': 'pond'},
        {'name': 'p', 'type': 'phosphorous', 'location': 'pond'},
        {'name': 'tss', 'type': 'solids', 'location': 'pond'},
        {'name': 'VOLITISED_N', 'type': 'nitrogen', 'location': 'pool'},
        {'name': 'TAN_DISCHARGE_POOL', 'type': 'nitrogen', 'location': 'pool'},
        {'name': 'NOX_DISCHARGE_POOL', 'type': 'nitrogen', 'location': 'pool'},
        {'name': 'MICROALGAE_CHL_DISCHARGE_POOL', 'type': 'chlorophyl', 'location': 'pool'},
        {'name': 'DON_DISCHARGE_POOL', 'type': 'nitrogen', 'location': 'pool'},
        {'name': 'P_DISCHARGE_POOL', 'type': 'phosphorous', 'location': 'pool'},
        {'name': 'TSS_DISCHARGE_POOL', 'type': 'solids', 'location': 'pool'},
    ], # the nutrient concentrations of interest (all as mg/L of pond water)
}

metric_constants = {
    'MILIMETRES_IN_METRE': 1000,
    'METERS_IN_HECTARES': 10000,
    'LITRES_IN_M3': 1000,
    'LITRES_IN_MEGALITRE': 1000000,
    'GRAMS_IN_KG': 1000,
    'KG_IN_TONNES': 1000,
    'MILLIGRAMS_IN_TONNE': 1000000000,
    'MILLIGRAMS_IN_KG': 1000000,
    'MILLIGRAMS_IN_GRAM': 1000,
    'DAYS_IN_YEAR': 365,
    'DAYS_IN_WEEK': 7,
}

biological_constants = {
    'MICROALGAE_N_TO_CHL_RATIO': 13,
    'MICROALGAE_N_TO_P_RATIO': 16,
    'PROPORTION_N_IN_PROTEIN': 0.16,
    'PROPORTION_P_IN_FEED': 0.015, # Jackson et al 2003
}

aquaculture_pond_constants = {
    'REMINERALISATION_DAILY_RATE': 0.06, # remineralisaion rate of TAN as a proportion of total N in the sed per day - Burford and Lorenzen 2004
    'NITRIFICATION_DAILY_RATE': 0.15,  # nitrification rate per day - Burford and Lorenzen 2004
    'VOLATILISATION_OF_NH4_DAILY_RATE': 0.05, # volatilisation rate of ammonia per day - Burford and Lorenzen 2004
    'TAN_PRODUCTION_DAILY_RATE': 0.9, # q_tan
    'TOTAL_FEED_N_WASTE_PROPORTION': 0.78, # proportion of feed N not harvested in the prawn biomass - Jackson et al 2003
    'PROPORTION_OF_DAILY_FEED_P_TO_WATER': 0.911, # feed p that ends up in water - Teichert-Coddington et al 2000, the rest goes to the prawns (8.9 %)
    'TOTAL_SOLID_PROD_TONNES_CYCLE_HA': 204,  # Funge-Smith and Briggs 1998
    'PROPORTION_SOLIDS_TO_POND': 0.972, # Funge-Smith and Briggs 1998 - CHECK THIS DESCRIPTION
    'PROPORTION_OF_DAILY_POND_SOLIDS_TO_SUSPENDED_SOLIDS': 0.036, # Funge-Smith and Briggs 1998 - CHECK THIS DESCRIPTION
}

microalgae_constants = {
    'SEDIMENTATION_DAILY_RATE': 0.5,  # sedimentation rate of microalgae - Burford and Lorenzen 2004
    'MAX_GROWTH_RATE': 1.45, # micro max growth rate per day - Burford and Lorenzen 2004
    'N_TO_CHL_RATIO': 13, # nitrogen to chl ratio in algae - Burford and Lorenzen 2004
    'N_TO_P_MICRO': 16, # Redford ratio
    'K_CHL': 14, # Burford and Lorenzen 2004
    'K_OTHER': 2.5,  # Burford and Lorenzen 2004
    'Ks_n': 0.008,  # Burford and Lorenzen 2004
    'Ks_p': 0.00042,  # Lorenzen et al 1997
    'Io_Isat_RATIO': 2.4,  # Burford and Lorenzen 2004
}

settlement_pond_constants = {
    'DAILY_REDUCTION_RATES': {
        'nitrogen': 1 - np.sqrt(1 - 0.21),  # Jackson et al 2003
        'phosphorous': 1 - np.sqrt(1 - 0.33),  # Jackson et al 2003
        'solids': 1 - np.sqrt(1 - 0.6), # Jackson et al 2003
    },
}
        