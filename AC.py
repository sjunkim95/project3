import pickle
class AC:
    def __init__(self, ap_list, client_list):
        self.ap_dict = {ap.ap_name: ap for ap in ap_list}
        self.client_list = client_list
        self.n = 0
        self.client_standard_support = {}
        self.connected_client_ap = {}
        self.logs = []
        self.pickle_dict = {}
        # Key is the name network entities -> All AC AP Client
        # Prefer APs with higher or more compatible WiFi standards. {ap_name:WiFi}
        for client in self.client_list:
            for ap in self.ap_dict:
                # Compare Client WiFi and AP's WiFi, client prefer AP with higher WiFi
                if self.ap_dict[ap].standard >= client.standard:
                    self.client_standard_support[ap] = self.ap_dict[ap].standard

        # If there is more than one higher WiFi standard, go for support k, v, r
        if len(self.client_standard_support) >= 1:
            # To get the keys, what AP can support for client
            standard_support_keys = self.client_standard_support.keys()
            compare_dict = {}
            for client in self.client_list:
                for key in standard_support_keys:
                    count = 0
                    # add the count when client.suport and ap.support is same
                    if client.supports_11k == self.ap_dict[key].supports_11k:
                        count += 1
                    if client.supports_11v == self.ap_dict[key].supports_11v:
                        count += 1
                    if client.supports_11r == self.ap_dict[key].supports_11r:
                        count += 1
                    compare_dict[key] = count
          #  print(compare_dict) -> {'AP1': 3, 'AP2': 1, 'AP3': 2, 'AP4': 3}

            # The max number of the value, is the match for the client
            max_dict_number = max(compare_dict.values())
            # With the max number, find which AP match the clint
            tie_values = self.max_value_dict(compare_dict, max_dict_number)
            # Now if there is more than one AP that supports, find max Power for final AP
            if len(tie_values) >= 1 :
                max_power_key = self.tie_values_dict(tie_values)
               # print("max power key임", max_power_key)
                for client in self.client_list:
                    if '/' in client.speed:
                        speed_standard = max(client.speed.split('/'))
                        self.prefer_high_band(max_power_key,speed_standard)
                    else:
                        speed_standard = client.speed
                        self.prefer_high_band(max_power_key,speed_standard)
                    if client.supports_11r == self.ap_dict[max_power_key].supports_11r:
                        self.connected_client_ap[max_power_key] = client
                     #   print("그럼 마지막으로1," , self.ap_dict[max_power_key].connect(client))
                        self.logs.append(f"Step {self.step_n()}: {client.client_name} CONNECTION LOCATION {self.ap_dict[max_power_key].connect(client)}")
                    else:
                        self.connected_client_ap[max_power_key] = client
                      #  print("그럼 마지막으로2,", self.ap_dict[max_power_key].connect(client))
                        self.logs.append(f"Step {self.step_n()}: {client} DISCONNECTS AT LOCATION {client.x} {client.y}")


        self.channel_preferences()
        self.cover_rad()
        
        self.pickle_dict["AP"] = self.ap_dict
        self.pickle_dict["CLIENT"] = self.client_list
        self.pickle_dict["LOGS"] = self.logs
        with open("pickle_file.dat", "wb") as file:
            pickle.dump(self.pickle_dict, file)

    def cover_rad(self):
        for ap_name in self.ap_dict:
            for client in self.client_list:
              #  print("음?", self.ap_dict[ap_name].coverage_radius, type(self.ap_dict[ap_name].coverage_radius))
                if pow(int(self.ap_dict[ap_name].coverage_radius), 2) < (pow(self.ap_dict[ap_name].x - client.x, 2) + pow(self.ap_dict[ap_name].y - client.y, 2)):
                    self.logs.append(f"Step {self.step_n()}: {client} DISCONNECTS AT LOCATION {client.x} {client.y}")

    def channel_preferences(self):
        preferred_channel_list = [1, 6, 11]
        preferred_channel_list_count = {}
        for ap_name in self.ap_dict:
            if self.ap_dict[ap_name].channel in preferred_channel_list:
                if self.ap_dict[ap_name].channel not in preferred_channel_list_count:
                    preferred_channel_list_count[self.ap_dict[ap_name].channel] = 1
                else:
                    self.ap_dict[ap_name].channel += 1
            else:
                if self.ap_dict[ap_name].channel not in preferred_channel_list_count:
                    preferred_channel_list_count[self.ap_dict[ap_name].channel] = 1
                else:
                    preferred_channel_list_count[self.ap_dict[ap_name].channel] += 1

    def tie_values_dict(self, dictionary):
        if len(dictionary) > 1:
            left_keys = list(dictionary.keys())
            max_power_key = ''
            for i in range(len(left_keys)):
                for j in range(1, len(left_keys)):
                    if self.ap_dict[left_keys[i]].power_level > self.ap_dict[left_keys[j]].power_level:
                        max_power_key = left_keys[i]
                    elif self.ap_dict[left_keys[j]].power_level > self.ap_dict[left_keys[i]].power_level:
                        max_power_key = left_keys[j]
            return max_power_key

    def max_value_dict(self, dictionary, max_number):
        max_dict = {}
        for k, v in dictionary.items():
            if v == max_number:
                max_dict[k] = v
        return max_dict

    def prefer_high_band(self, power_key, max_standard):
        if max_standard >= self.ap_dict[power_key].standard:
            return True

    def step_n(self):
        self.n += 1
        return self.n


