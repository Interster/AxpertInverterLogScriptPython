

stringvaninverter = '2020-08-23 17:14:33.243004,233.8 49.9 233.8 49.9 0210 0138 004 418 52.00 000 100 0048 0000 000.0 00.00 00001 00010101 00 00 00000 110'
lysvaninverter = stringvaninverter.split(',')
lysgetalle = lysvaninverter[1].split(' ')

# Dit gee:
# Grid voltage, Grid frequency, AC output voltage, AC output frequency,
#['233.8', '49.9', '233.8', '49.9', '0210', '0138', '004', '418', '52.00', '000', '100', '0048', '0000', '000.0', '00.00', '00001', '00010101', '00', '00', '00000', '110']
# Breek dit op in stukke:
#
# 0 Grid voltage, 1 Grid frequency, 2 AC output voltage, 3 AC output frequency,
# ['233.8', '49.9', '233.8', '49.9',
# 4 AC output apparent power, 5 AC output active power
#'0210', '0138',
# 6 Output load percent, 7 BUS voltage, 8 Battery voltage, 9 Battery charging current
#'004', '418', '52.00', '000',
# 10 Battery capacity, 11 Inverter heat sink temperature, 
#'100', '0048',
# 12 PV Input current 1, 13 PV Input voltage 1, 
#'0000', '000.0',
# 14 Battery voltage from SCC 1, 15 Battery discharge current
#'00.00', '00001',
# 16 Device status, 17 Battery voltage offset for fans on, 18 EEPROM version
#'00010101', '00', '00',
# 19 PV Charging power 1, 20 Device status
#'00000', '110']

print('PV charing power ' + lysgetalle[19])
# Druk nou die waarde wat na 'n getal verander is
print(int(lysgetalle[19]))
print('AC output active power ' + lysgetalle[5])
print(int(lysgetalle[19]))
