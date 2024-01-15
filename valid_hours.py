
import numpy as np
import pandas as pd
import geopandas as gpd

class stats_valid_hours_madrid:
    """
    Class used to represent Madrid's valid and invalid air quality measurements.
    This info should be obtained from Madrid's open data website.

    Attributes
    ----------
    valid_hours : pd.Series
        a pandas Series with valid measurements.
    unvalid_lectures : pd.Series
        a pandas Series with valid measurements.
    """

    def __init__(self, df, option = 1) -> pd.DataFrame:

        """ 
        Parameters
        ----------
        df : pd.DataFrame
           a pandas DataFrame with hourly measurements. The DataFrame is 
           expected to be like the ones delivered by Madrid's open data webpage:
            https://datos.madrid.es/portal/site/egob
        option : int
            possibility to choose the values time span.
            Option 1 takes all valid values
            Option 2 takes only nighttime hours
            Option 3 takes only daytime hours

        """
        #get columns of interest only from H1 and V1 to H24 and V24
        idx_hours_valid = df.columns[6:54]

        #get columns of interest daytime and nighttime
        # nighttime
        idx1_morning = df.columns[6:18]
        idx2_night = df.columns[44:54]
        idx2_nighttime = idx1_morning.union(idx2_night, sort = False)  

        # daytime
        idx_daytime = df.columns[18:44]

        #lists to store values
        valid_hours_lectures = []
        unvalid_hours_lectures = []

        if option == 1:
            cols = idx_hours_valid
        elif option == 2:
            cols = idx2_nighttime
        else:
            cols = idx_daytime

        #loop around rows
        for (row_index, rowData) in df[cols].iterrows():
            # change type to float and change validate values to -1 and 1
            string_array = rowData.values.astype(str)
            #print(len(rowData.values) == len(string_array))
            string_array = np.char.replace(string_array, 'V', '1')
            string_array = np.char.replace(string_array, 'N', '-1')
            float_array = string_array.astype(float)

            #lists that will hold values and loop
            valid_lectures = []
            unvalid_lectures = []
            for i, val in enumerate(float_array):
                lecture = val * float_array[i+1]                #this multiplies the values by the validity, 1 if is valid 0 otherwise
                valid_lectures.append(lecture)                  #values are included in the valid lectures list
                unvalid_lectures.append(float_array[i])         #list with validity equal to zero
                if i == (len(float_array)-2):                   # break to get out of the loop when i+1 is out of index
                    break
            valid_lectures = valid_lectures[::2]                #keeps H*V not V*H
            unvalid_lectures = unvalid_lectures[1::2]
            negative_count = unvalid_lectures.count(-1)         #count of lectures that are 0 and valid
            unvalid_lectures = [-1] * negative_count
            valid_lectures = [i for i in valid_lectures if i > 0]
            #print(valid_lectures)
            valid_hours_lectures.append(valid_lectures)
            unvalid_hours_lectures.append(unvalid_lectures)


        self.valid_hours = pd.Series(valid_hours_lectures)
        self.unvalid_lectures = pd.Series(unvalid_hours_lectures)

class stats_valid_hours_eeuu:

    """
    Class used to represent Europe's valid air quality measurements.
    
      Attributes
    ----------
    valid_hours : pd.Series
    a pandas Series with valid measurements.
       
        
    """
    def __init__(self, df):

        """
        Parameters
        ----------
        df : pd.DataFrame
           a pandas DataFrame with hourly measurements. The DataFrame
            is expected to be like the ones delivered by the EEA in this webpage:
            https://discomap.eea.europa.eu/map/fme/AirQualityExport.htm.

        """

        #change date columns to datetime
        df.loc[:,'DatetimeBegin'] = pd.to_datetime(df['DatetimeBegin'])
        idx_hours_valid = df.loc[df['Validity'] == 1][['DatetimeBegin', 'AirPollutant', 'AirQualityStationEoICode','Concentration']]

        self.valid_hours = idx_hours_valid