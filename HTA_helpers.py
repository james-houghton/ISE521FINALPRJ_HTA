"""
Creates list of Timestamps evenly distributed at the given frequency

Input
-----
frequency: Integer value defining interval size in minutes for aggregating EPB data into time blocks

Output
------
time_list: List of Timestamps for binning EPB records into time blocks.
"""
def gen_times_list(bin_type):

    def gen_hourly():
        time_list = []
        for time in pd.date_range('2018-11-06 07:00:00', '2018-11-06 21:00:00', freq='60 Min'):
            time_list.extend(pd.date_range(time, freq='1H', periods=1).strftime("%Y-%m-%d %H:%M:%S").tolist())
        return time_list

    def agg_times_list ():
        time_0 = '2018-11-06 07:00:00' #start
        time_1a = '2018-11-06 10:00:00' #10am
        time_2a = '2018-11-06 12:00:00' #12am
        time_3 = '2018-11-06 14:00:00' #2pm
        time_4 = '2018-11-06 16:00:00' #4pm
        time_5 = '2018-11-06 18:00:00' #6pm
        time_6 = '2018-11-06 21:00:00' #9pm
        return list([time_0,time_1a,time_2a,time_3,time_4,time_5,time_6])

    if bin_type == 'hourly':
        return gen_hourly()
    else:
        return agg_times_list()

def gen_counts(voter_data,bin_type):
    usrVoter_data = voter_data
    usrBin_type = bin_type


    #import voter_data from static file

    #precincts = p_list




#def compute_voter_counts(EPB_count_data,time_list):
