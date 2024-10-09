from Adafruit_IO import Client
import time
import random



#Conexión con el servidor
aio = Client('hola', 'Ya tu sabes')

#aio.send('var1', 45)
#aio.send('var-bool', 'OFF')
#data = aio.receive('var1')
#print('Received value: {0}'.format(data.value))


while True:
    time.sleep(0.5)
    #Numérica aleatoria Python-->Adafruit IO
    # print(aio.send('var1', random.randint(0, 100)))
    aio.send('var1', random.randint(0, 100))
    print(aio.value)
    #Lectura Adafruit IO-->Python
    data = aio.receive('var1')
    print('Received num value: {0}'.format(data.value))
    data2 = aio.receive('var-bool')
    print('Received bool value: {0}'.format(data2.value))