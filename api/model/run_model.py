import matplotlib.pyplot as plt
import pandas as pd

from data import ParameterStore
from model import WholeFarm
from utils import nutrient_matrix_to_dataframe

input_parameters = {
    'pond_area_ha': 1,
    'pond_depth_metres': 1.5,
    'pond_cycle_length_days': 180,
    'total_crop_production_area': 403,
    'production_output_tonnes_ha_crop': 10,
    'fcr': 1.5,
    'prop_production_area_as_settlement': 0.3,
    'settlement_pond_mean_depth': 1.5,
    'stocking_period_days': 168,
    'batch_number': 168,
    'proportion_protein_in_feed': 0.47,
    'daily_exchange_rate_proportion': 0.02,
    'harvest_day_exchange_rate_proportion': 1,
    'background_water_tan_mg_L': 0.059,
    'background_water_nox_mg_L': 0.059,
    'background_water_don_mg_L': 0.029,
    'background_water_micro_chl_mg_L': 0,
    'background_water_p_mg_L': 0.00677,
    'background_water_tss_mg_L': 40.33,
    'initial_pond_micro_chl_mg_L': 0.0013,
    'initial_settlement_pond_tss_mg_L': 18,
}

def run_whole_farm_model():
    farm = WholeFarm(input_parameters)

    # single pond
    single_pond_nutrient_conc = farm.pond.pond_cycle_nutrient_conc_matrix

    # single_pond_nitrogen_plot = farm.get_single_pond_nitrogen_plot()
    # plt.show()

    # single_pond_phosphorous_plot = farm.get_single_pond_phosphorous_plot()
    # plt.show()

    yearly_production_farm_nutrient_concentration = farm.farm_production.yearly_nutrient_concentration

    farm_output = farm.get_whole_farm_nutrient_output()

    conc_json = nutrient_matrix_to_dataframe(farm_output['discharge_conc']).to_json()
    print(conc_json)
    # nutrient_matrix_to_dataframe(farm_output['discharge_total']).to_csv('discharge_total.csv')
    # nutrient_matrix_to_dataframe(farm_output['discharge_vol']).to_csv('discharge_vol.csv')
    # nutrient_matrix_to_dataframe(farm_output['discharge_conc']).to_csv('discharge_conc.csv')
if __name__ == "__main__":    
    run_whole_farm_model()
