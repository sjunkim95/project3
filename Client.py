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
        self.minimal_rssi = -60
        self.connected_ap = None # 처음엔 연결된 AP가 없음
        self.logs = []

    def __repr__(self):
        return f"{self.client_name}, {self.x}, {self.y}, {self.standard}, {self.speed}, {self.supports_11k}, {self.supports_11v}, {self.supports_11r}, {self.minimal_rssi}"

    def __eq__(self, other):
        return isinstance(other, Client) and self.client_name == other.client_name

    def __hash__(self):
        return hash(self.client_name)

    def connect_to_ap(self, ap):
        if self.connected_ap:
            self.disconnect_ap()
        self.connected_ap = ap # 클라이언트를 AP에 연결
        ap.connected_clients.append(self)
        print(f"{self.client_name} is connected to {ap.ap_name}")
        self.logs.append(f"{self.client_name} connect to {ap.ap_name}")

    def disconnect_ap(self):
        if self.connected_ap:
            print(f"{self.connected_ap.ap_name} disconnected from {self.connected_ap.ap_name}")
            self.logs.append(f"{self.client_name} disconnected from {self.connected_ap.ap_name}")
            if self in self.connected_ap.connected_clients:
                self.connected_ap.connected_clients.remove(self)
            self.connected_ap = None # 연결된 AP 해제
        else:
            print(f"{self.client_name} is not connected to any AP")
            self.logs.append(f"{self.client_name} is not connected to any AP")

    def move(self, move_x, move_y, ap_list):

        self.x = move_x
        self.y = move_y

        print(f"{self.client_name} moved to ({self.x}, {self.y})")
        self.logs.append(f"{self.client_name} moved to ({self.x}, {self.y})")

        # 클라이언트가 이동한 후, AP 연결 상태를 재점검
        self.roam(ap_list)  # 이동 후 가장 좋은 AP로 roam

    def roam(self, ap_list):
        # 현재의 AP 신호가 약하면, 다른 AP로 연결, Roam to another AP
        if not self.connected_ap:
            print(f"{self.client_name} is not connected to any AP")
            return

        current_rssi = self.connected_ap.calculate_rssi(self.x, self.y)
        best_ap = None
        best_rssi = current_rssi  # 현재 AP의 RSSI를 기준으로 roam 시작

        for ap in ap_list:
            if ap == self.connected_ap:
                continue # 이미 연결된 AP는 무시
            rssi = ap.calculate_rssi(self.x, self.y)
            if rssi > best_rssi + 5 and ap.can_connect(self): # Roam when RSSI is good enough
                best_ap = ap
                best_rssi = rssi

        if best_ap and best_ap != self.connected_ap:
            print(f"{self.client_name} roamed from {self.connected_ap.ap_name} to {best_ap.ap_name}")
            self.connect_to_ap(best_ap)  # 새로운 AP에 연결
        else:
            print(f"{self.client_name} stays connected to {self.connected_ap.ap_name}")
