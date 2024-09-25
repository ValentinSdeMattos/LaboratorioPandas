import pandas as pd
import numpy as np
import datetime as dt

import pandas as pd 

emisiones_2016 = pd.read_csv('emisiones-2016.csv', sep = ';')
emisiones_2017 = pd.read_csv('emisiones-2017.csv', sep = ';')
emisiones_2018 = pd.read_csv('emisiones-2018.csv', sep = ';')
emisiones_2019 = pd.read_csv('emisiones-2019.csv', sep = ';')
emisiones = pd.concat([emisiones_2016, emisiones_2017, emisiones_2018, emisiones_2019])
emisiones

columnas = ['ESTACION', 'MAGNITUD', 'ANO', 'MES']
columnas.extend([col for col in emisiones if col.startswith('D')])
emisiones = emisiones[columnas]
emisiones

emisiones = emisiones.melt(id_vars=['ESTACION', 'MAGNITUD', 'ANO', 'MES'], var_name='DIA', value_name='VALOR')
emisiones
emisiones['DIA'] = emisiones.DIA.str.strip('D')
emisiones['FECHA'] = emisiones.ANO.apply(str) + '/' + emisiones.MES.apply(str) + '/' + emisiones.DIA.apply(str)
emisiones['FECHA'] = pd.to_datetime(emisiones.FECHA, format='%Y/%m/%d', infer_datetime_format=True, errors='coerce')
emisiones

emisiones = emisiones.drop(emisiones[np.isnat(emisiones.FECHA)].index)
emisiones.sort_values(['ESTACION', 'MAGNITUD', 'FECHA'])

print('Estaciones:', emisiones.ESTACION.unique())
print('Contaminantes:', emisiones.MAGNITUD.unique())

def evolucion(estacion, contaminante, desde, hasta):
    return emisiones[(emisiones.ESTACION == estacion) & (emisiones.MAGNITUD == contaminante) & (emisiones.FECHA >= desde) & (emisiones.FECHA <= hasta)].sort_values('FECHA').VALOR
evolucion(56, 8, dt.datetime.strptime('2017/12/21', '%Y/%m/%d'), dt.datetime.strptime('2018/04/13', '%Y/%m/%d'))

emisiones.groupby('MAGNITUD').VALOR.describe()
emisiones.groupby(['ESTACION', 'MAGNITUD']).VALOR.describe()

def resumen(estacion, contaminante):
    return emisiones[(emisiones.ESTACION == estacion) & (emisiones.MAGNITUD == contaminante)].VALOR.describe()

print('Resumen Dióxido de Nitrógeno en Plaza Elíptica:\n', resumen(56, 8),'\n', sep='')
print('Resumen Dióxido de Nitrógeno en Plaza del Carmen:\n', resumen(35, 8), sep='')

def evolucion_mensual(contaminante, año):
    return emisiones[(emisiones.MAGNITUD == contaminante) & (emisiones.ANO == año)].groupby(['ESTACION', 'MES']).VALOR.mean().unstack('MES')

evolucion_mensual(8, 2019)






