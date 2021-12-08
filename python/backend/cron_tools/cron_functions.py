from json.encoder import py_encode_basestring
from cron_tools.optimizer.optimizer import optimizer_milp_function
import json
import requests
import math


def microgrid_dayahead_optimizer():
    '''
    This function will solve the MILP model used to optimize the microgrid operation
    '''
    URL = "http://nginx:80/"

    
    data_nodes = requests.get(url=URL + "v1/api/node_information", headers={"accept" : "application/json"})
    print(data_nodes.status_code)
    data_nodes = json.loads(data_nodes.text)
    # print(data_nodes)
    data_branches = requests.get(url=URL + "v1/api/branch_information", headers={"accept" : "application/json"})
    data_branches = json.loads(data_branches.text)
    # print(data_branches)
    data_milp = requests.get(url=URL + "v1/api/milp_parameters", headers={"accept" : "application/json"})
    data_milp = json.loads(data_milp.text)
    # print(data_milp)

    if not data_nodes:
        optimizer_milp_function(print("Data nodes is empty!"))
    elif not data_branches:
        optimizer_milp_function(print("Data branches is empty!"))
    elif not data_milp:
        optimizer_milp_function(print("Data of milp parameters is empty!"))
    else:
        input_data = {}

        input_data['set_of_time'] = []
        for x in range(24):
            input_data['set_of_time'].append(str(x+1))
        input_data['set_of_nodes'] = []
        input_data['set_of_nodes'] = [t['name'] for t in data_nodes]
        input_data['set_of_lines'] = []
        for x in range(len(data_branches)):
            input_data['set_of_lines'].append([data_branches[x]['initial_node'],data_branches[x]['end_node']])
        cont1 = 0
        for index in data_nodes:
            if index['der'] == 'pv':
                cont1 += 1
                input_data['set_of_photovoltaic_systems'] = [str(cont1)]
        cont2 = 0
        for index in data_nodes:    
            if index['der'] == 'bess':
                cont2 += 1
                input_data['set_of_energy_storage_systems'] = [str(cont2)]
        cont5 = 0
        for index in data_nodes:    
            if index['der'] == 'genset':
                cont5 += 1
                input_data['set_of_thermal_generator'] = [str(cont5)]
        input_data['set_of_outage'] = ['6']
        input_data['set_of_scenarios'] = ['1']
        input_data['probability_of_scen'] = [1.0]
        input_data['coefficient_demand_scen'] = [1.0]
        input_data['coefficient_pv_scen'] = [1.0]
        input_data['type_of_bus'] = []
        for index in data_nodes:
            if index['type'] == 'PCC':
                input_data['type_of_bus'].append(1)
            elif index['type'] == 'Ref':
                input_data['type_of_bus'].append(2)
            else:
                input_data['type_of_bus'].append(0)
        input_data['resistance_raa'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['resistance_raa'].append(data_branches[x]['resistance_aa'])
        input_data['resistance_rbb'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['resistance_rbb'].append(data_branches[x]['resistance_bb'])
        input_data['resistance_rcc'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['resistance_rcc'].append(data_branches[x]['resistance_cc'])
        input_data['resistance_rab'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['resistance_rab'].append(data_branches[x]['resistance_ab'])
        input_data['resistance_rac'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['resistance_rac'].append(data_branches[x]['resistance_ac'])
        input_data['resistance_rbc'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['resistance_rbc'].append(data_branches[x]['resistance_bc'])   
        input_data['reactance_xaa'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xaa'].append(data_branches[x]['reactance_aa'])
        input_data['reactance_xbb'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xbb'].append(data_branches[x]['reactance_bb'])
        input_data['reactance_xcc'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xcc'].append(data_branches[x]['reactance_cc'])
        input_data['reactance_xab'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xab'].append(data_branches[x]['reactance_ab'])
        input_data['reactance_xbb'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xbb'].append(data_branches[x]['reactance_bb'])      
        input_data['reactance_xcc'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xcc'].append(data_branches[x]['reactance_cc'])
        input_data['reactance_xab'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xab'].append(data_branches[x]['reactance_ab'])  
        input_data['reactance_xac'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xac'].append(data_branches[x]['reactance_ac'])
        input_data['reactance_xbc'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['reactance_xbc'].append(data_branches[x]['reactance_bc'])
        input_data['nominal_voltage'] = data_milp[0]['nominal_voltage_kv']
        input_data['maximum_current_of_lines'] = []
        for x in range(len(input_data['set_of_lines'])):
            input_data['maximum_current_of_lines'].append(data_branches[x]['max_current'])
        input_data['maximum_power_PCC'] = []
        for x in range(len(input_data['set_of_nodes'])):
            if x == 0:
                input_data['maximum_power_PCC'].append(data_milp[x]['max_power_pcc_kw'])
            else:
                input_data['maximum_power_PCC'].append(0)
        input_data['variation_of_time'] = 1
        input_data['cost_of_the_energy'] = []
        for x in range(1,10):
            input_data['cost_of_the_energy'].append(data_milp[0]['pcc_cost_t0' + str(x)])
        for x in range(10,25):
            input_data['cost_of_the_energy'].append(data_milp[0]['pcc_cost_t' + str(x)])
        input_data['cost_of_load_curtailment'] = []
        for index in data_nodes:
            if index['der'] == 'pv':
                input_data['cost_of_load_curtailment'].append(0)
            else:
                input_data['cost_of_load_curtailment'].append(data_milp[0]['load_curt_cost'])
        input_data['nominal_active_load_phase_a'] = []
        input_data['nominal_active_load_phase_b'] = []
        input_data['nominal_active_load_phase_c'] = []
        input_data['nominal_reactive_load_phase_a'] = []
        input_data['nominal_reactive_load_phase_b'] = []
        input_data['nominal_reactive_load_phase_c'] = []
        for cont6 in range(len(data_nodes)):
            input_data['nominal_active_load_phase_a'].append(nominal_active_load_phase_a(data_nodes[cont6]['name'],data_nodes[cont6]['nominal_kva'], data_nodes[cont6]['power_factor']))
            input_data['nominal_active_load_phase_b'].append(nominal_active_load_phase_b(data_nodes[cont6]['name'],data_nodes[cont6]['nominal_kva'], data_nodes[cont6]['power_factor']))
            input_data['nominal_active_load_phase_c'].append(nominal_active_load_phase_c(data_nodes[cont6]['name'],data_nodes[cont6]['nominal_kva'], data_nodes[cont6]['power_factor']))
            input_data['nominal_reactive_load_phase_a'].append(nominal_reactive_load_phase_a(data_nodes[cont6]['name'],data_nodes[cont6]['nominal_kva'], data_nodes[cont6]['power_factor']))
            input_data['nominal_reactive_load_phase_b'].append(nominal_reactive_load_phase_b(data_nodes[cont6]['name'],data_nodes[cont6]['nominal_kva'], data_nodes[cont6]['power_factor']))
            input_data['nominal_reactive_load_phase_c'].append(nominal_reactive_load_phase_c(data_nodes[cont6]['name'],data_nodes[cont6]['nominal_kva'], data_nodes[cont6]['power_factor']))
        input_data['profile_active_load_phase_a'] = []
        input_data['profile_active_load_phase_b'] = []
        input_data['profile_active_load_phase_c'] = []
        input_data['profile_reactive_load_phase_a'] = []
        input_data['profile_reactive_load_phase_b'] = []
        input_data['profile_reactive_load_phase_c'] = []
        for x in range(len(data_nodes)):
            input_data['profile_active_load_phase_a'].append(profile_active_load_phase_a(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor'], len('set_of_time')))
            input_data['profile_active_load_phase_b'].append(profile_active_load_phase_b(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor'], len('set_of_time')))
            input_data['profile_active_load_phase_c'].append(profile_active_load_phase_c(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor'], len('set_of_time')))
            input_data['profile_reactive_load_phase_a'].append(profile_reactive_load_phase_a(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor'], len('set_of_time')))
            input_data['profile_reactive_load_phase_b'].append(profile_reactive_load_phase_b(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor'], len('set_of_time')))
            input_data['profile_reactive_load_phase_c'].append(profile_reactive_load_phase_c(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor'], len('set_of_time')))
        input_data['photovoltaic_generation_phase_a'] = []
        input_data['photovoltaic_generation_phase_b'] = []
        input_data['photovoltaic_generation_phase_c'] = []
        for x in range(len(data_nodes)):
            input_data['photovoltaic_generation_phase_a'].append(photovoltaic_generation_phase_a(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor']))
            input_data['photovoltaic_generation_phase_b'].append(photovoltaic_generation_phase_b(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor']))
            input_data['photovoltaic_generation_phase_c'].append(photovoltaic_generation_phase_c(data_nodes[x]['name'],data_nodes[x]['nominal_kva'], data_nodes[x]['power_factor']))
        input_data['profile_photovoltaic_generation'] = [0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.15, 0.30, 0.70, 0.90, 0.95, 1.00, 0.95, 0.90, 0.70, 0.40, 0.25, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        input_data['location_of_thermal_generation'] = {}
        input_data['minimum_active_power_thermal_generation'] = []
        input_data['maximum_active_power_thermal_generation'] = []
        input_data['minimum_reactive_power_thermal_generation'] = []
        input_data['maximum_reactive_power_thermal_generation'] = []
        for x in range(1,len('set_of_nodes')+2):
            input_data['location_of_thermal_generation'][str(x)] = []
        cont3 = 0
        for index in data_nodes:
            if index['der'] == 'genset':
                cont3 += 1
                input_data['location_of_thermal_generation'][str(index['id'])] = [str(cont3)]
                input_data['minimum_active_power_thermal_generation'].append(index['minimum_kva'])
                input_data['maximum_active_power_thermal_generation'].append(index['maximum_kva']*index['power_factor'])
                input_data['minimum_reactive_power_thermal_generation'].append(-math.sqrt(math.pow(index['maximum_kva'],2)-math.pow((index['maximum_kva']*index['power_factor']),2)))
                input_data['maximum_reactive_power_thermal_generation'].append(math.sqrt(math.pow(index['maximum_kva'],2)-math.pow((index['maximum_kva']*index['power_factor']),2)))
        input_data['cost_thermal_generation'] = []
        input_data['cost_thermal_generation'].append(data_milp[0]['genset_cost'])
        input_data['location_of_energy_storage_system'] = {}
        input_data['initial_energy_of_the_ess'] = []
        input_data['minimum_energy_capacity_ess'] = []
        input_data['maximum_energy_capacity_ess'] = []
        input_data['maximum_power_ess'] = []
        input_data['ess_efficiency'] = []
        for x in range(1,len('set_of_nodes')+2):
            input_data['location_of_energy_storage_system'][str(x)] = []
        cont4 = 0
        for index in data_nodes:
            if index['der'] == 'bess':
                cont4 += 1
                input_data['location_of_energy_storage_system'][str(index['id'])] = [str(cont4)]
                input_data['initial_energy_of_the_ess'].append(2)
                input_data['minimum_energy_capacity_ess'].append(index['soc_min_bat'] * index['bat_nom_energy'])
                input_data['maximum_energy_capacity_ess'].append(index['soc_max_bat'] * index['bat_nom_energy'])
                input_data['maximum_power_ess'].append(index['maximum_kva'])
                input_data['ess_efficiency'].append(0.9)
        input_data['number_discrete_blocks_piecewise_linearization'] = []
        for x in range(data_milp[0]['num_blocks_linearization']):
            input_data['number_discrete_blocks_piecewise_linearization'].append(str(x+1))
        
        
        

        #with open('./cron_tools/optimizer/input_data.json') as json_file:
        #    input_data = json.load(json_file)


        return optimizer_milp_function(input_data)


def write_results_database(resultado):
    '''
    This function will write the results (economic dispatch) in database
    '''
    URL = "http://nginx:80/"


    dispatch = requests.get(url=URL + "v1/api/economic_dispatch", headers={"accept" : "application/json"})
    print(dispatch.status_code)
    dispatch = json.loads(dispatch.text)
    
    if not dispatch:
        dispatch = {"bat_power_t00": resultado['power_of_the_ess'][0], "bat_power_t01": resultado['power_of_the_ess'][1], "bat_power_t02": resultado['power_of_the_ess'][2], 
        "bat_power_t03": resultado['power_of_the_ess'][3], "bat_power_t04": resultado['power_of_the_ess'][4], "bat_power_t05": resultado['power_of_the_ess'][5],
        "bat_power_t06": resultado['power_of_the_ess'][6], "bat_power_t07": resultado['power_of_the_ess'][7], "bat_power_t08": resultado['power_of_the_ess'][8],
        "bat_power_t09": resultado['power_of_the_ess'][9], "bat_power_t10": resultado['power_of_the_ess'][10], "bat_power_t11": resultado['power_of_the_ess'][11], 
        "bat_power_t12": resultado['power_of_the_ess'][12], "bat_power_t13": resultado['power_of_the_ess'][13], "bat_power_t14": resultado['power_of_the_ess'][14],
        "bat_power_t15": resultado['power_of_the_ess'][15], "bat_power_t16": resultado['power_of_the_ess'][16], "bat_power_t17": resultado['power_of_the_ess'][17],
        "bat_power_t18": resultado['power_of_the_ess'][18], "bat_power_t19": resultado['power_of_the_ess'][19], "bat_power_t20": resultado['power_of_the_ess'][20],
        "bat_power_t21": resultado['power_of_the_ess'][21], "bat_power_t22": resultado['power_of_the_ess'][22], "bat_power_t23": resultado['power_of_the_ess'][23],
        "load_curt_t00": resultado['total_load_curtailment']['scen_1'][0], "load_curt_t01": resultado['total_load_curtailment']['scen_1'][1], "load_curt_t02": resultado['total_load_curtailment']['scen_1'][2],
        "load_curt_t03": resultado['total_load_curtailment']['scen_1'][3], "load_curt_t04": resultado['total_load_curtailment']['scen_1'][4], "load_curt_t05": resultado['total_load_curtailment']['scen_1'][5],
        "load_curt_t06": resultado['total_load_curtailment']['scen_1'][6], "load_curt_t07": resultado['total_load_curtailment']['scen_1'][7], "load_curt_t08": resultado['total_load_curtailment']['scen_1'][8],
        "load_curt_t09": resultado['total_load_curtailment']['scen_1'][9], "load_curt_t10": resultado['total_load_curtailment']['scen_1'][10], "load_curt_t11": resultado['total_load_curtailment']['scen_1'][11],
        "load_curt_t12": resultado['total_load_curtailment']['scen_1'][12], "load_curt_t13": resultado['total_load_curtailment']['scen_1'][13], "load_curt_t14": resultado['total_load_curtailment']['scen_1'][14],
        "load_curt_t15": resultado['total_load_curtailment']['scen_1'][15], "load_curt_t16": resultado['total_load_curtailment']['scen_1'][16], "load_curt_t17": resultado['total_load_curtailment']['scen_1'][17],
        "load_curt_t18": resultado['total_load_curtailment']['scen_1'][18], "load_curt_t19": resultado['total_load_curtailment']['scen_1'][19], "load_curt_t20": resultado['total_load_curtailment']['scen_1'][20],
        "load_curt_t21": resultado['total_load_curtailment']['scen_1'][21], "load_curt_t22": resultado['total_load_curtailment']['scen_1'][22], "load_curt_t23": resultado['total_load_curtailment']['scen_1'][23],
        "pv_curt_t00": resultado['total_pv_curtailment']['scen_1'][0], "pv_curt_t01": resultado['total_pv_curtailment']['scen_1'][1], "pv_curt_t02": resultado['total_pv_curtailment']['scen_1'][2],
        "pv_curt_t03": resultado['total_pv_curtailment']['scen_1'][3], "pv_curt_t04": resultado['total_pv_curtailment']['scen_1'][4], "pv_curt_t05": resultado['total_pv_curtailment']['scen_1'][5],
        "pv_curt_t06": resultado['total_pv_curtailment']['scen_1'][6], "pv_curt_t07": resultado['total_pv_curtailment']['scen_1'][7], "pv_curt_t08": resultado['total_pv_curtailment']['scen_1'][8],
        "pv_curt_t09": resultado['total_pv_curtailment']['scen_1'][9], "pv_curt_t10": resultado['total_pv_curtailment']['scen_1'][10], "pv_curt_t11": resultado['total_pv_curtailment']['scen_1'][11],
        "pv_curt_t12": resultado['total_pv_curtailment']['scen_1'][12], "pv_curt_t13": resultado['total_pv_curtailment']['scen_1'][13], "pv_curt_t14": resultado['total_pv_curtailment']['scen_1'][14],
        "pv_curt_t15": resultado['total_pv_curtailment']['scen_1'][15], "pv_curt_t16": resultado['total_pv_curtailment']['scen_1'][16], "pv_curt_t17": resultado['total_pv_curtailment']['scen_1'][17],
        "pv_curt_t18": resultado['total_pv_curtailment']['scen_1'][18], "pv_curt_t19": resultado['total_pv_curtailment']['scen_1'][19], "pv_curt_t20": resultado['total_pv_curtailment']['scen_1'][20],
        "pv_curt_t21": resultado['total_pv_curtailment']['scen_1'][21], "pv_curt_t22": resultado['total_pv_curtailment']['scen_1'][22], "pv_curt_t23": resultado['total_pv_curtailment']['scen_1'][23]}
        
        data = requests.post(url=URL + "/v1/api/economic_dispatch/", data=dispatch, headers={"accept" : "application/json"})
        print(data.status_code)
        print(data.text)

    else:
        dispatch = {"bat_power_t00": resultado['power_of_the_ess'][0], "bat_power_t01": resultado['power_of_the_ess'][1], "bat_power_t02": resultado['power_of_the_ess'][2], 
        "bat_power_t03": resultado['power_of_the_ess'][3], "bat_power_t04": resultado['power_of_the_ess'][4], "bat_power_t05": resultado['power_of_the_ess'][5],
        "bat_power_t06": resultado['power_of_the_ess'][6], "bat_power_t07": resultado['power_of_the_ess'][7], "bat_power_t08": resultado['power_of_the_ess'][8],
        "bat_power_t09": resultado['power_of_the_ess'][9], "bat_power_t10": resultado['power_of_the_ess'][10], "bat_power_t11": resultado['power_of_the_ess'][11], 
        "bat_power_t12": resultado['power_of_the_ess'][12], "bat_power_t13": resultado['power_of_the_ess'][13], "bat_power_t14": resultado['power_of_the_ess'][14],
        "bat_power_t15": resultado['power_of_the_ess'][15], "bat_power_t16": resultado['power_of_the_ess'][16], "bat_power_t17": resultado['power_of_the_ess'][17],
        "bat_power_t18": resultado['power_of_the_ess'][18], "bat_power_t19": resultado['power_of_the_ess'][19], "bat_power_t20": resultado['power_of_the_ess'][20],
        "bat_power_t21": resultado['power_of_the_ess'][21], "bat_power_t22": resultado['power_of_the_ess'][22], "bat_power_t23": resultado['power_of_the_ess'][23],
        "load_curt_t00": resultado['total_load_curtailment']['scen_1'][0], "load_curt_t01": resultado['total_load_curtailment']['scen_1'][1], "load_curt_t02": resultado['total_load_curtailment']['scen_1'][2],
        "load_curt_t03": resultado['total_load_curtailment']['scen_1'][3], "load_curt_t04": resultado['total_load_curtailment']['scen_1'][4], "load_curt_t05": resultado['total_load_curtailment']['scen_1'][5],
        "load_curt_t06": resultado['total_load_curtailment']['scen_1'][6], "load_curt_t07": resultado['total_load_curtailment']['scen_1'][7], "load_curt_t08": resultado['total_load_curtailment']['scen_1'][8],
        "load_curt_t09": resultado['total_load_curtailment']['scen_1'][9], "load_curt_t10": resultado['total_load_curtailment']['scen_1'][10], "load_curt_t11": resultado['total_load_curtailment']['scen_1'][11],
        "load_curt_t12": resultado['total_load_curtailment']['scen_1'][12], "load_curt_t13": resultado['total_load_curtailment']['scen_1'][13], "load_curt_t14": resultado['total_load_curtailment']['scen_1'][14],
        "load_curt_t15": resultado['total_load_curtailment']['scen_1'][15], "load_curt_t16": resultado['total_load_curtailment']['scen_1'][16], "load_curt_t17": resultado['total_load_curtailment']['scen_1'][17],
        "load_curt_t18": resultado['total_load_curtailment']['scen_1'][18], "load_curt_t19": resultado['total_load_curtailment']['scen_1'][19], "load_curt_t20": resultado['total_load_curtailment']['scen_1'][20],
        "load_curt_t21": resultado['total_load_curtailment']['scen_1'][21], "load_curt_t22": resultado['total_load_curtailment']['scen_1'][22], "load_curt_t23": resultado['total_load_curtailment']['scen_1'][23],
        "pv_curt_t00": resultado['total_pv_curtailment']['scen_1'][0], "pv_curt_t01": resultado['total_pv_curtailment']['scen_1'][1], "pv_curt_t02": resultado['total_pv_curtailment']['scen_1'][2],
        "pv_curt_t03": resultado['total_pv_curtailment']['scen_1'][3], "pv_curt_t04": resultado['total_pv_curtailment']['scen_1'][4], "pv_curt_t05": resultado['total_pv_curtailment']['scen_1'][5],
        "pv_curt_t06": resultado['total_pv_curtailment']['scen_1'][6], "pv_curt_t07": resultado['total_pv_curtailment']['scen_1'][7], "pv_curt_t08": resultado['total_pv_curtailment']['scen_1'][8],
        "pv_curt_t09": resultado['total_pv_curtailment']['scen_1'][9], "pv_curt_t10": resultado['total_pv_curtailment']['scen_1'][10], "pv_curt_t11": resultado['total_pv_curtailment']['scen_1'][11],
        "pv_curt_t12": resultado['total_pv_curtailment']['scen_1'][12], "pv_curt_t13": resultado['total_pv_curtailment']['scen_1'][13], "pv_curt_t14": resultado['total_pv_curtailment']['scen_1'][14],
        "pv_curt_t15": resultado['total_pv_curtailment']['scen_1'][15], "pv_curt_t16": resultado['total_pv_curtailment']['scen_1'][16], "pv_curt_t17": resultado['total_pv_curtailment']['scen_1'][17],
        "pv_curt_t18": resultado['total_pv_curtailment']['scen_1'][18], "pv_curt_t19": resultado['total_pv_curtailment']['scen_1'][19], "pv_curt_t20": resultado['total_pv_curtailment']['scen_1'][20],
        "pv_curt_t21": resultado['total_pv_curtailment']['scen_1'][21], "pv_curt_t22": resultado['total_pv_curtailment']['scen_1'][22], "pv_curt_t23": resultado['total_pv_curtailment']['scen_1'][23]}

        data = requests.put(url=URL + "/v1/api/economic_dispatch/1", data=dispatch, headers={"accept" : "application/json"})
        print(data.status_code)
        print(data.text)
    



def nominal_active_load_phase_a(node_name, nominal_kva, power_factor):
    if node_name == '4':
        return 3.65
    elif node_name == '13':
        return 3.65
    else:
        return 0

def nominal_active_load_phase_b(node_name, nominal_kva, power_factor):
    if node_name == '4':
        return 2.50
    elif node_name == '13':
        return 2.50
    else:
        return 0

def nominal_active_load_phase_c(node_name, nominal_kva, power_factor):
    if node_name == '4':
        return 2.85
    elif node_name == '13':
        return 2.85
    else:
        return 0

def nominal_reactive_load_phase_a(node_name, nominal_kva, power_factor):
    if node_name == '4':
        return 3.00
    elif node_name == '13':
        return 3.00
    else:
        return 0

def nominal_reactive_load_phase_b(node_name, nominal_kva, power_factor):
    if node_name == '4':
        return 2.75
    elif node_name == '13':
        return 2.75
    else:
        return 0

def nominal_reactive_load_phase_c(node_name, nominal_kva, power_factor):
    if node_name == '4':
        return 1.75
    elif node_name == '13':
        return 1.75
    else:
        return 0

def photovoltaic_generation_phase_a(node_name, nominal_kva, power_factor):
    if node_name == '12':
        return 5.0
    else:
        return 0

def photovoltaic_generation_phase_b(node_name, nominal_kva, power_factor):
    if node_name == '12':
        return 5.0
    else:
        return 0

def photovoltaic_generation_phase_c(node_name, nominal_kva, power_factor):
    if node_name == '12':
        return 5.0
    else:
        return 0

def profile_active_load_phase_a(node_name, nominal_kva, power_factor, timesteps):
    if node_name == '4':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    elif node_name == '13':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    else:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def profile_active_load_phase_b(node_name, nominal_kva, power_factor, timesteps):
    if node_name == '4':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    elif node_name == '13':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    else:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def profile_active_load_phase_c(node_name, nominal_kva, power_factor, timesteps):
    if node_name == '4':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    elif node_name == '13':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    else:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def profile_reactive_load_phase_a(node_name, nominal_kva, power_factor, timesteps):
    if node_name == '4':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    elif node_name == '13':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    else:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def profile_reactive_load_phase_b(node_name, nominal_kva, power_factor, timesteps):
    if node_name == '4':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    elif node_name == '13':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    else:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def profile_reactive_load_phase_c(node_name, nominal_kva, power_factor, timesteps):
    if node_name == '4':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    elif node_name == '13':
        return [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.25, 0.40, 0.80, 0.75, 0.60, 0.90, 0.75, 0.80, 0.85, 0.90, 1.00, 1.00, 1.00, 0.90, 0.55, 0.20, 0.10]
    else:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def profile_photovoltaic_generation(node_name, nominal_kva, power_factor, timesteps):
    return [0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.15, 0.30, 0.70, 0.90, 0.95, 1.00, 0.95, 0.90, 0.70, 0.40, 0.25, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]