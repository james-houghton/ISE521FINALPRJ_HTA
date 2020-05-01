#import copy_pd_Poll_Pads as cp
import pandas as pd
import numpy as np
from statsmodels.stats import diagnostic as ts
#pushed to main file at 3:30 on 8/5


def gen_times_list(frequency):
    #****frequency defaults to mins. Enter value as number
    freq = str(frequency) + 'Min'
    #freq = freq
    time_list = []
    for time in pd.date_range('2018-11-06 07:00:00', '2018-11-06 22:00:00', freq=freq):
        time_list.extend(pd.date_range(time, freq='1H', periods=1).strftime("%Y-%m-%d %H:%M:%S").tolist())
    return time_list


def gen_dataFrame(path):
    #pv_log =  pd.read_csv(path, index_col = False, parse_dates = ['Times'],  error_bad_lines=False)
    pv_log =  pd.read_csv(path, index_col = False, parse_dates = ['checkin_time'],  error_bad_lines=False)

    #need to find permanate name for headers
    #ts = pd.Series(pv_log['Times'])
    ts = pd.Series(pv_log['checkin_time'])
    #build in logic to adjust DateOffset for Daylight savings time
    ts = pd.to_datetime(ts) + pd.DateOffset(hours=-5)
    PName =pd.Series(pv_log['location'],dtype=object)
    PP = pd.Series(pv_log['device'],dtype=object)
    #P_Code = pd.Series(pv_log['p_code'],dtype=object)
    P_Code = pd.Series(pv_log['precinct'],dtype=object)
    df = pd.DataFrame( {'DateTime': ts,'PName':PName, 'Poll Pad':PP, 'P_Code':P_Code} )
    return df


def get_precinct_codes(df):
    df = df.groupby('PName').head(1)
    p = pd.Series(df['P_Code']).tolist()
    return p


def precinct_filter(df,precinct):
    #may be able to remove next line
    precinct = precinct
    df = df[df['P_Code'] == precinct ]
    return df


def CI_by_Precinct(input_df,precinct_list,time_list):


    df = input_df
    precincts = precinct_list
    times = time_list

    #Filter rows by precinct and get CI_counts for each interval
    precinct_counts = []
    for i in range(len(precincts)):
        #apply filter
        precinct_i = precinct_filter(df, precincts[i]);
        temp_total = 0
        counts = []
        for j in range(len(times)):
            count = len(precinct_i[precinct_i.DateTime < times[j]]) - temp_total
            counts.append(count)
            temp_total += count
        #pass filtered df for sampling
        precinct_counts.append(counts)

    results_df = pd.DataFrame(precinct_counts, index = precincts , columns = times)
    results_df = results_df.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, by=None)
    return results_df

def CI_df(results_df,frequency):
    df = results_df
    #****frequency defaults to mins. Enter value as number
    freq = str(frequency) + 'Min'
    #freq = frequency
    df_T = df.T
    t = pd.DatetimeIndex(pd.date_range('2018-11-06 07:00:00', '2018-11-06 22:00:00', freq=freq))
    df2 = pd.DataFrame(df_T, index = t)
    return df2

#----------------------------------------------------------------------------------
#Ljung Box test scripts
def signifigant_precincts(output_df, frequency):
    df = output_df
    #****frequency defaults to mins. Enter value as number
    freq = str(frequency) + 'Min'
    #freq=freq
    signifigant_precinct_list = []

    precincts = np.asarray(df.index.values, dtype = int).tolist()

    t = pd.DatetimeIndex(pd.date_range('2018-11-06 07:00:00', '2018-11-06 22:00:00', freq=freq))
    df_T = df.T

    for precinct in precincts:
        df= pd.Series(df_T[precinct])
        #df2 = pd.DataFrame(input_df, index = t)
        df2 = pd.DataFrame(df, index = t)
        x = ts.acorr_ljungbox(df2)

        y = pd.Series(x[1]).tolist()
        yt =pd.Series(x[1]).min()

        if yt < .05:
            #print(precinct)
            signifigant_precinct_list.append(precinct)
    #print(len(signifigant_precinct_list))

    #define filter_df in init area
    #filtered_df = df_T.filter(items = signifigant_precinct_list )
    return signifigant_precinct_list

def filter_df(df,list):
    df = df
    list = list

    #added lines to shift index and fill NAN at end
    df2 = df.shift(-1)
    df2 = df2.fillna(0)
    filtered_df= df2.filter(items = list)
    return filtered_df


class test_ePoll_log:

    def __init__(self,file_path, frequency):

        self.path = file_path
        self.freq = frequency
        #freq = str(frequency) + 'Min'

        self.time_list = gen_times_list(self.freq)
        self.input_df = gen_dataFrame(self.path)
        self.precinct_list = get_precinct_codes(self.input_df)
        self.output_df = CI_by_Precinct(self.input_df, self.precinct_list,self.time_list)
        self.CI_df = CI_df(self.output_df,self.freq)
        self.significant_precincts_list = signifigant_precincts(self.output_df, self.freq)


        self.significant_precincts_df = filter_df(self.CI_df,self.significant_precincts_list)



#current thought is to use this class to store above listed attributes
#will be called in other scripts with example below

#new_df = test_ePoll_log()
#df1 = pd.DataFrame(new_df.precinct_counts, index = new_df.time_list)
