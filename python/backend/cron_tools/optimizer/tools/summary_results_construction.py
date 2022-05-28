""""
========================== Summary Results =========================
"""
import json
import numpy as np


class SummaryResults:
	def __init__(self, data, results):
		self.data = data
		self.results = results

	# Function to write results in an txt file
	def WritingUnfeasibleOutputFile(self):
		data = self.data
		results = self.results
		
		#output_file.write("\nInfeasible problem! The default solution will be adopted!\n")
		
		output_file = {}
		output_file["status"] = []
		output_file["status"].append(results.Status)
		output_file["objective_function"] = []
		output_file["objective_function"].append(results.ObjectiveFunctionValue)
		output_file["power_of_the_ess"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3.8, -4.2, 0.0, 0.0, 0.0, 0.0, 0.0] 
		
		output_file["active_power_genset_w_outage"] = {}
		for s in data.S:
			aux_list = []
			aux_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
			
			output_file["active_power_genset_w_outage"]["scen_" + s] = {}
			output_file["active_power_genset_w_outage"]["scen_" + s]= aux_list
		
		output_file["total_load_curtailment"] = {}
		output_file["total_pv_curtailment"] = {}
		for s in data.S:
			aux_list_2 = []
			aux_list_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

			output_file["total_load_curtailment"]["scen_" + s] = {}
			output_file["total_load_curtailment"]["scen_" + s]= aux_list_2
		
			aux_list_3 = []
			aux_list_3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

			output_file["total_pv_curtailment"]["scen_" + s] = {}
			output_file["total_pv_curtailment"]["scen_" + s]= aux_list_3
		
		
		return output_file


	def WritingFeasibleOutputFile(self):
		data = self.data
		results = self.results

		output_file = {}
		output_file["status"] = []
		output_file["status"].append(results.Status)
		output_file["objective_function"] = []
		output_file["objective_function"].append(results.ObjectiveFunctionValue)
		output_file["power_of_the_ess"] = []
		for t in data.T:
			output_file["power_of_the_ess"].append(results.PB['1'][t])

		# Grid-connected and islanded operation
		if len(data.O) >= 1:
			output_file["active_power_genset"] = {}
			for s in data.S:
				for c in data.O:
					aux_list = []
					aux_list = [(results.PG['1'][t][c][s]) for t in data.T]
			
					output_file["active_power_genset"]["scen_" + s] = {}
					output_file["active_power_genset"]["scen_" + s]= aux_list

			self.List_TOS = [];
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_TOS += [[t,c,s]]

			self.Tot_lc = {};
			self.Tot_pvd = {};
			for (t,c,s) in self.List_TOS:
				self.Tot_lc[(t,c,s)] = 0
				self.Tot_pvd[(t,c,s)] = 0

			output_file["total_load_curtailment"] = {}
			output_file["total_pv_curtailment"] = {}
			for s in data.S:
				for c in data.O:
					for t in data.T:
						for i in data.N:
							if data.PDa[(i,t)] != 0:
								self.Tot_lc[(t,c,s)] =  ((1 - results.xd[i][t][c][s]) * (data.PDa[(i,t)] + data.PDb[(i,t)] + data.PDc[(i,t)]) * data.sd[(s)])

				aux_list_2 = []
				for c in data.O:
					aux_list_2 = [(self.Tot_lc[(t,c,s)]) for t in data.T]

				output_file["total_load_curtailment"]["scen_" + s] = {}
				output_file["total_load_curtailment"]["scen_" + s]= aux_list_2


				for c in data.O:
					for t in data.T:
						for i in data.N:
							if data.PVa[(i,t)] != 0:
								self.Tot_pvd[(t,c,s)] = self.Tot_pvd[(t,c,s)] + ((1 - results.xd[i][t][c][s]) * (data.PVa[(i,t)] + data.PVb[(i,t)] + data.PVc[(i,t)]) *  data.srs[(s)])

				aux_list_3 = []
				for c in data.O:
					aux_list_3 = [(self.Tot_pvd[(t,c,s)]) for t in data.T]

				output_file["total_pv_curtailment"]["scen_" + s] = {}
				output_file["total_pv_curtailment"]["scen_" + s]= aux_list_3

		# Grid-connected operation
		else:
			output_file["active_power_genset"] = {}
			for s in data.S:
				aux_list = []
				aux_list = [(results.PG_con['1'][t][s]) for t in data.T]
			
				output_file["active_power_genset"]["scen_" + s] = {}
				output_file["active_power_genset"]["scen_" + s]= aux_list
			
			output_file["total_load_curtailment"] = {}
			output_file["total_pv_curtailment"] = {}
			for s in data.S:
				aux_list_2 = []
				aux_list_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

				output_file["total_load_curtailment"]["scen_" + s] = {}
				output_file["total_load_curtailment"]["scen_" + s]= aux_list_2

				output_file["total_pv_curtailment"]["scen_" + s] = {}
				output_file["total_pv_curtailment"]["scen_" + s]= aux_list_2


		return output_file
	