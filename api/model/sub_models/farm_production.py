import numpy as np

from data import sate_variables_names, metric_constants, biological_constants, aquaculture_pond_constants, microalgae_constants
from .production_pond import ProductionPond

class FarmProduction:
    def __init__(self, parameter_store, model_rain_and_evaporation_at_pond_level=False):
        self.pond = ProductionPond(parameter_store)
        self.parameters = parameter_store
        self.yearly_production_outputs = self.__get_farm_yearly_production_matrices(parameter_store)

        self.yearly_nutrient_concentration = self.yearly_production_outputs['nutrient_concentration']

        self.yearly_water_volume = self.yearly_production_outputs['water_volume']
        self.yearly_nutrient_discharge = self.yearly_production_outputs['nutrient_discharge']
        self.yearly_topup_volume = self.yearly_production_outputs['topup_volume']


    def __get_farm_yearly_production_matrices(self, model_rain_and_evaporation_at_pond_level=False):
            ''' set the yearly farm production nutrient concentration, nutrient discharge, and water
            volume discharge matrices.
            '''
            batch_lags = [x for x in range(self.parameters.stocking_period_days)]

            if model_rain_and_evaporation_at_pond_level:
                # TODO
                pass

            # initialise yearly cumulative matrices
            number_of_nutrients_modelled = len([nutrient for nutrient in sate_variables_names['STATE_VARIABLES'] if nutrient['location'] == 'pond'])
            cumulative_pond_nutrient_concentration_matrix = np.zeros((metric_constants['DAYS_IN_YEAR'], number_of_nutrients_modelled))
            cumulative_batch_water_exchange_volume_matrix = np.zeros((metric_constants['DAYS_IN_YEAR']))
            cumulative_batch_nutrient_exchange_matrix = np.zeros((metric_constants['DAYS_IN_YEAR'], number_of_nutrients_modelled))

            for batch_lag in batch_lags:
                # add batch nutrient concentration
                pond_nutrient_concentration_matrix = self.pond.get_yearly_nutrient_conc_matrix(batch_lag)
                cumulative_pond_nutrient_concentration_matrix += pond_nutrient_concentration_matrix

                # over flow and top-up
                net_rain_and_evaporation_volume_for_batch = self.pond.get_net_yearly_rain_and_evaporation_volume(batch_lag) * self.parameters.batch_size_ha
                overflow_volume = np.array([0 if volume < 0 else volume for volume in net_rain_and_evaporation_volume_for_batch])
                topup_volume = np.array([0 if volume > 0 else volume for volume in net_rain_and_evaporation_volume_for_batch])

                # add batch water volume flow
                yearly_water_exchange_volume_for_batch = self.pond.get_yearly_water_exchange_matrix(batch_lag) * self.parameters.batch_size_ha
                yearly_all_water_volume_for_batch = yearly_water_exchange_volume_for_batch + overflow_volume
                cumulative_batch_water_exchange_volume_matrix += yearly_all_water_volume_for_batch

                # add batch nutrient exchange
                cumulative_batch_nutrient_exchange_matrix += (pond_nutrient_concentration_matrix.T * yearly_all_water_volume_for_batch).T

            # average concentration
            mean_farm_nutrient_concentration_matrix = np.array(cumulative_pond_nutrient_concentration_matrix / self.parameters.stocking_period_days)

            return {
                'nutrient_concentration': mean_farm_nutrient_concentration_matrix,
                'water_volume': cumulative_batch_water_exchange_volume_matrix,
                'nutrient_discharge': cumulative_batch_nutrient_exchange_matrix,
                'topup_volume': topup_volume,
            }

    def get_active_area(self, day):
        if day <= self.parameters.stocking_period_days:
            return (self.parameters.total_crop_production_area / self.parameters.stocking_period_days) * day
        if day > self.parameters.stocking_period_days + self.parameters.pond_cycle_length_days:
            return 0
        if day >= self.parameters.pond_cycle_length_days + 1:
            return self.parameters.total_crop_production_area \
            - ((self.parameters.total_crop_production_area / self.parameters.stocking_period_days) * (day - self.parameters.pond_cycle_length_days))

        return self.parameters.total_crop_production_area

