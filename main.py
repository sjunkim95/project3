from Client import Client
from AC import AC
from AP import AP

"""
input_lines = [
"AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 10 75",
"AP AP2 100 100 11 20 5 WiFi7 false true false 40 60",
"AP AP3 0 0 4 20 2.4/5 WiFi6 true true false 50 10 75",
"AP AP4 0 0 3 15 2.4/5 WiFi6 true true true 50 10 75",
"AP AP5 0 0 7 15 2.4/5 WiFi4 true true true 50 10 75",
"CLIENT Client1 10 10 WiFi6 2.4/5 true true true 73",
"MOVE Client1 10 9",
]
"""

AP_list = []
client_list = []

print("AP, Client Command, 명령어를 입력하세요: ")

while True:
    line = input().strip()
    # when there is an empty line, break.
    if not line:
        break

    tokens = line.split()
    command = tokens[0]

    if command == "AP":
        ap_name, ap_x, ap_y, ap_channel, ap_power_level = tokens[1:6]
        ap_frequency, ap_standard = tokens[6:8]
        ap_support_11k, ap_support_11v, ap_support_11r = map(lambda x: x.lower() == "true", tokens[8:11])
        ap_coverage_radius, ap_device_limit = map(int, tokens[11:13])
        if len(tokens) == 14:
            ap_minimal_rssi = int(tokens[13])
        else:
            ap_minimal_rssi = 0
        AP_list.append(
            AP(ap_name, int(ap_x), int(ap_y), int(ap_channel), int(ap_power_level), ap_frequency, ap_standard, ap_support_11k,
               ap_support_11v, ap_support_11r, ap_coverage_radius, ap_device_limit, ap_minimal_rssi))

    elif command == "CLIENT":
        client_name, client_x, client_y, client_standard, client_speed = tokens[1:6]
        client_support_11k, client_support_11v, client_support_11r = map(lambda x: x.lower() == "true", tokens[6:9])
        client_minimal_rssi = int(tokens[9])

        # Create a Client Class, and append to Client List
        client_list.append(Client(client_name, int(client_x), int(client_y), client_standard, client_speed,
                                  client_support_11k, client_support_11v, client_support_11r, client_minimal_rssi))
        # AC instances
ac = AC(AP_list, client_list)

print("Move command: ")

while True:
    line = input().strip()
    if not line:
        break

    tokens = line.split()
    if tokens[0] == "MOVE":
        client_name, move_x, move_y = tokens[1], int(tokens[2]), int(tokens[3])
        for client in ac.client_list:
            if client.client_name == client_name:
                client.move(move_x, move_y, AP_list) # client moving
                client.roam(AP_list) # after moving roam

