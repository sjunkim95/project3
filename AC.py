import pickle


class AC:
    def __init__(self, ap_list, client_list):
        self.ap_dict = {ap.ap_name: ap for ap in ap_list}
        self.client_list = client_list
        self.client_standard_support = {}
        self.connected_client_ap = {}  # 클라이언트가 연결된 AP 저장, save the AP connected to the client
        self.logs = []

        # 클라이언트와 AP 간의 연결 관리
        for client in self.client_list:
            best_ap = self.find_best_ap(client)
            if best_ap:
                best_ap.connect(client)
                self.connected_client_ap[client] = best_ap
                self.logs.append(f"Step {self.step_n()}: {client.client_name} connected to {best_ap.ap_name}")
            else:
                self.logs.append(f"Step {self.step_n()}: {client.client_name} could not be connected to any AP")

        # AP 커버리지 범위 체크, check the AP coverage
        self.cover_rad()

        # pickle을 사용하여 네트워크 상태 저장
        self.pickle_dict = {
            "AP": self.ap_dict,
            "CLIENT": self.client_list,
            "LOGS": self.logs
        }

        with open("pickle_file.dat", "wb") as file:
            pickle.dump(self.pickle_dict, file)

    def find_best_ap(self, client):
        # Find the best AP and return
        best_ap = None
        best_rssi = float("-inf")
        for ap in self.ap_dict.values():
            rssi = ap.calculate_rssi(client.x, client.y)
            can_connect = ap.can_connect(client)

            print(f"Checking AP {ap.ap_name}: RSSI={rssi}, Can Connect={can_connect}")

            if can_connect and rssi > best_rssi:
                best_ap = ap
                best_rssi = rssi

        if best_ap:
            print(f"Best AP {client.client_name}: {best_ap.ap_name}")
        else:
            print(f"No AP for {client.client_name}")

        return best_ap

    def move_client(self, client_name, move_x, move_y):

        # Connect to AP, after the movement
        for client in self.client_list:
            if client.client_name == client_name:
                client.move(move_x, move_y)
                self.logs.append(f"Step {self.step_n()}: {client.client_name} moved to ({move_x}, {move_y})")

                # Remove the client from the connected AP
                if client in self.connected_client_ap:
                    current_ap = self.connected_client_ap[client]
                    current_ap.disconnect(client)
                    del self.connected_client_ap[client]
                    self.logs.append(
                        f"Step {self.step_n()}: {client.client_name} disconnected from {current_ap.ap_name}")

                # 새로운 AP 찾기 및 연결
                best_ap = self.find_best_ap(client)
                if best_ap:
                    print(f"Best AP chosen: {best_ap.ap_name}")
                    if best_ap.can_connect(client):
                        print(f"{best_ap.ap_name} can connect {client.client_name}")
                        best_ap.connect(client)
                        self.connected_client_ap[client] = best_ap
                        print(f"Step {self.step_n()}: {client.client_name} connected to {best_ap.ap_name}")
                    else:
                        print(f"[DEBUG] {best_ap.ap_name} cannot connect {client.client_name}")
                else:
                    print(f"Step {self.step_n()}: {client.client_name} could not be connected to any AP")

    def cover_rad(self):
        # AP의 커버리지 밖으로 나가면 연결을 끊는다, disconnect the AP when goes off from coverage
        for client in list(self.connected_client_ap.keys()):
            ap = self.connected_client_ap[client]
            distance_sq = (ap.x - client.x) ** 2 + (ap.y - client.y) ** 2
            if distance_sq > ap.coverage_radius ** 2:
                ap.disconnect(client)
                del self.connected_client_ap[client]
                self.logs.append(f"Step {self.step_n()}: {client.client_name} DISCONNECTS AT LOCATION {ap.ap_name}")

    def step_n(self):
        # 로그에 기록할 단계 증가
        if not hasattr(self, 'n'):
            self.n = 0
        self.n += 1
        return self.n