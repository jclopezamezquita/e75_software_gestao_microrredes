""""
========================== Input data processing for the EMS solution =========================
"""
import json
from math import acos, atan, cos, sin, sqrt

class InputData:
	def __init__(self, input_data): # Passing arguments given to the class instantiation operator (_init_) to the class
		data = input_data

		self.T = data["set_of_time"]
		self.N = data["set_of_nodes"]
		self.L = [tuple(x) for x in data["set_of_lines"]]
		self.B = data["set_of_energy_storage_systems"]
		self.GD = data["set_of_thermal_generator"]
		self.O = data["set_of_outage"]
		self.S = data["set_of_scenarios"]
		self.Prob = {}
		for index in range(len(data["probability_of_scen"])):
			self.Prob[self.S[index]] = data["probability_of_scen"][index]
		self.srs = {}
		for index in range(len(data["coefficient_demand_scen"])):
			self.srs[self.S[index]] = data["coefficient_demand_scen"][index]
		self.sd = {}
		for index in range(len(data["coefficient_pv_scen"])):
			self.sd[self.S[index]] = data["coefficient_pv_scen"][index]		
		self.Tb = {}
		for index in range(len(data["type_of_bus"])):
			self.Tb[self.N[index]] = data["type_of_bus"][index]
		self.Raa = {}
		for index in range(len(data["resistance_raa"])):
			self.Raa[self.L[index]] = data["resistance_raa"][index]
		self.Rbb = {}
		for index in range(len(data["resistance_rbb"])):
			self.Rbb[self.L[index]] = data["resistance_rbb"][index]
		self.Rcc = {}
		for index in range(len(data["resistance_rcc"])):
			self.Rcc[self.L[index]] = data["resistance_rcc"][index]
		self.Rab = {}
		for index in range(len(data["resistance_rab"])):
			self.Rab[self.L[index]] = data["resistance_rab"][index]
		self.Rac = {}
		for index in range(len(data["resistance_rac"])):
			self.Rac[self.L[index]] = data["resistance_rac"][index]
		self.Rbc = {}
		for index in range(len(data["resistance_rbc"])):
			self.Rbc[self.L[index]] = data["resistance_rbc"][index]
		self.Xaa = {}
		for index in range(len(data["reactance_xaa"])):
			self.Xaa[self.L[index]] = data["reactance_xaa"][index]
		self.Xbb = {}
		for index in range(len(data["reactance_xbb"])):
			self.Xbb[self.L[index]] = data["reactance_xbb"][index]
		self.Xcc = {}
		for index in range(len(data["reactance_xcc"])):
			self.Xcc[self.L[index]] = data["reactance_xcc"][index]
		self.Xab = {}
		for index in range(len(data["reactance_xab"])):
			self.Xab[self.L[index]] = data["reactance_xab"][index]
		self.Xac = {}
		for index in range(len(data["reactance_xac"])):
			self.Xac[self.L[index]] = data["reactance_xac"][index]
		self.Xbc = {}
		for index in range(len(data["reactance_xbc"])):
			self.Xbc[self.L[index]] = data["reactance_xbc"][index]
		self.Vnom = data["nominal_voltage"]
		self.Imax = {}
		for index in range(len(data["maximum_current_of_lines"])):
			self.Imax[self.L[index]] = data["maximum_current_of_lines"][index]
		self.Smax = {}
		for index in range(len(data["maximum_power_PCC"])):
			self.Smax[self.N[index]] = data["maximum_power_PCC"][index]
		self.delta_t = data["variation_of_time"]
		self.cEDS = {}
		for index in range(len(data["cost_of_the_energy"])):
			self.cEDS[self.T[index]] = data["cost_of_the_energy"][index]
		self.alpha_c = {}
		for index in range(len(data["cost_of_load_curtailment"])):
			self.alpha_c[self.N[index]] = data["cost_of_load_curtailment"][index]
		self.PDa_0 = {}
		for index in range(len(data["nominal_active_load_phase_a"])):
			self.PDa_0[self.N[index]] = data["nominal_active_load_phase_a"][index]
		self.PDb_0 = {}
		for index in range(len(data["nominal_active_load_phase_b"])):
			self.PDb_0[self.N[index]] = data["nominal_active_load_phase_b"][index]
		self.PDc_0 = {}
		for index in range(len(data["nominal_active_load_phase_c"])):
			self.PDc_0[self.N[index]] = data["nominal_active_load_phase_c"][index]
		self.QDa_0 = {}
		for index in range(len(data["nominal_reactive_load_phase_a"])):
			self.QDa_0[self.N[index]] = data["nominal_reactive_load_phase_a"][index]
		self.QDb_0 = {}
		for index in range(len(data["nominal_reactive_load_phase_b"])):
			self.QDb_0[self.N[index]] = data["nominal_reactive_load_phase_b"][index]
		self.QDc_0 = {}
		for index in range(len(data["nominal_reactive_load_phase_c"])):
			self.QDc_0[self.N[index]] = data["nominal_reactive_load_phase_c"][index]
		self.fm_pa = {}
		for x in range(len(data["set_of_nodes"])):
			self.fm_pa[self.N[x]] = {}
			for index in range(len(data["set_of_time"])):
				self.fm_pa[self.N[x]][self.T[index]] = data["profile_active_load_phase_a"][x][index]
		self.fm_pb = {}
		for x in range(len(data["set_of_nodes"])):
			self.fm_pb[self.N[x]] = {}
			for index in range(len(data["set_of_time"])):
				self.fm_pb[self.N[x]][self.T[index]] = data["profile_active_load_phase_b"][x][index]
		self.fm_pc = {}
		for x in range(len(data["set_of_nodes"])):
			self.fm_pc[self.N[x]] = {}
			for index in range(len(data["set_of_time"])):
				self.fm_pc[self.N[x]][self.T[index]] = data["profile_active_load_phase_c"][x][index]
		self.fm_qa = {}
		for x in range(len(data["set_of_nodes"])):
			self.fm_qa[self.N[x]] = {}
			for index in range(len(data["set_of_time"])):
				self.fm_qa[self.N[x]][self.T[index]] = data["profile_reactive_load_phase_a"][x][index]
		self.fm_qb = {}
		for x in range(len(data["set_of_nodes"])):
			self.fm_qb[self.N[x]] = {}
			for index in range(len(data["set_of_time"])):
				self.fm_qb[self.N[x]][self.T[index]] = data["profile_reactive_load_phase_b"][x][index]
		self.fm_qc = {}
		for x in range(len(data["set_of_nodes"])):
			self.fm_qc[self.N[x]] = {}
			for index in range(len(data["set_of_time"])):
				self.fm_qc[self.N[x]][self.T[index]] = data["profile_reactive_load_phase_c"][x][index]
		self.PVa_0 = {}
		for index in range(len(data["photovoltaic_generation_phase_a"])):
			self.PVa_0[self.N[index]] = data["photovoltaic_generation_phase_a"][index]
		self.PVb_0 = {}
		for index in range(len(data["photovoltaic_generation_phase_b"])):
			self.PVb_0[self.N[index]] = data["photovoltaic_generation_phase_b"][index]
		self.PVc_0 = {}
		for index in range(len(data["photovoltaic_generation_phase_c"])):
			self.PVc_0[self.N[index]] = data["photovoltaic_generation_phase_c"][index]
		self.fpv ={}
		for index in range(len(data["profile_photovoltaic_generation"])):
			self.fpv[self.T[index]] = data["profile_photovoltaic_generation"][index]
		self.dict_nos_gd = data["location_of_thermal_generation"]
		self.PG_min = {}
		self.PG_max = {}
		self.QG_min = {}
		self.QG_max = {}
		self.cost_PG = {}
		for index in range(len(data["set_of_thermal_generator"])):
			self.PG_min[self.GD[index]] = data["minimum_active_power_thermal_generation"][index]
			self.PG_max[self.GD[index]] = data["maximum_active_power_thermal_generation"][index]
			self.QG_min[self.GD[index]] = data["minimum_reactive_power_thermal_generation"][index]
			self.QG_max[self.GD[index]] = data["maximum_reactive_power_thermal_generation"][index]
			self.cost_PG[self.GD[index]] = data["cost_thermal_generation"][index]
		self.dict_nos_bs = data["location_of_energy_storage_system"]
		self.PBmax = {}
		self.EBi = {}
		self.EBmin = {}
		self.EBmax = {}
		self.eta = {}
		for index in range(len(data["set_of_energy_storage_systems"])):
			self.PBmax[self.B[index]] = data["maximum_power_ess"][index]
			self.EBi[self.B[index]] = data["initial_energy_of_the_ess"][index]
			self.EBmin[self.B[index]] = data["minimum_energy_capacity_ess"][index]
			self.EBmax[self.B[index]] = data["maximum_energy_capacity_ess"][index]
			self.eta[self.B[index]] = data["ess_efficiency"][index]
		self.Y = data["number_discrete_blocks_piecewise_linearization"]

		self.Vmax = self.Vnom * 1.05 # kV
		self.Vmin = self.Vnom * 0.92 # kV

	# Function to calculate Parameters
	def CalculateParameters(self):
		self.PDa = {};
		self.PDb = {};
		self.PDc = {};
		self.QDa = {};
		self.QDb = {};
		self.QDc = {};
	
		# Transforms the demands in variate values in the time
		self.List_NT = [];
		for i in self.N:
			for t in self.T:
				self.List_NT += [[i, t]]

		for (i,t) in self.List_NT:
			self.PDa[(i,t)] = ' '
			self.PDb[(i,t)] = ' '
			self.PDc[(i,t)] = ' '
			self.QDa[(i,t)] = ' '
			self.QDa[(i,t)] = ' '
			self.QDa[(i,t)] = ' '
		
		for (i,t) in self.List_NT:
			self.PDa[(i,t)] = self.fm_pa[i][t] * self.PDa_0[i] 
			self.PDb[(i,t)] = self.fm_pb[i][t] * self.PDb_0[i] 
			self.PDc[(i,t)] = self.fm_pc[i][t] * self.PDc_0[i]
			self.QDa[(i,t)] = self.fm_qa[i][t] * self.QDa_0[i]
			self.QDb[(i,t)] = self.fm_qb[i][t] * self.QDb_0[i]
			self.QDc[(i,t)] = self.fm_qc[i][t] * self.QDc_0[i]

		self.PVa = {};
		self.PVb = {};
		self.PVc = {};

		for (i,t) in self.List_NT:
			self.PVa[(i,t)] = ' '
			self.PVb[(i,t)] = ' '
			self.PVc[(i,t)] = ' '

		# Transforms the PV generation in variate values in the time
		for (i,t) in self.List_NT:
			self.PVa[(i,t)] = self.fpv[t] * self.PVa_0[i]
			self.PVb[(i,t)] = self.fpv[t] * self.PVb_0[i]
			self.PVc[(i,t)] = self.fpv[t] * self.PVc_0[i]

		for (i,j) in self.L:
			self.Raa[(i,j)] = self.Raa[(i,j)]/1000
			self.Rbb[(i,j)] = self.Rbb[(i,j)]/1000
			self.Rcc[(i,j)] = self.Rcc[(i,j)]/1000
			self.Rab[(i,j)] = self.Rab[(i,j)]/1000
			self.Rac[(i,j)] = self.Rac[(i,j)]/1000
			self.Rbc[(i,j)] = self.Rbc[(i,j)]/1000
			self.Xaa[(i,j)] = self.Xaa[(i,j)]/1000
			self.Xbb[(i,j)] = self.Xbb[(i,j)]/1000
			self.Xcc[(i,j)] = self.Xcc[(i,j)]/1000
			self.Xab[(i,j)] = self.Xab[(i,j)]/1000
			self.Xac[(i,j)] = self.Xac[(i,j)]/1000
			self.Xbc[(i,j)] = self.Xbc[(i,j)]/1000

		# Calculats the impedance magnitude and angle in the lines
		self.Thaa = {};
		self.Zaa = {};
		self.Thbb = {};
		self.Zbb = {};
		self.Thcc = {};
		self.Zcc = {};
		self.Thab = {};
		self.Zab = {};
		self.Thac = {};
		self.Zac = {};
		self.Thbc = {};
		self.Zbc = {};

		for (i,j) in self.L:
			self.Zaa[(i,j)] = ' '
			self.Zbb[(i,j)] = ' '
			self.Zcc[(i,j)] = ' '
			self.Zab[(i,j)] = ' '
			self.Zac[(i,j)] = ' '
			self.Zbc[(i,j)] = ' '
			self.Thaa[(i,j)] = ' '
			self.Thbb[(i,j)] = ' '
			self.Thcc[(i,j)] = ' '
			self.Thab[(i,j)] = ' '
			self.Thac[(i,j)] = ' '
			self.Thbc[(i,j)] = ' '

		for (i,j) in self.L:
			self.Thaa[(i,j)] = atan(self.Xaa[(i,j)] / self.Raa[(i,j)])
			self.Zaa[(i,j)] = sqrt(self.Raa[(i,j)]**2 + self.Xaa[(i,j)]**2)
			self.Thbb[(i,j)] = atan(self.Xbb[(i,j)] / self.Rbb[(i,j)])
			self.Zbb[(i,j)] = sqrt(self.Rbb[(i,j)]**2 + self.Xbb[(i,j)]**2)
			self.Thcc[(i,j)] = atan(self.Xcc[(i,j)] / self.Rcc[(i,j)])
			self.Zcc[(i,j)] = sqrt(self.Rcc[(i,j)]**2 + self.Xcc[(i,j)]**2)
			self.Thab[(i,j)] = 0
			self.Zab[(i,j)] = sqrt(self.Rab[(i,j)]**2 + self.Xab[(i,j)]**2)
			self.Thac[(i,j)] = 0
			self.Zac[(i,j)] = sqrt(self.Rac[(i,j)]**2 + self.Xac[(i,j)]**2)
			self.Thbc[(i,j)] = 0
			self.Zbc[(i,j)] = sqrt(self.Rbc[(i,j)]**2 + self.Xbc[(i,j)]**2)

		# Defines the angles of the phases
		self.Tha0 = {};
		self.Thb0 = {};
		self.Thc0 = {};

		for i in self.N:
			self.Tha0[i] = 0
			self.Thb0[i] = -2.0944
			self.Thc0[i] = 2.0944

		# Calculation of Transformed Impedance Components
		self.Raa_p = {};
		self.Xaa_p = {};
		self.Rbb_p = {};
		self.Xbb_p = {};
		self.Rcc_p = {};
		self.Xcc_p = {};
		self.Rab_p = {};
		self.Xab_p = {};
		self.Rac_p = {};
		self.Xac_p = {};
		self.Rbc_p = {};
		self.Xbc_p = {};
		self.Rba_p = {};
		self.Xba_p = {};
		self.Rca_p = {};
		self.Xca_p = {};
		self.Rcb_p = {};
		self.Xcb_p = {};
		
		for (i,j) in self.L:
			self.Raa_p[(i,j)] = ' '
			self.Xaa_p[(i,j)] = ' '
			self.Rbb_p[(i,j)] = ' '
			self.Xbb_p[(i,j)] = ' '
			self.Rcc_p[(i,j)] = ' '
			self.Xcc_p[(i,j)] = ' '
			self.Rab_p[(i,j)] = ' '
			self.Xab_p[(i,j)] = ' '
			self.Rac_p[(i,j)] = ' '
			self.Xac_p[(i,j)] = ' '
			self.Rbc_p[(i,j)] = ' '
			self.Xbc_p[(i,j)] = ' '
			self.Rba_p[(i,j)] = ' '
			self.Xba_p[(i,j)] = ' '
			self.Rca_p[(i,j)] = ' '
			self.Xca_p[(i,j)] = ' '
			self.Rcb_p[(i,j)] = ' '
			self.Xcb_p[(i,j)] = ' '

		for (i,j) in self.L:
			self.Raa_p[(i,j)] = self.Zaa[(i,j)] * cos(self.Thaa[(i,j)] + self.Tha0[i] - self.Tha0[i])
			self.Xaa_p[(i,j)] = self.Zaa[(i,j)] * sin(self.Thaa[(i,j)] + self.Tha0[i] - self.Tha0[i])
			self.Rbb_p[(i,j)] = self.Zbb[(i,j)] * cos(self.Thbb[(i,j)] + self.Thb0[i] - self.Thb0[i])
			self.Xbb_p[(i,j)] = self.Zbb[(i,j)] * sin(self.Thbb[(i,j)] + self.Thb0[i] - self.Thb0[i])
			self.Rcc_p[(i,j)] = self.Zcc[(i,j)] * cos(self.Thcc[(i,j)] + self.Thc0[i] - self.Thc0[i])
			self.Xcc_p[(i,j)] = self.Zcc[(i,j)] * sin(self.Thcc[(i,j)] + self.Thc0[i] - self.Thc0[i])
			self.Rab_p[(i,j)] = self.Zab[(i,j)] * cos(self.Thab[(i,j)] + self.Thb0[i] - self.Tha0[i])
			self.Xab_p[(i,j)] = self.Zab[(i,j)] * sin(self.Thab[(i,j)] + self.Thb0[i] - self.Tha0[i])
			self.Rac_p[(i,j)] = self.Zac[(i,j)] * cos(self.Thac[(i,j)] + self.Thc0[i] - self.Tha0[i])
			self.Xac_p[(i,j)] = self.Zac[(i,j)] * sin(self.Thac[(i,j)] + self.Thc0[i] - self.Tha0[i])
			self.Rbc_p[(i,j)] = self.Zbc[(i,j)] * cos(self.Thbc[(i,j)] + self.Thc0[i] - self.Thb0[i])
			self.Xbc_p[(i,j)] = self.Zbc[(i,j)] * sin(self.Thbc[(i,j)] + self.Thc0[i] - self.Thb0[i])
			self.Rba_p[(i,j)] = self.Zab[(i,j)] * cos(self.Thab[(i,j)] + self.Tha0[i] - self.Thb0[i])
			self.Xba_p[(i,j)] = self.Zab[(i,j)] * sin(self.Thab[(i,j)] + self.Tha0[i] - self.Thb0[i])
			self.Rca_p[(i,j)] = self.Zac[(i,j)] * cos(self.Thac[(i,j)] + self.Tha0[i] - self.Thc0[i])
			self.Xca_p[(i,j)] = self.Zac[(i,j)] * sin(self.Thac[(i,j)] + self.Tha0[i] - self.Thc0[i])
			self.Rcb_p[(i,j)] = self.Zbc[(i,j)] * cos(self.Thbc[(i,j)] + self.Thb0[i] - self.Thc0[i])
			self.Xcb_p[(i,j)] = self.Zbc[(i,j)] * sin(self.Thbc[(i,j)] + self.Thb0[i] - self.Thc0[i])		

		self.List_NL = [];
		for a in self.N:
			for (i,j) in self.L:
				self.List_NL += [[a,i,j]]

		self.df = {};
		for (a,i,j) in self.List_NL:
			self.df[(a,i,j)] = ' '

		for a in self.N:
			for (i,j) in self.L:
				if int(a) == int(i):
					self.df[(a,i,j)] = -1
				elif int(a) == int(j):
					self.df[(a,i,j)] = 1
				else:
					self.df[(a,i,j)] = 0

		self.p = {};
		for (a,i,j) in self.List_NL:
			self.p[(a,i,j)] = ' '

		for i in self.N:
			for (a,j) in self.L:
				if int(i) == int(a):
					self.p[(i,a,j)] = 1
				else:
					self.p[(i,a,j)] = 0

		# Define linearization block
		self.PS_Dsmax = {}
		self.QS_Dsmax = {}
		for i in self.N:
			self.PS_Dsmax[(i)] = ' '
			self.QS_Dsmax[(i)] = ' '

		self.PS_ms = {};
		self.QS_ms = {};
		for i in self.N:
			for y in self.Y:
				self.PS_ms[(i,y)] = ' '
				self.QS_ms[(i,y)] = ' '
	
		for i in self.N:
			self.PS_Dsmax[(i)] = self.Smax[i]/len(self.Y)
			self.QS_Dsmax[(i)] = self.Smax[i]/len(self.Y)
			for y in self.Y:
				self.PS_ms[(i,y)] = ((2 * (int(y))) - 1) * self.PS_Dsmax[(i)]
				self.QS_ms[(i,y)] = ((2 * (int(y))) - 1) * self.QS_Dsmax[(i)]

		self.S_Dsmax = {};
		self.S_ms = {};
		for (i,j) in self.L:
			self.S_Dsmax[(i,j)] = ' '
			for y in self.Y:
				self.S_ms[(i,j,y)] = ' '
		
		for (i,j) in self.L:
			self.S_Dsmax[(i,j)] = (self.Vnom * self.Imax[i,j]) / len(self.Y)
			for y in self.Y:
				self.S_ms[(i,j,y)] = ((2 * (int(y))) - 1) * self.S_Dsmax[(i,j)]

		return(self.PDa, self.PDb, self.PDc, self.QDa, self.QDb, self.QDc, self.PVa, self.PVb, self.PVc, self.Raa_p, self.Rbb_p, self.Rcc_p, self.Rab_p, self.Rac_p, self.Rbc_p, self.df, self.PS_Dsmax, self.QS_Dsmax, self.PS_ms, self.QS_ms, self.S_Dsmax, self.S_ms)

	'''
	def ProcessingInfoTypeofSolution(self, solution_type):
		if solution_type == 1:
			self.S = ['1']
			self.Prob = {'1' : 1.0}
			self.srs = {'1' :1.0}
			self.sd = {'1' : 1.0}
			return ("Type_1", self.S, self.Prob, self.srs, self.sd)
		else:
			self.S = ['1','2','3','4','5','6','7','8','9']
			self.Prob = {'1' : 0.02,
				   '2' : 0.06,
				   '3' : 0.02,
				   '4' : 0.16,
				   '5' : 0.48,
				   '6' : 0.16,
				   '7' : 0.02,
				   '8' : 0.06,
				   '9' : 0.02}
			self.srs = {'1' : 1.0,
				   '2' : 0.8,
				   '3' : 0.6,
				   '4' : 1.0,
				   '5' : 0.8,
				   '6' : 0.6,
				   '7' : 1.0,
				   '8' : 0.8,
				   '9' : 0.6}
			self.sd = {'1' : 1.0,
				   '2' : 1.0,
				   '3' : 1.0,
				   '4' : 0.8,
				   '5' : 0.8,
				   '6' : 0.8,
				   '7' : 0.6,
				   '8' : 0.6,
				   '9' : 0.6}
			return ("Type_2", self.S, self.Prob, self.srs, self.sd)
	'''
	
	def SavingApproximations(self,results):
		
		self.List_LTS = [];
		for (i,j) in self.L:
			for t in self.T:
				for s in self.S:
					self.List_LTS += [[i, j, t, s]]
		
		self.List_NTS = [];
		for i in self.N:
			for t in self.T:
				for s in self.S:
					self.List_NTS += [[i, t, s]]

		self.List_LTOS = [];
		for (i,j) in self.L:
			for t in self.T:
				for c in self.O:
					for s in self.S:
						self.List_LTOS += [[i, j, t, c, s]]

		self.List_NTOS = [];
		for i in self.N:
			for t in self.T:
				for c in self.O:
					for s in self.S:
						self.List_NTOS += [[i, t, c, s]]

		self.Pa_0_con = {};
		self.Pb_0_con = {};
		self.Pc_0_con = {};
		self.Qa_0_con = {};
		self.Qb_0_con = {};
		self.Qc_0_con = {};
		for (i,j,t,s) in self.List_LTS:
			self.Pa_0_con[(i,j,t,s)] = ' '
			self.Pb_0_con[(i,j,t,s)] = ' '
			self.Pc_0_con[(i,j,t,s)] = ' '
			self.Qa_0_con[(i,j,t,s)] = ' '
			self.Qb_0_con[(i,j,t,s)] = ' '
			self.Qc_0_con[(i,j,t,s)] = ' '

		for (i,j,t,s) in self.List_LTS:
			self.Pa_0_con[(i,j,t,s)] = results.Pa_con[i,j][t][s]
			self.Pb_0_con[(i,j,t,s)] = results.Pb_con[i,j][t][s]
			self.Pc_0_con[(i,j,t,s)] = results.Pc_con[i,j][t][s]
			self.Qa_0_con[(i,j,t,s)] = results.Qa_con[i,j][t][s]
			self.Qb_0_con[(i,j,t,s)] = results.Qb_con[i,j][t][s]
			self.Qc_0_con[(i,j,t,s)] = results.Qc_con[i,j][t][s]

		self.Va_0_con = {};	
		self.Vb_0_con = {};
		self.Vc_0_con = {};
		for (i,t,s) in self.List_NTS:
			self.Va_0_con[(i,t,s)] = ' '
			self.Vb_0_con[(i,t,s)] = ' '
			self.Vc_0_con[(i,t,s)] = ' '

		for (i,t,s) in self.List_NTS:
			self.Va_0_con[(i,t,s)] = results.Va_con[i][t][s]
			self.Vb_0_con[(i,t,s)] = results.Vb_con[i][t][s]
			self.Vc_0_con[(i,t,s)] = results.Vc_con[i][t][s]

		self.Pa_0 = {};
		self.Pb_0 = {};
		self.Pc_0 = {};
		self.Qa_0 = {};
		self.Qb_0 = {};
		self.Qc_0 = {};
		for (i,j,t,c,s) in self.List_LTOS:
			self.Pa_0[(i,j,t,c,s)] = ' '
			self.Pb_0[(i,j,t,c,s)] = ' '
			self.Pc_0[(i,j,t,c,s)] = ' '
			self.Qa_0[(i,j,t,c,s)] = ' '
			self.Qb_0[(i,j,t,c,s)] = ' '
			self.Qc_0[(i,j,t,c,s)] = ' '

		for (i,j,t,c,s) in self.List_LTOS:
			self.Pa_0[(i,j,t,c,s)] = results.Pa[i,j][t][c][s]
			self.Pb_0[(i,j,t,c,s)] = results.Pb[i,j][t][c][s]
			self.Pc_0[(i,j,t,c,s)] = results.Pc[i,j][t][c][s]
			self.Qa_0[(i,j,t,c,s)] = results.Qa[i,j][t][c][s]
			self.Qb_0[(i,j,t,c,s)] = results.Qb[i,j][t][c][s]
			self.Qc_0[(i,j,t,c,s)] = results.Qc[i,j][t][c][s]

		self.Va_0 = {};	
		self.Vb_0 = {};	
		self.Vc_0 = {};	
		for (i,t,c,s) in self.List_NTOS:
			self.Va_0[(i,t,c,s)] = ' '
			self.Vb_0[(i,t,c,s)] = ' '
			self.Vc_0[(i,t,c,s)] = ' '

		for (i,t,c,s) in self.List_NTOS:
			self.Va_0[(i,t,c,s)] = results.Va[i][t][c][s]
			self.Vb_0[(i,t,c,s)] = results.Vb[i][t][c][s]
			self.Vc_0[(i,t,c,s)] = results.Vc[i][t][c][s]

		return True
		
		
	