import math

class AP:
    def __init__(self, ap_name, x, y, channel, power_level, frequency, standard, supports_11k, supports_11v, supports_11r, coverage_radius, device_limit, minimal_rssi=0):
        self.ap_name = ap_name
        self.x = x
        self.y = y
        self.channel = channel
        self.power_level = power_level
        self.frequency = frequency
        self.standard = standard
        self.supports_11k = supports_11k
        self.supports_11v = supports_11v
        self.supports_11r = supports_11r
        self.coverage_radius = coverage_radius
        self.device_limit = device_limit
        self.minimal_rssi = minimal_rssi
        self.connected_clients = []

    def __repr__(self):
        return f'{self.ap_name}, {self.x}, {self.y}, {self.channel}, {self.channel}, {self.power_level}, {self.frequency}, {self.standard}, {self.supports_11k}, {self.supports_11v}, {self.supports_11r}, {self.coverage_radius}, {self.device_limit}, {self.minimal_rssi}'

    def calculate_rssi(self, client_x, client_y):
        distance = math.sqrt((self.x-client_x)**2 + (self.y-client_y)**2)
        rssi = self.power_level - 20 * math.log10(distance) - 20 * math.log10(float(self.frequency.split('/')[0])) - 32.44
        return rssi

    def connect(self, client_object):
        self.connected_clients.append(client_object)
        return self.connected_clients

    def disconnect(self, client_object):
        rssi = self.calculate_rssi(client_object.x, client_object.y)
        if rssi < self.minimal_rssi:
            return False

    def device_space(self):
        temp = list(self.connected_clients)
        if len(temp) >= self.device_limit:
            return f"TRIED {self.ap_name} BUT WAS DENIED"
        else:
            return True
