GREEN_RED = [
    [0.0, 'rgb(83, 153, 15)'],
    [0.1111111111111111, 'rgb(42, 195, 23)'],
    [0.2222222222222222, 'rgb(19, 197, 67)'],
    [0.3333333333333333, 'rgb(119, 229, 34)'],
    [0.4444444444444444, 'rgb(161, 243, 27)'],
    [0.5555555555555556, 'rgb(210, 220, 20)'],
    [0.6666666666666666, 'rgb(202, 194, 27)'],
    [0.7777777777777778, 'rgb(215, 135, 36)'],
    [0.8888888888888888, 'rgb(220, 91, 24)'],
    [1.0, 'rgb(205, 23, 23)']
]

VALID_COLUMNS = [
     'AÑO_ACCIDENTE', 'MES_ACCIDENTE', 'DIA_ACCIDENTE',
     'GRAVEDAD_ACCIDENTE', 'CLASE_ACCIDENTE', 'CANT_HERIDOS_EN _SITIO_ACCIDENTE',
     'CANT_MUERTOS_EN _SITIO_ACCIDENTE',  'POT', 'PIEZA_URBANA', 'BUS_SUBIDA', 'BUS_BAJADA', 'TRAFICO', 
     'ES_FESTIVO', 'TIPO_FESTIVO', 'DIA_DEL_AÑO', 'SEMANA_DEL_AÑO', 'CUATRIMESTRE_DEL_AÑO', 'JUNIOR_LOCAL', 'JUNIOR_VISITANTE', 
     'JUNIOR_GANO', 'RELEVANCIA_PARTIDO', 'HIPOTESIS_ACCIDENTE', 
     'VEHICULO_NO_REGISTRA',  'hour', 'month', 'month_name', 'day of week', 'day', 'day_name'
]

VALID_COLUMNS_DICT = {
     'YEAR':'AÑO_ACCIDENTE', 'MONTH':'MES_ACCIDENTE', 'DAY':'DIA_ACCIDENTE',
     'SEVERITY':'GRAVEDAD_ACCIDENTE', 'ACCIDENT CLASS':'CLASE_ACCIDENTE', 'WOUNDED PERSONS':'CANT_HERIDOS_EN _SITIO_ACCIDENTE',
     'CASUALTIES':'CANT_MUERTOS_EN _SITIO_ACCIDENTE',  'POT':'POT', 'ZONE':'PIEZA_URBANA', 'TRAFFIC':'TRAFICO', 
     'IS HOLIDAY':'ES_FESTIVO', 'HOLIDAY TYPE':'TIPO_FESTIVO', 'DAY':'DIA_DEL_AÑO', 'WEEK':'SEMANA_DEL_AÑO', 'QUARTER':'CUATRIMESTRE_DEL_AÑO',
     'TEAM HOME':'JUNIOR_LOCAL', 'TEAM AWAY':'JUNIOR_VISITANTE', 'TEAM RESULT':'JUNIOR_GANO', 'MATCH IMPORTANCE':'RELEVANCIA_PARTIDO', 
     'ACCIDENT TYPE':'HIPOTESIS_ACCIDENTE', 'HOUR':'SOLO_HORA', 'WEEK DAY':'day of week' }

'''

'SITIO_EXACTO_ACCIDENTE',
'LONGITUD', 
'LATITUD',
'VEHICULO_AUTOMOVIL', 'VEHICULO_CAMIONETA', 'VEHICULO_BUS', 'VEHICULO_CAMION', 'VEHICULO_CAMPERO', 'VEHICULO_BUSETA', 'VEHICULO_BICICLETA', 
     'VEHICULO_MICROBUS', 'VEHICULO_TRACTO_CAMION', 'VEHICULO_VOLQUETA', 'VEHICULO_MOTOCARRO', 'VEHICULO_DESCONOCIDO', 'VEHICULO_CUATRIMOTO', 
     'VEHICULO_MAQUINARIA_AGRICOLA', 'VEHICULO_TRACCION_ANIMAL', 'VEHICULO_MAQUIRIA_INDUSTRIAL', 'VEHICULO_CAMION_RNMA', 'VEHICULO_DUMPER_VOLQUETAARTICULADA', 
     'VEHICULO_REMOLQUE', 'VEHICULO_SEMIREMOLQUE', 'VEHICULO_RETROEXCAVADORA', 'VEHICULO_MONTACARGAS', 'VEHICULO_BUS_ARTICULADO', 'VEHICULO_MINICARGADOR', 'VEHICULO_MINI_EXCAVADORA', 
     'VEHICULO_MOTOCICLETA', 'RESULTADO_LOCAL', 'RESULTADO_VISITANTE', 'C_TRAFICO', 'ID', 'impact-e', 'legend', 'date_time','SOLO_HORA','address'
'''