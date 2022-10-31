import requests

URL = "http://localhost:8051/"


# Dados da tabela node_information
parameters_node_1 = {"name": "1", "type": "PCC", "der": "pcc", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 100, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_1, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_2 = {"name": "2", "type": "Ref", "der": "genset", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 23.43, "power_factor": 0.768}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_2, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_3 = {"name": "3", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_3, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_4 = {"name": "4", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_4, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_5 = {"name": "5", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_5, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_6 = {"name": "6", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_6, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_7 = {"name": "7", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_7, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_8 = {"name": "8", "type": "PQ", "der": "bess", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 5, "power_factor": 1, "soc_min_bat": 0.2, "soc_max_bat": 1, "bat_nom_energy": 12}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_8, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_9 = {"name": "9", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_9, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_10 = {"name": "10", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_10, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_11 = {"name": "11", "type": "PQ", "der": "none", "nominal_kva": 0, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 1}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_11, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_12 = {"name": "12", "type": "PQ", "der": "pv", "nominal_kva": 5, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 0}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_12, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_node_13 = {"name": "13", "type": "PQ", "der": "load", "nominal_kva": 4.24, "minimum_kva": 0, "maximum_kva": 0, "power_factor": 0.707}
data = requests.post(url=URL + "v1/api/node_information", data=parameters_node_13, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)


# Dados da tabela branch_information
parameters_branch_1_2 = {"name": "1-2", "initial_node": "1", "end_node": "2", "resistance_aa": 0.0118525, "resistance_bb": 0.0118525, "resistance_cc": 0.0118525,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa": 0.00617199, "reactance_bb": 0.00617199, "reactance_cc": 0.00617199, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_1_2, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_2_3 = {"name": "2-3", "initial_node": "2", "end_node": "3", "resistance_aa": 0.0202962, "resistance_bb": 0.0202962, "resistance_cc": 0.0202962,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa": 0.0310448, "reactance_bb": 0.0310448, "reactance_cc": 0.0310448, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_2_3, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_3_4 = {"name": "3-4", "initial_node": "3", "end_node": "4", "resistance_aa": 0.0158024, "resistance_bb": 0.0158024, "resistance_cc": 0.0158024,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa": 0.00200096, "reactance_bb": 0.00200096, "reactance_cc": 0.00200096, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_3_4, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_4_5 = {"name": "4-5", "initial_node": "4", "end_node": "5", "resistance_aa": 0.0139073, "resistance_bb": 0.0139073, "resistance_cc": 0.0139073,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa": 0.0055358, "reactance_bb": 0.0055358, "reactance_cc": 0.0055358, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_4_5, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_5_6 = {"name": "5-6", "initial_node": "5", "end_node": "6", "resistance_aa": 0.0149768, "resistance_bb": 0.0149768, "resistance_cc": 0.0149768,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.00675726, "reactance_bb":  0.00675726, "reactance_cc":  0.00675726, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_5_6, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_6_7 = {"name": "6-7", "initial_node": "6", "end_node": "7", "resistance_aa": 0.0127794, "resistance_bb": 0.0127794, "resistance_cc": 0.0127794,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.00685883, "reactance_bb":  0.00685883, "reactance_cc":  0.00685883, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_6_7, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_7_8 = {"name": "7-8", "initial_node": "7", "end_node": "8", "resistance_aa": 0.0128593, "resistance_bb": 0.0128593, "resistance_cc": 0.0128593,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.00294372, "reactance_bb":  0.00294372, "reactance_cc":  0.00294372, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_7_8, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_8_9 = {"name": "8-9", "initial_node": "8", "end_node": "9", "resistance_aa": 0.0154258, "resistance_bb": 0.0154258, "resistance_cc": 0.0154258,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.00870617, "reactance_bb":  0.00870617, "reactance_cc":  0.00870617, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_8_9, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_9_10 = {"name": "9-10", "initial_node": "9", "end_node": "10", "resistance_aa": 0.0173957, "resistance_bb": 0.0173957, "resistance_cc": 0.0173957,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.00538124, "reactance_bb":  0.00538124, "reactance_cc":  0.00538124, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_9_10, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_10_11 = {"name": "10-11", "initial_node": "10", "end_node": "11", "resistance_aa": 0.0149572, "resistance_bb": 0.0149572, "resistance_cc": 0.0149572,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.00351784, "reactance_bb":  0.00351784, "reactance_cc":  0.00351784, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_10_11, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_11_12 = {"name": "11-12", "initial_node": "11", "end_node": "12", "resistance_aa": 0.0184425, "resistance_bb": 0.0184425, "resistance_cc": 0.0184425,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.0120617, "reactance_bb":  0.0120617, "reactance_cc":  0.0120617, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_11_12, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)

parameters_branch_12_13 = {"name": "12-13", "initial_node": "12", "end_node": "13", "resistance_aa": 0.0125872, "resistance_bb": 0.0125872, "resistance_cc": 0.0125872,
"resistance_ab": 0.00, "resistance_ac": 0.00, "resistance_bc": 0.00, "reactance_aa":  0.000213601, "reactance_bb":  0.000213601, "reactance_cc":  0.000213601, 
"reactance_ab": 0.00, "reactance_ac": 0.00, "reactance_bc": 0.00, "max_current": 140}
data = requests.post(url=URL + "v1/api/branch_information", data=parameters_branch_12_13, headers={"accept" : "application/json"})
print(data.status_code)
print(data.text)


# Dados da tabela milp_parameters
# model_parameters = {"min_voltage_pu": 0.92, "max_voltage_pu": 1.05, "nominal_voltage_kv": 0.22, "num_blocks_linearization": 20, "pcc_cost_t01": 0.145, 
# "pcc_cost_t02": 0.145, "pcc_cost_t03": 0.145, "pcc_cost_t04": 0.145, "pcc_cost_t05": 0.145, "pcc_cost_t06": 0.145, "pcc_cost_t07": 0.145, "pcc_cost_t08": 0.145, 
# "pcc_cost_t09": 0.145, "pcc_cost_t10": 0.145, "pcc_cost_t11": 0.145, "pcc_cost_t12": 0.145, "pcc_cost_t13": 0.145, "pcc_cost_t14": 0.145, "pcc_cost_t15": 0.145, 
# "pcc_cost_t16": 0.25, "pcc_cost_t17":  0.25, "pcc_cost_t18":  0.42, "pcc_cost_t19":  0.42, "pcc_cost_t20":  0.42, "pcc_cost_t21":  0.25,  "pcc_cost_t22":  0.25, 
# "pcc_cost_t23":  0.145, "pcc_cost_t24":  0.145, "load_pred_error": 0.2, "pv_generation_pred_error": 0.2, "genset_cost": 0.5, "max_power_pcc_kw": 100, "load_curt_cost": 500} 
# data = requests.post(url=URL + "v1/api/milp_parameters", data=model_parameters, headers={"accept" : "application/json"})
# print(data.status_code)
# print(data.text)


# Dados da tabela economic_dispatch
# dispatch = {"bat_power_t00": 0.0, "bat_power_t01": 0.0, "bat_power_t02": 0.0, "bat_power_t03": 0.0, "bat_power_t04": 0.0, "bat_power_t05": 0.0, "bat_power_t06": 0.0,
# "bat_power_t07": 0.0714, "bat_power_t08": 0.4049, "bat_power_t09": 2.5961, "bat_power_t10": 0.0, "bat_power_t11": 1.0394, "bat_power_t12": 3.4019, "bat_power_t13": 0.0,
# "bat_power_t14": 0.4859, "bat_power_t15": 0.0, "bat_power_t16": 0.0, "bat_power_t17": 0.0, "bat_power_t18": -1.7334, "bat_power_t19": -3.1997, "bat_power_t20": -3.0668,
# "bat_power_t21": 0.0, "bat_power_t22": 0.0, "bat_power_t23": 0.0, "genset_power_t00": 0.0, "genset_power_t01": 0.0, "genset_power_t02": 0.0, "genset_power_t03": 0.0,
# "genset_power_t04": 0.0, "genset_power_t05": 0.0, "genset_power_t06": 0.0,"genset_power_t07": 0.0, "genset_power_t08": 0.0, "genset_power_t09": 0.0, "genset_power_t10": 0.0,
# "genset_power_t11": 0.0, "genset_power_t12": 0.0, "genset_power_t13": 0.0, "genset_power_t14": 0.0, "genset_power_t15": 0.0, "genset_power_t16": 0.0, "genset_power_t17": 0.0,
# "genset_power_t18": 0.0, "genset_power_t19": 0.0, "genset_power_t20": 0.0, "genset_power_t21": 0.0, "genset_power_t22": 0.0, "genset_power_t23": 0.0, "load_curt_t00": 0.0, 
# "load_curt_t01": 0.0, "load_curt_t02": 0.0, "load_curt_t03": 0.0, "load_curt_t04": 0.0, "load_curt_t05": 0.0, "load_curt_t06": 0.0, "load_curt_t07": 0.0, "load_curt_t08": 0.0, 
# "load_curt_t09": 0.0, "load_curt_t10": 0.0, "load_curt_t11": 0.0, "load_curt_t12": 0.0, "load_curt_t13": 0.0, "load_curt_t14": 0.0, "load_curt_t15": 0.0, "load_curt_t16": 0.0,
# "load_curt_t17": 0.0, "load_curt_t18": 0.0, "load_curt_t19": 0.0, "load_curt_t20": 0.0, "load_curt_t21": 0.0, "load_curt_t22": 0.0, "load_curt_t23": 0.0, "pv_curt_t00": 0.0, 
# "pv_curt_t01": 0.0, "pv_curt_t02": 0.0, "pv_curt_t03": 0.0, "pv_curt_t04": 0.0, "pv_curt_t05": 0.0, "pv_curt_t06": 0.0, "pv_curt_t07": 0.0, "pv_curt_t08": 0.0, "pv_curt_t09": 0.0, 
# "pv_curt_t10": 0.0, "pv_curt_t11": 0.0, "pv_curt_t12": 0.0, "pv_curt_t13": 0.0, "pv_curt_t14": 0.0, "pv_curt_t15": 0.0, "pv_curt_t16": 0.0, "pv_curt_t17": 0.0, "pv_curt_t18": 0.0, 
# "pv_curt_t19": 0.0, "pv_curt_t20": 0.0, "pv_curt_t21": 0.0, "pv_curt_t22": 0.0, "pv_curt_t23": 0.0}
# data = requests.post(url=URL + "/v1/api/economic_dispatch/", data=dispatch, headers={"accept" : "application/json"})
# print(data.status_code)
# print(data.text)
