import requests
import datetime

URL = "http://localhost:8051/"
now = datetime.datetime.now()
iso_format = now.isoformat()

# Dados da tabela node_measurement
measurement_node_1 = {"time_iso": iso_format, "active_power_a_kw": -100, "active_power_b_kw": -100, "active_power_c_kw": -100, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22}
data = requests.post(url=URL + "v1/api/node_measurement/no/1", data=measurement_node_1, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurement_node_2 = {"time_iso": iso_format, "active_power_a_kw": 10, "active_power_b_kw": 10, "active_power_c_kw": 10, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22}
data = requests.post(url=URL + "v1/api/node_measurement/no/2", data=measurement_node_2, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurement_node_3 = {"time_iso": iso_format, "active_power_a_kw": 10, "active_power_b_kw": 10, "active_power_c_kw": 10, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22}
data = requests.post(url=URL + "v1/api/node_measurement/no/3", data=measurement_node_3, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurement_node_4 = {"time_iso": iso_format, "active_power_a_kw": 10, "active_power_b_kw": 10, "active_power_c_kw": 10, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22, "soc_kwh": 0.4}
data = requests.post(url=URL + "v1/api/node_measurement/no/4", data=measurement_node_4, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurement_node_5 = {"time_iso": iso_format, "active_power_a_kw": 10, "active_power_b_kw": 10, "active_power_c_kw": 10, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22}
data = requests.post(url=URL + "v1/api/node_measurement/no/5", data=measurement_node_5, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurement_node_6 = {"time_iso": iso_format, "active_power_a_kw": 10, "active_power_b_kw": 10, "active_power_c_kw": 10, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22}
data = requests.post(url=URL + "v1/api/node_measurement/no/6", data=measurement_node_6, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurement_node_7 = {"time_iso": iso_format, "active_power_a_kw": 10, "active_power_b_kw": 10, "active_power_c_kw": 10, "reactive_power_a_kvar": 10,
"reactive_power_b_kvar": 10, "reactive_power_c_kvar": 10, "voltage_a_kv": 0.22, "voltage_b_kv": 0.22, "voltage_c_kv": 0.22}
data = requests.post(url=URL + "v1/api/node_measurement/no/7", data=measurement_node_7, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)


# Dados da tabela branch_measurement
measurements_branch_1_2 = {"time_iso": iso_format, "active_power_flow_a_kw": 10, "active_power_flow_b_kw": 10, "active_power_flow_c_kw": 10, 
"reactive_power_flow_a_kvar": 8, "reactive_power_flow_b_kvar": 8, "reactive_power_flow_c_kvar": 8, "current_a_A": 1.5, "current_b_A": 1.5, "current_c_A": 1.5}
data = requests.post(url=URL + "v1/api/branch_measurement/branch/1", data=measurements_branch_1_2, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurements_branch_1_3 = {"time_iso": iso_format, "active_power_flow_a_kw": 10, "active_power_flow_b_kw": 10, "active_power_flow_c_kw": 10, 
"reactive_power_flow_a_kvar": 8, "reactive_power_flow_b_kvar": 8, "reactive_power_flow_c_kvar": 8, "current_a_A": 1.5, "current_b_A": 1.5, "current_c_A": 1.5}
data = requests.post(url=URL + "v1/api/branch_measurement/branch/2", data=measurements_branch_1_3, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurements_branch_1_4 = {"time_iso": iso_format, "active_power_flow_a_kw": 10, "active_power_flow_b_kw": 10, "active_power_flow_c_kw": 10, 
"reactive_power_flow_a_kvar": 8, "reactive_power_flow_b_kvar": 8, "reactive_power_flow_c_kvar": 8, "current_a_A": 1.5, "current_b_A": 1.5, "current_c_A": 1.5}
data = requests.post(url=URL + "v1/api/branch_measurement/branch/3", data=measurements_branch_1_4, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurements_branch_1_5 = {"time_iso": iso_format, "active_power_flow_a_kw": 10, "active_power_flow_b_kw": 10, "active_power_flow_c_kw": 10, 
"reactive_power_flow_a_kvar": 8, "reactive_power_flow_b_kvar": 8, "reactive_power_flow_c_kvar": 8, "current_a_A": 1.5, "current_b_A": 1.5, "current_c_A": 1.5}
data = requests.post(url=URL + "v1/api/branch_measurement/branch/4", data=measurements_branch_1_5, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurements_branch_1_6 = {"time_iso": iso_format, "active_power_flow_a_kw": 10, "active_power_flow_b_kw": 10, "active_power_flow_c_kw": 10, 
"reactive_power_flow_a_kvar": 8, "reactive_power_flow_b_kvar": 8, "reactive_power_flow_c_kvar": 8, "current_a_A": 1.5, "current_b_A": 1.5, "current_c_A": 1.5}
data = requests.post(url=URL + "v1/api/branch_measurement/branch/5", data=measurements_branch_1_6, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

measurements_branch_1_7 = {"time_iso": iso_format, "active_power_flow_a_kw": 10, "active_power_flow_b_kw": 10, "active_power_flow_c_kw": 10, 
"reactive_power_flow_a_kvar": 8, "reactive_power_flow_b_kvar": 8, "reactive_power_flow_c_kvar": 8, "current_a_A": 1.5, "current_b_A": 1.5, "current_c_A": 1.5}
data = requests.post(url=URL + "v1/api/branch_measurement/branch/6", data=measurements_branch_1_7, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)
