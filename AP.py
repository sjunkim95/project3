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
        self.minimal_rssi = -60
        self.connected_clients = []

    def __repr__(self):
        return f'AP {self.ap_name}: {self.x}, {self.y}, {self.channel}, {self.power_level}, {self.frequency}, {self.standard}, {self.supports_11k}, {self.supports_11v}, {self.supports_11r}, {self.coverage_radius}, {self.device_limit}, {self.minimal_rssi}'

    def calculate_rssi(self, client_x, client_y):
        distance = math.sqrt((self.x - client_x) ** 2 + (self.y - client_y) ** 2)

        if distance == 0:
            return self.power_level  # AP와 동일한 위치일 경우 신호 감쇄 없음

        # rssi 변수 계산
        try:
            frequency_value = float(self.frequency.split('/')[0])  # 주파수 추출 부분. '2.4/5'와 같은 값을 처리하도록 수정
            rssi = self.power_level - 20 * math.log10(distance) - 20 * math.log10(frequency_value) - 32.44
            print(f"[DEBUG] AP {self.ap_name}: Calculated RSSI={rssi} for client at ({client_x}, {client_y})")
            return rssi
        except Exception as e:
            print(f"[ERROR] Failed to calculate RSSI: {e}")
            return -100  # 예외 발생 시 기본 값 설정

    def can_connect(self, client):
        rssi = self.calculate_rssi(client.x, client.y)
        can_connect = rssi >= self.minimal_rssi and len(self.connected_clients) < self.device_limit
        # 신호강도가 RSSI기준을 충족하는지, AP의 수용 가능 인원이 충족되는지, 둘다 충족할시 return True
        print(f"[DEBUG] {self.ap_name}: RSSI={rssi}, Min RSSI={self.minimal_rssi}, Clients={len(self.connected_clients)}/{self.device_limit}, Can Connect={can_connect}")
        return can_connect

    def connect(self, client):
        if self.can_connect(client):
            self.connected_clients.append(client)
            client.connected_ap = self
            print(f"[INFO] {client.client_name} connected to {self.ap_name}")
            return True

    def disconnect(self, client):
        if client in self.connected_clients:
            self.connected_clients.remove(client)
            if client.connected_ap == self:
                client.connected_ap = None
            print(f"[INFO] {client.client_name} disconnected from {self.ap_name}")
