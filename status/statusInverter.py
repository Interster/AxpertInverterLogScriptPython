import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Axpert.out', skiprows=1, names=['Date', 'Time', 'Grid voltage', 
                    'Grid frequency', 'AC output voltage', 'AC output frequency', 
                    'AC output apparent power', 'AC output active power', 
                    'Output load percent', 'Bus voltage', 'Battery voltage', 
                    'Battery charging current', 'Battery capacity', 
                    'Inverter heat sink temperature', 'PV input current for battery', 
                    'PV input voltage 1', 'Battery voltage from SCC', 
                    'Battery discharge current', 'Device status 1', 
                    'Battery voltage offset for fans on', 'EEPROM version', 
                    'PV charging power', 
                    'Device status 2'],
                    sep=' ', engine='python')

print('Datum: ' + str(str(df['Date'].iloc[-1])) + '  Tyd: ' + str(df['Time'].iloc[-1]))
print('')
print('Grid voltage: ' + str(str(df['Grid voltage'].iloc[-1])) + 
      '[V] Groter as nul, dan is lynkrag aan')
print('Las drywing: ' + str(str(df['AC output active power'].iloc[-1])) + '[W]')
print('Panele drywing: ' + str(str(df['PV charging power'].iloc[-1])) + '[W]')