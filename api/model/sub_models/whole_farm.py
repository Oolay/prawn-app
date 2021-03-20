import numpy as np

from data.environmental_data import yearly_evap_and_rain_per_ha
from data import ParameterStore
from data.constants import (
    metric_constants,
    biological_constants,
    aquaculture_pond_constants,
    microalgae_constants,
    settlement_pond_constants,
)
from .production_pond import ProductionPond
from .farm_production import FarmProduction
from utils import nutrient_matrix_to_dataframe, plot_nitrogen_components, plot_phosphorous_components, plot_total_suspended_solids

class WholeFarm:
    def __init__(self, input_parameters):
        self.parameters = ParameterStore(input_parameters)
        self.farm_production = FarmProduction(self.parameters)
        self.pond = self.farm_production.pond


    def get_total_settlement_pond_area(self, active_farm_production_area, staggered_area=False):
        settlement_pond_operation_thresholds = [
            (83, 25),
            (150, 45),
            (273, 81),
        ] # (production_area, settlement_pond area)

        if staggered_area == None:
            return active_farm_production_area * 0.3

        for threshold, area in settlement_pond_operation_thresholds:
            if active_farm_production_area <= threshold:
                return area

        # TODO consider sorting these from smallest to largest
        largest_threshold, largest_threshold_settlement_area = settlement_pond_operation_thresholds[-1]

        return largest_threshold_settlement_area + ((active_farm_production_area - largest_threshold) * 0.3)


    def get_whole_farm_nutrient_output(self):
        day = 1

        settlement_reduction_rates = settlement_pond_constants['DAILY_REDUCTION_RATES']

        settlement_reduction_vector = np.array([
            settlement_reduction_rates['nitrogen'],
            settlement_reduction_rates['nitrogen'],
            settlement_reduction_rates['solids'],
            settlement_reduction_rates['nitrogen'],
            settlement_reduction_rates['nitrogen'],
            settlement_reduction_rates['phosphorous'],
            settlement_reduction_rates['solids'],
        ])

        initial_settlement_pond_area = self.get_total_settlement_pond_area(self.farm_production.get_active_area(1))

        settlement_pond_total_nutrients = np.array(self.parameters.initial_settlement_pond_nutrients_mg_L) \
            * initial_settlement_pond_area \
            * metric_constants['METERS_IN_HECTARES'] \
            * self.parameters.settlement_pond_mean_depth \
            * metric_constants['LITRES_IN_M3']

        discharge_conc = []
        discharge_total = []
        discharge_vol = []

        for total_day_nutrients, volume, rain_and_evaporation_mm in zip(self.farm_production.yearly_nutrient_discharge, self.farm_production.yearly_water_volume, yearly_evap_and_rain_per_ha):

            settlement_pond_area = self.get_total_settlement_pond_area(self.farm_production.get_active_area(day))
            settlement_pond_vol_L = settlement_pond_area \
                * metric_constants['METERS_IN_HECTARES'] \
                * self.parameters.settlement_pond_mean_depth \
                * metric_constants['LITRES_IN_M3']
            settlement_pond_rain_and_evaporation_L = settlement_pond_area \
                * metric_constants['METERS_IN_HECTARES'] \
                * (rain_and_evaporation_mm / metric_constants['MILIMETRES_IN_METRE']) \
                * metric_constants['LITRES_IN_M3']
            settlement_pond_vol_L += settlement_pond_rain_and_evaporation_L
            settlement_pond_total_nutrients += total_day_nutrients
            settlement_pond_conc_nutrients = settlement_pond_total_nutrients \
                / (settlement_pond_vol_L + volume)

            # settlement pond reduction
            settlement_pond_total_nutrients -= (settlement_pond_conc_nutrients * settlement_reduction_vector) \
                * (settlement_pond_vol_L + volume)

            new_settlement_pond_conc_nutrients = settlement_pond_total_nutrients \
                / (settlement_pond_vol_L + volume)

            water_discharge = volume + settlement_pond_rain_and_evaporation_L

            if water_discharge < 0:
                water_discharge = 0

            settlement_pond_leaving_nutrients = new_settlement_pond_conc_nutrients * water_discharge
            settlement_pond_total_nutrients -= settlement_pond_leaving_nutrients
            discharge_conc.append(new_settlement_pond_conc_nutrients)
            discharge_total.append(settlement_pond_leaving_nutrients)
            discharge_vol.append(water_discharge)

            day += 1

        return {
            'discharge_conc': np.array(discharge_conc), 
            'discharge_total': np.array(discharge_total), 
            'discharge_vol': np.array(discharge_vol),
        }


    def get_single_pond_nitrogen_plot(self):
        single_pond_nutrient_conc = self.pond.pond_cycle_nutrient_conc_matrix

        nitrogen_plot = plot_nitrogen_components(
            single_pond_nutrient_conc, 
            xlabel='Day of annual production cycle',
            ylabels=['Concentration as N (mg/L)', 'P concentration (mg/L)', 'Microalgae concentration as N (mg/L)', 'TSS concentration (mg/L)'],
            isConcentrationData=True
        )

        return nitrogen_plot


    def get_single_pond_phosphorous_plot(self):
        single_pond_nutrient_conc = self.pond.pond_cycle_nutrient_conc_matrix

        nitrogen_plot = plot_phosphorous_components(
            single_pond_nutrient_conc, 
            xlabel='Day of annual production cycle',
            ylabels=['Concentration as N (mg/L)', 'P concentration (mg/L)', 'Microalgae concentration as N (mg/L)', 'TSS concentration (mg/L)'],
            isConcentrationData=True
        )

        return nitrogen_plot


    def get_single_pond_total_suspended_solids_plot(self):
        single_pond_nutrient_conc = self.pond.pond_cycle_nutrient_conc_matrix

        nitrogen_plot = plot_total_suspended_solids(
            single_pond_nutrient_conc, 
            xlabel='Day of annual production cycle',
            ylabels=['Concentration as N (mg/L)', 'P concentration (mg/L)', 'Microalgae concentration as N (mg/L)', 'TSS concentration (mg/L)'],
            isConcentrationData=True
        )

        return nitrogen_plot