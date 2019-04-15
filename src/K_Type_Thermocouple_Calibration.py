'''
Austen K. Scruggs
02/15/2019
Description: Takes thermocouple mV converts to Celsius by linear fit
'''

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

# directory where calibration data is held
calibration_data_directory = '/home/austen/media/winshare/Groups/Smith_G/Austen/Projects/Thermodenuder/Thermocouples/'
save_directory = '/home/austen/Documents/'

# import calibration data
calibration_data = pd.read_csv(calibration_data_directory + 'K-Type Table.csv', sep=',', header=0)
calibration_2darray = np.array(calibration_data)

# get data frame dimensions and create index arrays
df_dims = calibration_data.shape
nrows = int(df_dims[0])
ncols = int(df_dims[1])
row_index = np.arange(0, nrows, 1)
col_index = np.arange(1, ncols, 1)

# preallocate arrays
celsius_array =[]
mV_array = []

# for loop to create flattened arrays, creating mV space and temperature space
for row in row_index:
    for col in col_index:
        mV_array.append(calibration_2darray[row][col])
        celsius_array.append(calibration_2darray[row][0] + col)

x = sm.add_constant(mV_array)
y = celsius_array
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())
prstd, iv_l, iv_u = wls_prediction_std(results)
y_fit = [(X * results.params[1]) + results.params[0] for X in mV_array]
R2 = 10000
R1 = 1000
Gain = 1 + (R2/R1)
key_temperatures = np.array([0.0, 25.0, 100.0, 200.0, 300.0])
key_mV = ((key_temperatures - (results.params[0])) / (results.params[1])) * Gain
print(key_mV)

fig0, ax0 = plt.subplots()
ax0.plot(mV_array, celsius_array, ls='', marker='.', color='black', label='Calibration Data')
ax0.plot(mV_array, results.fittedvalues, ls='', marker='.', color='red', label="OLS Predicted")
ax0.plot(mV_array, y_fit, ls='-', color='blue', label='fit: y = ' + str(results.params[1]) + 'x + ' + str(results.params[0]))
ax0.plot(mV_array, iv_u, color='green', ls='--', label='Confidence Intervals')
ax0.plot(mV_array, iv_l, color='green', ls='--')
ax0.set_xlabel('mV')
ax0.set_ylabel('\u00b0 C')
ax0.set_title('K-Type Thermocouple Calibration \n Millivolts to Celsius')
ax0.grid(True)
ax0.legend(loc=1)
plt.tight_layout()
plt.savefig(save_directory + 'Thermocouple_Calibration_Curve.pdf', format='pdf')
plt.savefig(save_directory + 'Thermocouple_Calibration_Curve.png', format='png')
plt.show()

fig1, ax1 = plt.subplots()
ax1.plot(np.array(mV_array) * Gain, np.array(y_fit), ls='-', color='orange', label='Gain Curve')
ax1.plot(key_mV, key_temperatures, ls='', marker='x', color='red', label='Gain Curve: Key Temperatures')
ax1.set_xlabel('mV')
ax1.set_ylabel('\u00b0 C')
ax1.set_title('K-Type Thermocouple Calibration w Gain \n Millivolts to Celsius')
ax1.grid(True)
ax1.legend(loc=1)
plt.tight_layout()
plt.savefig(save_directory + 'Thermocouple_Calibration_GainCurve.pdf', format='pdf')
plt.savefig(save_directory + 'Thermocouple_Calibration_GainCurve.png', format='png')
plt.show()


