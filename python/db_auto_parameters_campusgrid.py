import requests

URL = "http://localhost:8051/"


# Dados da tabela node_information
parameters_node_1 = {"name": "1", "type": "PCC", "der": "pcc", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 1000, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_1, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_2 = {"name": "2", "type": "PQ", "der": "genset", "nominal_kva": 150, "minimum_kva": 0, "maximum_kva": 150, "power_factor": 0.707}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_2, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_3 = {"name": "3", "type": "PQ", "der": "load", "nominal_kva": 371, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_3, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_4 = {"name": "4", "type": "Ref", "der": "bess", "nominal_kva": 1275, "minimum_kva": 0, "maximum_kva": 1275, "power_factor": 1, "soc_min_bat": 0.20, "soc_max_bat": 0.95, "bat_nom_energy": 1275}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_4, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_5 = {"name": "5", "type": "PQ", "der": "pv", "nominal_kva": 736, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_5, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_6 = {"name": "6", "type": "PQ", "der": "ev1", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_6, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_7 = {"name": "7", "type": "PQ", "der": "ev2", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_7, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

# Dados da tabela branch_information
parameters_branch_1_2 = {"name": "1-2", "initial_node": "1", "end_node": "2", "resistance_aa": 0.4138, "resistance_bb": 0.4138, "resistance_cc": 0.4138,
"resistance_ab": 0.0523, "resistance_ac": 0.0523, "resistance_bc": 0.0523, "reactance_aa":  0.8258, "reactance_bb":  0.8258, "reactance_cc":  0.8258, 
"reactance_ab":  0.4765, "reactance_ac":  0.4765, "reactance_bc":  0.4765, "max_current": 999}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_2, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_1_3 = {"name": "1-3", "initial_node": "1", "end_node": "3", "resistance_aa": 0.4138, "resistance_bb": 0.4138, "resistance_cc": 0.4138,
"resistance_ab": 0.0523, "resistance_ac": 0.0523, "resistance_bc": 0.0523, "reactance_aa":  0.8258, "reactance_bb":  0.8258, "reactance_cc":  0.8258, 
"reactance_ab":  0.4765, "reactance_ac":  0.4765, "reactance_bc":  0.4765, "max_current": 999}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_3, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)
 
parameters_branch_1_4 = {"name": "1-4", "initial_node": "1", "end_node": "4", "resistance_aa": 0.4138, "resistance_bb": 0.4138, "resistance_cc": 0.4138,
"resistance_ab": 0.0523, "resistance_ac": 0.0523, "resistance_bc": 0.0523, "reactance_aa":  0.8258, "reactance_bb":  0.8258, "reactance_cc":  0.8258, 
"reactance_ab":  0.4765, "reactance_ac":  0.4765, "reactance_bc":  0.4765, "max_current": 999}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_4, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_1_5 = {"name": "1-5", "initial_node": "1", "end_node": "5", "resistance_aa": 0.4138, "resistance_bb": 0.4138, "resistance_cc": 0.4138,
"resistance_ab": 0.0523, "resistance_ac": 0.0523, "resistance_bc": 0.0523, "reactance_aa":  0.8258, "reactance_bb":  0.8258, "reactance_cc":  0.8258, 
"reactance_ab":  0.4765, "reactance_ac":  0.4765, "reactance_bc":  0.4765, "max_current": 999}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_5, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_1_6 = {"name": "1-6", "initial_node": "1", "end_node": "6", "resistance_aa": 0.4138, "resistance_bb": 0.4138, "resistance_cc": 0.4138,
"resistance_ab": 0.0523, "resistance_ac": 0.0523, "resistance_bc": 0.0523, "reactance_aa":  0.8258, "reactance_bb":  0.8258, "reactance_cc":  0.8258, 
"reactance_ab":  0.4765, "reactance_ac":  0.4765, "reactance_bc":  0.4765, "max_current": 999}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_6, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_1_7 = {"name": "1-7", "initial_node": "1", "end_node": "7", "resistance_aa": 0.4138, "resistance_bb": 0.4138, "resistance_cc": 0.4138,
"resistance_ab": 0.0523, "resistance_ac": 0.0523, "resistance_bc": 0.0523, "reactance_aa":  0.8258, "reactance_bb":  0.8258, "reactance_cc":  0.8258, 
"reactance_ab":  0.4765, "reactance_ac":  0.4765, "reactance_bc":  0.4765, "max_current": 999}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_7, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

# Dados da tabela milp_parameters
model_parameters = {"min_voltage_pu": 0.95, "max_voltage_pu": 1.05, "nominal_voltage_kv": 11.9, "num_blocks_linearization": 20, "pcc_cost_t01": 0.116, 
"pcc_cost_t02": 0.116, "pcc_cost_t03": 0.116, "pcc_cost_t04": 0.116, "pcc_cost_t05": 0.116, "pcc_cost_t06": 0.116, "pcc_cost_t07": 0.116, "pcc_cost_t08": 0.116, 
"pcc_cost_t09": 0.116, "pcc_cost_t10": 0.116, "pcc_cost_t11": 0.116, "pcc_cost_t12": 0.116, "pcc_cost_t13": 0.116, "pcc_cost_t14": 0.116, "pcc_cost_t15": 0.116, 
"pcc_cost_t16": 0.167, "pcc_cost_t17":  0.167, "pcc_cost_t18":  0.254, "pcc_cost_t19":  0.254, "pcc_cost_t20":  0.254, "pcc_cost_t21":  0.167,  "pcc_cost_t22":  0.167, 
"pcc_cost_t23":  0.116, "pcc_cost_t24":  0.116, "load_pred_error": 0.1, "pv_generation_pred_error": 0.1, "genset_cost": 30, "max_power_pcc_kw": 1000, "load_curt_cost": 500} 
data = requests.post(url=URL + "v1/api/milp_parameters", data=model_parameters, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

# EV parameters
EV_parameters = {"EV_battery_size_1": 0, "EV_power_size_1": 0, "EV_initial_SoC_1": 0, "EV_arrival_time_1": 0, "EV_departure_time_1": 0, 
"EV_battery_size_2": 0, "EV_power_size_2": 0, "EV_initial_SoC_2": 0, "EV_arrival_time_2": 0, "EV_departure_time_2": 0} 
data = requests.post(url=URL + "v1/api/ev_parameters", data=EV_parameters, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)


# Dados da tabela economic_dispatch
dispatch = {"bat_power_t00": 0.0, "bat_power_t01": 0.0, "bat_power_t02": 0.0, "bat_power_t03": 0.0, "bat_power_t04": 0.0, "bat_power_t05": 0.0, "bat_power_t06": 0.0,
"bat_power_t07": 0.0714, "bat_power_t08": 0.4049, "bat_power_t09": 2.5961, "bat_power_t10": 0.0, "bat_power_t11": 1.0394, "bat_power_t12": 3.4019, "bat_power_t13": 0.0,
"bat_power_t14": 0.4859, "bat_power_t15": 0.0, "bat_power_t16": 0.0, "bat_power_t17": 0.0, "bat_power_t18": -1.7334, "bat_power_t19": -3.1997, "bat_power_t20": -3.0668,
"bat_power_t21": 0.0, "bat_power_t22": 0.0, "bat_power_t23": 0.0, "genset_power_t00": 0.0, "genset_power_t01": 0.0, "genset_power_t02": 0.0, "genset_power_t03": 0.0,
"genset_power_t04": 0.0, "genset_power_t05": 0.0, "genset_power_t06": 2.10,"genset_power_t07": 1.35, "genset_power_t08": 0.0, "genset_power_t09": 0.0, "genset_power_t10": 0.0,
"genset_power_t11": 0.0, "genset_power_t12": 0.0, "genset_power_t13": 0.0, "genset_power_t14": 0.0, "genset_power_t15": 0.0, "genset_power_t16": 0.0, "genset_power_t17": 0.0,
"genset_power_t18": 0.0, "genset_power_t19": 0.0, "genset_power_t20": 0.0, "genset_power_t21": 0.0, "genset_power_t22": 0.0, "genset_power_t23": 0.0, "load_curt_t00": 0.0, 
"load_curt_t01": 0.0, "load_curt_t02": 0.0, "load_curt_t03": 0.0, "load_curt_t04": 0.0, "load_curt_t05": 0.0, "load_curt_t06": 0.0, "load_curt_t07": 0.0, "load_curt_t08": 0.0, 
"load_curt_t09": 0.0, "load_curt_t10": 0.0, "load_curt_t11": 0.0, "load_curt_t12": 0.0, "load_curt_t13": 0.0, "load_curt_t14": 0.0, "load_curt_t15": 0.0, "load_curt_t16": 0.0,
"load_curt_t17": 0.0, "load_curt_t18": 0.0, "load_curt_t19": 0.0, "load_curt_t20": 0.0, "load_curt_t21": 0.0, "load_curt_t22": 0.0, "load_curt_t23": 0.0, "pv_curt_t00": 0.0, 
"pv_curt_t01": 0.0, "pv_curt_t02": 0.0, "pv_curt_t03": 0.0, "pv_curt_t04": 0.0, "pv_curt_t05": 0.0, "pv_curt_t06": 0.0, "pv_curt_t07": 0.0, "pv_curt_t08": 0.0, "pv_curt_t09": 0.0, 
"pv_curt_t10": 0.0, "pv_curt_t11": 0.0, "pv_curt_t12": 0.0, "pv_curt_t13": 0.0, "pv_curt_t14": 0.0, "pv_curt_t15": 0.0, "pv_curt_t16": 0.0, "pv_curt_t17": 0.0, "pv_curt_t18": 0.0, 
"pv_curt_t19": 0.0, "pv_curt_t20": 0.0, "pv_curt_t21": 0.0, "pv_curt_t22": 0.0, "pv_curt_t23": 0.0, "ev_1_power_t00": 0.0, "ev_1_power_t01": 0.0, "ev_1_power_t02": 0.0, "ev_1_power_t03": 0.0, "ev_1_power_t04": 0.0, "ev_1_power_t05": 0.0, "ev_1_power_t06": 0.0,
"ev_1_power_t07": 0.0714, "ev_1_power_t08": 0.4049, "ev_1_power_t09": 2.5961, "ev_1_power_t10": 0.0, "ev_1_power_t11": 1.0394, "ev_1_power_t12": 3.4019, "ev_1_power_t13": 0.0,
"ev_1_power_t14": 0.4859, "ev_1_power_t15": 0.0, "ev_1_power_t16": 0.0, "ev_1_power_t17": 0.0, "ev_1_power_t18": -1.7334, "ev_1_power_t19": -3.1997, "ev_1_power_t20": -3.0668,
"ev_1_power_t21": 0.0, "ev_1_power_t22": 0.0, "ev_1_power_t23": 0.0, "ev_2_power_t00": 0.0, "ev_2_power_t01": 0.0, "ev_2_power_t02": 0.0, "ev_2_power_t03": 0.0, "ev_2_power_t04": 0.0, "ev_2_power_t05": 0.0, "ev_2_power_t06": 0.0,
"ev_2_power_t07": 0.0714, "ev_2_power_t08": 0.4049, "ev_2_power_t09": 2.5961, "ev_2_power_t10": 0.0, "ev_2_power_t11": 1.0394, "ev_2_power_t12": 3.4019, "ev_2_power_t13": 0.0,
"ev_2_power_t14": 0.4859, "ev_2_power_t15": 0.0, "ev_2_power_t16": 0.0, "ev_2_power_t17": 0.0, "ev_2_power_t18": -1.7334, "ev_2_power_t19": -3.1997, "ev_2_power_t20": -3.0668,
"ev_2_power_t21": 0.0, "ev_2_power_t22": 0.0, "ev_2_power_t23": 0.0}
data = requests.post(url=URL + "/v1/api/economic_dispatch/", data=dispatch, headers={"accept" : "application/json"})
print(data.status_code)
# print(data.text)
