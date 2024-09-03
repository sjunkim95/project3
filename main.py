from Client import Client
from AC import AC
from AP import AP
import math

input_lines = [
"AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 10 75",
"AP AP2 100 100 11 20 5 WiFi7 false true false 40 60",
"AP AP3 0 0 4 20 2.4/5 WiFi6 true true false 50 10 75",
"AP AP4 0 0 3 15 2.4/5 WiFi6 true true true 50 10 75",
"AP AP5 0 0 7 15 2.4/5 WiFi4 true true true 50 10 75",
"CLIENT Client1 10 10 WiFi6 2.4/5 true true true 73",
"MOVE Client1 10 9",
]

AP_list = []
client_list = []

for lines in input_lines:
    line = lines.split()
    command = line[0]

    if command == "AP":
        ap_name = line[1]
        ap_x = int(line[2])
        ap_y = int(line[3])
        ap_channel = int(line[4])
        ap_power_level = int(line[5])
        ap_frequency = str(line[6])
        ap_standard = str(line[7])
        ap_support_11k = str(line[8])
        ap_support_11v = str(line[9])
        ap_support_11r = str(line[10])
        ap_coverage_radius = int(line[11])
        ap_device_limit = int(line[12])
        if len(line) == 14:
            ap_minimal_rssi = int(line[13])
            # Create an AP class and append it to an AP List when minimal_rssi exist
            AP_list.append(
                AP(ap_name, ap_x, ap_y, ap_channel, ap_power_level, ap_frequency, ap_standard, ap_support_11k,
                   ap_support_11v, ap_support_11r, ap_coverage_radius, ap_device_limit, ap_minimal_rssi))
        else:
            # Create an AP class and append it to an AP List when minimal_rssi does not exist
            AP_list.append(
                AP(ap_name, ap_x, ap_y, ap_channel, ap_power_level, ap_frequency, ap_standard, ap_support_11k,
                   ap_support_11v, ap_support_11r, ap_coverage_radius, ap_device_limit))

    elif command == "CLIENT":
        client_name = line[1]
        client_x = int(line[2])
        client_y = int(line[3])
        client_standard = str(line[4])
        client_speed = str(line[5])
        client_support_11k = str(line[6])
        client_support_11v = str(line[7])
        client_support_11r = str(line[8])
        client_minimal_rssi = int(line[9])

        # Create a Client Class, and append to Client List
        client_list.append(Client(client_name, client_x, client_y, client_standard, client_speed, client_support_11k, client_support_11v, client_support_11r, client_minimal_rssi))
        # Inheritance
        class_object = AC(AP_list, client_list)

    elif command == "MOVE":
        move_x = int(line[2])
        move_y = int(line[3])
        for i in range(len(client_list)):
            if client_list[i].client_name == line[1]:
                class_object.client_list[i].move(move_x, move_y)


