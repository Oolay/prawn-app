import numpy as np
from scipy.integrate import odeint

from data.constants import sate_variables_names, metric_constants, biological_constants, aquaculture_pond_constants, microalgae_constants
from data.environmental_data import yearly_evap_and_rain_per_ha

class ProductionPond:
    def __init__(self, parameter_store, batch_lag=0, model_rain_and_evaporation=False):
        self.parameters = parameter_store
        self.batch_lag = batch_lag
        self.model_rain_and_evaporation = model_rain_and_evaporation
        self.pond_cycle_water_exchange_matrix = self.__get_pond_cycle_water_exchange_matrix()

        pond_cycle_nutrient_matrix = self.__get_pond_cycle_nutrient_matrix()

        self.pond_cycle_nutrient_conc_matrix = pond_cycle_nutrient_matrix[:, :7] # TODO replace magic mumber
        self.pond_cycle_nutrient_pool_matrix = pond_cycle_nutrient_matrix[:, 7:]


    def __get_daily_feed(self, day_of_pond_cycle):
        total_feed_input_per_crop = self.parameters.total_feed_input_pond_crop

        if day_of_pond_cycle <= 30:
            return (total_feed_input_per_crop * 0.02) / 30

        if day_of_pond_cycle <= 60:
            return (total_feed_input_per_crop * 0.05) / 30

        if day_of_pond_cycle <= 90:
            return (total_feed_input_per_crop * 0.13) / 30

        if day_of_pond_cycle <= 120:
            return (total_feed_input_per_crop * 0.20) / 30

        if day_of_pond_cycle <= 180:
            return (total_feed_input_per_crop * 0.30) / 30
        
        return 0


    def __get_daily_total_N_waste(self, day_of_pond_cycle):
        return (
            self.__get_daily_feed(day_of_pond_cycle) * metric_constants['MILLIGRAMS_IN_TONNE'] * self.parameters.proportion_of_N_in_feed * aquaculture_pond_constants['TOTAL_FEED_N_WASTE_PROPORTION']
        ) / self.parameters.pond_volume_litres


    def __get_daily_total_P_in_feed(self, day_of_pond_cycle):
            return (
                self.__get_daily_feed(day_of_pond_cycle) * metric_constants['MILLIGRAMS_IN_TONNE'] * biological_constants['PROPORTION_P_IN_FEED']
            ) / self.parameters.pond_volume_litres


    def __get_daily_exchange_rate(self, day_of_pond_cycle):
        # no exchange on first and last day of pond cycle
        if (day_of_pond_cycle == 1) | (day_of_pond_cycle == self.parameters.pond_cycle_length_days):
            return 0

        return self.parameters.daily_exchange_rate_proportion


    def __get_microalge_growth_rate(self, tan, nox, p, micro_chl):
        N_limitation = (tan + nox) / ((tan + nox) + microalgae_constants['Ks_n'])  # Burford and Lorenzen 2004
        P_limitation = p / (p + microalgae_constants['Ks_p'])

        k = microalgae_constants['K_CHL'] * micro_chl + microalgae_constants['K_OTHER'] # Burford and Lorenzen 2004, light absorbtion
        light_limitation = (np.exp(1) / k) * (np.exp((-microalgae_constants['Io_Isat_RATIO']) *
                            np.exp(-k * self.parameters.pond_depth_metres)) - np.exp(-microalgae_constants['Io_Isat_RATIO']))
        
        return microalgae_constants['MAX_GROWTH_RATE'] * light_limitation * N_limitation * P_limitation


    def __get_net_water_volume_change(self, day_of_pond_cycle):
        if self.batch_lag + day_of_pond_cycle > metric_constants['DAYS_IN_YEAR']:
            return yearly_evap_and_rain_per_ha[int((self.batch_lag + day_of_pond_cycle) - metric_constants['DAYS_IN_YEAR'])] * self.parameters.pond_area_ha

        return yearly_evap_and_rain_per_ha[int(self.batch_lag + day_of_pond_cycle)] * self.parameters.pond_area_ha


    def __get_rain_overflow_volume(self, net_water_volume_change):
        if net_water_volume_change < 0:
            return 0

        return net_water_volume_change


    def __get_evaporation_topup_volume(self, net_water_volume_change):
        if net_water_volume_change < 0:
            return net_water_volume_change * -1

        return 0


    def __model_single_pond(self, pond_nutrient_concentrations, day_of_pond_cycle):
        tan = pond_nutrient_concentrations[0]  # conc of tan mg/L
        nox = pond_nutrient_concentrations[1]  # conc of nox mg/L
        micro_chl = pond_nutrient_concentrations[2]  # conc of microalgae mg/L
        sed_n = pond_nutrient_concentrations[3]  # mass of sediment N mg/L 
        don = pond_nutrient_concentrations[4]  # conc of don mg/L
        p = pond_nutrient_concentrations[5]  # conc of phosphorous mg/L
        ts = pond_nutrient_concentrations[6]  # total solids

        total_N_waste_t = self.__get_daily_total_N_waste(day_of_pond_cycle)
        total_feed_p_t = self.__get_daily_total_P_in_feed(day_of_pond_cycle)

        daily_exchange_rate = self.__get_daily_exchange_rate(day_of_pond_cycle)

        microalgae_growth_rate = self.__get_microalge_growth_rate(tan, nox, p, micro_chl)
     
        net_water_volume_change = self.__get_net_water_volume_change(day_of_pond_cycle) if self.model_rain_and_evaporation else 0

        rain_overflow_vol = self.__get_rain_overflow_volume(net_water_volume_change)
        evap_top_up_volume = self.__get_evaporation_topup_volume(net_water_volume_change)

        volume_change = self.parameters.pond_volume_litres / (self.parameters.pond_volume_litres + rain_overflow_vol) # this only needs to deal with rain surplus, change caused by evap dealt with by top-up
        topup = evap_top_up_volume / (self.parameters.pond_volume_litres + net_water_volume_change) # ratio of evap top up with pond vol
        overflow = rain_overflow_vol / (self.parameters.pond_volume_litres + net_water_volume_change)

        # state changes
        dtandt = (aquaculture_pond_constants['TAN_PRODUCTION_DAILY_RATE'] * total_N_waste_t) \
            + (aquaculture_pond_constants['REMINERALISATION_DAILY_RATE'] * sed_n) \
            + ((daily_exchange_rate + topup) * self.parameters.background_water_tan_mg_L) \
            - ((aquaculture_pond_constants['NITRIFICATION_DAILY_RATE'] + aquaculture_pond_constants['VOLATILISATION_OF_NH4_DAILY_RATE'] + daily_exchange_rate) * tan) \
            - (microalgae_growth_rate * biological_constants['MICROALGAE_N_TO_CHL_RATIO'] * micro_chl * (tan / (tan + nox))) \
            + ((volume_change - 1) * tan)

        dnoxdt = (aquaculture_pond_constants['NITRIFICATION_DAILY_RATE'] * tan) \
            + ((daily_exchange_rate + topup) * self.parameters.background_water_nox_mg_L) \
            - (daily_exchange_rate * nox) \
            - (microalgae_growth_rate * biological_constants['MICROALGAE_N_TO_CHL_RATIO'] * micro_chl * (nox / (nox + tan))) \
            + ((volume_change - 1) * nox)

        dmicro_chldt = (microalgae_growth_rate * micro_chl) \
            + ((daily_exchange_rate + topup) * self.parameters.background_water_micro_chl_mg_L) \
            - ((daily_exchange_rate + microalgae_constants['SEDIMENTATION_DAILY_RATE']) * micro_chl) \
            + ((volume_change - 1) * micro_chl)
        
        dsed_ndt = (microalgae_constants['SEDIMENTATION_DAILY_RATE'] * biological_constants['MICROALGAE_N_TO_CHL_RATIO'] * micro_chl) \
            - (aquaculture_pond_constants['REMINERALISATION_DAILY_RATE'] * sed_n)
        
        ddondt = ((1 - aquaculture_pond_constants['TAN_PRODUCTION_DAILY_RATE']) * total_N_waste_t) \
            + ((daily_exchange_rate + topup) * self.parameters.background_water_don_mg_L) \
            - (daily_exchange_rate * don) \
            + ((volume_change - 1) * don)
        
        dpdt = (total_feed_p_t * aquaculture_pond_constants['PROPORTION_OF_DAILY_FEED_P_TO_WATER']) \
            + ((daily_exchange_rate + topup) * self.parameters.background_water_p_mg_L) \
            - (daily_exchange_rate * p) \
            - ((microalgae_growth_rate * biological_constants['MICROALGAE_N_TO_CHL_RATIO'] * micro_chl) / biological_constants['MICROALGAE_N_TO_P_RATIO']) \
            + ((volume_change - 1) * p)
        
        dtsdt = self.parameters.daily_total_suspended_solids_production \
                + ((daily_exchange_rate + topup) * self.parameters.background_water_tss_mg_L) \
                - (daily_exchange_rate * ts) \
                + ((volume_change - 1) * ts)
        
        
        # keep track of discharge pools
        dnvoldt = aquaculture_pond_constants['VOLATILISATION_OF_NH4_DAILY_RATE'] * tan
        dtan_discharge_pooldt = (daily_exchange_rate + overflow) * tan
        dnox_discharge_pooldt = (daily_exchange_rate + overflow) * nox
        dmicro_chl_discharge_pooldt = (daily_exchange_rate + overflow) * micro_chl
        ddon_discharge_pooldt = (daily_exchange_rate + overflow) * don
        dp_discharge_pooldt = (daily_exchange_rate + overflow) * p
        dts_discharge_pooldt = (daily_exchange_rate + overflow) * ts

        return [dtandt, dnoxdt,  dmicro_chldt, dsed_ndt, ddondt, dpdt, dtsdt, dnvoldt, dtan_discharge_pooldt, dnox_discharge_pooldt, \
            dmicro_chl_discharge_pooldt, ddon_discharge_pooldt, dp_discharge_pooldt, dts_discharge_pooldt]


    def __get_pond_cycle_water_exchange_matrix(self):
        days_without_water_exchange = 1  # no exchange on first day
        days_for_harvest = 1 # whole pond drained on last day only
        pond_cycle_days_with_normal_water_exchange =  self.parameters.pond_cycle_length_days - (days_without_water_exchange + days_for_harvest)

        return np.concatenate(
            (
                np.zeros(days_without_water_exchange),
                np.full(pond_cycle_days_with_normal_water_exchange, self.parameters.daily_exchange_rate_proportion),
                np.full(days_for_harvest, self.parameters.harvest_day_exchange_rate_proportion),
            )
        )

    def __get_pond_cycle_nutrient_matrix(self):
        days_of_pond_cycle = np.array([x + 1 for x in range(self.parameters.pond_cycle_length_days)])

        return odeint(
            self.__model_single_pond,
            self.parameters.initial_pond_model_state,
            days_of_pond_cycle,
        )


    def __convert_pond_cycle_matrix_to_yearly_matrix(self, pond_cycle_matrix, batch_lag):
        """ Convert a pond cycle matrix to a yearly matrix
        
        [pond_cycle_days, cols] --> [days_in_year, cols]
        """

        number_of_columns = pond_cycle_matrix.shape[1] if len(pond_cycle_matrix.shape) == 2 else None

        last_day_of_pond_cycle = batch_lag + self.parameters.pond_cycle_length_days
        number_of_days_in_year_not_in_pond_cycle = metric_constants['DAYS_IN_YEAR'] - self.parameters.pond_cycle_length_days

        # case where pond still in operation at end of year and over laps into following year
        if last_day_of_pond_cycle > metric_constants['DAYS_IN_YEAR']:
            days_overlapping_into_following_year = last_day_of_pond_cycle - metric_constants['DAYS_IN_YEAR']
            split_day = self.parameters.pond_cycle_length_days - days_overlapping_into_following_year

            pond_cycle_matrix_days_not_operating = np.zeros((number_of_days_in_year_not_in_pond_cycle, number_of_columns)) if number_of_columns \
                else np.zeros((number_of_days_in_year_not_in_pond_cycle,))

            # [days_in_year, ]
            yearly_nutrient_matrix = np.concatenate(
                (
                    pond_cycle_matrix[split_day:,],
                    pond_cycle_matrix_days_not_operating,
                    pond_cycle_matrix[:split_day,]
                )
            )

            return yearly_nutrient_matrix

        # case where pond does not overflow into folowing year
        days_in_year_after_pond_cycle = number_of_days_in_year_not_in_pond_cycle - batch_lag

        pond_cycle_matrix_days_not_operating_before_pond_start = np.zeros((batch_lag, number_of_columns)) if number_of_columns \
            else np.zeros((batch_lag, ))
        pond_cycle_matrix_days_not_operating_after_pond_finish = np.zeros((days_in_year_after_pond_cycle, number_of_columns)) if number_of_columns \
            else np.zeros((days_in_year_after_pond_cycle, ))
        
        yearly_nutrient_matrix = np.concatenate(
            (
                pond_cycle_matrix_days_not_operating_before_pond_start,
                pond_cycle_matrix,
                pond_cycle_matrix_days_not_operating_after_pond_finish
            )
        )

        return yearly_nutrient_matrix


    def get_net_yearly_rain_and_evaporation_volume(self, batch_lag):
        '''returns array with with the net volume exchanged from rain and evaporation of year for pond'''
        # used to make the volume of exchange for the days the pond is not operating equal to 0
        days_pond_not_operating_adjustment =  self.__convert_pond_cycle_matrix_to_yearly_matrix(
            np.ones(self.parameters.pond_cycle_length_days),
            batch_lag
        )

        return yearly_evap_and_rain_per_ha * self.parameters.pond_area_ha * days_pond_not_operating_adjustment



    def get_yearly_water_exchange_matrix(self, batch_lag=None):
        '''get 1D water exchange volume matrix in context of year

        Returns
        
        pond_yearly_water_exchange_matix: array, shape(days_in_year,)
        '''

        batch_lag_for_yearly_matrix = batch_lag if batch_lag else self.batch_lag

        pond_yearly_water_exchange_matrix = self.__convert_pond_cycle_matrix_to_yearly_matrix(self.pond_cycle_water_exchange_matrix, batch_lag_for_yearly_matrix)

        return pond_yearly_water_exchange_matrix * self.parameters.pond_volume_litres


    def get_yearly_nutrient_conc_matrix(self, batch_lag=None):
        '''get the nutrient concentration matrix in context of year

        Returns
        
        pond_yearly_nutrient_matix: array, shape(days_in_year, number_of_state_variables)
        '''

        batch_lag_for_yearly_matrix = batch_lag if batch_lag else self.batch_lag

        if self.pond_cycle_nutrient_conc_matrix is None:
            # TODO handle exception when nutrient matrix not set
            return

        pond_yearly_nutrient_matrix = self.__convert_pond_cycle_matrix_to_yearly_matrix(self.pond_cycle_nutrient_conc_matrix, batch_lag_for_yearly_matrix)

        return pond_yearly_nutrient_matrix


    def get_yearly_nutrient_pool_matrix(self, batch_lag=None):
        '''get the nutrient pool quantity matrix in context of year

        Returns
        
        pond_yearly_nutrient_matix: array, shape(days_in_year, number_of_state_variables)
        '''

        batch_lag_for_yearly_matrix = batch_lag if batch_lag else self.batch_lag

        if self.pond_cycle_nutrient_pool_matrix is None:
            # TODO handle exception when nutrient matrix not set
            return

        pond_yearly_nutrient_matrix = self.__convert_pond_cycle_matrix_to_yearly_matrix(self.pond_cycle_nutrient_pool_matrix, batch_lag_for_yearly_matrix)

        return pond_yearly_nutrient_matrix