import zmq
import random
import time
import math

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect('tcp://127.0.0.1:5555')


class InstrumentPrice(object):
    def __init__(self):
        self.symbol = 'AAPL'
        self.t = time.time()
        self.value = 100.
        self.sigma = 0.4
        self.r = 0.01
    def simulateValue(self):
        t = time.time()
        dt = (t - self.t) / (252 * 8 * 60 * 60)
        dt *= 500
        self.t = t
        self.value *= math.exp((self.r - 0.5 * self.sigma ** 2) * dt + self.sigma * math.sqrt(dt) * random.gauss(0, 1))
        return self.value


ip = InstrumentPrice()

while True:
    msg = '{} {:.2f}'.format(ip.symbol, ip.simulateValue())
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random() * 2)