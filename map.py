import webbrowser
import numpy as np
import math
import os
import gmplot
import AlgorithmFactory
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
'''def create_map_plot(city = (['ALL', 'BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']), 
                          pin = (['HEAT', 'SCATTER']), 
                           slider = slider):'''

class MapPlot():
        '''
        
        '''
        map_data_mod = {}
        slider = widgets.IntSlider(value = 30, min = 5, max = 50, step = 5, 
                              description = "clusters num", continuous_update=False, readout = True)
        def input_data(self, map_data):
            self.map_data_mod = map_data
            self.map_data_mod['CMPLNT_FR_TM'] = self.map_data_mod['CMPLNT_FR_TM'].str.split(':').str[0]
            self.map_data_mod['CMPLNT_FR_DT'] = self.map_data_mod['CMPLNT_FR_DT'].str.split('/').str[0] + '/' + self.map_data_mod['CMPLNT_FR_DT'].str.split('/').str[2]

            self.map_data_mod = self.map_data_mod.loc[(self.map_data_mod['CMPLNT_FR_DT'].str.split('/').str[1] == '2022')]
            self.map_data_mod = self.map_data_mod.loc[(self.map_data_mod['CMPLNT_FR_DT'].str.split('/').str[0] == '09')]     
            
            
        
        def create_map_plot(self):
            @interact
            def map_plot(city = (['ALL', 'BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']), 
                                      pin = (['HEAT', 'SCATTER']), 
                                       slider = self.slider):
                curr_data = self.map_data_mod
                first_place = "New York, USA"
                if city != 'ALL':
                    curr_data = curr_data.loc[curr_data['BORO_NM'] == city]
                    first_place = city + ", USA"
                min_num = len(curr_data)
                min_num = min(1000, len(curr_data))
                curr_data = curr_data.sample(n = min_num, replace = False)

                coords = np.array(curr_data[['Latitude', 'Longitude']], dtype='float64')
                mask = np.any(np.isnan(coords) | np.equal(coords, 0), axis=1)
                coords[~mask]
                for i in range(len(coords)):
                    if math.isnan (coords[i][1]):
                        print(i)
                        print(coords[i])
                        print('have null')
                up = slider
                Ks = range(1, up)
                algorithmFactory = AlgorithmFactory.create("kmean")
                kmean = algorithmFactory.calculate(up, Ks, coords)
                lat_list = []
                long_list = []

                for i in range(len(kmean)):
                    lat_list.append(kmean[up - 2].cluster_centers_[i][0])
                    long_list.append(kmean[up - 2].cluster_centers_[i][1])
                