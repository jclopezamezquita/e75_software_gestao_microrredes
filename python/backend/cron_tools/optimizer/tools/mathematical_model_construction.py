""""
========================== Mathematical Modelling ==============================
"""
import os
import sys
from pulp import *
import math

class MathematicalModel:
	def __init__(self, data):
		self.data = data

	def ConstructionOfLists(self):
		# self.List formed by sets T, S and C
		data = self.data
		self.List_LTS = [];
		for (i,j) in data.L:
			for t in data.T:
				for s in data.S:
					self.List_LTS += [[i, j, t, s]]
		self.List_NTS = [];
		for i in data.N:
			for t in data.T:
				for s in data.S:
					self.List_NTS += [[i, t, s]]
		self.List_GDTS = [];
		for i in data.GD:
			for t in data.T:
				for s in data.S:
					self.List_GDTS += [[i, t, s]]
		self.List_LTOS = [];
		for (i,j) in data.L:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_LTOS += [[i, j, t, c, s]]
		self.List_NTOS = [];
		for i in data.N:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_NTOS += [[i, t, c, s]]
		self.List_GDTOS = [];
		for i in data.GD:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_GDTOS += [[i, t, c, s]]
		self.List_BT = [];
		for i in data.B:
			for t in data.T:
				self.List_BT += [[i, t]]
		self.List_NTSY = [];
		for i in data.N:
			for t in data.T:
				for s in data.S:
					for y in data.Y:
						self.List_NTSY += [[i, t, s, y]]
		self.List_LTSY = [];
		for (i,j) in data.L:
			for t in data.T:
				for s in data.S:
					for y in data.Y:
						self.List_LTSY += [[i, j, t, s, y]]
		self.List_NTOSY = [];
		for i in data.N:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						for y in data.Y:
							self.List_NTOSY += [[i, t, c, s, y]]
		self.List_LTOSY = [];
		for (i,j) in data.L:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						for y in data.Y:
							self.List_LTOSY += [[i, j, t, c, s, y]]
		self.List_GDTSY = [];
		for i in data.GD:
			for t in data.T:
				for s in data.S:
					for y in data.Y:
						self.List_GDTSY += [[i, t, s, y]]
		self.List_GDTOSY = [];
		for i in data.GD:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						for y in data.Y:
							self.List_GDTOSY += [[i, t, c, s, y]]
		
		#return (self.List_NTS, self.List_NTOS, self.List_LTS, self.List_LTOS, self.List_SETS, self.List_SETOS, self.List_sPDTS, self.List_sQDTS, self.List_sPDTOS, self.List_sQDTOS, self.List_GDTS, self.List_GDTOS, self.List_sPVT, self.List_sPVTO, self.List_BT, self.List_LTSY, self.List_LTOSY, self.List_SETSY, self.List_SETOSY, self.List_GDTSY, self.List_GDTOSY)

	def ProblemFormultion_ColdStart(self):
		data = self.data

		# Type of problem
		prob_CS = LpProblem("Cold_Start_for_EMS",LpMinimize)

		# Declare variables
		# Grid - without outage (grid-connected operation)
		Pa_con = LpVariable.dicts("Pa_con",(data.L, data.T, data.S))
		Pb_con = LpVariable.dicts("Pb_con",(data.L, data.T, data.S))
		Pc_con = LpVariable.dicts("Pc_con",(data.L, data.T, data.S))
		Qa_con = LpVariable.dicts("Qa_con",(data.L, data.T, data.S))
		Qb_con = LpVariable.dicts("Qb_con",(data.L, data.T, data.S))
		Qc_con = LpVariable.dicts("Qc_con",(data.L, data.T, data.S))
		Va_con = LpVariable.dicts("Va_con",(data.N, data.T, data.S))
		Vb_con = LpVariable.dicts("Vb_con",(data.N, data.T, data.S))
		Vc_con = LpVariable.dicts("Vc_con",(data.N, data.T, data.S))
		PS_a_con = LpVariable.dicts("PS_a_con",(data.N, data.T, data.S))
		PS_b_con = LpVariable.dicts("PS_b_con",(data.N, data.T, data.S))
		PS_c_con = LpVariable.dicts("PS_c_con",(data.N, data.T, data.S))
		QS_a_con = LpVariable.dicts("QS_a_con",(data.N, data.T, data.S))
		QS_b_con = LpVariable.dicts("QS_b_con",(data.N, data.T, data.S))
		QS_c_con = LpVariable.dicts("QS_c_con",(data.N, data.T, data.S))
		PS_con = LpVariable.dicts("PS_con",(data.N, data.T, data.S))
		QS_con = LpVariable.dicts("QS_con",(data.N, data.T, data.S))

		# Genset - without outage (grid-connected operation)
		PGa_con = LpVariable.dicts("PGa_con",(data.GD, data.T, data.S))
		PGb_con = LpVariable.dicts("PGb_con",(data.GD, data.T, data.S))
		PGc_con = LpVariable.dicts("PGc_con",(data.GD, data.T, data.S))
		QGa_con = LpVariable.dicts("QGa_con",(data.GD, data.T, data.S))
		QGb_con = LpVariable.dicts("QGb_con",(data.GD, data.T, data.S))
		QGc_con = LpVariable.dicts("QGc_con",(data.GD, data.T, data.S))
		PG_con = LpVariable.dicts("PG_con",(data.GD, data.T, data.S))
		QG_con = LpVariable.dicts("QG_con",(data.GD, data.T, data.S))

		# Grid - with outage (grid islanded operation)
		Pa = LpVariable.dicts("Pa",(data.L, data.T, data.O, data.S))
		Pb = LpVariable.dicts("Pb",(data.L, data.T, data.O, data.S))
		Pc = LpVariable.dicts("Pc",(data.L, data.T, data.O, data.S))
		Qa = LpVariable.dicts("Qa",(data.L, data.T, data.O, data.S))
		Qb = LpVariable.dicts("Qb",(data.L, data.T, data.O, data.S))
		Qc = LpVariable.dicts("Qc",(data.L, data.T, data.O, data.S))
		Va = LpVariable.dicts("Va",(data.N, data.T, data.O, data.S))
		Vb = LpVariable.dicts("Vb",(data.N, data.T, data.O, data.S))
		Vc = LpVariable.dicts("Vc",(data.N, data.T, data.O, data.S))
		PS_a = LpVariable.dicts("PS_a",(data.N, data.T, data.O, data.S))
		PS_b = LpVariable.dicts("PS_b",(data.N, data.T, data.O, data.S))
		PS_c = LpVariable.dicts("PS_c",(data.N, data.T, data.O, data.S))
		QS_a = LpVariable.dicts("QS_a",(data.N, data.T, data.O, data.S))
		QS_b = LpVariable.dicts("QS_b",(data.N, data.T, data.O, data.S))
		QS_c = LpVariable.dicts("QS_c",(data.N, data.T, data.O, data.S))
		PS = LpVariable.dicts("PS",(data.N, data.T, data.O, data.S))
		QS = LpVariable.dicts("QS",(data.N, data.T, data.O, data.S))
		xd = LpVariable.dicts("xd",(data.N, data.T, data.O, data.S),0,1)

		# Genset - with outage (grid islanded operation)
		PGa = LpVariable.dicts("PGa",(data.GD, data.T, data.O, data.S))
		PGb = LpVariable.dicts("PGb",(data.GD, data.T, data.O, data.S))
		PGc = LpVariable.dicts("PGc",(data.GD, data.T, data.O, data.S))
		PG = LpVariable.dicts("PG",(data.GD, data.T, data.O, data.S))
		QGa = LpVariable.dicts("QGa",(data.GD, data.T, data.O, data.S))
		QGb = LpVariable.dicts("QGb",(data.GD, data.T, data.O, data.S))
		QGc = LpVariable.dicts("QGc",(data.GD, data.T, data.O, data.S))
		QG = LpVariable.dicts("QG",(data.GD, data.T, data.O, data.S))

		# Objective function
		lpSum([])

		if len(data.O) >= 1:
			prob_CS += \
				lpSum([data.Prob[(s)] * (0.01/len(data.O) * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a[i][t][c][s]+PS_b[i][t][c][s]+PS_c[i][t][c][s]) for (i,t,c,s) in self.List_NTOS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG[i][t][c][s] for (i,t,c,s) in self.List_GDTOS]) + \
				lpSum([data.delta_t * data.alpha_c[(i)] * data.sd[(s)] * (data.PDa[(i,t)]+data.PDb[(i,t)]+data.PDc[(i,t)]) * (1-xd[i][t][c][s]) for (i,t,c,s) in self.List_NTOS])) + \
				0.99 * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a_con[i][t][s] + PS_b_con[i][t][s] + PS_c_con[i][t][s]) for (i,t,s) in self.List_NTS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG_con[i][t][s] for (i,t,s) in self.List_GDTS]))) for s in data.S]), "Objective_Function_CS"
		else:
			prob_CS += \
				lpSum([data.Prob[(s)] * (0.01/1000000 * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a[i][t][c][s]+PS_b[i][t][c][s]+PS_c[i][t][c][s]) for (i,t,c,s) in self.List_NTOS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG[i][t][c][s] for (i,t,c,s) in self.List_GDTOS]) + \
				lpSum([data.delta_t * data.alpha_c[(i)] * data.sd[(s)] * (data.PDa[(i,t)]+data.PDb[(i,t)]+data.PDc[(i,t)]) * (1-xd[i][t][c][s]) for (i,t,c,s) in self.List_NTOS])) + \
				0.99 * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a_con[i][t][s] + PS_b_con[i][t][s] + PS_c_con[i][t][s]) for (i,t,s) in self.List_NTS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG_con[i][t][s] for (i,t,s) in self.List_GDTS]))) for s in data.S]), "Objective_Function_CS"

		# Active Power Flow ---------------------------------------------------------------- 
		for (i,t,s) in self.List_NTS:
			prob_CS += lpSum([Pa_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) + PS_a_con[i][t][s] + \
			lpSum([PGa_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.PDa[(i,t)] * data.sd[(s)] == 0, "Active_Power_Balance_Phase_a_con_CS_%s" %str((i,t,s))
		
		for (i,t,s) in self.List_NTS:
			prob_CS += lpSum([Pb_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) + PS_b_con[i][t][s] + \
			lpSum([PGb_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.PDb[(i,t)] * data.sd[(s)] == 0, "Active_Power_Balance_Phase_b_con_CS_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob_CS += lpSum([Pc_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) + PS_c_con[i][t][s] + \
			lpSum([PGc_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.PDc[(i,t)] * data.sd[(s)] == 0, "Active_Power_Balance_Phase_c_con_CS_%s" %str((i,t,s))

		# Reactive Power Flow ----------------------------------------------------------------
		for (i,t,s) in self.List_NTS:
			prob_CS += lpSum([Qa_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) + QS_a_con[i][t][s] + \
			lpSum([QGa_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.QDa[(i,t)] * data.sd[(s)] == 0, "Reactive_Power_Balance_Phase_a_con_CS_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob_CS += lpSum([Qb_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) + QS_b_con[i][t][s] + \
			lpSum([QGb_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.QDb[(i,t)] * data.sd[(s)] == 0, "Reactive_Power_Balance_Phase_b_con_CS_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob_CS += lpSum([Qc_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) + QS_c_con[i][t][s] + \
			lpSum([QGc_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.QDc[(i,t)] * data.sd[(s)] == 0, "Reactive_Power_Balance_Phase_c_con_CS_%s" %str((i,t,s))

		# Genset  ----------------------------------------------------------------
		for (n,t,s) in self.List_GDTS:
			prob_CS += PGa_con[n][t][s] +  PGb_con[n][t][s] + PGc_con[n][t][s] - PG_con[n][t][s] == 0, "Total_active_power_GD_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += QGa_con[n][t][s] +  QGb_con[n][t][s] + QGc_con[n][t][s] - QG_con[n][t][s] == 0, "Total_reactive_power_GD_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += data.PG_min[(n)] <= PG_con[n][t][s], "Active_Power_Limit_GD_1_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += PG_con[n][t][s] <= data.PG_max[(n)], "Active_Power_Limit_GD_2_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += data.QG_min[(n)] <= QG_con[n][t][s], "Reactive_Power_Limit_GD_1_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += QG_con[n][t][s] <= data.QG_max[(n)], "Reactive_Power_Limit_GD_2_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += PGa_con[n][t][s] == 0, "Grid_connected_active_phase_a_con_CS_%s" %str((n,t,s))
		
		for (n,t,s) in self.List_GDTS:
			prob_CS += PGb_con[n][t][s] == 0, "Grid_connected_active_phase_b_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += PGc_con[n][t][s] == 0, "Grid_connected_active_phase_c_con_CS_%s" %str((n,t,s))
		
		for (n,t,s) in self.List_GDTS:
			prob_CS += QGa_con[n][t][s] == 0, "Grid_connected_reactive_phase_a_con_CS_%s" %str((n,t,s))
		
		for (n,t,s) in self.List_GDTS:
			prob_CS += QGb_con[n][t][s] == 0, "Grid_connected_reactive_phase_b_con_CS_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob_CS += QGc_con[n][t][s] == 0, "Grid_connected_reactive_phase_c_con_CS_%s" %str((n,t,s))

		# Island Operation
		for (i,t,c,s) in self.List_NTOS:
			if int(t) >= int(c) and int(t) < int(c) + 2:
				prob_CS += PS_a[i][t][c][s] == 0, "Island_operation_active_phase_a_CS_%s" %str((i,t,c,s))
				prob_CS += PS_b[i][t][c][s] == 0, "Island_operation_active_phase_b_CS_%s" %str((i,t,c,s))
				prob_CS += PS_c[i][t][c][s] == 0, "Island_operation_active_phase_c_CS_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			if int(t) >= int(c) and int(t) < int(c) + 2:
				prob_CS += QS_a[i][t][c][s] == 0, "Island_operation_reactive_phase_a_CS_%s" %str((i,t,c,s))
				prob_CS += QS_b[i][t][c][s] == 0, "Island_operation_reactive_phase_b_CS_%s" %str((i,t,c,s))
				prob_CS += QS_c[i][t][c][s] == 0, "Island_operation_reactive_phase_c_CS_%s" %str((i,t,c,s))

		# ------------------------------------------------------------------------------
		#------------- Operation with outage - COLD START ------------------------------
		# ------------------------------------------------------------------------------
		#
		# Active Power Flow ----------------------------------------------------------------
		for (i,t,c,s) in self.List_NTOS:
			prob_CS += lpSum([Pa[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) + PS_a[i][t][c][s] + \
			lpSum([PGa[a][t][c][s] for a in data.dict_nos_gd[i]])  - data.PDa[(i,t)] * data.sd[(s)] * xd[i][t][c][s] == 0, "Active_Power_Balance_Phase_a_CS_%s" %str((i,t,c,s))
		
		for (i,t,c,s) in self.List_NTOS:
			prob_CS += lpSum([Pb[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) + PS_b[i][t][c][s] + \
			lpSum([PGb[a][t][c][s] for a in data.dict_nos_gd[i]]) - data.PDb[(i,t)] * data.sd[(s)] * xd[i][t][c][s] == 0, "Active_Power_Balance_Phase_b_CS_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob_CS += lpSum([Pc[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) + PS_c[i][t][c][s] + \
			lpSum([PGc[a][t][c][s] for a in data.dict_nos_gd[i]]) - data.PDc[(i,t)] * data.sd[(s)] * xd[i][t][c][s] == 0, "Active_Power_Balance_Phase_c_CS_%s" %str((i,t,c,s))

		# Reactive Power Flow ----------------------------------------------------------------
		for (i,t,c,s) in self.List_NTOS:
			prob_CS += lpSum([Qa[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) + QS_a[i][t][c][s] + \
			lpSum([QGa[a][t][c][s] for a in data.dict_nos_gd[i]]) - data.QDa[(i,t)] * data.sd[(s)] * xd[i][t][c][s] == 0, "Reactive_Power_Balance_Phase_a_CS_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob_CS += lpSum([Qb[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) + QS_b[i][t][c][s] + \
			lpSum([QGb[a][t][c][s] for a in data.dict_nos_gd[i]]) - data.QDb[(i,t)] * data.sd[(s)] * xd[i][t][c][s] == 0, "Reactive_Power_Balance_Phase_b_CS_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob_CS += lpSum([Qc[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) + QS_c[i][t][c][s] + \
			lpSum([QGc[a][t][c][s] for a in data.dict_nos_gd[i]]) - data.QDc[(i,t)] * data.sd[(s)] * xd[i][t][c][s] == 0, "Reactive_Power_Balance_Phase_c_CS_%s" %str((i,t,c,s))
		
		# Genset --------------------------------------------------------------------
		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += PGa[n][t][c][s] +  PGb[n][t][c][s] + PGc[n][t][c][s] - PG[n][t][c][s] == 0, "Total_active_power_GD_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += QGa[n][t][c][s] +  QGb[n][t][c][s] + QGc[n][t][c][s] - QG[n][t][c][s] == 0, "Total_reactive_power_GD_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += data.PG_min[(n)] <= PG[n][t][c][s], "Active_Power_Limit_GD_1_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += PG[n][t][c][s] <= data.PG_max[(n)], "Active_Power_Limit_GD_2_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += data.QG_min[(n)] <= QG[n][t][c][s], "Reactive_Power_Limit_GD_1_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += QG[n][t][c][s] <= data.QG_max[(n)], "Reactive_Power_Limit_GD_2_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += PGa[n][t][c][s] == 0, "Grid_connected_active_phase_a_CS_%s" %str((n,t,c,s))
		
		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += PGb[n][t][c][s] == 0, "Grid_connected_active_phase_b_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += PGc[n][t][c][s] == 0, "Grid_connected_active_phase_c_CS_%s" %str((n,t,c,s))
		
		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += QGa[n][t][c][s] == 0, "Grid_connected_reactive_phase_a_CS_%s" %str((n,t,c,s))
		
		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += QGb[n][t][c][s] == 0, "Grid_connected_reactive_phase_b_CS_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob_CS += QGc[n][t][c][s] == 0, "Grid_connected_reactive_phase_c_CS_%s" %str((n,t,c,s))

		#----------------- FIX Variables --------------------------------------------------
		for (n,t,s) in self.List_NTS:
			if data.Tb[(n)] != 1:
				prob_CS += PS_a_con[n][t][s] == 0, "Fix_Active_Power_Bus_Load_con_a_CS_%s" %str((n,t,s))
				prob_CS += PS_b_con[n][t][s] == 0, "Fix_Active_Power_Bus_Load_con_b_CS_%s" %str((n,t,s))
				prob_CS += PS_c_con[n][t][s] == 0, "Fix_Active_Power_Bus_Load_con_c_CS_%s" %str((n,t,s))
				prob_CS += QS_a_con[n][t][s] == 0, "Fix_REactive_Power_Bus_Load_con_a_CS_%s" %str((n,t,s))
				prob_CS += QS_b_con[n][t][s] == 0, "Fix_REactive_Power_Bus_Load_con_b_CS_%s" %str((n,t,s))
				prob_CS += QS_c_con[n][t][s] == 0, "Fix_REactive_Power_Bus_Load_con_c_CS_%s" %str((n,t,s))

		for (n,t,c,s) in self.List_NTOS:
			if data.Tb[(n)] != 1:
				prob_CS += PS_a[n][t][c][s] == 0, "Fix_Active_Power_Bus_Load_a_CS_%s" %str((n,t,c,s))
				prob_CS += PS_b[n][t][c][s] == 0, "Fix_Active_Power_Bus_Load_b_CS_%s" %str((n,t,c,s))
				prob_CS += PS_c[n][t][c][s] == 0, "Fix_Active_Power_Bus_Load_c_CS_%s" %str((n,t,c,s))
				prob_CS += QS_a[n][t][c][s] == 0, "Fix_Reactive_Power_Bus_Load_a_CS_%s" %str((n,t,c,s))
				prob_CS += QS_b[n][t][c][s] == 0, "Fix_Reactive_Power_Bus_Load_b_CS_%s" %str((n,t,c,s))
				prob_CS += QS_c[n][t][c][s] == 0, "Fix_Reactive_Power_Bus_Load_c_CS_%s" %str((n,t,c,s))

		for (n,t,s) in self.List_NTS:
			prob_CS += Va_con[n][t][s] == data.Vnom, "Fix_Voltage_con_a_CS_%s" %str((n,t,s))
			prob_CS += Vb_con[n][t][s] == data.Vnom, "Fix_Voltage_con_b_CS_%s" %str((n,t,s))
			prob_CS += Vc_con[n][t][s] == data.Vnom, "Fix_Voltage_con_c_CS_%s" %str((n,t,s))	

		for (n,t,c,s) in self.List_NTOS:
			prob_CS += Va[n][t][c][s] == data.Vnom, "Fix_Voltage_a_CS_%s" %str((n,t,c,s))
			prob_CS += Vb[n][t][c][s] == data.Vnom, "Fix_Voltage_b_CS_%s" %str((n,t,c,s))
			prob_CS += Vc[n][t][c][s] == data.Vnom, "Fix_Voltage_c_CS_%s" %str((n,t,c,s))

		return prob_CS

	def WritingProblemFileCS(self, prob_CS, filename):
		# The problem data is written to an .lp file
		prob_CS.writeLP(filename + ".lp")

	def Solving_Model_CS(self,prob_CS):
		data = self.data
		try:
			cwd = os.getcwd()
			prob_CS.solve(solver=MOSEK(task_file_name = 'dump.task.gz'))
		except Exception as e:
			prob_CS.solve()

		self.Status = LpStatus[prob_CS.status]
		self.ObjectiveFunctionValue = value(prob_CS.objective)

		Variablenames = prob_CS.variables() # This is a self.List
		# Getting a self.Lists with the name and value of all problem variables
		varDic = {}
		for v in prob_CS.variables():
			varDic[v.name] = v.varValue
		self.varDic = varDic

		# Creating dictionaries for variables depending of self.List_LTS
		self.Pa_con = self.CreateDictionaryForEachVariable_LTS(varDic, 'Pa_con')
		self.Pb_con = self.CreateDictionaryForEachVariable_LTS(varDic, 'Pb_con')
		self.Pc_con = self.CreateDictionaryForEachVariable_LTS(varDic, 'Pc_con')
		self.Qa_con = self.CreateDictionaryForEachVariable_LTS(varDic, 'Qa_con')
		self.Qb_con = self.CreateDictionaryForEachVariable_LTS(varDic, 'Qb_con')
		self.Qc_con = self.CreateDictionaryForEachVariable_LTS(varDic, 'Qc_con')

		# Creating dictionaries for variables depending of self.List_NTS
		self.Va_con = self.CreateDictionaryForEachVariable_NTS(varDic, 'Va_con')
		self.Vb_con = self.CreateDictionaryForEachVariable_NTS(varDic, 'Vb_con')
		self.Vc_con = self.CreateDictionaryForEachVariable_NTS(varDic, 'Vc_con')

		# Creating dictionaries for variables depending of self.List_LTOS
		self.Pa = self.CreateDictionaryForEachVariable_LTOS(varDic, 'Pa')
		self.Pb = self.CreateDictionaryForEachVariable_LTOS(varDic, 'Pb')
		self.Pc = self.CreateDictionaryForEachVariable_LTOS(varDic, 'Pc')
		self.Qa = self.CreateDictionaryForEachVariable_LTOS(varDic, 'Qa')
		self.Qb = self.CreateDictionaryForEachVariable_LTOS(varDic, 'Qb')
		self.Qc = self.CreateDictionaryForEachVariable_LTOS(varDic, 'Qc')

		# Creating dictionaries for variables depending of self.List_NTOS
		self.Va = self.CreateDictionaryForEachVariable_NTOS(varDic, 'Va')
		self.Vb = self.CreateDictionaryForEachVariable_NTOS(varDic, 'Vb')
		self.Vc = self.CreateDictionaryForEachVariable_NTOS(varDic, 'Vc')
		

	def ProblemFormulation(self):
		data = self.data

		# Type of problem
		prob = LpProblem("EMS_three_phase_for_Microgrids",LpMinimize)

		# Declare variables
		# Grid - without outage (grid-connected operation)
		Pa_con = LpVariable.dicts("Pa_con",(data.L, data.T, data.S))
		Pb_con = LpVariable.dicts("Pb_con",(data.L, data.T, data.S))
		Pc_con = LpVariable.dicts("Pc_con",(data.L, data.T, data.S))
		Qa_con = LpVariable.dicts("Qa_con",(data.L, data.T, data.S))
		Qb_con = LpVariable.dicts("Qb_con",(data.L, data.T, data.S))
		Qc_con = LpVariable.dicts("Qc_con",(data.L, data.T, data.S))
		Va_con = LpVariable.dicts("Va_con",(data.N, data.T, data.S))
		Vb_con = LpVariable.dicts("Vb_con",(data.N, data.T, data.S))
		Vc_con = LpVariable.dicts("Vc_con",(data.N, data.T, data.S))
		Plss_a_con = LpVariable.dicts("Plss_a_con",(data.L, data.T, data.S))
		Plss_b_con = LpVariable.dicts("Plss_b_con",(data.L, data.T, data.S))
		Plss_c_con = LpVariable.dicts("Plss_c_con",(data.L, data.T, data.S))
		Qlss_a_con = LpVariable.dicts("Qlss_a_con",(data.L, data.T, data.S))
		Qlss_b_con = LpVariable.dicts("Qlss_b_con",(data.L, data.T, data.S))
		Qlss_c_con = LpVariable.dicts("Qlss_c_con",(data.L, data.T, data.S))
		PS_a_con = LpVariable.dicts("PS_a_con",(data.N, data.T, data.S))
		PS_b_con = LpVariable.dicts("PS_b_con",(data.N, data.T, data.S))
		PS_c_con = LpVariable.dicts("PS_c_con",(data.N, data.T, data.S))
		QS_a_con = LpVariable.dicts("QS_a_con",(data.N, data.T, data.S))
		QS_b_con = LpVariable.dicts("QS_b_con",(data.N, data.T, data.S))
		QS_c_con = LpVariable.dicts("QS_c_con",(data.N, data.T, data.S))
		PS_con = LpVariable.dicts("PS_con",(data.N, data.T, data.S))
		QS_con = LpVariable.dicts("QS_con",(data.N, data.T, data.S))
		
		# Genset - without outage (grid-connected operation)
		PGa_con = LpVariable.dicts("PGa_con",(data.GD, data.T, data.S))
		PGb_con = LpVariable.dicts("PGb_con",(data.GD, data.T, data.S))
		PGc_con = LpVariable.dicts("PGc_con",(data.GD, data.T, data.S))
		QGa_con = LpVariable.dicts("QGa_con",(data.GD, data.T, data.S))
		QGb_con = LpVariable.dicts("QGb_con",(data.GD, data.T, data.S))
		QGc_con = LpVariable.dicts("QGc_con",(data.GD, data.T, data.S))
		PG_con = LpVariable.dicts("PG_con",(data.GD, data.T, data.S))
		QG_con = LpVariable.dicts("QG_con",(data.GD, data.T, data.S))

		# Grid - with outage (grid islanded operation)
		Pa = LpVariable.dicts("Pa",(data.L, data.T, data.O, data.S))
		Pb = LpVariable.dicts("Pb",(data.L, data.T, data.O, data.S))
		Pc = LpVariable.dicts("Pc",(data.L, data.T, data.O, data.S))
		Qa = LpVariable.dicts("Qa",(data.L, data.T, data.O, data.S))
		Qb = LpVariable.dicts("Qb",(data.L, data.T, data.O, data.S))
		Qc = LpVariable.dicts("Qc",(data.L, data.T, data.O, data.S))
		Va = LpVariable.dicts("Va",(data.N, data.T, data.O, data.S))
		Vb = LpVariable.dicts("Vb",(data.N, data.T, data.O, data.S))
		Vc = LpVariable.dicts("Vc",(data.N, data.T, data.O, data.S))
		Plss_a = LpVariable.dicts("Plss_a",(data.L, data.T, data.O, data.S))
		Plss_b = LpVariable.dicts("Plss_b",(data.L, data.T, data.O, data.S))
		Plss_c = LpVariable.dicts("Plss_c",(data.L, data.T, data.O, data.S))
		Qlss_a = LpVariable.dicts("Qlss_a",(data.L, data.T, data.O, data.S))
		Qlss_b = LpVariable.dicts("Qlss_b",(data.L, data.T, data.O, data.S))
		Qlss_c = LpVariable.dicts("Qlss_c",(data.L, data.T, data.O, data.S))
		PS_a = LpVariable.dicts("PS_a",(data.N, data.T, data.O, data.S))
		PS_b = LpVariable.dicts("PS_b",(data.N, data.T, data.O, data.S))
		PS_c = LpVariable.dicts("PS_c",(data.N, data.T, data.O, data.S))
		QS_a = LpVariable.dicts("QS_a",(data.N, data.T, data.O, data.S))
		QS_b = LpVariable.dicts("QS_b",(data.N, data.T, data.O, data.S))
		QS_c = LpVariable.dicts("QS_c",(data.N, data.T, data.O, data.S))
		PS = LpVariable.dicts("PS",(data.N, data.T, data.O, data.S))
		QS = LpVariable.dicts("QS",(data.N, data.T, data.O, data.S))
		xd = LpVariable.dicts("xd",(data.N, data.T, data.O, data.S),cat='Binary')

		# Genset - with outage (grid islanded operation)
		PGa = LpVariable.dicts("PGa",(data.GD, data.T, data.O, data.S))
		PGb = LpVariable.dicts("PGb",(data.GD, data.T, data.O, data.S))
		PGc = LpVariable.dicts("PGc",(data.GD, data.T, data.O, data.S))
		PG = LpVariable.dicts("PG",(data.GD, data.T, data.O, data.S))
		QGa = LpVariable.dicts("QGa",(data.GD, data.T, data.O, data.S))
		QGb = LpVariable.dicts("QGb",(data.GD, data.T, data.O, data.S))
		QGc = LpVariable.dicts("QGc",(data.GD, data.T, data.O, data.S))
		QG = LpVariable.dicts("QG",(data.GD, data.T, data.O, data.S))

		# Energy Storage System - Battery
		EB = LpVariable.dicts("EB",(data.B, data.T))
		PB = LpVariable.dicts("PB",(data.B, data.T))
		QB = LpVariable.dicts("QB",(data.B, data.T))
		QB_dis_a = LpVariable.dicts("QB_dis_a",(data.B, data.T))
		QB_dis_b = LpVariable.dicts("QB_dis_b",(data.B, data.T))
		QB_dis_c = LpVariable.dicts("QB_dis_c",(data.B, data.T))
		b_ch = LpVariable.dicts("b_ch",(data.B, data.T),cat='Binary')
		b_dis = LpVariable.dicts("b_dis",(data.B, data.T),cat='Binary')
		PB_ch = LpVariable.dicts("PB_ch",(data.B, data.T))
		PB_dis = LpVariable.dicts("PB_dis",(data.B, data.T))
		PB_ch_a = LpVariable.dicts("PB_ch_a",(data.B, data.T))
		PB_ch_b = LpVariable.dicts("PB_ch_b",(data.B, data.T))
		PB_ch_c = LpVariable.dicts("PB_ch_c",(data.B, data.T))
		PB_dis_a = LpVariable.dicts("PB_dis_a",(data.B, data.T))
		PB_dis_b = LpVariable.dicts("PB_dis_b",(data.B, data.T))
		PB_dis_c = LpVariable.dicts("PB_dis_c",(data.B, data.T))
		
		# --------------------------- Linearization: Without outage -----------------------------------
		# Variables for linearization
		# Power flow (Pa_con, Pb_con, Pc_con and Qa_con, Qb_con, Qc_con): without outage
		Pa_sqr_con = LpVariable.dicts("Pa_sqr_con",(data.L, data.T, data.S))
		Pb_sqr_con = LpVariable.dicts("Pb_sqr_con",(data.L, data.T, data.S))
		Pc_sqr_con = LpVariable.dicts("Pc_sqr_con",(data.L, data.T, data.S))
		Qa_sqr_con = LpVariable.dicts("Qa_sqr_con",(data.L, data.T, data.S))
		Qb_sqr_con = LpVariable.dicts("Qb_sqr_con",(data.L, data.T, data.S))
		Qc_sqr_con = LpVariable.dicts("Qc_sqr_con",(data.L, data.T, data.S))
		Pa_Dp_con = LpVariable.dicts("Pa_Dp_con",(data.L, data.T, data.S, data.Y),0)
		Pb_Dp_con = LpVariable.dicts("Pb_Dp_con",(data.L, data.T, data.S, data.Y),0)
		Pc_Dp_con = LpVariable.dicts("Pc_Dp_con",(data.L, data.T, data.S, data.Y),0)
		Qa_Dp_con = LpVariable.dicts("Qa_Dp_con",(data.L, data.T, data.S, data.Y),0)
		Qb_Dp_con = LpVariable.dicts("Qb_Dp_con",(data.L, data.T, data.S, data.Y),0)
		Qc_Dp_con = LpVariable.dicts("Qc_Dp_con",(data.L, data.T, data.S, data.Y),0)
		Pa_p_con = LpVariable.dicts("Pa_p_con",(data.L, data.T, data.S),0)
		Pb_p_con = LpVariable.dicts("Pb_p_con",(data.L, data.T, data.S),0)
		Pc_p_con = LpVariable.dicts("Pc_p_con",(data.L, data.T, data.S),0)
		Qa_p_con = LpVariable.dicts("Qa_p_con",(data.L, data.T, data.S),0)
		Qb_p_con = LpVariable.dicts("Qb_p_con",(data.L, data.T, data.S),0)
		Qc_p_con = LpVariable.dicts("Qc_p_con",(data.L, data.T, data.S),0)
		Pa_n_con = LpVariable.dicts("Pa_n_con",(data.L, data.T, data.S),0)
		Pb_n_con = LpVariable.dicts("Pb_n_con",(data.L, data.T, data.S),0)
		Pc_n_con = LpVariable.dicts("Pc_n_con",(data.L, data.T, data.S),0)
		Qa_n_con = LpVariable.dicts("Qa_n_con",(data.L, data.T, data.S),0)
		Qb_n_con = LpVariable.dicts("Qb_n_con",(data.L, data.T, data.S),0)
		Qc_n_con = LpVariable.dicts("Qc_n_con",(data.L, data.T, data.S),0)

		# Linearization of PS_con and QS_con: without outage
		PSsqr_con = LpVariable.dicts("PSsqr_con",(data.N, data.T, data.S),0)
		QSsqr_con = LpVariable.dicts("QSsqr_con",(data.N, data.T, data.S),0)
		PS_Dp_con = LpVariable.dicts("PS_Dp_con",(data.N, data.T, data.S, data.Y),0)
		QS_Dp_con = LpVariable.dicts("QS_Dp_con",(data.N, data.T, data.S, data.Y),0)
		PS_p_con = LpVariable.dicts("PS_p_con",(data.N, data.T, data.S),0)
		PS_n_con = LpVariable.dicts("PS_n_con",(data.N, data.T, data.S),0)
		QS_p_con = LpVariable.dicts("QS_p_con",(data.N, data.T, data.S),0)
		QS_n_con = LpVariable.dicts("QS_n_con",(data.N, data.T, data.S),0)

		# Linearization of voltage: without outage
		Va_sqr_con = LpVariable.dicts("Va_sqr_con",(data.N, data.T, data.S), data.Vmin**2, data.Vmax**2)
		Vb_sqr_con = LpVariable.dicts("Vb_sqr_con",(data.N, data.T, data.S), data.Vmin**2, data.Vmax**2)
		Vc_sqr_con = LpVariable.dicts("Vc_sqr_con",(data.N, data.T, data.S), data.Vmin**2, data.Vmax**2)

		# --------------------------- With outage --------------------------------------
		# Power flow (Pa, Pb, Pc and Qa, Qb, Qc): with outage
		Pa_sqr = LpVariable.dicts("Pa_sqr",(data.L, data.T, data.O, data.S))
		Pb_sqr = LpVariable.dicts("Pb_sqr",(data.L, data.T, data.O, data.S))
		Pc_sqr = LpVariable.dicts("Pc_sqr",(data.L, data.T, data.O, data.S))
		Qa_sqr = LpVariable.dicts("Qa_sqr",(data.L, data.T, data.O, data.S))
		Qb_sqr = LpVariable.dicts("Qb_sqr",(data.L, data.T, data.O, data.S))
		Qc_sqr = LpVariable.dicts("Qc_sqr",(data.L, data.T, data.O, data.S))
		Pa_Dp = LpVariable.dicts("Pa_Dp",(data.L, data.T, data.O, data.S, data.Y),0)
		Pb_Dp = LpVariable.dicts("Pb_Dp",(data.L, data.T, data.O, data.S, data.Y),0)
		Pc_Dp = LpVariable.dicts("Pc_Dp",(data.L, data.T, data.O, data.S, data.Y),0)
		Qa_Dp = LpVariable.dicts("Qa_Dp",(data.L, data.T, data.O, data.S, data.Y),0)
		Qb_Dp = LpVariable.dicts("Qb_Dp",(data.L, data.T, data.O, data.S, data.Y),0)
		Qc_Dp = LpVariable.dicts("Qc_Dp",(data.L, data.T, data.O, data.S, data.Y),0)
		Pa_p = LpVariable.dicts("Pa_p",(data.L, data.T, data.O, data.S),0)
		Pb_p = LpVariable.dicts("Pb_p",(data.L, data.T, data.O, data.S),0)
		Pc_p = LpVariable.dicts("Pc_p",(data.L, data.T, data.O, data.S),0)
		Qa_p = LpVariable.dicts("Qa_p",(data.L, data.T, data.O, data.S),0)
		Qb_p = LpVariable.dicts("Qb_p",(data.L, data.T, data.O, data.S),0)
		Qc_p = LpVariable.dicts("Qc_p",(data.L, data.T, data.O, data.S),0)
		Pa_n = LpVariable.dicts("Pa_n",(data.L, data.T, data.O, data.S),0)
		Pb_n = LpVariable.dicts("Pb_n",(data.L, data.T, data.O, data.S),0)
		Pc_n = LpVariable.dicts("Pc_n",(data.L, data.T, data.O, data.S),0)
		Qa_n = LpVariable.dicts("Qa_n",(data.L, data.T, data.O, data.S),0)
		Qb_n = LpVariable.dicts("Qb_n",(data.L, data.T, data.O, data.S),0)
		Qc_n = LpVariable.dicts("Qc_n",(data.L, data.T, data.O, data.S),0)

		# Linearization of PS and QS: with outage
		PSsqr = LpVariable.dicts("PSsqr",(data.N, data.T, data.O, data.S),0)
		QSsqr = LpVariable.dicts("QSsqr",(data.N, data.T, data.O, data.S),0)
		PS_Dp = LpVariable.dicts("PS_Dp",(data.N, data.T, data.O, data.S, data.Y),0)
		QS_Dp = LpVariable.dicts("QS_Dp",(data.N, data.T, data.O, data.S, data.Y),0)
		PS_p = LpVariable.dicts("PS_p",(data.N, data.T, data.O, data.S),0)
		PS_n = LpVariable.dicts("PS_n",(data.N, data.T, data.O, data.S),0)
		QS_p = LpVariable.dicts("QS_p",(data.N, data.T, data.O, data.S),0)
		QS_n = LpVariable.dicts("QS_n",(data.N, data.T, data.O, data.S),0)

		# Linearization of voltage: with outage
		Va_sqr = LpVariable.dicts("Va_sqr",(data.N, data.T, data.O, data.S), data.Vmin**2, data.Vmax**2)
		Vb_sqr = LpVariable.dicts("Vb_sqr",(data.N, data.T, data.O, data.S), data.Vmin**2, data.Vmax**2)
		Vc_sqr = LpVariable.dicts("Vc_sqr",(data.N, data.T, data.O, data.S), data.Vmin**2, data.Vmax**2)

		# Objective function
		lpSum([])
		if len(data.O) >= 1: 
			prob += \
				lpSum([data.Prob[(s)] * (0.01/len(data.O) * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a[i][t][c][s]+PS_b[i][t][c][s]+PS_c[i][t][c][s]) for (i,t,c,s) in self.List_NTOS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG[i][t][c][s] for (i,t,c,s) in self.List_GDTOS]) + \
				lpSum([data.delta_t * data.alpha_c[(i)] * data.sd[(s)] * (data.PDa[(i,t)] + data.PDb[(i,t)] + data.PDc[(i,t)]) * (1-xd[i][t][c][s]) for (i,t,c,s) in self.List_NTOS])) + \
				0.99 * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a_con[i][t][s] + PS_b_con[i][t][s] + PS_c_con[i][t][s]) for (i,t,s) in self.List_NTS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG_con[i][t][s] for (i,t,s) in self.List_GDTS]))) for s in data.S]), "Objective_Function"
		
		else:
			prob += \
				lpSum([data.Prob[(s)] * (0.01/1000000 * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a[i][t][c][s]+PS_b[i][t][c][s]+PS_c[i][t][c][s]) for (i,t,c,s) in self.List_NTOS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG[i][t][c][s] for (i,t,c,s) in self.List_GDTOS]) + \
				lpSum([data.delta_t * data.alpha_c[(i)] * data.sd[(s)] * (data.PDa[(i,t)] + data.PDb[(i,t)] + data.PDc[(i,t)]) * (1-xd[i][t][c][s]) for (i,t,c,s) in self.List_NTOS])) + \
				0.99 * (lpSum([data.cEDS[(t)] * data.delta_t * (PS_a_con[i][t][s] + PS_b_con[i][t][s] + PS_c_con[i][t][s]) for (i,t,s) in self.List_NTS]) + \
				lpSum([data.cost_PG[(i)] * data.delta_t * PG_con[i][t][s] for (i,t,s) in self.List_GDTS]))) for s in data.S]), "Objective_Function"

		# --------------------- Constraints --------------------------------------------
		# --------------------- Without outage------------------------------------------
		# Active losses ----------------------------------------------------------------
		for (i,j,t,s) in self.List_LTS:
			prob += (1/(data.Va_0_con[(i,t,s)] * data.Va_0_con[(i,t,s)])) * (data.Raa_p[(i,j)] * Pa_sqr_con[i,j][t][s] + data.Raa_p[(i,j)] * Qa_sqr_con[i,j][t][s] - \
					data.Xaa_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] +  data.Xaa_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Pa_con[i,j][t][s]) + \
				(1/(data.Va_0_con[(i,t,s)] * data.Vb_0_con[(i,t,s)])) * (data.Rab_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] + data.Rab_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] - \
					data.Xab_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] +  data.Xab_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Pa_con[i,j][t][s]) + \
				(1/(data.Va_0_con[(i,t,s)] * data.Vc_0_con[(i,t,s)])) * (data.Rac_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] + data.Rac_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] - \
					data.Xac_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] +  data.Xac_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Pa_con[i,j][t][s]) == Plss_a_con[i,j][t][s], "Active_Power_Losses_a_con_%s" %str((i,j,t,s)) 
		
		for (i,j,t,s) in self.List_LTS:
			prob += (1/(data.Vb_0_con[(i,t,s)] * data.Va_0_con[(i,t,s)])) * (data.Rba_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] + data.Rba_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] - \
					data.Xba_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] +  data.Xba_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Pb_con[i,j][t][s]) + \
				(1/(data.Vb_0_con[(i,t,s)] * data.Vb_0_con[(i,t,s)])) * (data.Rbb_p[(i,j)] * Pb_sqr_con[i,j][t][s] + data.Rbb_p[(i,j)] * Qb_sqr_con[i,j][t][s] - \
					data.Xbb_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] +  data.Xbb_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Pb_con[i,j][t][s]) + \
				(1/(data.Vb_0_con[(i,t,s)] * data.Vc_0_con[(i,t,s)])) * (data.Rbc_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] + data.Rbc_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] - \
					data.Xbc_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] +  data.Xbc_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Pb_con[i,j][t][s]) == Plss_b_con[i,j][t][s], "Active_Power_Losses_b_con_%s" %str((i,j,t,s)) 

		for (i,j,t,s) in self.List_LTS:
			prob += (1/(data.Vc_0_con[(i,t,s)] * data.Va_0_con[(i,t,s)])) * (data.Rca_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] + data.Rca_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] - \
					data.Xca_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] +  data.Xca_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Pc_con[i,j][t][s]) + \
				(1/(data.Vc_0_con[(i,t,s)] * data.Vb_0_con[(i,t,s)])) * (data.Rcb_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] + data.Rcb_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] - \
					data.Xcb_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] +  data.Xcb_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Pc_con[i,j][t][s]) + \
				(1/(data.Vc_0_con[(i,t,s)] * data.Vc_0_con[(i,t,s)])) * (data.Rcc_p[(i,j)] * Pc_sqr_con[i,j][t][s] + data.Rcc_p[(i,j)] * Qc_sqr_con[i,j][t][s] - \
					data.Xcc_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] +  data.Xcc_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Pc_con[i,j][t][s]) == Plss_c_con[i,j][t][s], "Active_Power_Losses_c_con_%s" %str((i,j,t,s)) 

		# Reactive losses ----------------------------------------------------------------
		for (i,j,t,s) in self.List_LTS:
			prob += (1/(data.Va_0_con[(i,t,s)] * data.Va_0_con[(i,t,s)])) * (data.Raa_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] - data.Raa_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] + \
					data.Xaa_p[(i,j)] * Pa_sqr_con[i,j][t][s] +  data.Xaa_p[(i,j)] * Qa_sqr_con[i,j][t][s]) + \
				(1/(data.Va_0_con[(i,t,s)] * data.Vb_0_con[(i,t,s)])) * (data.Rab_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] - data.Rab_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] + \
					data.Xab_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] +  data.Xab_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Qa_con[i,j][t][s]) + \
				(1/(data.Va_0_con[(i,t,s)] * data.Vc_0_con[(i,t,s)])) * (data.Rac_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Qa_con[i,j][t][s] - data.Rac_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] + \
					data.Xac_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Pa_con[i,j][t][s] +  data.Xac_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Qa_con[i,j][t][s]) == Qlss_a_con[i,j][t][s], "Reactive_Power_Losses_a_con_%s" %str((i,j,t,s)) 
		
		for (i,j,t,s) in self.List_LTS:
			prob += (1/(data.Vb_0_con[(i,t,s)] * data.Va_0_con[(i,t,s)])) * (data.Rba_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] - data.Rba_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] + \
					data.Xba_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] +  data.Xba_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Qb_con[i,j][t][s]) + \
				(1/(data.Vb_0_con[(i,t,s)] * data.Vb_0_con[(i,t,s)])) * (data.Rbb_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] - data.Rbb_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] + \
					data.Xbb_p[(i,j)] * Pb_sqr_con[i,j][t][s] +  data.Xbb_p[(i,j)] * Qb_sqr_con[i,j][t][s]) + \
				(1/(data.Vb_0_con[(i,t,s)] * data.Vc_0_con[(i,t,s)])) * (data.Rbc_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Qb_con[i,j][t][s] - data.Rbc_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] + \
					data.Xbc_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Pb_con[i,j][t][s] +  data.Xbc_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Qb_con[i,j][t][s]) == Qlss_b_con[i,j][t][s], "Reactive_Power_Losses_b_con_%s" %str((i,j,t,s)) 

		for (i,j,t,s) in self.List_LTS:
			prob += (1/(data.Vc_0_con[(i,t,s)] * data.Va_0_con[(i,t,s)])) * (data.Rca_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] - data.Rca_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] + \
					data.Xca_p[(i,j)] * data.Pa_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] +  data.Xca_p[(i,j)] * data.Qa_0_con[(i,j,t,s)] * Qc_con[i,j][t][s]) + \
				(1/(data.Vc_0_con[(i,t,s)] * data.Vb_0_con[(i,t,s)])) * (data.Rcb_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] - data.Rcb_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] + \
					data.Xcb_p[(i,j)] * data.Pb_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] +  data.Xcb_p[(i,j)] * data.Qb_0_con[(i,j,t,s)] * Qc_con[i,j][t][s]) + \
				(1/(data.Vc_0_con[(i,t,s)] * data.Vc_0_con[(i,t,s)])) * (data.Rcc_p[(i,j)] * data.Pc_0_con[(i,j,t,s)] * Qc_con[i,j][t][s] - data.Rcc_p[(i,j)] * data.Qc_0_con[(i,j,t,s)] * Pc_con[i,j][t][s] + \
					data.Xcc_p[(i,j)] * Pc_sqr_con[i,j][t][s] +  data.Xcc_p[(i,j)] * Qc_sqr_con[i,j][t][s]) == Qlss_c_con[i,j][t][s], "Reactive_Power_Losses_c_con_%s" %str((i,j,t,s))

		# Active Power Flow ----------------------------------------------------------------
		for (i,t,s) in self.List_NTS:
			prob += lpSum([Pa_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Plss_a_con[a,j][t][s]) * data.p[(i,a,j)] for (a,j) in data.L]) + \
			PS_a_con[i][t][s] + lpSum([PGa_con[a][t][s] for a in data.dict_nos_gd[i]]) + lpSum([PB_dis_a[a][t] for a in data.dict_nos_bs[i]]) - \
			lpSum([PB_ch_a[a][t] for a in data.dict_nos_bs[i]]) - data.PDa[(i,t)] * data.sd[(s)] + data.PVa[(i,t)] * data.srs[(s)] == 0, "Active_Power_Balance_Phase_a_con_%s" %str((i,t,s))
		
		for (i,t,s) in self.List_NTS:
			prob += lpSum([Pb_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Plss_b_con[a,j][t][s]) * data.p[(i,a,j)] for (a,j) in data.L]) + \
			PS_b_con[i][t][s] + lpSum([PGb_con[a][t][s] for a in data.dict_nos_gd[i]]) + lpSum([PB_dis_b[a][t] for a in data.dict_nos_bs[i]]) - \
			lpSum([PB_ch_b[a][t] for a in data.dict_nos_bs[i]]) - data.PDb[(i,t)] * data.sd[(s)] + data.PVb[(i,t)] * data.srs[(s)] == 0, "Active_Power_Balance_Phase_b_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += lpSum([Pc_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Plss_c_con[a,j][t][s]) * data.p[(i,a,j)] for (a,j) in data.L]) + \
			PS_c_con[i][t][s] + lpSum([PGc_con[a][t][s] for a in data.dict_nos_gd[i]]) + lpSum([PB_dis_c[a][t] for a in data.dict_nos_bs[i]]) - \
			lpSum([PB_ch_c[a][t] for a in data.dict_nos_bs[i]]) - data.PDc[(i,t)] * data.sd[(s)] + data.PVc[(i,t)] * data.srs[(s)] == 0, "Active_Power_Balance_Phase_c_con_%s" %str((i,t,s))

		# Reactive Power Flow ----------------------------------------------------------------
		for (i,t,s) in self.List_NTS:
			prob += lpSum([Qa_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Qlss_a_con[a,j][t][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			QS_a_con[i][t][s] + lpSum([QGa_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.QDa[(i,t)] * data.sd[(s)] == 0, "Reactive_Power_Balance_Phase_a_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += lpSum([Qb_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Qlss_b_con[a,j][t][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			QS_b_con[i][t][s] + lpSum([QGb_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.QDb[(i,t)] * data.sd[(s)] == 0, "Reactive_Power_Balance_Phase_b_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += lpSum([Qc_con[a,j][t][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Qlss_c_con[a,j][t][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			QS_c_con[i][t][s] + lpSum([QGc_con[a][t][s] for a in data.dict_nos_gd[i]]) - data.QDc[(i,t)] * data.sd[(s)] == 0, "Reactive_Power_Balance_Phase_c_con_%s" %str((i,t,s))

		# Voltage Droop in the Lines ----------------------------------------------------------------
		for (i,j,t,s) in self.List_LTS:
			prob += 2* (data.Raa_p[(i,j)] * Pa_con[i,j][t][s] + data.Xaa_p[(i,j)] * Qa_con[i,j][t][s]) + 2*(data.Rab_p[(i,j)] * Pb_con[i,j][t][s] + data.Xab_p[(i,j)] * Qb_con[i,j][t][s]) \
				+ 2* (data.Rac_p[(i,j)] * Pc_con[i,j][t][s] + data.Xac_p[(i,j)] * Qc_con[i,j][t][s]) \
				- (1/(data.Va_0_con[(i,t,s)]**2)) * (data.Raa_p[(i,j)]**2 + data.Xaa_p[(i,j)]**2) * (Pa_sqr_con[i,j][t][s] + Qa_sqr_con[i,j][t][s]) - Va_sqr_con[i][t][s] + Va_sqr_con[j][t][s] == 0, "Voltage_drop_phase_a_%s" %str((i,j,t,s)) 
	
		for (i,j,t,s) in self.List_LTS:
			prob += 2* (data.Rab_p[(i,j)] * Pa_con[i,j][t][s] + data.Xab_p[(i,j)] * Qa_con[i,j][t][s]) + 2*(data.Rbb_p[(i,j)] * Pb_con[i,j][t][s] + data.Xbb_p[(i,j)] * Qb_con[i,j][t][s]) \
				+ 2* (data.Rbc_p[(i,j)] * Pc_con[i,j][t][s] + data.Xbc_p[(i,j)] * Qc_con[i,j][t][s]) \
				- (1/(data.Vb_0_con[(i,t,s)]**2)) * (data.Rbb_p[(i,j)]**2 + data.Xbb_p[(i,j)]**2) * (Pb_sqr_con[i,j][t][s] + Qb_sqr_con[i,j][t][s]) - Vb_sqr_con[i][t][s] + Vb_sqr_con[j][t][s] == 0, "Voltage_drop_phase_b_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += 2* (data.Rac_p[(i,j)] * Pa_con[i,j][t][s] + data.Xac_p[(i,j)] * Qa_con[i,j][t][s]) + 2*(data.Rbc_p[(i,j)] * Pb_con[i,j][t][s] + data.Xbc_p[(i,j)] * Qb_con[i,j][t][s]) \
				+ 2* (data.Rcc_p[(i,j)] * Pc_con[i,j][t][s] + data.Xcc_p[(i,j)] * Qc_con[i,j][t][s]) \
				- (1/(data.Vc_0_con[(i,t,s)]**2)) * (data.Rcc_p[(i,j)]**2 + data.Xcc_p[(i,j)]**2) * (Pc_sqr_con[i,j][t][s] + Qc_sqr_con[i,j][t][s]) - Vc_sqr_con[i][t][s] + Vc_sqr_con[j][t][s] == 0, "Voltage_drop_phase_c_%s" %str((i,j,t,s))

		# Limite máximo de fluxo de corrente e equações de linearização ----------------------------------------------------------------
		for (i,j,t,s) in self.List_LTS:
			prob += (Pa_sqr_con[i,j][t][s] + Qa_sqr_con[i,j][t][s]) <= data.Imax[(i,j)]**2 * Va_sqr_con[i][t][s], "Current_Limit_phase_a_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += (Pb_sqr_con[i,j][t][s] + Qb_sqr_con[i,j][t][s]) <= data.Imax[(i,j)]**2 * Vb_sqr_con[i][t][s], "Current_Limit_phase_b_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += (Pc_sqr_con[i,j][t][s] + Qc_sqr_con[i,j][t][s]) <= data.Imax[(i,j)]**2 * Vc_sqr_con[i][t][s], "Current_Limit_phase_c_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pa_sqr_con[i,j][t][s] - lpSum([data.S_ms[(i,j,y)] * Pa_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Pa_sqr_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qa_sqr_con[i,j][t][s] - lpSum([data.S_ms[(i,j,y)] * Qa_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Qa_sqr_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pb_sqr_con[i,j][t][s] - lpSum([data.S_ms[(i,j,y)] * Pb_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Pb_sqr_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qb_sqr_con[i,j][t][s] - lpSum([data.S_ms[(i,j,y)] * Qb_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Qb_sqr_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pc_sqr_con[i,j][t][s] - lpSum([data.S_ms[(i,j,y)] * Pc_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Pc_sqr_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qc_sqr_con[i,j][t][s] - lpSum([data.S_ms[(i,j,y)] * Qc_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Qc_sqr_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pa_p_con[i,j][t][s] - Pa_n_con[i,j][t][s] - Pa_con[i,j][t][s] == 0, "Define_Pa_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qa_p_con[i,j][t][s] - Qa_n_con[i,j][t][s] - Qa_con[i,j][t][s] == 0, "Define_Qa_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pb_p_con[i,j][t][s] - Pb_n_con[i,j][t][s] - Pb_con[i,j][t][s] == 0, "Define_Pb_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qb_p_con[i,j][t][s] - Qb_n_con[i,j][t][s] - Qb_con[i,j][t][s] == 0, "Define_Qb_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pc_p_con[i,j][t][s] - Pc_n_con[i,j][t][s] - Pc_con[i,j][t][s] == 0, "Define_Pc_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qc_p_con[i,j][t][s] - Qc_n_con[i,j][t][s] - Qc_con[i,j][t][s] == 0, "Define_Qc_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pa_p_con[i,j][t][s] + Pa_n_con[i,j][t][s] - lpSum([Pa_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Pa_abs_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qa_p_con[i,j][t][s] + Qa_n_con[i,j][t][s] - lpSum([Qa_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Qa_abs_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pb_p_con[i,j][t][s] + Pb_n_con[i,j][t][s] - lpSum([Pb_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Pb_abs_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qb_p_con[i,j][t][s] + Qb_n_con[i,j][t][s] - lpSum([Qb_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Qb_abs_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Pc_p_con[i,j][t][s] + Pc_n_con[i,j][t][s] - lpSum([Pc_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Pc_abs_con_%s" %str((i,j,t,s))

		for (i,j,t,s) in self.List_LTS:
			prob += Qc_p_con[i,j][t][s] + Qc_n_con[i,j][t][s] - lpSum([Qc_Dp_con[i,j][t][s][y] for y in data.Y]) == 0, "Define_Qc_abs_con_%s" %str((i,j,t,s))

		for (i,j,t,s,y) in self.List_LTSY:
			prob += Pa_Dp_con[i,j][t][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Pa_con_%s" %str((i,j,t,s,y))

		for (i,j,t,s,y) in self.List_LTSY:
			prob += Qa_Dp_con[i,j][t][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Qa_con_%s" %str((i,j,t,s,y))

		for (i,j,t,s,y) in self.List_LTSY:
			prob += Pb_Dp_con[i,j][t][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Pb_con_%s" %str((i,j,t,s,y))

		for (i,j,t,s,y) in self.List_LTSY:
			prob += Qb_Dp_con[i,j][t][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Qb_con_%s" %str((i,j,t,s,y))

		for (i,j,t,s,y) in self.List_LTSY:
			prob += Pc_Dp_con[i,j][t][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Pc_con_%s" %str((i,j,t,s,y))

		for (i,j,t,s,y) in self.List_LTSY:
			prob += Qc_Dp_con[i,j][t][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Qc_con_%s" %str((i,j,t,s,y))


		# Limite potência aparente fornecida pelo PCC ----------------------------------------------------------------
		for (i,t,s) in self.List_NTS:
			prob += PS_a_con[i][t][s] + PS_b_con[i][t][s] + PS_c_con[i][t][s] - PS_con[i][t][s] == 0, "Active_power_limit_PCC_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += QS_a_con[i][t][s] + QS_b_con[i][t][s] + QS_c_con[i][t][s] - QS_con[i][t][s] == 0, "Reactive_power_limit_PCC_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += PSsqr_con[i][t][s] + QSsqr_con[i][t][s] <= data.Smax[(i)]**2, "Power_limit_PCC_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += PSsqr_con[i][t][s] - lpSum([data.PS_ms[(i,y)] * PS_Dp_con[i][t][s][y] for y in data.Y]) == 0, "Define_PSsqr_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += QSsqr_con[i][t][s] - lpSum([data.QS_ms[(i,y)] * QS_Dp_con[i][t][s][y] for y in data.Y]) == 0, "Define_QSsqr_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += PS_p_con[i][t][s] - PS_n_con[i][t][s] - PS_con[i][t][s] == 0, "Definition_PS_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += QS_p_con[i][t][s] - QS_n_con[i][t][s] - QS_con[i][t][s] == 0, "Definition_QS_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += PS_p_con[i][t][s] + PS_n_con[i][t][s] - lpSum([PS_Dp_con[i][t][s][y] for y in data.Y]) == 0, "Definition_PS_abs_con_%s" %str((i,t,s))

		for (i,t,s) in self.List_NTS:
			prob += QS_p_con[i][t][s] + QS_n_con[i][t][s] - lpSum([QS_Dp_con[i][t][s][y] for y in data.Y]) == 0, "Definition_QS_abs_con_%s" %str((i,t,s))

		for (i,t,s,y) in self.List_NTSY:
			prob += PS_Dp_con[i][t][s][y] <= data.PS_Dsmax[(i)], "Definition_block_PS_con_%s" %str((i,t,s,y))

		for (i,t,s,y) in self.List_NTSY:
			prob += QS_Dp_con[i][t][s][y] <= data.QS_Dsmax[(i)], "Definition_block_QS_con_%s" %str((i,t,s,y))

		# Genset ----------------------------------------------------------------
		for (n,t,s) in self.List_GDTS:
			prob += PGa_con[n][t][s] +  PGb_con[n][t][s] + PGc_con[n][t][s] - PG_con[n][t][s] == 0, "Total_active_power_GD_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += QGa_con[n][t][s] +  QGb_con[n][t][s] + QGc_con[n][t][s] - QG_con[n][t][s] == 0, "Total_reactive_power_GD_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += data.PG_min[(n)] <= PG_con[n][t][s], "Active_Power_Limit_GD_1_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += PG_con[n][t][s] <= data.PG_max[(n)], "Active_Power_Limit_GD_2_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += data.QG_min[(n)] <= QG_con[n][t][s], "Reactive_Power_Limit_GD_1_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += QG_con[n][t][s] <= data.QG_max[(n)], "Reactive_Power_Limit_GD_2_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += PGa_con[n][t][s] == 0, "Grid_connected_active_phase_a_con_%s" %str((n,t,s))
		
		for (n,t,s) in self.List_GDTS:
			prob += PGb_con[n][t][s] == 0, "Grid_connected_active_phase_b_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += PGc_con[n][t][s] == 0, "Grid_connected_active_phase_c_con_%s" %str((n,t,s))
		
		for (n,t,s) in self.List_GDTS:
			prob += QGa_con[n][t][s] == 0, "Grid_connected_reactive_phase_a_con_%s" %str((n,t,s))
		
		for (n,t,s) in self.List_GDTS:
			prob += QGb_con[n][t][s] == 0, "Grid_connected_reactive_phase_b_con_%s" %str((n,t,s))

		for (n,t,s) in self.List_GDTS:
			prob += QGc_con[n][t][s] == 0, "Grid_connected_reactive_phase_c_con_%s" %str((n,t,s))

		# Island Operation
		for (i,t,c,s) in self.List_NTOS:
			if int(t) >= int(c) and int(t) < int(c) + 2:
				prob += PS_a[i][t][c][s] == 0, "Island_operation_active_phase_a_%s" %str((i,t,c,s))
				prob += PS_b[i][t][c][s] == 0, "Island_operation_active_phase_b_%s" %str((i,t,c,s))
				prob += PS_c[i][t][c][s] == 0, "Island_operation_active_phase_c_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			if int(t) >= int(c) and int(t) < int(c) + 2:
				prob += QS_a[i][t][c][s] == 0, "Island_operation_reactive_phase_a_%s" %str((i,t,c,s))
				prob += QS_b[i][t][c][s] == 0, "Island_operation_reactive_phase_b_%s" %str((i,t,c,s))
				prob += QS_c[i][t][c][s] == 0, "Island_operation_reactive_phase_c_%s" %str((i,t,c,s))

		#------------- Operation with outage -------------------------------------------
		# Active losses ----------------------------------------------------------------
		for (i,j,t,c,s) in self.List_LTOS:
			prob += (1/(data.Va_0[(i,t,c,s)] * data.Va_0[(i,t,c,s)])) * (data.Raa_p[(i,j)] * Pa_sqr[i,j][t][c][s] + data.Raa_p[(i,j)] * Qa_sqr[i,j][t][c][s] - \
					data.Xaa_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] +  data.Xaa_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Pa[i,j][t][c][s]) + \
				(1/(data.Va_0[(i,t,c,s)] * data.Vb_0[(i,t,c,s)])) * (data.Rab_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] + data.Rab_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] - \
					data.Xab_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] +  data.Xab_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Pa[i,j][t][c][s]) + \
				(1/(data.Va_0[(i,t,c,s)] * data.Vc_0[(i,t,c,s)])) * (data.Rac_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] + data.Rac_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] - \
					data.Xac_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] +  data.Xac_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Pa[i,j][t][c][s]) == Plss_a[i,j][t][c][s], "Active_Power_Losses_a_%s" %str((i,j,t,c,s))
		
		for (i,j,t,c,s) in self.List_LTOS:
			prob += (1/(data.Vb_0[(i,t,c,s)] * data.Va_0[(i,t,c,s)])) * (data.Rba_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] + data.Rba_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] - \
					data.Xba_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] +  data.Xba_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Pb[i,j][t][c][s]) + \
				(1/(data.Vb_0[(i,t,c,s)] * data.Vb_0[(i,t,c,s)])) * (data.Rbb_p[(i,j)] * Pb_sqr[i,j][t][c][s] + data.Rbb_p[(i,j)] * Qb_sqr[i,j][t][c][s] - \
					data.Xbb_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] +  data.Xbb_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Pb[i,j][t][c][s]) + \
				(1/(data.Vb_0[(i,t,c,s)] * data.Vc_0[(i,t,c,s)])) * (data.Rbc_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] + data.Rbc_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] - \
					data.Xbc_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] +  data.Xbc_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Pb[i,j][t][c][s]) == Plss_b[i,j][t][c][s], "Active_Power_Losses_b_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += (1/(data.Vc_0[(i,t,c,s)] * data.Va_0[(i,t,c,s)])) * (data.Rca_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] + data.Rca_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] - \
					data.Xca_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] +  data.Xca_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Pc[i,j][t][c][s]) + \
				(1/(data.Vc_0[(i,t,c,s)] * data.Vb_0[(i,t,c,s)])) * (data.Rcb_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] + data.Rcb_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] - \
					data.Xcb_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] +  data.Xcb_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Pc[i,j][t][c][s]) + \
				(1/(data.Vc_0[(i,t,c,s)] * data.Vc_0[(i,t,c,s)])) * (data.Rcc_p[(i,j)] * Pc_sqr[i,j][t][c][s] + data.Rcc_p[(i,j)] * Qc_sqr[i,j][t][c][s] - \
					data.Xcc_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] +  data.Xcc_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Pc[i,j][t][c][s]) == Plss_c[i,j][t][c][s], "Active_Power_Losses_c_%s" %str((i,j,t,c,s))

		# Reactive losses ----------------------------------------------------------------
		for (i,j,t,c,s) in self.List_LTOS:
			prob += (1/(data.Va_0[(i,t,c,s)] * data.Va_0[(i,t,c,s)])) * (data.Raa_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] - data.Raa_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] + \
					data.Xaa_p[(i,j)] * Pa_sqr[i,j][t][c][s] +  data.Xaa_p[(i,j)] * Qa_sqr[i,j][t][c][s]) + \
				(1/(data.Va_0[(i,t,c,s)] * data.Vb_0[(i,t,c,s)])) * (data.Rab_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] - data.Rab_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] + \
					data.Xab_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] +  data.Xab_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Qa[i,j][t][c][s]) + \
				(1/(data.Va_0[(i,t,c,s)] * data.Vc_0[(i,t,c,s)])) * (data.Rac_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Qa[i,j][t][c][s] - data.Rac_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] + \
					data.Xac_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Pa[i,j][t][c][s] +  data.Xac_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Qa[i,j][t][c][s]) == Qlss_a[i,j][t][c][s], "Reactive_Power_Losses_a_%s" %str((i,j,t,c,s))
		
		for (i,j,t,c,s) in self.List_LTOS:
			prob += (1/(data.Vb_0[(i,t,c,s)] * data.Va_0[(i,t,c,s)])) * (data.Rba_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] - data.Rba_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] + \
					data.Xba_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] +  data.Xba_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Qb[i,j][t][c][s]) + \
				(1/(data.Vb_0[(i,t,c,s)] * data.Vb_0[(i,t,c,s)])) * (data.Rbb_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] - data.Rbb_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] + \
					data.Xbb_p[(i,j)] * Pb_sqr[i,j][t][c][s] +  data.Xbb_p[(i,j)] * Qb_sqr[i,j][t][c][s]) + \
				(1/(data.Vb_0[(i,t,c,s)] * data.Vc_0[(i,t,c,s)])) * (data.Rbc_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Qb[i,j][t][c][s] - data.Rbc_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] + \
					data.Xbc_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Pb[i,j][t][c][s] +  data.Xbc_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Qb[i,j][t][c][s]) == Qlss_b[i,j][t][c][s], "Reactive_Power_Losses_b_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += (1/(data.Vc_0[(i,t,c,s)] * data.Va_0[(i,t,c,s)])) * (data.Rca_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] - data.Rca_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] + \
					data.Xca_p[(i,j)] * data.Pa_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] +  data.Xca_p[(i,j)] * data.Qa_0[(i,j,t,c,s)] * Qc[i,j][t][c][s]) + \
				(1/(data.Vc_0[(i,t,c,s)] * data.Vb_0[(i,t,c,s)])) * (data.Rcb_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] - data.Rcb_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] + \
					data.Xcb_p[(i,j)] * data.Pb_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] +  data.Xcb_p[(i,j)] * data.Qb_0[(i,j,t,c,s)] * Qc[i,j][t][c][s]) + \
				(1/(data.Vc_0[(i,t,c,s)] * data.Vc_0[(i,t,c,s)])) * (data.Rcc_p[(i,j)] * data.Pc_0[(i,j,t,c,s)] * Qc[i,j][t][c][s] - data.Rcc_p[(i,j)] * data.Qc_0[(i,j,t,c,s)] * Pc[i,j][t][c][s] + \
					data.Xcc_p[(i,j)] * Pc_sqr[i,j][t][c][s] +  data.Xcc_p[(i,j)] * Qc_sqr[i,j][t][c][s]) == Qlss_c[i,j][t][c][s], "Reactive_Power_Losses_c_%s" %str((i,j,t,c,s))


		# Active Power Flow ----------------------------------------------------------------
		for (i,t,c,s) in self.List_NTOS:
			prob += lpSum([Pa[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Plss_a[a,j][t][c][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			PS_a[i][t][c][s] + lpSum([PGa[a][t][c][s] for a in data.dict_nos_gd[i]]) + lpSum([PB_dis_a[a][t] for a in data.dict_nos_bs[i]]) - \
			lpSum([PB_ch_a[a][t] for a in data.dict_nos_bs[i]]) + ((- data.PDa[(i,t)] * data.sd[(s)]) + (data.PVa[(i,t)] * data.srs[(s)])) * xd[i][t][c][s] == 0, "Active_Power_Balance_Phase_a_%s" %str((i,t,c,s))
		
		for (i,t,c,s) in self.List_NTOS:
			prob += lpSum([Pb[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Plss_b[a,j][t][c][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			PS_b[i][t][c][s] + lpSum([PGb[a][t][c][s] for a in data.dict_nos_gd[i]]) + lpSum([PB_dis_b[a][t] for a in data.dict_nos_bs[i]]) - \
			lpSum([PB_ch_b[a][t] for a in data.dict_nos_bs[i]]) + ((- data.PDb[(i,t)] * data.sd[(s)]) + data.PVb[(i,t)] * data.srs[(s)]) * xd[i][t][c][s] == 0, "Active_Power_Balance_Phase_b_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += lpSum([Pc[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Plss_c[a,j][t][c][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			PS_c[i][t][c][s] + lpSum([PGc[a][t][c][s] for a in data.dict_nos_gd[i]]) + lpSum([PB_dis_c[a][t] for a in data.dict_nos_bs[i]]) - \
			lpSum([PB_ch_c[a][t] for a in data.dict_nos_bs[i]]) + ((- data.PDc[(i,t)] * data.sd[(s)]) + data.PVc[(i,t)] * data.srs[(s)]) * xd[i][t][c][s] == 0, "Active_Power_Balance_Phase_c_%s" %str((i,t,c,s))

		# Reactive Power Flow ----------------------------------------------------------------
		for (i,t,c,s) in self.List_NTOS:
			prob += lpSum([Qa[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Qlss_a[a,j][t][c][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			QS_a[i][t][c][s] + lpSum([QGa[a][t][c][s] for a in data.dict_nos_gd[i]]) + lpSum([QB_dis_a[a][t] for a in data.dict_nos_bs[i]]) - (data.QDa[(i,t)] * data.sd[(s)]) * xd[i][t][c][s] == 0, "Reactive_Power_Balance_Phase_a_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += lpSum([Qb[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Qlss_b[a,j][t][c][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			QS_b[i][t][c][s] + lpSum([QGb[a][t][c][s] for a in data.dict_nos_gd[i]]) + lpSum([QB_dis_b[a][t] for a in data.dict_nos_bs[i]]) - (data.QDb[(i,t)] * data.sd[(s)]) * xd[i][t][c][s] == 0, "Reactive_Power_Balance_Phase_b_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += lpSum([Qc[a,j][t][c][s] * data.df[(i,a,j)] for (a,j) in data.L]) - lpSum([(Qlss_c[a,j][t][c][s] * data.p[(i,a,j)]) for (a,j) in data.L]) + \
			QS_c[i][t][c][s] + lpSum([QGc[a][t][c][s] for a in data.dict_nos_gd[i]]) + lpSum([QB_dis_c[a][t] for a in data.dict_nos_bs[i]]) - (data.QDc[(i,t)] * data.sd[(s)]) * xd[i][t][c][s] == 0, "Reactive_Power_Balance_Phase_c_%s" %str((i,t,c,s))

		# Voltage Droop in the Lines ----------------------------------------------------------------
		for (i,j,t,c,s) in self.List_LTOS:
			prob += 2* (data.Raa_p[(i,j)] * Pa[i,j][t][c][s] + data.Xaa_p[(i,j)] * Qa[i,j][t][c][s]) + 2*(data.Rab_p[(i,j)] * Pb[i,j][t][c][s] + data.Xab_p[(i,j)] * Qb[i,j][t][c][s]) \
				+ 2* (data.Rac_p[(i,j)] * Pc[i,j][t][c][s] + data.Xac_p[(i,j)] * Qc[i,j][t][c][s]) \
				- (1/(data.Va_0[(i,t,c,s)]**2)) * (data.Raa_p[(i,j)]**2 + data.Xaa_p[(i,j)]**2) * (Pa_sqr[i,j][t][c][s] + Qa_sqr[i,j][t][c][s]) - Va_sqr[i][t][c][s] + Va_sqr[j][t][c][s] == 0, "Voltage_drop_phase_a_%s" %str((i,j,t,c,s)) 
	
		for (i,j,t,c,s) in self.List_LTOS:
			prob += 2* (data.Rab_p[(i,j)] * Pa[i,j][t][c][s] + data.Xab_p[(i,j)] * Qa[i,j][t][c][s]) + 2*(data.Rbb_p[(i,j)] * Pb[i,j][t][c][s] + data.Xbb_p[(i,j)] * Qb[i,j][t][c][s]) \
				+ 2* (data.Rbc_p[(i,j)] * Pc[i,j][t][c][s] + data.Xbc_p[(i,j)] * Qc[i,j][t][c][s]) \
				- (1/(data.Vb_0[(i,t,c,s)]**2)) * (data.Rbb_p[(i,j)]**2 + data.Xbb_p[(i,j)]**2) * (Pb_sqr[i,j][t][c][s] + Qb_sqr[i,j][t][c][s]) - Vb_sqr[i][t][c][s] + Vb_sqr[j][t][c][s] == 0, "Voltage_drop_phase_b_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += 2* (data.Rac_p[(i,j)] * Pa[i,j][t][c][s] + data.Xac_p[(i,j)] * Qa[i,j][t][c][s]) + 2*(data.Rbc_p[(i,j)] * Pb[i,j][t][c][s] + data.Xbc_p[(i,j)] * Qb[i,j][t][c][s]) \
				+ 2* (data.Rcc_p[(i,j)] * Pc[i,j][t][c][s] + data.Xcc_p[(i,j)] * Qc[i,j][t][c][s]) \
				- (1/(data.Vc_0[(i,t,c,s)]**2)) * (data.Rcc_p[(i,j)]**2 + data.Xcc_p[(i,j)]**2) * (Pc_sqr[i,j][t][c][s] + Qc_sqr[i,j][t][c][s]) - Vc_sqr[i][t][c][s] + Vc_sqr[j][t][c][s] == 0, "Voltage_drop_phase_c_%s" %str((i,j,t,c,s))


		# Limite máximo de fluxo de corrente e equações de linearização ----------------------------------------------------------------
		for (i,j,t,c,s) in self.List_LTOS:
			prob += (Pa_sqr[i,j][t][c][s] + Qa_sqr[i,j][t][c][s]) <= data.Imax[(i,j)]**2 * Va_sqr[i][t][c][s], "Current_Limit_phase_a_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += (Pb_sqr[i,j][t][c][s] + Qb_sqr[i,j][t][c][s]) <= data.Imax[(i,j)]**2 * Vb_sqr[i][t][c][s], "Current_Limit_phase_b_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += (Pc_sqr[i,j][t][c][s] + Qc_sqr[i,j][t][c][s]) <= data.Imax[(i,j)]**2 * Vc_sqr[i][t][c][s], "Current_Limit_phase_c_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pa_sqr[i,j][t][c][s] - lpSum([data.S_ms[(i,j,y)] * Pa_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Pa_sqr_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qa_sqr[i,j][t][c][s] - lpSum([data.S_ms[(i,j,y)] * Qa_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Qa_sqr_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pb_sqr[i,j][t][c][s] - lpSum([data.S_ms[(i,j,y)] * Pb_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Pb_sqr_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qb_sqr[i,j][t][c][s] - lpSum([data.S_ms[(i,j,y)] * Qb_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Qb_sqr_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pc_sqr[i,j][t][c][s] - lpSum([data.S_ms[(i,j,y)] * Pc_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Pc_sqr_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qc_sqr[i,j][t][c][s] - lpSum([data.S_ms[(i,j,y)] * Qc_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Qc_sqr_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pa_p[i,j][t][c][s] - Pa_n[i,j][t][c][s] - Pa[i,j][t][c][s] == 0, "Define_Pa_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qa_p[i,j][t][c][s] - Qa_n[i,j][t][c][s] - Qa[i,j][t][c][s] == 0, "Define_Qa_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pb_p[i,j][t][c][s] - Pb_n[i,j][t][c][s] - Pb[i,j][t][c][s] == 0, "Define_Pb_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qb_p[i,j][t][c][s] - Qb_n[i,j][t][c][s] - Qb[i,j][t][c][s] == 0, "Define_Qb_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pc_p[i,j][t][c][s] - Pc_n[i,j][t][c][s] - Pc[i,j][t][c][s] == 0, "Define_Pc_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qc_p[i,j][t][c][s] - Qc_n[i,j][t][c][s] - Qc[i,j][t][c][s] == 0, "Define_Qc_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pa_p[i,j][t][c][s] + Pa_n[i,j][t][c][s] - lpSum([Pa_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Pa_abs_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qa_p[i,j][t][c][s] + Qa_n[i,j][t][c][s] - lpSum([Qa_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Qa_abs_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pb_p[i,j][t][c][s] + Pb_n[i,j][t][c][s] - lpSum([Pb_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Pb_abs_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qb_p[i,j][t][c][s] + Qb_n[i,j][t][c][s] - lpSum([Qb_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Qb_abs_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Pc_p[i,j][t][c][s] + Pc_n[i,j][t][c][s] - lpSum([Pc_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Pc_abs_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s) in self.List_LTOS:
			prob += Qc_p[i,j][t][c][s] + Qc_n[i,j][t][c][s] - lpSum([Qc_Dp[i,j][t][c][s][y] for y in data.Y]) == 0, "Define_Qc_abs_%s" %str((i,j,t,c,s))

		for (i,j,t,c,s,y) in self.List_LTOSY:
			prob += Pa_Dp[i,j][t][c][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Pa_%s" %str((i,j,t,c,s,y))

		for (i,j,t,c,s,y) in self.List_LTOSY:
			prob += Qa_Dp[i,j][t][c][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Qa_%s" %str((i,j,t,c,s,y))

		for (i,j,t,c,s,y) in self.List_LTOSY:
			prob += Pb_Dp[i,j][t][c][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Pb_%s" %str((i,j,t,c,s,y))

		for (i,j,t,c,s,y) in self.List_LTOSY:
			prob += Qb_Dp[i,j][t][c][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Qb_%s" %str((i,j,t,c,s,y))

		for (i,j,t,c,s,y) in self.List_LTOSY:
			prob += Pc_Dp[i,j][t][c][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Pc_%s" %str((i,j,t,c,s,y))

		for (i,j,t,c,s,y) in self.List_LTOSY:
			prob += Qc_Dp[i,j][t][c][s][y] <= data.S_Dsmax[(i,j)], "Definition_block_Qc_%s" %str((i,j,t,c,s,y))


		# Limete potência aparente fornecida pelo PCC ----------------------------------------------------------------
		for (i,t,c,s) in self.List_NTOS:
			prob += PS_a[i][t][c][s] + PS_b[i][t][c][s] + PS_c[i][t][c][s] - PS[i][t][c][s] == 0, "Active_power_limit_PCC_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += QS_a[i][t][c][s] + QS_b[i][t][c][s] + QS_c[i][t][c][s] - QS[i][t][c][s] == 0, "Reactive_power_limit_PCC_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += PSsqr[i][t][c][s] + QSsqr[i][t][c][s] <= data.Smax[(i)]**2, "Power_limit_PCC_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += PSsqr[i][t][c][s] - lpSum([data.PS_ms[(i,y)] * PS_Dp[i][t][c][s][y] for y in data.Y]) == 0, "Define_PSsqr_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += QSsqr[i][t][c][s] - lpSum([data.QS_ms[(i,y)] * QS_Dp[i][t][c][s][y] for y in data.Y]) == 0, "Define_QSsqr_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += PS_p[i][t][c][s] - PS_n[i][t][c][s] - PS[i][t][c][s] == 0, "Definition_PS_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += QS_p[i][t][c][s] - QS_n[i][t][c][s] - QS[i][t][c][s] == 0, "Definition_QS_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += PS_p[i][t][c][s] + PS_n[i][t][c][s] - lpSum([PS_Dp[i][t][c][s][y] for y in data.Y]) == 0, "Definition_PS_abs_%s" %str((i,t,c,s))

		for (i,t,c,s) in self.List_NTOS:
			prob += QS_p[i][t][c][s] + QS_n[i][t][c][s] - lpSum([QS_Dp[i][t][c][s][y] for y in data.Y]) == 0, "Definition_QS_abs_%s" %str((i,t,c,s))

		for (i,t,c,s,y) in self.List_NTOSY:
			prob += PS_Dp[i][t][c][s][y] <= data.PS_Dsmax[(i)], "Definition_block_PS_%s" %str((i,t,c,s,y))

		for (i,t,c,s,y) in self.List_NTOSY:
			prob += QS_Dp[i][t][c][s][y] <= data.QS_Dsmax[(i)], "Definition_block_QS_%s" %str((i,t,c,s,y))

		# Genset --------------------------------------------------------------------
		for (n,t,c,s) in self.List_GDTOS:
			prob += PGa[n][t][c][s] + PGb[n][t][c][s] + PGc[n][t][c][s] - PG[n][t][c][s] == 0, "Total_active_power_GD_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob += QGa[n][t][c][s] + QGb[n][t][c][s] + QGc[n][t][c][s] - QG[n][t][c][s] == 0, "Total_reactive_power_GD_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob += data.PG_min[(n)] <= PG[n][t][c][s], "Active_Power_Limit_GD_1_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob += PG[n][t][c][s] <= data.PG_max[(n)], "Active_Power_Limit_GD_2_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob += data.QG_min[(n)] <= QG[n][t][c][s], "Reactive_Power_Limit_GD_1_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			prob += QG[n][t][c][s] <= data.QG_max[(n)], "Reactive_Power_Limit_GD_2_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_GDTOS:
			if int(t) < int(c) and int(t) >= int(c) + 2:
				prob += PGa[n][t][c][s] == 0, "Grid_connected_active_phase_a_%s" %str((n,t,c,s))
				prob += PGb[n][t][c][s] == 0, "Grid_connected_active_phase_b_%s" %str((n,t,c,s))
				prob += PGc[n][t][c][s] == 0, "Grid_connected_active_phase_c_%s" %str((n,t,c,s))
				prob += QGa[n][t][c][s] == 0, "Grid_connected_reactive_phase_a_%s" %str((n,t,c,s))
				prob += QGb[n][t][c][s] == 0, "Grid_connected_reactive_phase_b_%s" %str((n,t,c,s))
				prob += QGc[n][t][c][s] == 0, "Grid_connected_reactive_phase_c_%s" %str((n,t,c,s))

		# Energy Storage System -----------------------------------------------------------
		for (i,t) in self.List_BT:
			if int(t) == 1:
				prob += EB[i]['1'] - data.EBi[(i)] - PB[i]['1'] * data.delta_t == 0, "State_of_Charge_1_%s" %str((i,t))
			else:
				prob += EB[i][t] - EB[i][str(int(t)-1)] - PB[i][t] * data.delta_t == 0, "State_of_Charge_2_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB[i][t] + PB_dis[i][t] * 1/(data.eta[(i)]) - PB_ch[i][t] * data.eta[(i)] == 0, "Total_input_output_power_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_ch[i][t] - PB_ch_a[i][t] - PB_ch_b[i][t] - PB_ch_c[i][t] == 0, "Total_charging_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_ch_a[i][t] == PB_ch_b[i][t], "Balance_power_charging_1_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_ch_b[i][t] == PB_ch_c[i][t], "Balance_power_charging_2_%s" %str((i,t))
		
		for (i,t)  in self.List_BT:
			prob += PB_ch_a[i][t] == PB_ch_c[i][t], "Balance_power_charging_3_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_dis[i][t] - PB_dis_a[i][t] - PB_dis_b[i][t] - PB_dis_c[i][t] == 0, "Total_discharging_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_dis_a[i][t] == PB_dis_b[i][t], "Balance_power_discharging_1_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_dis_b[i][t] == PB_dis_c[i][t], "Balance_power_discharging_2_%s" %str((i,t))
		
		for (i,t)  in self.List_BT:
			prob += PB_dis_a[i][t] == PB_dis_c[i][t], "Balance_power_discharging_3_%s" %str((i,t))
		
		for (i,t)  in self.List_BT:
			prob += QB[i][t] - QB_dis_a[i][t] - QB_dis_b[i][t] - QB_dis_c[i][t] == 0, "Total_reactive_discharging_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += QB_dis_a[i][t] == QB_dis_b[i][t], "Balance_reactive_power_discharging_1_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += QB_dis_b[i][t] == QB_dis_c[i][t], "Balance_reactive_power_discharging_2_%s" %str((i,t))
		
		for (i,t)  in self.List_BT:
			prob += QB_dis_a[i][t] == QB_dis_c[i][t], "Balance_reactive_power_discharging_3_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += QB[i][t] - PB_dis[i][t] * math.tan(math.acos(0.707)) <= 0, "Limits_reactive_power_1_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += - QB[i][t] - PB_dis[i][t] * math.tan(math.acos(0.707)) <= 0, "Limits_reactive_power_2_%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += 0 <= PB_ch[i][t], "Limits_charging_power_1%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_ch[i][t] <= data.PBmax[(i)] * b_ch[i][t], "Limits_charging_power_2%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += 0 <= PB_dis[i][t], "Limits_discharging_power_1%s" %str((i,t))

		for (i,t)  in self.List_BT:
			prob += PB_dis[i][t] <= data.PBmax[(i)] * b_dis[i][t], "Limits_discharging_power_2%s" %str((i,t))

		for (i,t) in self.List_BT:
			prob += data.EBmin[(i)] <= EB[i][t], "ESS_limits_1_%s" %str((i,t))

		for (i,t) in self.List_BT:
			prob += EB[i][t] <= data.EBmax[(i)], "ESS_limits_2_%s" %str((i,t))

		for (i,t) in self.List_BT:
			prob += b_ch[i][t] + b_dis[i][t] <= 1, "ESS_Operation_Mode_%s" %str((i,t))

		#----------------- FIX Variables --------------------------------------------------
		for (n,t,s) in self.List_NTS:
			if data.Tb[(n)] == 1:
				prob += Va_con[n][t][s] == data.Vnom, "Fix_Voltage_SE_con_a_%s" %str((n,t,s))
				prob += Vb_con[n][t][s] == data.Vnom, "Fix_Voltage_SE_con_b_%s" %str((n,t,s))
				prob += Vc_con[n][t][s] == data.Vnom, "Fix_Voltage_SE_con_c_%s" %str((n,t,s))
				prob += Va_sqr_con[n][t][s] == data.Vnom**2, "Fix_Voltage_sqr_SE_con_a_%s" %str((n,t,s))
				prob += Vb_sqr_con[n][t][s] == data.Vnom**2, "Fix_Voltage_sqr_SE_con_b_%s" %str((n,t,s))
				prob += Vc_sqr_con[n][t][s] == data.Vnom**2, "Fix_Voltage_sqr_SE_con_c_%s" %str((n,t,s))
			else:
				prob += PS_a_con[n][t][s] == 0, "Fix_Active_Power_Bus_Load_con_a_%s" %str((n,t,s))
				prob += PS_b_con[n][t][s] == 0, "Fix_Active_Power_Bus_Load_con_b_%s" %str((n,t,s))
				prob += PS_c_con[n][t][s] == 0, "Fix_Active_Power_Bus_Load_con_c_%s" %str((n,t,s))
				prob += QS_a_con[n][t][s] == 0, "Fix_REactive_Power_Bus_Load_con_a_%s" %str((n,t,s))
				prob += QS_b_con[n][t][s] == 0, "Fix_REactive_Power_Bus_Load_con_b_%s" %str((n,t,s))
				prob += QS_c_con[n][t][s] == 0, "Fix_REactive_Power_Bus_Load_con_c_%s" %str((n,t,s))

		for (n,t,c,s) in self.List_NTOS:
			if data.Tb[(n)] == 1 and int(t) < int(c) and int(t) >= int(c) + 2:
				prob += Va[n][t][c][s] == data.Vnom, "Fix_Voltage_a_%s" %str((n,t,c,s))
				prob += Vb[n][t][c][s] == data.Vnom, "Fix_Voltage_b_%s" %str((n,t,c,s))
				prob += Vc[n][t][c][s] == data.Vnom, "Fix_Voltage_c_%s" %str((n,t,c,s))
				prob += Va_sqr[n][t][c][s] == data.Vnom**2, "Fix_Voltage_sqr_SE_a_%s" %str((n,t,c,s))
				prob += Vb_sqr[n][t][c][s] == data.Vnom**2, "Fix_Voltage_sqr_SE_b_%s" %str((n,t,c,s))
				prob += Vc_sqr[n][t][c][s] == data.Vnom**2, "Fix_Voltage_sqr_SE_c_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_NTOS:
			if data.Tb[(n)] == 2 and int(t) >= int(c) and int(t) < int(c) + 2:
				prob += Va[n][t][c][s] == data.Vnom, "Fix_Voltage_cc_a_%s" %str((n,t,s))
				prob += Vb[n][t][c][s] == data.Vnom, "Fix_Voltage_cc_b_%s" %str((n,t,s))
				prob += Vc[n][t][c][s] == data.Vnom, "Fix_Voltage_cc_c_%s" %str((n,t,s))
				prob += Va_sqr[n][t][c][s] == data.Vnom**2, "Fix_Voltage_sqr_cc_a_%s" %str((n,t,c,s))
				prob += Vb_sqr[n][t][c][s] == data.Vnom**2, "Fix_Voltage_sqr_cc_b_%s" %str((n,t,c,s))
				prob += Vc_sqr[n][t][c][s] == data.Vnom**2, "Fix_Voltage_sqr_cc_c_%s" %str((n,t,c,s))

		for (n,t,c,s) in self.List_NTOS:
			if data.Tb[(n)] != 1:
				prob += PS_a[n][t][c][s] == 0, "Fix_Active_Power_Bus_Load_a_%s" %str((n,t,c,s))
				prob += PS_b[n][t][c][s] == 0, "Fix_Active_Power_Bus_Load_b_%s" %str((n,t,c,s))
				prob += PS_c[n][t][c][s] == 0, "Fix_Active_Power_Bus_Load_c_%s" %str((n,t,c,s))
				prob += QS_a[n][t][c][s] == 0, "Fix_Reactive_Power_Bus_Load_a_%s" %str((n,t,c,s))
				prob += QS_b[n][t][c][s] == 0, "Fix_Reactive_Power_Bus_Load_b_%s" %str((n,t,c,s))
				prob += QS_c[n][t][c][s] == 0, "Fix_Reactive_Power_Bus_Load_c_%s" %str((n,t,c,s))	

		return prob

	def WritingProblemFile(self, prob, filename):
		# The problem data is written to an .lp file
		prob.writeLP(filename + ".lp")

	#def PrintProblemScreen(self, prob):
		##Print problem
	#	print(prob)


	# Function to solve the model and obtain the results
	def Solving_Model(self,prob):
		data = self.data

		try:
			cwd = os.getcwd()
			prob.solve(solver=MOSEK(task_file_name = 'dump.task.gz', options = {mosek.dparam.optimizer_max_time: 43200.0}))
		except Exception as e:
			prob.solve()
		#try:
		#	cwd = os.getcwd()
		#	solverdir = 'cbc.exe' # extracted and renamed CBC solver binary
		#	solverdir = os.path.join(cwd, solverdir)
		#	solver = COIN_CMD(path=solverdir)
		#	prob.solve(solver)
		#except Exception as e:
		#	#cwd = os.getcwd()
		#	#solverdir = 'cbc.exe' # extracted and renamed CBC solver binary
		#	#solverdir = os.path.join(cwd, solverdir)
		#	#solver = COIN_CMD(path=solverdir)
		#	prob.solve()

		self.Status = LpStatus[prob.status]
		self.ObjectiveFunctionValue = value(prob.objective)

		Variablenames = prob.variables() # This is a self.List
		# Getting a self.Lists with the name and value of all problem variables
		varDic = {}
		for v in prob.variables():
			varDic[v.name] = v.varValue
		self.varDic = varDic


		# Creating dictionaries for variable depending of self.List_NTOS
		self.xd = self.CreateDictionaryForEachVariable_NTOS(varDic, 'xd')

		# Creating dictionaries for variables depending of self.List_GDTS
		self.PG_con = self.CreateDictionaryForEachVariable_GDTS(varDic, 'PG_con')

		# Creating dictionaries for variables depending of self.List_GDTOS
		self.PG = self.CreateDictionaryForEachVariable_GDTOS(varDic, 'PG')

		# Creating dictionaries for variables depending of self.List_BT
		self.EB = self.CreateDictionaryForEachVariable_BT(varDic, 'EB')
		self.PB = self.CreateDictionaryForEachVariable_BT(varDic, 'PB')
		self.PB_ch = self.CreateDictionaryForEachVariable_BT(varDic, 'PB_ch')
		self.PB_dis = self.CreateDictionaryForEachVariable_BT(varDic, 'PB_dis')
		

	def CreateDictionaryForEachVariable_LTS(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + "_"
		variable_name = {}
		for (i,j) in data.L:
			variable_name[(i,j)] ={}
			for t in data.T:
				variable_name[(i,j)][t] ={}
				for s in data.S:
					for key in varDic:
						if key.startswith(aux_variable_name + "(" + "'" + i + "'" + ",_" + "'" + j + "'" + ")" +"_"+ t +"_"+ s):
							variable_name[(i,j)][t][s] = varDic[key]
		return variable_name

	def CreateDictionaryForEachVariable_NTS(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + '_'
		variable_name = {}
		for i in data.N:
			variable_name[i] ={}
			for t in data.T:
				variable_name[i][t] ={}
				for s in data.S:
					for key in varDic:
						if key.startswith(aux_variable_name + i +'_'+ t +'_'+ s):
							variable_name[i][t][s] = varDic[key]
		return variable_name

	def CreateDictionaryForEachVariable_GDTS(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + '_'
		variable_name = {}
		for i in data.GD:
			variable_name[i] ={}
			for t in data.T:
				variable_name[i][t] ={}
				for s in data.S:
					for key in varDic:
						if key.startswith(aux_variable_name + i +'_'+ t +'_'+ s):
							variable_name[i][t][s] = varDic[key]
		return variable_name

	def CreateDictionaryForEachVariable_LTOS(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + "_"
		variable_name = {}
		for (i,j) in data.L:
			variable_name[(i,j)] ={}
			for t in data.T:
				variable_name[(i,j)][t] ={}
				for c in data.O:
					variable_name[(i,j)][t][c] ={}
					for s in data.S:
						for key in varDic:
							if key.startswith(aux_variable_name + "(" + "'" + i + "'" + ",_" + "'" + j + "'" + ")" +"_"+ t +"_"+ c +"_"+ s):
								variable_name[(i,j)][t][c][s] = varDic[key]
		return variable_name

	def CreateDictionaryForEachVariable_NTOS(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + '_'
		variable_name = {}
		for i in data.N:
			variable_name[i] ={}
			for t in data.T:
				variable_name[i][t] ={}
				for c in data.O:
					variable_name[i][t][c] ={}
					for s in data.S:
						for key in varDic:
							if key.startswith(aux_variable_name + i +'_'+ t +'_'+ c +'_'+ s):
								variable_name[i][t][c][s] = varDic[key]
		return variable_name

	def CreateDictionaryForEachVariable_GDTOS(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + '_'
		variable_name = {}
		for i in data.GD:
			variable_name[i] ={}
			for t in data.T:
				variable_name[i][t] ={}
				for c in data.O:
					variable_name[i][t][c] ={}
					for s in data.S:
						for key in varDic:
							if key.startswith(aux_variable_name + i +'_'+ t +'_'+ c +'_'+ s):
								variable_name[i][t][c][s] = varDic[key]
		return variable_name

	def CreateDictionaryForEachVariable_BT(self, varDic, variable_name):
		data = self.data
		aux_variable_name = variable_name + '_'
		variable_name = {}
		for i in data.B:
			variable_name[i] = {}
			for t in data.T:
				for key in varDic:
					if key.endswith(aux_variable_name + i +'_'+ t):
						variable_name[i][t] = varDic[key]
		return variable_name


	
