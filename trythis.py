from scipy import interpolate
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np
import math

def get_dydx(x_list, y_list):
    test_output = []
    for index in range(0,len(x_list)-1):
        slope = (y_list[index+1] - y_list[index])/(x_list[index+1] - x_list[index])
        test_output.append(slope)
    test_output.append(slope)
    return np.array(test_output)

classa = 31
classes = [32,33,34,35,36,37,38,39,40,47,49,50,51,52,53,54,55,56,57,59,60,67,69,70,71,73,74,76,77,79,80,81,82,84,89,90,91,97]
langs = ['Linear']
dicts = {k:[] for k in langs}
for classa in classes:
    data = pd.read_pickle("class_"+str(classa)+".0.pkl")
    new_data = data.groupby("MMSI").apply(np.array)
    new_data = new_data.reset_index()
    X = new_data[0]
    total_LAT_error = []
    total_LON_error = []
    final_LAT = []
    final_LON = []
    kinds= langs
    for interpolation_type in kinds:
        total_LAT_error = []
        total_LON_error = []
        #print("Trying " + interpolation_type)
        for row in X:
            time_series = np.array(row[:,1:6], dtype=np.float64)
            #print(time_series)
            time_series = time_series[np.argsort(time_series[:,0])]
            time_series = time_series.T
            time = time_series[0]
            LAT = time_series[1]
            LON = time_series[2]
            try:
                COG = get_dydx(time, LAT)
            except Exception as e:
                continue
            LAT_removed = LAT[1::3]
            LON_removed = LON[1::3]
            COG_removed = COG[1::3]
            time_removed = time[1::3]
            #print(np.arange(4,LAT.size, 5))
            #print(type(LAT), type(COG))
            if(LAT.size != LON.size or LON.size != COG.size or COG.size != time.size):
                print("CRAP")
                exit(1)
            LAT_test = np.delete(LAT, np.arange(1, LAT.size, 3))
            LON_test = np.delete(LON, np.arange(1, LON.size, 3))
            COG_test = np.delete(COG, np.arange(1, COG.size, 3))
            time_test = np.delete(time, np.arange(1, time.size, 3))
            try:
                
                f = interpolate.CubicHermiteSpline(time_test, LAT_test, COG_test, extrapolate=True)
                error = mean_absolute_error(f(time_removed.astype(np.float)), LAT_removed.astype(np.float))
                total_LAT_error.append(error)
                f = interpolate.CubicHermiteSpline(time_test, LON_test, COG_test, extrapolate=True)
                error = mean_absolute_error(f(time_removed.astype(np.float)), LON_removed.astype(np.float))
                
                #print(f(time_removed.astype(np.float)))
                #print(error)
                total_LON_error.append(error)
            except Exception as e:
                #print(e)
                continue
        final_LAT.append(np.mean(total_LAT_error))
        final_LON.append(np.mean(total_LON_error))
    print(classa, final_LAT, final_LON)
for k in dicts:
    print(k,dicts[k])
