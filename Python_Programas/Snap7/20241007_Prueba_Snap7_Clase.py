import snap7 #Código probado con Snap7 V1.1
from snap7.util import *
import os
import math
import time
import random

#Limpieza y actualizacion de la pantalla
clear = lambda: os.system('cls')

#Conexión con el PLC
plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)
print("Conectado")

# salida = plc.ab_read(40, 2)
# salida = get_int(salida, 0)
# print(salida)

def leer_sal_int(byte):
    lectura = plc.ab_read(byte, 2)
    lectura = get_int(lectura, 0)
    return lectura

# print(leer_sal_int(40))
# entrada = plc.eb_read(20, 1)
# entrada = get_bool(entrada, 0, 5)
# print(entrada)

def leer_entrada_booleana(byte, bit):
    lectura = plc.eb_read(byte, 1)
    lectura = get_bool(lectura, 0, bit)
    return lectura

# print(leer_entrada_booleana(20, 5))
def esccribir_marca_int(byte, valor):
    lectura = plc.mb_read(byte, 2)
    lectura_int = set_int(lectura, 0, valor)
    plc.mb_write(byte, 2, lectura_int)


while True:
    aleatorio = random.randint(0, 27648)
    time.sleep(1)
    esccribir_marca_int(50, aleatorio)
    print(aleatorio)

"""
def leer_digital(tipo, byte, bit):
    if tipo == 'salida':
        salida = plc.ab_read(byte, 1)  # Byte cero un byte
        lectura = get_bool(salida, 0, bit)  # Byte 0 bit 5
    elif tipo == 'entrada':
        entrada = plc.eb_read(byte, 1)  # Byte cero un byte
        lectura = get_bool(entrada, 0, bit)  # Byte 0 bit 5
    elif tipo == 'marca':
        marca = plc.mb_read(byte, 1)  # Byte cero un byte
        lectura = get_bool(marca, 0, bit)  # Byte 0 bit 5
    return lectura

def escribir_digital(tipo, byte, bit, valor):
    if tipo == 'salida':
        lectura = plc.ab_read(byte, 1)  # Byte uno un byte
        set_bool(lectura, 0, bit, valor)  # Primer byte, bit 7, poner en 1
        plc.ab_write(byte, lectura)
    elif tipo == 'entrada':
        lectura = plc.eb_read(byte, 1)  # Byte uno un byte
        set_bool(lectura, 0, bit, valor)  # Primer byte, bit 7, poner en 1
        plc.eb_write(byte, lectura)
    elif tipo == 'marca':
        lectura = plc.mb_read(byte, 1)  # Byte uno un byte
        set_bool(lectura, 0, bit, valor)  # Primer byte, bit 7, poner en 1
        plc.mb_write(byte, lectura)

def leer_entero(tipo, byte):
    if tipo == 'salida':
        lectura = plc.ab_read(byte, 2)
        lectura = get_int(lectura, 0)
    elif tipo == 'entrada':
        lectura = plc.eb_read(byte, 2)
        lectura = get_int(lectura, 0)
    elif tipo == 'marca':
        lectura = plc.mb_read(byte, 2)
        lectura = get_int(lectura, 0)
    return lectura

def escribir_entero(tipo, byte, valor):
    if tipo == 'salida':
        lectura = plc.ab_read(byte, 2)
        lectura = set_int(lectura, 0, valor)
        plc.ab_write(byte, lectura)
    elif tipo == 'entrada':
        lectura = plc.eb_read(byte, 2)
        lectura = set_int(lectura, 0, valor)
        plc.eb_write(byte, lectura)
    elif tipo == 'marca':
        lectura = plc.mb_read(byte, 2)
        lectura = set_int(lectura, 0, valor)
        plc.mb_write(byte, lectura)
apagar = 0

while True:
    #Lectura de byte del área de marcas
    marca = plc.mb_read(20, 1)  # Se indica Byte 20, tamaño 1 byte
    marca = get_byte(marca, 0)
    print('Marca MB20: ', marca)

    
    #Leer salida digital
    salida1 = plc.ab_read(0, 1) #Byte cero un byte
    salida1 = get_bool(salida1, 0, 5) #Byte 0 bit 5
    print('Salida Q0.5: ', salida1)

    #Escribir salida digital
    salida2 = plc.ab_read(1, 1)  # Byte uno un byte
    set_bool(salida2, 0, 7, 1) #Primer byte, bit 7, poner en 1
    plc.ab_write(1, salida2)

    #Leer entrada análoga IW80
    entrada1 = plc.eb_read(80, 2)
    entrada1 = get_int(entrada1, 0)
    print('Entrada IW80: ', entrada1)

    #Leer entrada digital I10.4
    entrada2 = plc.eb_read(10, 1)
    entrada2 = get_bool(entrada2, 0, 4)
    print('Entrada I10.4: ', entrada2)

    print('Salida función: ', leer_digital('salida', 40, 3))
    escribir_digital('salida', 66, 5, 0)
    
    print('Entero leído: ', leer_entero('entrada', 88))

    escribir_entero('salida', 40, 188)
    
    #Reto 1: Si I0.0 entonces S Q0.0. Si no I0.0 entonces R Q0.0
    if leer_digital('entrada', 0, 0) == 1:
        escribir_digital('salida', 0, 0, 1)
    else:
        escribir_digital('salida', 0, 0, 0)
    #Reto 2: hacer implementación en Python-Snap7 para encender salidas del PLC de forma secuencial (Q0.0 a Q0.7) y volver a iniciar repetidamente. A medida que una enciende, la anterior se apaga. Esto generará un efecto “culebra” en el PLC. Modificar la velocidad y hacerlo lo más rápido posible. Visualizar efectos.
    for i in range(0, 8):
        time.sleep(0.1)
        if i == 0:
            escribir_digital('salida', 0, i, 1)  # Actual ON
            escribir_digital('salida', 0, 7, 0)  # Anterior OFF
        else:
            escribir_digital('salida', 0, i, 1) #Actual ON
            escribir_digital('salida', 0, i-1, 0) #Anterior OFF

    #Reto 3: encender todos secuencialmente, luego apagarlos secuencialmente. Repetir.
    if apagar == 1:
        for i in range(0, 8):
            time.sleep(0.1)
            escribir_digital('salida', 0, i, 1)  # Actual ON
        apagar = 0
    else:
        for i in range(0, 8):
            time.sleep(0.1)
            escribir_digital('salida', 0, i, 0)  # Actual ON
        apagar = 1
"""
