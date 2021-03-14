from data.constants import metric_constants, biological_constants, aquaculture_pond_constants

class ParameterStore:    
    def __init__(self, input_parameters):
        # input parameters
        self.pond_area_ha = input_parameters['pond_area_ha']
        self.pond_depth_metres = input_parameters['pond_depth_metres']
        self.pond_cycle_length_days = input_parameters['pond_cycle_length_days']
        self.total_crop_production_area = input_parameters['total_crop_production_area']
        self.production_output_tonnes_ha_crop = input_parameters['production_output_tonnes_ha_crop']
        self.fcr = input_parameters['fcr']
        self.prop_production_area_as_settlement = input_parameters['prop_production_area_as_settlement']
        self.settlement_pond_mean_depth = input_parameters['settlement_pond_mean_depth']
        self.stocking_period_days = input_parameters['stocking_period_days']
        self.batch_number = input_parameters['batch_number']
        self.proportion_protein_in_feed = input_parameters['proportion_protein_in_feed']
        self.daily_exchange_rate_proportion = input_parameters['daily_exchange_rate_proportion']
        self.harvest_day_exchange_rate_proportion = input_parameters['harvest_day_exchange_rate_proportion']
        self.background_water_tan_mg_L = input_parameters['background_water_tan_mg_L']
        self.background_water_nox_mg_L = input_parameters['background_water_nox_mg_L']
        self.background_water_don_mg_L = input_parameters['background_water_don_mg_L']
        self.background_water_micro_chl_mg_L = input_parameters['background_water_micro_chl_mg_L']
        self.background_water_p_mg_L = input_parameters['background_water_p_mg_L']
        self.background_water_tss_mg_L = input_parameters['background_water_tss_mg_L']
        self.initial_pond_micro_chl_mg_L = input_parameters['initial_pond_micro_chl_mg_L']
        self.initial_settlement_pond_tss_mg_L = input_parameters['initial_settlement_pond_tss_mg_L']

        # calculated parameters
        self.batch_size_ha = self.total_crop_production_area / self.stocking_period_days

        self.production_output_tonnes_pond_crop = self.production_output_tonnes_ha_crop * self.pond_area_ha
        self.pond_volume_litres = self.pond_area_ha * metric_constants['METERS_IN_HECTARES'] * self.pond_depth_metres * metric_constants['LITRES_IN_M3']
        self.total_feed_input_pond_crop = self.production_output_tonnes_pond_crop * self.fcr
        self.proportion_of_N_in_feed = self.proportion_protein_in_feed * biological_constants['PROPORTION_N_IN_PROTEIN']
        self.daily_total_suspended_solids_production = (
            (
                (
                    aquaculture_pond_constants['TOTAL_SOLID_PROD_TONNES_CYCLE_HA']
                    * aquaculture_pond_constants['PROPORTION_SOLIDS_TO_POND']
                    * metric_constants['MILLIGRAMS_IN_TONNE']
                    * aquaculture_pond_constants['PROPORTION_OF_DAILY_POND_SOLIDS_TO_SUSPENDED_SOLIDS']
                )
                / self.pond_cycle_length_days
            )
            / (self.pond_area_ha * metric_constants['METERS_IN_HECTARES'] * self.pond_depth_metres * metric_constants['LITRES_IN_M3'])
        )
            
        # initial state parameters in order of sate_variables_names 
        self.initial_pond_model_state = [
            self.background_water_tan_mg_L,
            self.background_water_nox_mg_L,
            self.initial_pond_micro_chl_mg_L,
            0,
            self.background_water_don_mg_L,
            self.background_water_p_mg_L,
            self.background_water_tss_mg_L,
            0, 0, 0 ,0, 0, 0, 0,
        ]

        # settlement pond parameters
        self.settlement_pond_volume_litres = self.total_crop_production_area * self.prop_production_area_as_settlement * \
            metric_constants['METERS_IN_HECTARES'] * self.settlement_pond_mean_depth * metric_constants['LITRES_IN_M3']
        self.initial_settlement_pond_nutrients_mg_L = [
            self.background_water_tan_mg_L,
            self.background_water_nox_mg_L,
            self.initial_pond_micro_chl_mg_L,
            0,
            self.background_water_don_mg_L,
            self.background_water_p_mg_L,
            self.initial_settlement_pond_tss_mg_L,
        ]
