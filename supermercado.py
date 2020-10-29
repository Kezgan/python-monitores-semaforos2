import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

clientes = 9
maxClientes = 3
clientesSupermercado = []
clientesCaja = []
monitorCaja = threading.Condition()

class Cliente(threading.Thread):
    def __init__(self):
        super().__init__()

    def entrarAlSupermercado(self):
        logging.info(f'Entrando al supermercado')
        clientesSupermercado.append(self)
        time.sleep(1)
        logging.info(f'Agarrando producto y yendo a la caja')
        time.sleep(3)
        self.dirigirseACaja()

    def dirigirseACaja(self):
        clientesCaja.append(self)
        logging.info(f'Haciendo cola')
        time.sleep(2)
        if (self.primero()):
            self.pagar()

    def pagar(self):
        with monitorCaja:
            logging.info(f'Despertando para poder pagar')
            time.sleep(1)
            monitorCaja.notify()

    def primero(self):
        return clientesCaja.index(self) == 0

    def run(self):
        if (len(clientesSupermercado) < maxClientes):
            self.entrarAlSupermercado()
            clientesSupermercado.pop(0)
        else:
            logging.info(f'Esto está muy lleno, me voy a mi casa')

class Caja(threading.Thread):
    def __init__(self):
        super().__init__()

    def atenderCliente(self):
        with monitorCaja:
            while (len(clientesCaja) == 0):
                logging.info(f'No hay nadie haciendo cola, sigo durmiendo')
                monitorCaja.wait()
            logging.info(f'Cobrando al cliente')
            time.sleep(2)
            clientesCaja.pop(0)
            logging.info(f'"Gracias por su compra!"')

    def run(self):
        while(True):
            self.atenderCliente()

Caja().start()

for c in range(clientes):
    Cliente().start()

# Cuando termina de atender a las 3 primeras personas no sigue con las demas personas que se fueron a sus casas