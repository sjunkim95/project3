class Client:
    def __init__(self, client_name, x, y, standard, speed, supports_11k, supports_11v, supports_11r, minimal_rssi):
        self.client_name = client_name
        self.x = x
        self.y = y
        self.standard = standard
        self.speed = speed
        self.supports_11k = supports_11k
        self.supports_11v = supports_11v
        self.supports_11r = supports_11r
        self.minimal_rssi = minimal_rssi
        self.logs = []

    def __repr__(self):
        return f"{self.client_name}, {self.x}, {self.y}, {self.standard}, {self.speed}, {self.supports_11k}, {self.supports_11v}, {self.supports_11r}, {self.minimal_rssi}"

    def move(self, move_x, move_y):
        self.x = move_x
        self.y = move_y
        return f"{self.x}, {self.y}"

    def connection(self):
        self.logs.append(f"{self.client_name} connect to {AP.ap_name} with signal strength {AP.calculate_rssi()}")

    def disconnect(self):
        self.logs.append(f"{self.client_name} disconnect")

    def roam(self):
        pass


