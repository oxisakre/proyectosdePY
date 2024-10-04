import csv

# Nombres de los archivos de entrada y salida
archivo_entrada = 'entrada.csv'
archivo_salida = 'salida.csv'

# Leer el archivo CSV de entrada con coma como delimitador
with open(archivo_entrada, 'r', encoding='utf-8') as f_in:
    lector_csv = csv.reader(f_in, delimiter=',')
    filas = list(lector_csv)

# Escribir el archivo CSV de salida con punto y coma como delimitador
with open(archivo_salida, 'w', newline='', encoding='utf-8') as f_out:
    escritor_csv = csv.writer(f_out, delimiter=';')
    escritor_csv.writerows(filas)
