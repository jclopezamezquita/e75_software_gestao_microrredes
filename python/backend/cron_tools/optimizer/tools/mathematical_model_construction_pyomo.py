""""
========================== Mathematical Modelling ==============================
"""
import os
import sys
from pyomo.environ import *
import math
import subprocess
from pyomo.opt import SolverFactory

class MathematicalModel:
	def __init__(self, data):
		self.data = data

	def ConstructionOfLists(self):
		# self.List formed by sets T, S and C
		data = self.data
		self.List_LTS = []
		for (i,j) in data.L:
			for t in data.T:
				for s in data.S:
					self.List_LTS += [[i, j, t, s]]
		self.List_NTS = []
		for i in data.N:
			for t in data.T:
				for s in data.S:
					self.List_NTS += [[i, t, s]]
		self.List_GDTS = []
		for i in data.GD:
			for t in data.T:
				for s in data.S:
					self.List_GDTS += [[i, t, s]]
		self.List_LTOS = []
		for (i,j) in data.L:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_LTOS += [[i, j, t, c, s]]
		self.List_NTOS = []
		for i in data.N:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_NTOS += [[i, t, c, s]]
		self.List_GDTOS = []
		for i in data.GD:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						self.List_GDTOS += [[i, t, c, s]]
		self.List_BT = []
		for i in data.B:
			for t in data.T:
				self.List_BT += [[i, t]]
		'''
		self.List_EVT = []
		for i in data.EV:
			for t in data.T:
				self.List_EVT += [[i, t]]
		self.List_EVTd = []
		for i in data.EV:
			for t in data.T:
				if int(t) >= int(data.t_arrival[i]) and int(t) <= int(data.t_departure[i]):
					self.List_EVTd.append([i, t])
		'''
		self.List_NTSY = []
		for i in data.N:
			for t in data.T:
				for s in data.S:
					for y in data.Y:
						self.List_NTSY += [[i, t, s, y]]
		self.List_LTSY = []
		for (i,j) in data.L:
			for t in data.T:
				for s in data.S:
					for y in data.Y:
						self.List_LTSY += [[i, j, t, s, y]]
		self.List_NTOSY = []
		for i in data.N:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						for y in data.Y:
							self.List_NTOSY += [[i, t, c, s, y]]
		self.List_LTOSY = []
		for (i,j) in data.L:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						for y in data.Y:
							self.List_LTOSY += [[i, j, t, c, s, y]]
		'''
		self.List_GDTSY = []
		for i in data.GD:
			for t in data.T:
				for s in data.S:
					for y in data.Y:
						self.List_GDTSY += [[i, t, s, y]]
		
		self.List_GDTOSY = []
		for i in data.GD:
			for t in data.T:
				for c in data.O:
					for s in data.S:
						for y in data.Y:
							self.List_GDTOSY += [[i, t, c, s, y]]
		'''
		#return (self.List_NTS, self.List_NTOS, self.List_LTS, self.List_LTOS, self.List_SETS, self.List_SETOS, self.List_sPDTS, self.List_sQDTS, self.List_sPDTOS, self.List_sQDTOS, self.List_GDTS, self.List_GDTOS, self.List_sPVT, self.List_sPVTO, self.List_BT, self.List_LTSY, self.List_LTOSY, self.List_SETSY, self.List_SETOSY, self.List_GDTSY, self.List_GDTOSY)

	def ProblemFormulation_ColdStart(self):
		data = self.data

		# Type of problem
		model_cs = ConcreteModel("Modelo_coldstar_EMS_PYOMO")

		# Declare variables
		model_cs.Pa = Var(data.L, data.T, data.S, within = Reals)
		model_cs.Pb = Var(data.L, data.T, data.S, within = Reals)
		model_cs.Pc = Var(data.L, data.T, data.S, within = Reals)
		model_cs.Qa = Var(data.L, data.T, data.S, within = Reals)
		model_cs.Qb = Var(data.L, data.T, data.S, within = Reals)
		model_cs.Qc = Var(data.L, data.T, data.S, within = Reals)
		model_cs.Va = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Vb = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Vc = Var(data.N, data.T, data.S, within = Reals)

		model_cs.Ppcc_a = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Ppcc_b = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Ppcc_c = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Qpcc_a = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Qpcc_b = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Qpcc_c = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Ppcc = Var(data.N, data.T, data.S, within = Reals)
		model_cs.Qpcc = Var(data.N, data.T, data.S, within = Reals)

		model_cs.PGa = Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.PGb = Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.PGc = Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.QGa = Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.QGb = Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.QGc = Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.PG =  Var(data.GD, data.T, data.S, within = NonNegativeReals)
		model_cs.QG =  Var(data.GD, data.T, data.S, within = NonNegativeReals)

		# Variables for contingences

		model_cs.Pa_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model_cs.Pb_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model_cs.Pc_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model_cs.Qa_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model_cs.Qb_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model_cs.Qc_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model_cs.Va_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Vb_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Vc_out = Var(data.N, data.T, data.O, data.S, within = Reals)

		model_cs.Ppcc_a_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Ppcc_b_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Ppcc_c_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Qpcc_a_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Qpcc_b_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Qpcc_c_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Ppcc_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model_cs.Qpcc_out = Var(data.N, data.T, data.O, data.S, within = Reals)

		model_cs.PGa_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.PGb_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.PGc_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.QGa_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.QGb_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.QGc_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.PG_out =  Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model_cs.QG_out =  Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)

		model_cs.xd = Var(data.N, data.T, data.O, data.S, domain = Reals, bounds = (0, 1))	

		# Objective function
		if len(data.O) >= 1 :
			cost_operation_contingency_cs = (sum(data.Prob[s]*(0.01/len(data.O) * (sum(data.cEDS[t] * data.delta_t * (model_cs.Ppcc_a_out[i, t, o, s] + model_cs.Ppcc_b_out[i, t, o, s] + model_cs.Ppcc_c_out[i, t, o, s]) for (i, t, o, s) in self.List_NTOS) + 
											sum([data.cost_PG[i] * data.delta_t * model_cs.PG_out[i,t,o, s] for (i,t,o,s) in self.List_GDTOS]) + 
											sum([data.delta_t * data.alpha_c[i] * data.sd[s] * (data.PDa[(i,t)]+data.PDb[(i,t)]+data.PDc[(i,t)]) * (1-model_cs.xd[i,t,o,s]) for (i,t,o,s) in self.List_NTOS]))) + 
											(0.99 * sum(data.cEDS[t] * data.delta_t * (model_cs.Ppcc_a[i, t,s] + model_cs.Ppcc_b[i, t,s] + model_cs.Ppcc_c[i, t,s]) for (i, t,s) in self.List_NTS) + 
											sum(data.cost_PG[i] * data.delta_t * model_cs.PG[i, t,s] for (i, t,s) in self.List_GDTS)) for s in data.S))
		else :
			cost_operation_contingency_cs = (sum(data.Prob[s]*(0.01/1000000 * (sum(data.cEDS[t] * data.delta_t * (model_cs.Ppcc_a_out[i, t, o, s] + model_cs.Ppcc_b_out[i, t, o, s] + model_cs.Ppcc_c_out[i, t, o, s]) for (i, t, o, s) in self.List_NTOS) + 
											sum([data.delta_t * data.alpha_c[i] * data.sd[s] * (data.PDa[(i,t)]+data.PDb[(i,t)]+data.PDc[(i,t)]) * (1-model_cs.xd[i,t,o,s]) for (i,t,o,s) in self.List_NTOS]))) +
											(0.99 * sum(data.cEDS[t] * data.delta_t * (model_cs.Ppcc_a[i, t,s] + model_cs.Ppcc_b[i, t,s] + model_cs.Ppcc_c[i, t,s]) for (i, t,s) in self.List_NTS)) for s in data.S))

		model_cs.objective_function_cs = Objective(expr=cost_operation_contingency_cs)

		# Constraints without contingences---------------------------------------------------------------- 

		#ACTIVE POWER BALANCE WITHOUT CONTINGENCES
		def active_power_balance_rule_a(model_cs, i,t, s):
			return (
				sum(model_cs.Pa[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) +
				model_cs.Ppcc_a[i, t, s] + sum(model_cs.PGa[a, t, s] for a in data.dict_nos_gd[i]) - data.PDa[(i,t)]*data.sd[s] == 0) 
		model_cs.active_power_balance_a = Constraint(self.List_NTS, rule=active_power_balance_rule_a)

		def active_power_balance_rule_b(model_cs, i,t, s):
			return (
				sum(model_cs.Pb[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) +
				model_cs.Ppcc_b[i, t, s] + sum(model_cs.PGb[a, t, s] for a in data.dict_nos_gd[i]) -
				data.PDb[(i,t)]*data.sd[s] == 0)
		model_cs.active_power_balance_b = Constraint(self.List_NTS, rule=active_power_balance_rule_b)

		def active_power_balance_rule_c(model_cs, i,t, s):
			return (
				sum(model_cs.Pc[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) +
				model_cs.Ppcc_c[i, t, s] + sum(model_cs.PGc[a, t, s] for a in data.dict_nos_gd[i]) -
				data.PDc[(i,t)]*data.sd[s] == 0)
		model_cs.active_power_balance_c = Constraint(self.List_NTS, rule=active_power_balance_rule_c)

		#REACTIVE POWER BALANCE
		def reactive_power_balance_rule_a(model_cs, i,t, s):
			return (
				sum(model_cs.Qa[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) +
				model_cs.Qpcc_a[i, t, s] + sum(model_cs.QGa[a, t, s] for a in data.dict_nos_gd[i]) -
				data.QDa[(i,t)]*data.sd[s] == 0)
		model_cs.reactive_power_balance_a = Constraint(self.List_NTS, rule=reactive_power_balance_rule_a)

		def reactive_power_balance_rule_b(model_cs, i,t, s):
			return (
				sum(model_cs.Qb[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) +
				model_cs.Qpcc_b[i, t, s] + sum(model_cs.QGb[a, t, s] for a in data.dict_nos_gd[i])-
				data.QDb[(i,t)]*data.sd[s] == 0)
		model_cs.reactive_power_balance_b = Constraint(self.List_NTS, rule=reactive_power_balance_rule_b)

		def reactive_power_balance_rule_c(model_cs, i,t, s):
			return (
				sum(model_cs.Qc[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) +
				model_cs.Qpcc_c[i, t, s]+ sum(model_cs.QGc[a, t, s] for a in data.dict_nos_gd[i]) -
				data.QDc[(i,t)]*data.sd[s] == 0)
		model_cs.reactive_power_balance_c = Constraint(self.List_NTS, rule=reactive_power_balance_rule_c)

		#Genset 
		def genset_power_rule(model_cs, i,t, s):
			return(model_cs.PGa[i, t, s] + model_cs.PGb[i, t, s] + model_cs.PGc[i, t, s] == model_cs.PG[i, t, s])
		model_cs.genset_power_active = Constraint(self.List_GDTS, rule=genset_power_rule)

		def genset_power_reactive_rule(model_cs, i,t, s):
			return(model_cs.QGa[i, t, s] + model_cs.QGb[i, t, s] + model_cs.QGc[i, t, s] == model_cs.QG[i, t, s])
		model_cs.genset_power_reactive = Constraint(self.List_GDTS, rule=genset_power_reactive_rule)

		def genset_power_active_limits_rule_1(model_cs, i,t, s):
			return(model_cs.PG[i, t, s] >= data.PG_min[i])
		model_cs.genset_power_active_limits_1 = Constraint(self.List_GDTS, rule = genset_power_active_limits_rule_1)

		def genset_power_active_limits_rule_2(model_cs, i,t, s):
			return(model_cs.PG[i, t, s] <= data.PG_max[i])
		model_cs.genset_power_active_limits_2 = Constraint(self.List_GDTS, rule = genset_power_active_limits_rule_2)

		def genset_power_reactive_limits_rule_1(model_cs, i,t, s):
			return(model_cs.QG[i, t, s] >= data.QG_min[i])
		model_cs.genset_power_reactive_limits_1 = Constraint(self.List_GDTS, rule = genset_power_reactive_limits_rule_1)

		def genset_power_reactive_limits_rule_2(model_cs, i,t, s):
			return(model_cs.QG[i, t, s] <= data.QG_max[i])
		model_cs.genset_power_reactive_limits_2 = Constraint(self.List_GDTS, rule = genset_power_reactive_limits_rule_2)

		def genset_operation_1_rule(model_cs, i,t, s):
			return(model_cs.PGa[i, t, s] == 0)
		model_cs.genset_operation_1 = Constraint(self.List_GDTS, rule = genset_operation_1_rule)

		def genset_operation_2_rule(model_cs, i,t, s):
			return(model_cs.PGb[i, t, s] == 0)
		model_cs.genset_operation_2 = Constraint(self.List_GDTS, rule = genset_operation_2_rule)

		def genset_operation_3_rule(model_cs, i,t, s):
			return(model_cs.PGc[i, t, s] == 0)
		model_cs.genset_operation_3 = Constraint(self.List_GDTS, rule = genset_operation_3_rule)

		def genset_operation_4_rule(model_cs, i,t, s):
			return(model_cs.QGa[i, t, s] == 0)
		model_cs.genset_operation_4 = Constraint(self.List_GDTS, rule = genset_operation_4_rule)

		def genset_operation_5_rule(model_cs, i,t, s):
			return(model_cs.QGb[i, t, s] == 0)
		model_cs.genset_operation_5 = Constraint(self.List_GDTS, rule = genset_operation_5_rule)

		def genset_operation_6_rule(model_cs, i,t, s):
			return(model_cs.QGc[i, t, s] == 0)
		model_cs.genset_operation_6 = Constraint(self.List_GDTS, rule = genset_operation_6_rule)

		#FIX VARIABLES

		def fix_voltage_a_rule(model_cs,i,t,s):
			return(model_cs.Va[i,t,s] == data.Vnom)
		model_cs.fix_voltage_a = Constraint(self.List_NTS, rule = fix_voltage_a_rule)

		def fix_voltage_b_rule(model_cs,i,t,s):
			return(model_cs.Vb[i,t,s] == data.Vnom)
		model_cs.fix_voltage_b = Constraint(self.List_NTS, rule = fix_voltage_b_rule)

		def fix_voltage_c_rule(model_cs,i,t,s):
			return(model_cs.Vc[i,t,s] == data.Vnom)
		model_cs.fix_voltage_c = Constraint(self.List_NTS, rule = fix_voltage_c_rule)

		model_cs.fix_active_power = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for s in data.S:
					if data.Tb[i] != 1:
						model_cs.fix_active_power.add(expr = model_cs.Ppcc_a[i,t,s] == 0)
						model_cs.fix_active_power.add(expr = model_cs.Ppcc_b[i,t,s] == 0)
						model_cs.fix_active_power.add(expr = model_cs.Ppcc_c[i,t,s] == 0)

		model_cs.fix_reactive_power = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for s in data.S:
					if data.Tb[i] != 1:
						model_cs.fix_reactive_power.add(expr=model_cs.Qpcc_a[i, t, s] == 0)
						model_cs.fix_reactive_power.add(expr=model_cs.Qpcc_b[i, t, s] == 0)
						model_cs.fix_reactive_power.add(expr=model_cs.Qpcc_c[i, t, s] == 0)

		# ------------------------------------------------------------------------------
		#------------- Operation with outage - COLD START ------------------------------
		# ------------------------------------------------------------------------------
		#
		#ACTIVE POWER BALANCE

		def active_power_balance_rule_a_out(model_cs, i, t, o, s):
			return (
				sum(model_cs.Pa_out[a, j, t, o, s] * data.df[(i, a, j)] for (a, j) in data.L) +
				sum(model_cs.PGa_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				model_cs.Ppcc_a_out[i, t, o, s] - data.PDa[(i, t)] * model_cs.xd[i, t, o, s] * data.sd[s] == 0
			)

		model_cs.active_power_balance_a_out = Constraint(self.List_NTOS, rule=active_power_balance_rule_a_out)

		def active_power_balance_rule_b_out(model_cs, i, t, o, s):
			return (
				sum(model_cs.Pb_out[a, j, t, o, s] * data.df[(i, a, j)] for (a, j) in data.L) +
				sum(model_cs.PGb_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				model_cs.Ppcc_b_out[i, t, o, s] -
				data.PDb[(i, t)] * model_cs.xd[i, t, o, s] * data.sd[s] == 0
			)

		model_cs.active_power_balance_b_out = Constraint(self.List_NTOS, rule=active_power_balance_rule_b_out)

		def active_power_balance_rule_c_out(model_cs, i, t, o, s):
			return (
				sum(model_cs.Pc_out[a, j, t, o, s] * data.df[(i, a, j)] for (a, j) in data.L) +
				sum(model_cs.PGc_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				model_cs.Ppcc_c_out[i, t, o, s] -
				data.PDc[(i, t)] * model_cs.xd[i, t, o, s] * data.sd[s] == 0
			)

		model_cs.active_power_balance_c_out = Constraint(self.List_NTOS, rule=active_power_balance_rule_c_out)

		#REACTIVE POWER BALANCE

		def reactive_power_balance_rule_a_out(model_cs, i, t, o, s):
			return (
				sum(model_cs.Qa_out[a, j, t, o, s] * data.df[(i, a, j)] for (a, j) in data.L) +
				sum(model_cs.QGa_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				model_cs.Qpcc_a_out[i, t, o, s] -
				data.QDa[(i, t)] * model_cs.xd[i, t, o, s] * data.sd[s] == 0
			)

		model_cs.reactive_power_balance_a_out = Constraint(self.List_NTOS, rule=reactive_power_balance_rule_a_out)

		def reactive_power_balance_rule_b_out(model_cs, i, t, o, s):
			return (
				sum(model_cs.Qb_out[a, j, t, o, s] * data.df[(i, a, j)] for (a, j) in data.L) +
				sum(model_cs.QGb_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				model_cs.Qpcc_b_out[i, t, o, s] -
				data.QDb[(i, t)] * model_cs.xd[i, t, o, s] * data.sd[s] == 0
			)

		model_cs.reactive_power_balance_b_out = Constraint(self.List_NTOS, rule=reactive_power_balance_rule_b_out)

		def reactive_power_balance_rule_c_out(model_cs, i, t, o, s):
			return (
				sum(model_cs.Qc_out[a, j, t, o, s] * data.df[(i, a, j)] for (a, j) in data.L) +
				sum(model_cs.QGc_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				model_cs.Qpcc_c_out[i, t, o, s] -
				data.QDc[(i, t)] * model_cs.xd[i, t, o, s] * data.sd[s] == 0
			)

		model_cs.reactive_power_balance_c_out = Constraint(self.List_NTOS, rule=reactive_power_balance_rule_c_out)

		#Genset Operation

		def genset_power_rule_out(model_cs, i, t, o, s):
			return (model_cs.PGa_out[i, t, o, s] + model_cs.PGb_out[i, t, o, s] + model_cs.PGc_out[i, t, o, s] == model_cs.PG_out[i, t, o, s])

		model_cs.genset_power_active_out = Constraint(self.List_GDTOS, rule=genset_power_rule_out)

		def genset_power_reactive_rule_out(model_cs, i, t, o, s):
			return (model_cs.QGa_out[i, t, o, s] + model_cs.QGb_out[i, t, o, s] + model_cs.QGc_out[i, t, o, s] == model_cs.QG_out[i, t, o, s])

		model_cs.genset_power_reactive_out = Constraint(self.List_GDTOS, rule=genset_power_reactive_rule_out)

		def genset_power_active_limits_rule_out_1(model_cs, i, t, o, s):
			return (model_cs.PG_out[i, t, o, s] >= data.PG_min[i])

		model_cs.genset_power_active_limits_1_out = Constraint(self.List_GDTOS, rule=genset_power_active_limits_rule_out_1)

		def genset_power_active_limits_rule_out_2(model_cs, i, t, o, s):
			return (model_cs.PG_out[i, t, o, s] <= data.PG_max[i])

		model_cs.genset_power_active_limits_2_out = Constraint(self.List_GDTOS, rule=genset_power_active_limits_rule_out_2)

		def genset_power_reactive_limits_rule_out_1(model_cs, i, t, o, s):
			return (model_cs.QG_out[i, t, o, s] >= data.QG_min[i])

		model_cs.genset_power_reactive_limits_1_out = Constraint(self.List_GDTOS, rule=genset_power_reactive_limits_rule_out_1)

		def genset_power_reactive_limits_rule_out_2(model_cs, i, t, o, s):
			return (model_cs.QG_out[i, t, o, s] <= data.QG_max[i])

		model_cs.genset_power_reactive_limits_2_out = Constraint(self.List_GDTOS, rule=genset_power_reactive_limits_rule_out_2)

		# FIX Variables: Islanded operation

		model_cs.islanded_operation = ConstraintList()
		for i in data.N:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if int(t) >= int(o) and int(t) < int(o) + 2:
							model_cs.islanded_operation.add(expr=model_cs.Ppcc_a_out[i, t, o, s] == 0)
							model_cs.islanded_operation.add(expr=model_cs.Ppcc_b_out[i, t, o, s] == 0)
							model_cs.islanded_operation.add(expr=model_cs.Ppcc_c_out[i, t, o, s] == 0)
							model_cs.islanded_operation.add(expr=model_cs.Qpcc_a_out[i, t, o, s] == 0)
							model_cs.islanded_operation.add(expr=model_cs.Qpcc_b_out[i, t, o, s] == 0)
							model_cs.islanded_operation.add(expr=model_cs.Qpcc_c_out[i, t, o, s] == 0)

		def fix_voltage_a_rule_out(model_cs, i, t, o, s):
			return (model_cs.Va_out[i, t, o, s] == data.Vnom)

		model_cs.fix_voltage_a_out = Constraint(self.List_NTOS, rule=fix_voltage_a_rule_out)

		def fix_voltage_b_rule_out(model_cs, i, t, o, s):
			return (model_cs.Vb_out[i, t, o, s] == data.Vnom)

		model_cs.fix_voltage_b_out = Constraint(self.List_NTOS, rule=fix_voltage_b_rule_out)

		def fix_voltage_c_rule_out(model_cs, i, t, o, s):
			return (model_cs.Vc_out[i, t, o, s] == data.Vnom)

		model_cs.fix_voltage_c_out = Constraint(self.List_NTOS, rule=fix_voltage_c_rule_out)

		model_cs.fix_active_power_out = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if data.Tb[i] != 1:
							model_cs.fix_active_power_out.add(expr=model_cs.Ppcc_a_out[i, t, o, s] == 0)
							model_cs.fix_active_power_out.add(expr=model_cs.Ppcc_b_out[i, t, o, s] == 0)
							model_cs.fix_active_power_out.add(expr=model_cs.Ppcc_c_out[i, t, o, s] == 0)

		model_cs.fix_reactive_power_out = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if data.Tb[i] != 1:
							model_cs.fix_reactive_power_out.add(expr=model_cs.Qpcc_a_out[i, t, o, s] == 0)
							model_cs.fix_reactive_power_out.add(expr=model_cs.Qpcc_b_out[i, t, o, s] == 0)
							model_cs.fix_reactive_power_out.add(expr=model_cs.Qpcc_c_out[i, t, o, s] == 0)
		return model_cs

	def Solving_Model_CS(self, model_cs):
		data = self.data
		try:
			solver = SolverFactory('cbc')
			results = solver.solve(model_cs)
		
		except Exception as e:
			print("Error al resolver el modelo:", e)

		# Saving variables of the problem
		self.Pa = model_cs.Pa.get_values()
		self.Pb = model_cs.Pb.get_values()
		self.Pc = model_cs.Pc.get_values()
		self.Qa = model_cs.Qa.get_values()
		self.Qb = model_cs.Qb.get_values()
		self.Qc = model_cs.Qc.get_values()
		self.Va = model_cs.Va.get_values()
		self.Vb = model_cs.Vb.get_values()
		self.Vc = model_cs.Vc.get_values()

		self.Pa_out = model_cs.Pa_out.get_values()
		self.Pb_out = model_cs.Pb_out.get_values()
		self.Pc_out = model_cs.Pc_out.get_values()
		self.Qa_out = model_cs.Qa_out.get_values()
		self.Qb_out = model_cs.Qb_out.get_values()
		self.Qc_out = model_cs.Qc_out.get_values()
		self.Va_out = model_cs.Va_out.get_values()
		self.Vb_out = model_cs.Vb_out.get_values()
		self.Vc_out = model_cs.Vc_out.get_values()
		
	def ProblemFormulation(self):
		data = self.data

		# Type of problem
		model = ConcreteModel("Modelo_EMS_PYOMO")

		model.Pa = Var(data.L, data.T, data.S,within = Reals)
		model.Pb = Var(data.L, data.T, data.S,within = Reals)
		model.Pc = Var(data.L, data.T, data.S,within = Reals)
		model.Qa = Var(data.L, data.T, data.S,within = Reals)
		model.Qb = Var(data.L, data.T, data.S,within = Reals)
		model.Qc = Var(data.L, data.T, data.S,within = Reals)
		model.Va = Var(data.N, data.T, data.S,within = Reals)
		model.Vb = Var(data.N, data.T, data.S,within = Reals)
		model.Vc = Var(data.N, data.T, data.S,within = Reals)

		model.Plss_a = Var(data.L, data.T, data.S,within = Reals)
		model.Plss_b = Var(data.L, data.T, data.S,within = Reals)
		model.Plss_c = Var(data.L, data.T, data.S,within = Reals)
		model.Qlss_a = Var(data.L, data.T, data.S,within = Reals)
		model.Qlss_b = Var(data.L, data.T, data.S,within = Reals)
		model.Qlss_c = Var(data.L, data.T, data.S,within = Reals)

		model.Ppcc_a = Var(data.N, data.T, data.S,within = Reals)
		model.Ppcc_b = Var(data.N, data.T, data.S,within = Reals)
		model.Ppcc_c = Var(data.N, data.T, data.S,within = Reals)
		model.Qpcc_a = Var(data.N, data.T, data.S,within = Reals)
		model.Qpcc_b = Var(data.N, data.T, data.S,within = Reals)
		model.Qpcc_c = Var(data.N, data.T, data.S,within = Reals)
		model.Ppcc = Var(data.N, data.T, data.S,within = Reals)
		model.Qpcc = Var(data.N, data.T, data.S,within = Reals)

		model.PGa = Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.PGb = Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.PGc = Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.QGa = Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.QGb = Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.QGc = Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.PG =  Var(data.GD, data.T, data.S,within = NonNegativeReals)
		model.QG =  Var(data.GD, data.T, data.S,within = NonNegativeReals)

		model.EB = Var(data.B, data.T, within = Reals)
		model.PB = Var(data.B, data.T, within = Reals)
		model.b_ch =     Var(data.B, data.T, within=Binary)
		model.b_dis =    Var(data.B, data.T, within=Binary)
		model.PB_ch =    Var(data.B, data.T, within = Reals)
		model.PB_dis =   Var(data.B, data.T, within = Reals)
		model.PB_ch_a =  Var(data.B, data.T, within = Reals)
		model.PB_ch_b =  Var(data.B, data.T, within = Reals)
		model.PB_ch_c =  Var(data.B, data.T, within = Reals)
		model.PB_dis_a = Var(data.B, data.T, within = Reals)
		model.PB_dis_b = Var(data.B, data.T, within = Reals)
		model.PB_dis_c = Var(data.B, data.T, within = Reals)

		#model.EEV =       Var(data.EV, data.T, within = NonNegativeReals)
		#model.PEV_ch =    Var(data.EV, data.T, within = NonNegativeReals)
		#model.PEV_ch_a =  Var(data.EV, data.T, within = NonNegativeReals)
		#model.PEV_ch_b =  Var(data.EV, data.T, within = NonNegativeReals)
		#model.PEV_ch_c =  Var(data.EV, data.T, within = NonNegativeReals)

		# Power flow linearization variables
		model.Pa_sqr = Var(data.L, data.T, data.S, within = Reals)
		model.Pb_sqr = Var(data.L, data.T, data.S, within = Reals)
		model.Pc_sqr = Var(data.L, data.T, data.S, within = Reals)
		model.Qa_sqr = Var(data.L, data.T, data.S, within = Reals)
		model.Qb_sqr = Var(data.L, data.T, data.S, within = Reals)
		model.Qc_sqr = Var(data.L, data.T, data.S, within = Reals)

		model.Pa_p = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Pa_n = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Pb_p = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Pb_n = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Pc_p = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Pc_n = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Qa_p = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Qa_n = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Qb_p = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Qb_n = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Qc_p = Var(data.L, data.T, data.S, within = NonNegativeReals)
		model.Qc_n = Var(data.L, data.T, data.S, within = NonNegativeReals)

		model.Pa_Dp = Var(data.L, data.T, data.S, data.Y, within = NonNegativeReals)
		model.Pb_Dp = Var(data.L, data.T, data.S, data.Y, within = NonNegativeReals)
		model.Pc_Dp = Var(data.L, data.T, data.S, data.Y, within = NonNegativeReals)
		model.Qa_Dp = Var(data.L, data.T, data.S, data.Y, within = NonNegativeReals)
		model.Qb_Dp = Var(data.L, data.T, data.S, data.Y, within = NonNegativeReals)
		model.Qc_Dp = Var(data.L, data.T, data.S, data.Y, within = NonNegativeReals)

		# Linearization of PCC
		model.Ppcc_sqr = Var(data.N, data.T, data.S, within = NonNegativeReals)
		model.Qpcc_sqr = Var(data.N, data.T, data.S, within = NonNegativeReals)
		model.Ppcc_p = Var(data.N, data.T, data.S, within = NonNegativeReals)
		model.Ppcc_n = Var(data.N, data.T, data.S, within = NonNegativeReals)
		model.Qpcc_n = Var(data.N, data.T, data.S, within = NonNegativeReals)
		model.Qpcc_p = Var(data.N, data.T, data.S, within = NonNegativeReals)
		model.Ppcc_Dp = Var(data.N, data.T, data.S, data.Y,within =  NonNegativeReals)
		model.Qpcc_Dp = Var(data.N, data.T, data.S, data.Y, within = NonNegativeReals)

		# Voltage linearization variables
		model.Va_sqr = Var(data.N, data.T, data.S, within = NonNegativeReals, bounds = (data.Vmin**2, data.Vmax**2))
		model.Vb_sqr = Var(data.N, data.T, data.S, within = NonNegativeReals, bounds = (data.Vmin**2, data.Vmax**2))
		model.Vc_sqr = Var(data.N, data.T, data.S, within = NonNegativeReals, bounds = (data.Vmin**2, data.Vmax**2))

		## ------ Variables for contingences --------------
		model.Pa_out =     Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Pb_out =     Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Pc_out =     Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qa_out =     Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qb_out =     Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qc_out =     Var(data.L, data.T, data.O, data.S, within = Reals)

		model.Va_out =     Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Vb_out =     Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Vc_out =     Var(data.N, data.T, data.O, data.S, within = Reals)

		model.Plss_a_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Plss_b_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Plss_c_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qlss_a_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qlss_b_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qlss_c_out = Var(data.L, data.T, data.O, data.S, within = Reals)

		model.Ppcc_a_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Ppcc_b_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Ppcc_c_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Qpcc_a_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Qpcc_b_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Qpcc_c_out = Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Ppcc_out =   Var(data.N, data.T, data.O, data.S, within = Reals)
		model.Qpcc_out =   Var(data.N, data.T, data.O, data.S, within = Reals)

		model.PGa_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.PGb_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.PGc_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.QGa_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.QGb_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.QGc_out = Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.PG_out =  Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.QG_out =  Var(data.GD, data.T, data.O, data.S, within = NonNegativeReals)
		model.oG_out =  Var(data.GD, data.T, data.O, data.S, domain = Binary)

		# Power flow linearization variables with contingences
		model.Pa_sqr_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Pb_sqr_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Pc_sqr_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qa_sqr_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qb_sqr_out = Var(data.L, data.T, data.O, data.S, within = Reals)
		model.Qc_sqr_out = Var(data.L, data.T, data.O, data.S, within = Reals)

		model.Pa_p_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Pa_n_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Pb_p_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Pb_n_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Pc_p_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Pc_n_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qa_p_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qa_n_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qb_p_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qb_n_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qc_p_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qc_n_out = Var(data.L, data.T, data.O, data.S, within = NonNegativeReals)

		# Variáveis com Dp deveriam ser maiores ou iguais a zerdata.O, mas ao inserir como NonNegativeReals o problema da infactível
		model.Pa_Dp_out = Var(data.L, data.T, data.O, data.S, data.Y, within = NonNegativeReals)
		model.Pb_Dp_out = Var(data.L, data.T, data.O, data.S, data.Y, within = NonNegativeReals)
		model.Pc_Dp_out = Var(data.L, data.T, data.O, data.S, data.Y, within = NonNegativeReals)
		model.Qa_Dp_out = Var(data.L, data.T, data.O, data.S, data.Y, within = NonNegativeReals)
		model.Qb_Dp_out = Var(data.L, data.T, data.O, data.S, data.Y, within = NonNegativeReals)
		model.Qc_Dp_out = Var(data.L, data.T, data.O, data.S, data.Y, within = NonNegativeReals)

		# Linearization of PCC
		model.Ppcc_sqr_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qpcc_sqr_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals)
		model.Ppcc_p_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals)
		model.Ppcc_n_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qpcc_n_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals)
		model.Qpcc_p_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals)
		model.Ppcc_Dp_out = Var(data.N, data.T, data.O, data.S, data.Y, within = NonNegativeReals)
		model.Qpcc_Dp_out = Var(data.N, data.T, data.O, data.S, data.Y, within = NonNegativeReals)

		# Voltage linearization variables

		model.Va_sqr_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals, bounds = (data.Vmin**2, data.Vmax**2))
		model.Vb_sqr_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals, bounds = (data.Vmin**2, data.Vmax**2))
		model.Vc_sqr_out = Var(data.N, data.T, data.O, data.S, within = NonNegativeReals, bounds = (data.Vmin**2, data.Vmax**2))

		model.xd =  Var(data.N, data.T, data.O, data.S, domain = Binary)

		# Objective function
		if len(data.O) >= 1 :
			cost_operation_contingency = (sum(data.Prob[s]*(0.01/len(data.O) * (sum(data.cEDS[t] * data.delta_t * (model.Ppcc_a_out[i, t, o, s] + model.Ppcc_b_out[i, t, o, s] + model.Ppcc_c_out[i, t, o, s]) for (i, t, o, s) in self.List_NTOS) + 
											sum([data.cost_PG[i] * data.delta_t * model.PG_out[i,t,o, s] for (i,t,o,s) in self.List_GDTOS]) + 
											sum([data.delta_t * data.alpha_c[i] * data.sd[s] * (data.PDa[(i,t)]+data.PDb[(i,t)]+data.PDc[(i,t)]) * (1-model.xd[i,t,o,s]) for (i,t,o,s) in self.List_NTOS]))) + 
											(0.99 * sum(data.cEDS[t] * data.delta_t * (model.Ppcc_a[i, t,s] + model.Ppcc_b[i, t,s] + model.Ppcc_c[i, t,s]) for (i, t,s) in self.List_NTS) + 
											sum(data.cost_PG[i] * data.delta_t * model.PG[i, t,s] for (i, t,s) in self.List_GDTS)) for s in data.S))
		else :
			cost_operation_contingency = (sum(data.Prob[s]*(0.01/1000000 * (sum(data.cEDS[t] * data.delta_t * (model.Ppcc_a_out[i, t, o, s] + model.Ppcc_b_out[i, t, o, s] + model.Ppcc_c_out[i, t, o, s]) for (i, t, o, s) in self.List_NTOS) + 
											sum([data.delta_t * data.alpha_c[i] * data.sd[s] * (data.PDa[(i,t)]+data.PDb[(i,t)]+data.PDc[(i,t)]) * (1-model.xd[i,t,o,s]) for (i,t,o,s) in self.List_NTOS]))) +
											(0.99 * sum(data.cEDS[t] * data.delta_t * (model.Ppcc_a[i, t,s] + model.Ppcc_b[i, t,s] + model.Ppcc_c[i, t,s]) for (i, t,s) in self.List_NTS)) for s in data.S))

		model.objective_function = Objective(expr=cost_operation_contingency)

		# --------------------- Constraints --------------------------------------------
		# --------------------- Without Contingences------------------------------------------
		# Active losses ----------------------------------------------------------------
		def active_losses_a_rule(model, i, j, t, s):
			return (
				(1 / (data.Va_0[i, t, s] * data.Va_0[i, t, s])) * 
		        (data.Raa_p[i, j] * model.Pa_sqr[i, j, t, s] + 
		         data.Raa_p[i, j] * model.Qa_sqr[i, j, t, s] - 
		         data.Xaa_p[i, j] * data.Pa_0[i, j, t, s] * model.Qa[i, j, t, s] + 
		         data.Xaa_p[i, j] * data.Qa_0[i, j, t, s] * model.Pa[i, j, t, s]) +
		        (1 / (data.Va_0[i, t, s] * data.Vb_0[i, t, s])) * 
		        (data.Rab_p[i, j] * data.Pb_0[i, j, t, s] * model.Pa[i, j, t, s] + 
		         data.Rab_p[i, j] * data.Qb_0[i, j, t, s] * model.Qa[i, j, t, s] - 
		         data.Xab_p[i, j] * data.Pb_0[i, j, t, s] * model.Qa[i, j, t, s] + 
		         data.Xab_p[i, j] * data.Qb_0[i, j, t, s] * model.Pa[i, j, t, s]) +
		        (1 / (data.Va_0[i, t, s] * data.Vc_0[i, t, s])) * 
		        (data.Rac_p[i, j] * data.Pc_0[i, j, t, s] * model.Pa[i, j, t, s] + 
		         data.Rac_p[i, j] * data.Qc_0[i, j, t, s] * model.Qa[i, j, t, s] - 
		         data.Xac_p[i, j] * data.Pc_0[i, j, t, s] * model.Qa[i, j, t, s] + 
		         data.Xac_p[i, j] * data.Qc_0[i, j, t, s] * model.Pa[i, j, t, s]) == model.Plss_a[i, j, t, s])
		model.active_losses_a = Constraint(self.List_LTS, rule=active_losses_a_rule)
		
		def active_losses_b_rule(model, i, j, t, s):
			return (
				(1 / (data.Vb_0[i, t, s] * data.Va_0[i, t, s])) * 
				(data.Rba_p[i, j] * data.Pa_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Rba_p[i, j] * data.Qa_0[i, j, t, s] * model.Qb[i, j, t, s] - 
				 data.Xba_p[i, j] * data.Pa_0[i, j, t, s] * model.Qb[i, j, t, s] + 
				 data.Xba_p[i, j] * data.Qa_0[i, j, t, s] * model.Pb[i, j, t, s]) +
				(1 / (data.Vb_0[i, t, s] * data.Vb_0[i, t, s])) * 
				(data.Rbb_p[i, j] * model.Pb_sqr[i, j, t, s]  + 
				 data.Rbb_p[i, j] * model.Qb_sqr[i, j, t, s]  - 
				 data.Xbb_p[i, j] * data.Pb_0[i, j, t, s] * model.Qb[i, j, t, s] + 
				 data.Xbb_p[i, j] * data.Qb_0[i, j, t, s] * model.Pb[i, j, t, s]) +
				(1 / (data.Vb_0[i, t, s] * data.Vc_0[i, t, s])) * 
				(data.Rbc_p[i, j] * data.Pc_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Rbc_p[i, j] * data.Qc_0[i, j, t, s] * model.Qb[i, j, t, s] - 
				 data.Xbc_p[i, j] * data.Pc_0[i, j, t, s] * model.Qb[i, j, t, s] + 
				 data.Xbc_p[i, j] * data.Qc_0[i, j, t, s] * model.Pb[i, j, t, s]) == model.Plss_b[i, j, t, s])
		model.active_losses_b = Constraint(self.List_LTS, rule=active_losses_b_rule)


		def active_losses_c_rule(model, i, j, t, s):
			return (
				(1 / (data.Vc_0[i, t, s] * data.Va_0[i, t, s])) * 
				(data.Rca_p[i, j] * data.Pa_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Rca_p[i, j] * data.Qa_0[i, j, t, s] * model.Qc[i, j, t, s] - 
				 data.Xca_p[i, j] * data.Pa_0[i, j, t, s] * model.Qc[i, j, t, s] + 
				 data.Xca_p[i, j] * data.Qa_0[i, j, t, s] * model.Pc[i, j, t, s]) +
				(1 / (data.Vc_0[i, t, s] * data.Vb_0[i, t, s])) * 
				(data.Rcb_p[i, j] * data.Pb_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Rcb_p[i, j] * data.Qb_0[i, j, t, s] * model.Qc[i, j, t, s] - 
				 data.Xcb_p[i, j] * data.Pb_0[i, j, t, s] * model.Qc[i, j, t, s] + 
				 data.Xcb_p[i, j] * data.Qb_0[i, j, t, s] * model.Pc[i, j, t, s]) +
				(1 / (data.Vc_0[i, t, s] * data.Vc_0[i, t, s])) * 
				(data.Rcc_p[i, j] * model.Pc_sqr[i, j, t, s]  + 
				 data.Rcc_p[i, j] * model.Qc_sqr[i, j, t, s]  - 
				 data.Xcc_p[i, j] * data.Pc_0[i, j, t, s] * model.Qc[i, j, t, s] + 
				 data.Xcc_p[i, j] * data.Qc_0[i, j, t, s] * model.Pc[i, j, t, s]) == model.Plss_c[i, j, t, s])
		model.active_losses_c = Constraint(self.List_LTS, rule=active_losses_c_rule)    

		# Reactive losses ----------------------------------------------------------------
		def reactive_losses_a_rule(model, i, j, t, s):
			return (
				(1 / (data.Va_0[i, t, s] * data.Va_0[i, t, s])) * 
				(data.Raa_p[i, j] * data.Pa_0[i, j, t, s] * model.Qa[i, j, t, s] - 
				 data.Raa_p[i, j] * data.Qa_0[i, j, t, s] * model.Pa[i, j, t, s] + 
				 data.Xaa_p[i, j] * model.Pa_sqr[i, j, t, s]  + 
				 data.Xaa_p[i, j] * model.Qa_sqr[i, j, t, s] ) +
				(1 / (data.Va_0[i, t, s] * data.Vb_0[i, t, s])) * 
				(data.Rab_p[i, j] * data.Pb_0[i, j, t, s] * model.Qa[i, j, t, s] - 
				 data.Rab_p[i, j] * data.Qb_0[i, j, t, s] * model.Pa[i, j, t, s] + 
				 data.Xab_p[i, j] * data.Pb_0[i, j, t, s] * model.Pa[i, j, t, s] + 
				 data.Xab_p[i, j] * data.Qb_0[i, j, t, s] * model.Qa[i, j, t, s]) +
				(1 / (data.Va_0[i, t, s] * data.Vc_0[i, t, s])) * 
				(data.Rac_p[i, j] * data.Pc_0[i, j, t, s] * model.Qa[i, j, t, s] - 
				 data.Rac_p[i, j] * data.Qc_0[i, j, t, s] * model.Pa[i, j, t, s] + 
				 data.Xac_p[i, j] * data.Pc_0[i, j, t, s] * model.Pa[i, j, t, s] + 
				 data.Xac_p[i, j] * data.Qc_0[i, j, t, s] * model.Qa[i, j, t, s]) == model.Qlss_a[i, j, t, s])
		model.reactive_losses_a = Constraint(self.List_LTS, rule=reactive_losses_a_rule)

		def reactive_losses_b_rule(model, i, j, t, s):
			return (
				(1 / (data.Vb_0[i, t, s] * data.Va_0[i, t, s])) * 
				(data.Rba_p[i, j] * data.Pa_0[i, j, t, s] * model.Qb[i, j, t, s] - 
				 data.Rba_p[i, j] * data.Qa_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Xba_p[i, j] * data.Pa_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Xba_p[i, j] * data.Qa_0[i, j, t, s] * model.Qb[i, j, t, s]) +
				(1 / (data.Vb_0[i, t, s] * data.Vb_0[i, t, s])) * 
				(data.Rbb_p[i, j] * data.Pb_0[i, j, t, s] * model.Qb[i, j, t, s] - 
				 data.Rbb_p[i, j] * data.Qb_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Xbb_p[i, j] * model.Pb_sqr[i, j, t, s]  + 
				 data.Xbb_p[i, j] * model.Qb_sqr[i, j, t, s] ) +
				(1 / (data.Vb_0[i, t, s] * data.Vc_0[i, t, s])) * 
				(data.Rbc_p[i, j] * data.Pc_0[i, j, t, s] * model.Qb[i, j, t, s] - 
				 data.Rbc_p[i, j] * data.Qc_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Xbc_p[i, j] * data.Pc_0[i, j, t, s] * model.Pb[i, j, t, s] + 
				 data.Xbc_p[i, j] * data.Qc_0[i, j, t, s] * model.Qb[i, j, t, s]) == model.Qlss_b[i, j, t, s])

		model.reactive_losses_b = Constraint(self.List_LTS, rule= reactive_losses_b_rule)

		def reactive_losses_c_rule(model, i, j, t, s):
			return (
				(1 / (data.Vc_0[i, t, s] * data.Va_0[i, t, s])) * 
				(data.Rca_p[i, j] * data.Pa_0[i, j, t, s] * model.Qc[i, j, t, s] - 
				 data.Rca_p[i, j] * data.Qa_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Xca_p[i, j] * data.Pa_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Xca_p[i, j] * data.Qa_0[i, j, t, s] * model.Qc[i, j, t, s]) +
				(1 / (data.Vc_0[i, t, s] * data.Vb_0[i, t, s])) * 
				(data.Rcb_p[i, j] * data.Pb_0[i, j, t, s] * model.Qc[i, j, t, s] - 
				 data.Rcb_p[i, j] * data.Qb_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Xcb_p[i, j] * data.Pb_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Xcb_p[i, j] * data.Qb_0[i, j, t, s] * model.Qc[i, j, t, s]) +
				(1 / (data.Vc_0[i, t, s] * data.Vc_0[i, t, s])) * 
				(data.Rcc_p[i, j] * data.Pc_0[i, j, t, s] * model.Qc[i, j, t, s] - 
				 data.Rcc_p[i, j] * data.Qc_0[i, j, t, s] * model.Pc[i, j, t, s] + 
				 data.Xcc_p[i, j] * model.Pc_sqr[i, j, t, s]  + 
				 data.Xcc_p[i, j] * model.Qc_sqr[i, j, t, s] ) == model.Qlss_c[i, j, t, s])

		model.reactive_losses_c = Constraint(self.List_LTS, rule= reactive_losses_c_rule)

		# Active Power Flow ----------------------------------------------------------------
		def active_power_balance_rule_a(model, i, t, s):
			return (
				sum(model.Pa[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Plss_a[a, j, t, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Ppcc_a[i, t, s] +
				sum(model.PGa[a, t, s] for a in data.dict_nos_gd[i]) +
				sum(model.PB_dis_a[a, t] for a in data.dict_nos_bs[i]) -
				sum(model.PB_ch_a[a, t] for a in data.dict_nos_bs[i]) -
				data.PDa[(i,t)]*data.sd[s] + data.PVa[(i,t)]*data.spv[s] == 0
			)

		model.active_power_balance_a = Constraint(self.List_NTS, rule=active_power_balance_rule_a)

		def active_power_balance_rule_b(model, i, t, s):
			return (
				sum(model.Pb[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Plss_b[a, j, t, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Ppcc_b[i, t, s] +
				sum(model.PGb[a, t, s] for a in data.dict_nos_gd[i]) +
				sum(model.PB_dis_b[a, t] for a in data.dict_nos_bs[i]) -
				sum(model.PB_ch_b[a, t] for a in data.dict_nos_bs[i]) -
				data.PDb[(i,t)]*data.sd[s] + data.PVb[(i,t)]*data.spv[s] == 0)

		model.active_power_balance_b = Constraint(self.List_NTS, rule=active_power_balance_rule_b)

		def active_power_balance_rule_c(model, i, t, s):
			return (
				sum(model.Pc[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Plss_c[a, j, t, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Ppcc_c[i, t, s] +
				sum(model.PGc[a, t, s] for a in data.dict_nos_gd[i]) +
				sum(model.PB_dis_c[a, t] for a in data.dict_nos_bs[i]) -
				sum(model.PB_ch_c[a, t] for a in data.dict_nos_bs[i]) -
				data.PDc[(i,t)]*data.sd[s] + data.PVc[(i,t)]*data.spv[s] == 0)
		model.active_power_balance_c = Constraint(self.List_NTS, rule=active_power_balance_rule_c)

		# Reactive Power Flow ----------------------------------------------------------------
		def reactive_power_balance_rule_a(model, i, t, s):
			return (
				sum(model.Qa[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Qlss_a[a, j, t, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Qpcc_a[i, t, s] +
				sum(model.QGa[a, t, s] for a in data.dict_nos_gd[i]) -
				data.QDa[(i,t)]*data.sd[s] == 0)
		model.reactive_power_balance_a = Constraint(self.List_NTS, rule=reactive_power_balance_rule_a)

		def reactive_power_balance_rule_b(model, i, t, s):
			return (
				sum(model.Qb[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Qlss_b[a, j, t, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Qpcc_b[i, t, s] +
				sum(model.QGb[a, t, s] for a in data.dict_nos_gd[i]) -
				data.QDb[(i,t)]*data.sd[s] == 0)
		model.reactive_power_balance_b = Constraint(self.List_NTS, rule=reactive_power_balance_rule_b)

		def reactive_power_balance_rule_c(model, i, t, s):
			return (
				sum(model.Qc[a, j, t, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Qlss_c[a, j, t, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Qpcc_c[i, t, s] +
				sum(model.QGc[a, t, s] for a in data.dict_nos_gd[i]) -
				data.QDc[(i,t)]*data.sd[s] == 0)
		model.reactive_power_balance_c = Constraint(self.List_NTS, rule=reactive_power_balance_rule_c)

		# Voltage Droop in the Lines ----------------------------------------------------------------
		def voltage_droop_rule_a(model, i, j, t, s):
			return((2*(data.Raa_p[i,j]*model.Pa[i, j, t, s] + data.Xaa_p[i,j]*model.Qa[i, j, t, s])) + 
				(2*(data.Rab_p[i,j]*model.Pb[i, j, t, s] + data.Xab_p[i,j]*model.Qb[i, j, t, s])) + 
				(2*(data.Rac_p[i,j]*model.Pc[i, j, t, s] + data.Xac_p[i,j]*model.Qc[i, j, t, s])) -
				(1/data.Va_0[i, t, s]**2) * ((data.Raa_p[i,j]**2 + data.Xaa_p[i,j]**2) * (model.Pa_sqr[i, j, t, s] + model.Qa_sqr[i, j, t, s])) ==
				model.Va_sqr[i, t, s] - model.Va_sqr[j, t, s])
		model.voltage_droop_a = Constraint(self.List_LTS, rule=voltage_droop_rule_a)
		
		def voltage_droop_rule_b(model, i, j, t, s):
			return((2*(data.Rba_p[i,j]*model.Pa[i, j, t, s] + data.Xba_p[i,j]*model.Qa[i, j, t, s])) + 
				(2*(data.Rbb_p[i,j]*model.Pb[i, j, t, s] + data.Xbb_p[i,j]*model.Qb[i, j, t, s])) + 
				(2*(data.Rbc_p[i,j]*model.Pc[i, j, t, s] + data.Xbc_p[i,j]*model.Qc[i, j, t, s])) -
				(1/data.Vb_0[i, t, s]**2) * ((data.Rbb_p[i,j]**2 + data.Xbb_p[i,j]**2) * (model.Pb_sqr[i, j, t, s] + model.Qb_sqr[i, j, t, s])) ==
				model.Vb_sqr[i, t, s] - model.Vb_sqr[j, t, s])
		model.voltage_droop_b = Constraint(self.List_LTS, rule=voltage_droop_rule_b)
		
		def voltage_droop_rule_c(model, i, j, t, s):
			return((2*(data.Rca_p[i,j]*model.Pa[i, j, t, s] + data.Xca_p[i,j]*model.Qa[i, j, t, s])) + 
				(2*(data.Rcb_p[i,j]*model.Pb[i, j, t, s] + data.Xcb_p[i,j]*model.Qb[i, j, t, s])) + 
				(2*(data.Rcc_p[i,j]*model.Pc[i, j, t, s] + data.Xcc_p[i,j]*model.Qc[i, j, t, s])) -
				(1/data.Vc_0[i, t, s]**2) * ((data.Rcc_p[i,j]**2 + data.Xcc_p[i,j]**2) * (model.Pc_sqr[i, j, t, s] + model.Qc_sqr[i, j, t, s])) ==
				model.Vc_sqr[i, t, s] - model.Vc_sqr[j, t, s])
		model.voltage_droop_c = Constraint(self.List_LTS, rule= voltage_droop_rule_c)

		# Limite máximo de fluxo de corrente e equações de linearização ----------------------------------------------------------------
		def current_limits_rule_a(model, i, j, t, s):
			return((model.Pa_sqr[i, j, t, s] + model.Qa_sqr[i, j, t, s]) <= data.Imax[i,j]**2 * (model.Va_sqr[i, t, s]))
		model.current_limits_a = Constraint(self.List_LTS, rule=current_limits_rule_a)

		def current_limits_rule_b(model, i, j, t, s):
			return((model.Pb_sqr[i, j, t, s] + model.Qb_sqr[i, j, t, s]) <= data.Imax[i,j]**2 * (model.Vb_sqr[i, t, s]))
		model.current_limits_b = Constraint(self.List_LTS, rule=current_limits_rule_b)

		def current_limits_rule_c(model, i, j, t, s):
			return((model.Pc_sqr[i, j, t, s] + model.Qc_sqr[i, j, t, s]) <= data.Imax[i,j]**2 * (model.Vc_sqr[i, t, s]))
		model.current_limits_c = Constraint(self.List_LTS, rule=current_limits_rule_c)

		# Active power linearization constraints
		def pa_calculation_rule(model, i, j, t, s):
			return( model.Pa_sqr[i, j, t, s] - sum(data.S_ms[i,j,y] * model.Pa_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.Pa_calculation = Constraint(self.List_LTS, rule=pa_calculation_rule)

		def pb_calculation_rule(model, i, j, t, s):
			return( model.Pb_sqr[i, j, t, s] - sum(data.S_ms[i,j,y] * model.Pb_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.Pb_calculation = Constraint(self.List_LTS, rule=pb_calculation_rule)

		def pc_calculation_rule(model, i, j, t, s):
			return( model.Pc_sqr[i, j, t, s] - sum(data.S_ms[i,j,y] * model.Pc_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.Pc_calculation = Constraint(self.List_LTS, rule=pc_calculation_rule)

		# Reactive power linearization constraints
		def qa_calculation_rule(model, i, j, t, s):
			return( model.Qa_sqr[i, j, t, s] - sum(data.S_ms[i,j,y] * model.Qa_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.Qa_calculation = Constraint(self.List_LTS, rule=qa_calculation_rule)

		def qb_calculation_rule(model, i, j, t, s):
			return( model.Qb_sqr[i, j, t, s] - sum(data.S_ms[i,j,y] * model.Qb_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.Qb_calculation = Constraint(self.List_LTS, rule=qb_calculation_rule)

		def qc_calculation_rule(model, i, j, t, s):
			return( model.Qc_sqr[i, j, t, s] - sum(data.S_ms[i,j,y] * model.Qc_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.Qc_calculation = Constraint(self.List_LTS, rule=qc_calculation_rule)

		# Linearizations variables
		def pa_p_rule(model, i, j, t, s):
			return( model.Pa_p[i, j, t, s] - model.Pa_n[i, j, t, s] - model.Pa[i, j, t, s] == 0)
		model.Pa_p_constraint = Constraint(self.List_LTS, rule=pa_p_rule)

		def pb_p_rule(model, i, j, t, s):
			return( model.Pb_p[i, j, t, s] - model.Pb_n[i, j, t, s] - model.Pb[i, j, t, s] == 0)
		model.Pb_p_constraint = Constraint(self.List_LTS, rule=pb_p_rule)

		def pc_p_rule(model, i, j, t, s):
			return( model.Pc_p[i, j, t, s] - model.Pc_n[i, j, t, s] - model.Pc[i, j, t, s] == 0)
		model.Pc_p_constraint = Constraint(self.List_LTS, rule=pc_p_rule)

		def qa_p_rule(model, i, j, t, s):
			return( model.Qa_p[i, j, t, s] - model.Qa_n[i, j, t, s] - model.Qa[i, j, t, s] == 0)
		model.Qa_p_constraint = Constraint(self.List_LTS, rule=qa_p_rule)

		def qb_p_rule(model, i, j, t, s):
			return( model.Qb_p[i, j, t, s] - model.Qb_n[i, j, t, s] - model.Qb[i, j, t, s] == 0)
		model.Qb_p_constraint = Constraint(self.List_LTS, rule=qb_p_rule)

		def qc_p_rule(model, i, j, t, s):
			return( model.Qc_p[i, j, t, s] - model.Qc_n[i, j, t, s] - model.Qc[i, j, t, s] == 0)
		model.Qc_p_constraint = Constraint(self.List_LTS, rule=qc_p_rule)

		def pa_abs_rule(model, i, j, t, s):
			return( model.Pa_p[i, j, t, s] + model.Pa_n[i, j, t, s] - sum(model.Pa_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.pa_abs = Constraint(self.List_LTS, rule=pa_abs_rule)

		def pb_abs_rule(model, i, j, t, s):
			return( model.Pb_p[i, j, t, s] + model.Pb_n[i, j, t, s] - sum(model.Pb_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.pb_abs = Constraint(self.List_LTS, rule=pb_abs_rule)

		def pc_abs_rule(model, i, j, t, s):
			return( model.Pc_p[i, j, t, s] + model.Pc_n[i, j, t, s] - sum(model.Pc_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.pc_abs = Constraint(self.List_LTS, rule=pc_abs_rule)

		def qa_abs_rule(model, i, j, t, s):
			return( model.Qa_p[i, j, t, s] + model.Qa_n[i, j, t, s] - sum(model.Qa_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.qa_abs = Constraint(self.List_LTS, rule=qa_abs_rule)

		def qb_abs_rule(model, i, j, t, s):
			return( model.Qb_p[i, j, t, s] + model.Qb_n[i, j, t, s] - sum(model.Qb_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.qb_abs = Constraint(self.List_LTS, rule=qb_abs_rule)

		def qc_abs_rule(model, i, j, t, s):
			return( model.Qc_p[i, j, t, s] + model.Qc_n[i, j, t, s] - sum(model.Qc_Dp[i, j, t, s, y] for y in data.Y) == 0)
		model.qc_abs = Constraint(self.List_LTS, rule=qc_abs_rule)

		def pa_limits_rule(model, i, j, t, s, y):
			return( model.Pa_Dp[i, j, t, s, y] <= data.S_Dp_max[i,j])
		model.pa_limits = Constraint(self.List_LTSY, rule=pa_limits_rule)

		def pb_limits_rule(model, i, j, t, s, y):
			return( model.Pb_Dp[i, j, t, s, y] <= data.S_Dp_max[i,j])
		model.pb_limits = Constraint(self.List_LTSY, rule=pb_limits_rule)

		def pc_limits_rule(model, i, j, t, s, y):
			return( model.Pc_Dp[i, j, t, s, y] <= data.S_Dp_max[i,j])
		model.pc_limits = Constraint(self.List_LTSY, rule=pc_limits_rule)

		def qa_limits_rule(model, i, j, t, s, y):
			return( model.Qa_Dp[i, j, t, s, y] <= data.S_Dp_max[i,j])
		model.qa_limits = Constraint(self.List_LTSY, rule=qa_limits_rule)

		def qb_limits_rule(model, i, j, t, s, y):
			return( model.Qb_Dp[i, j, t, s, y] <= data.S_Dp_max[i,j])
		model.qc_limits = Constraint(self.List_LTSY, rule=qb_limits_rule)

		def qc_limits_rule(model, i, j, t, s, y):
			return( model.Qc_Dp[i, j, t, s, y] <= data.S_Dp_max[i,j])
		model.qc_limits = Constraint(self.List_LTSY, rule=qc_limits_rule)

		# PCC constraints ---------------------------------------------------------
		def ative_power_pcc_rule(model, i, t, s):
			return(model.Ppcc[i, t, s] - model.Ppcc_a[i, t, s] - model.Ppcc_b[i, t, s] - model.Ppcc_c[i, t, s] == 0)
		model.ative_power_pcc = Constraint(self.List_NTS, rule=ative_power_pcc_rule)

		def reative_power_pcc_rule(model, i, t, s):
			return(model.Qpcc[i, t, s] - model.Qpcc_a[i, t, s] - model.Qpcc_b[i, t, s] - model.Qpcc_c[i, t, s] == 0)
		model.reative_power_pcc = Constraint(self.List_NTS, rule=reative_power_pcc_rule)

		# Apparent power --------------------------------------------------
		def apparent_power_pcc_rule(model, i, t, s):
			return(model.Ppcc_sqr[i, t, s] + model.Qpcc_sqr[i, t, s] <= data.Smax[i]**2)
		model.apparent_power_pcc = Constraint(self.List_NTS, rule=apparent_power_pcc_rule)

		# PCC piecewise linearization constraints ------------------------------
		def ppcc_calculation_rule(model, i, t, s):
			return( model.Ppcc_sqr[i, t, s] - sum(data.Spcc_ms[i,y] * model.Ppcc_Dp[i, t, s, y] for y in data.Y) == 0)
		model.Ppcc_calculation = Constraint(self.List_NTS, rule=ppcc_calculation_rule)

		def Qpcc_calculation_rule(model, i, t, s):
			return( model.Qpcc_sqr[i, t, s] - sum(data.Spcc_ms[i,y] * model.Qpcc_Dp[i, t, s, y] for y in data.Y) == 0)
		model.Qpcc_calculation = Constraint(self.List_NTS, rule=Qpcc_calculation_rule)

		def ppcc_p_rule(model, i, t, s):
			return( model.Ppcc_p[i, t, s] - model.Ppcc_n[i, t, s] - model.Ppcc[i, t, s] == 0)
		model.Ppcc_p_constraint = Constraint(self.List_NTS, rule=ppcc_p_rule)

		def qpcc_p_rule(model, i, t, s):
			return( model.Qpcc_p[i, t, s] - model.Qpcc_n[i, t, s] - model.Qpcc[i, t, s] == 0)
		model.Qpcc_p_constraint = Constraint(self.List_NTS, rule=qpcc_p_rule)

		def ppcc_abs_rule(model, i, t, s):
			return( model.Ppcc_p[i, t, s] + model.Ppcc_n[i, t, s] - sum(model.Ppcc_Dp[i, t, s, y] for y in data.Y) == 0)
		model.ppcc_abs = Constraint(self.List_NTS, rule=ppcc_abs_rule)

		def qpcc_abs_rule(model, i, t, s):
			return( model.Qpcc_p[i, t, s] + model.Qpcc_n[i, t, s] - sum(model.Qpcc_Dp[i, t, s, y] for y in data.Y) == 0)
		model.qpcc_abs = Constraint(self.List_NTS, rule=qpcc_abs_rule)

		# PCC limits --------------------------------------------------------
		def ppcc_limits_rule(model, i, t, s, y):
			return( model.Ppcc_Dp[i, t, s, y] <= data.Spcc_Dp_max[i])
		model.ppcc_limits = Constraint(self.List_NTSY, rule=ppcc_limits_rule)

		def qpcc_limits_rule(model, i, t, s, y):
			return( model.Qpcc_Dp[i, t, s, y] <= data.Spcc_Dp_max[i])
		model.qpcc_limits = Constraint(self.List_NTSY, rule=qpcc_limits_rule)        

		# Genset ----------------------------------------------------------------
		def genset_power_rule(model, i, t, s):
			return(model.PGa[i, t, s] + model.PGb[i, t, s] + model.PGc[i, t, s] == model.PG[i, t, s])
		model.genset_power_active = Constraint(self.List_GDTS, rule=genset_power_rule)

		def genset_power_reactive_rule(model, i, t, s):
			return(model.QGa[i, t, s] + model.QGb[i, t, s] + model.QGc[i, t, s] == model.QG[i, t, s])
		model.genset_power_reactive = Constraint(self.List_GDTS, rule=genset_power_reactive_rule)

		def genset_power_active_limits_rule_1(model, i, t, s):
			return(model.PG[i, t, s] >= data.PG_min[i])
		model.genset_power_active_limits_1 = Constraint(self.List_GDTS, rule=genset_power_active_limits_rule_1)

		def genset_power_active_limits_rule_2(model, i, t, s):
			return(model.PG[i, t, s] <= data.PG_max[i])
		model.genset_power_active_limits_2 = Constraint(self.List_GDTS, rule=genset_power_active_limits_rule_2)

		def genset_power_reactive_limits_rule_1(model, i, t, s):
			return(model.QG[i, t, s] >= data.QG_min[i])
		model.genset_power_reactive_limits_1 = Constraint(self.List_GDTS, rule=genset_power_reactive_limits_rule_1)

		def genset_power_reactive_limits_rule_2(model, i, t, s):
			return(model.QG[i, t, s] <= data.QG_max[i])
		model.genset_power_reactive_limits_2 = Constraint(self.List_GDTS, rule=genset_power_reactive_limits_rule_2)

		def genset_operation_1_rule_cm(model, i, t, s):
			return(model.PGa[i, t, s] == 0)
		model.genset_operation_1_cm = Constraint(self.List_GDTS, rule=genset_operation_1_rule_cm)

		def genset_operation_2_rule_cm(model, i, t, s):
			return(model.PGb[i, t, s] == 0)
		model.genset_operation_2_cm = Constraint(self.List_GDTS, rule=genset_operation_2_rule_cm)

		def genset_operation_3_rule_cm(model, i, t, s):
			return(model.PGc[i, t, s] == 0)
		model.genset_operation_3_cm = Constraint(self.List_GDTS, rule=genset_operation_3_rule_cm)

		def genset_operation_4_rule_cm(model, i, t, s):
			return(model.QGa[i, t, s] == 0)
		model.genset_operation_4_cm = Constraint(self.List_GDTS, rule=genset_operation_4_rule_cm)

		def genset_operation_5_rule_cm(model, i, t, s):
			return(model.QGb[i, t, s] == 0)
		model.genset_operation_5_cm = Constraint(self.List_GDTS, rule=genset_operation_5_rule_cm)

		def genset_operation_6_rule_cm(model, i, t, s):
			return(model.QGc[i, t, s] == 0)
		model.genset_operation_6_cm = Constraint(self.List_GDTS, rule=genset_operation_6_rule_cm)

		# Island Operation
		model.islanded_operation = ConstraintList()
		for i in data.N:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if int(t) >= int(o) and int(t) < int(o) + 2:
							model.islanded_operation.add(expr = model.Ppcc_a_out[i, t, o, s] == 0)
							model.islanded_operation.add(expr = model.Ppcc_b_out[i, t, o, s] == 0)
							model.islanded_operation.add(expr = model.Ppcc_c_out[i, t, o, s] == 0)
							model.islanded_operation.add(expr = model.Qpcc_a_out[i, t, o, s] == 0)
							model.islanded_operation.add(expr = model.Qpcc_b_out[i, t, o, s] == 0)
							model.islanded_operation.add(expr = model.Qpcc_c_out[i, t, o, s] == 0) 

		#------------- Operation with outage -------------------------------------------
		# Active losses ----------------------------------------------------------------
		def active_losses_a_rule_out(model, i, j, t, o, s):
			return(
				(1 / (data.Va_0_out[i, t, o, s] * data.Va_0_out[i, t, o, s])) * 
				(data.Raa_p[i, j] * model.Pa_sqr_out[i, j, t, o, s] + 
				 data.Raa_p[i, j] * model.Qa_sqr_out[i, j, t, o, s] - 
				 data.Xaa_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] + 
				 data.Xaa_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s]) +
				(1 / (data.Va_0_out[i, t, o, s] * data.Vb_0_out[i, t, o, s])) * 
				(data.Rab_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
				 data.Rab_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
				 data.Xab_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] + 
				 data.Xab_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s]) +
				(1 / (data.Va_0_out[i, t, o, s] * data.Vc_0_out[i, t, o, s])) * 
				(data.Rac_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
				 data.Rac_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
				 data.Xac_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] + 
				 data.Xac_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s]) == model.Plss_a_out[i, j, t, o, s])
		model.active_losses_a_out = Constraint(self.List_LTOS, rule=active_losses_a_rule_out)

		def active_losses_b_rule_out(model, i, j, t, o, s):
			return (
				(1 / (data.Vb_0_out[i, t, o, s] * data.Va_0_out[i, t, o, s])) * 
				(data.Rba_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Rba_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
				 data.Xba_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] + 
				 data.Xba_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s]) +
				(1 / (data.Vb_0_out[i, t, o, s] * data.Vb_0_out[i, t, o, s])) * 
				(data.Rbb_p[i, j] * model.Pb_sqr_out[i, j, t, o, s]  + 
				 data.Rbb_p[i, j] * model.Qb_sqr_out[i, j, t, o, s]  - 
				 data.Xbb_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] + 
				 data.Xbb_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s]) +
				(1 / (data.Vb_0_out[i, t, o, s] * data.Vc_0_out[i, t, o, s])) * 
				(data.Rbc_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Rbc_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
				 data.Xbc_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] + 
				 data.Xbc_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s]) == model.Plss_b_out[i, j, t, o, s])
		model.active_losses_b_out = Constraint(self.List_LTOS, rule=active_losses_b_rule_out)

		def active_losses_c_rule_out(model, i, j, t, o, s):
			return (
				(1 / (data.Vc_0_out[i, t, o, s] * data.Va_0_out[i, t, o, s])) * 
				(data.Rca_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Rca_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
				 data.Xca_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] + 
				 data.Xca_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s]) +
				(1 / (data.Vc_0_out[i, t, o, s] * data.Vb_0_out[i, t, o, s])) * 
				(data.Rcb_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Rcb_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
				 data.Xcb_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] + 
				 data.Xcb_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s]) +
				(1 / (data.Vc_0_out[i, t, o, s] * data.Vc_0_out[i, t, o, s])) * 
				(data.Rcc_p[i, j] * model.Pc_sqr_out[i, j, t, o, s]  + 
				 data.Rcc_p[i, j] * model.Qc_sqr_out[i, j, t, o, s]  - 
				 data.Xcc_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] + 
				 data.Xcc_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s]) == model.Plss_c_out[i, j, t, o, s])
		model.active_losses_c_out = Constraint(self.List_LTOS, rule=active_losses_c_rule_out)

		# Reactive losses ----------------------------------------------------------------
		def reactive_losses_a_rule_out(model, i, j, t, o, s):
			return (
				(1 / (data.Va_0_out[i, t, o, s] * data.Va_0_out[i, t, o, s])) * 
				(data.Raa_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
				 data.Raa_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
				 data.Xaa_p[i, j] * model.Pa_sqr_out[i, j, t, o, s]  + 
				 data.Xaa_p[i, j] * model.Qa_sqr_out[i, j, t, o, s] ) +
				(1 / (data.Va_0_out[i, t, o, s] * data.Vb_0_out[i, t, o, s])) * 
		        (data.Rab_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
		         data.Rab_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
		         data.Xab_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
		         data.Xab_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s]) +
		        (1 / (data.Va_0_out[i, t, o, s] * data.Vc_0_out[i, t, o, s])) * 
		        (data.Rac_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
		         data.Rac_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
		         data.Xac_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
		         data.Xac_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s]) == model.Qlss_a_out[i, j, t, o, s])
		model.reactive_losses_a_out = Constraint(self.List_LTOS, rule=reactive_losses_a_rule_out)

		def reactive_losses_b_rule_out(model, i, j, t, o, s):
			return (
				(1 / (data.Vb_0_out[i, t, o, s] * data.Va_0_out[i, t, o, s])) * 
				(data.Rba_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
				 data.Rba_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Xba_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Xba_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s]) +
				(1 / (data.Vb_0_out[i, t, o, s] * data.Vb_0_out[i, t, o, s])) * 
				(data.Rbb_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
				 data.Rbb_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Xbb_p[i, j] * model.Pb_sqr_out[i, j, t, o, s]  + 
				 data.Xbb_p[i, j] * model.Qb_sqr_out[i, j, t, o, s] ) +
				(1 / (data.Vb_0_out[i, t, o, s] * data.Vc_0_out[i, t, o, s])) * 
				(data.Rbc_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
				 data.Rbc_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Xbc_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
				 data.Xbc_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s]) == model.Qlss_b_out[i, j, t, o, s])
		model.reactive_losses_b_out = Constraint(self.List_LTOS, rule= reactive_losses_b_rule_out)

		def reactive_losses_c_rule_out(model, i, j, t, o, s):
			return (
				(1 / (data.Vc_0_out[i, t, o, s] * data.Va_0_out[i, t, o, s])) * 
				(data.Rca_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
				 data.Rca_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Xca_p[i, j] * data.Pa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Xca_p[i, j] * data.Qa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s]) +
				(1 / (data.Vc_0_out[i, t, o, s] * data.Vb_0_out[i, t, o, s])) * 
				(data.Rcb_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
				 data.Rcb_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Xcb_p[i, j] * data.Pb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Xcb_p[i, j] * data.Qb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s]) +
				(1 / (data.Vc_0_out[i, t, o, s] * data.Vc_0_out[i, t, o, s])) * 
				(data.Rcc_p[i, j] * data.Pc_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
				 data.Rcc_p[i, j] * data.Qc_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
				 data.Xcc_p[i, j] * model.Pc_sqr_out[i, j, t, o, s]  + 
				 data.Xcc_p[i, j] * model.Qc_sqr_out[i, j, t, o, s] ) == model.Qlss_c_out[i, j, t, o, s])
		model.reactive_losses_c_out = Constraint(self.List_LTOS, rule= reactive_losses_c_rule_out)

		# Active Power Flow ----------------------------------------------------------------
		def active_power_balance_rule_out_a(model, i, t, o, s):
			return (
				sum(model.Pa_out[a, j, t, o, s]*data.df[(i,a,j)] for (a,j) in data.L) -  
				sum(model.Plss_a_out[a, j, t, o, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Ppcc_a_out[i, t, o, s] +
				sum(model.PGa_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				sum(model.PB_dis_a[a, t] for a in data.dict_nos_bs[i]) -
				sum(model.PB_ch_a[a, t] for a in data.dict_nos_bs[i]) -
				((- data.PDa[(i,t)]*data.sd[s]) + (data.PVa[(i,t)]*data.spv[s])) * model.xd[i, t, o, s] == 0)
		model.active_power_balance_a_out = Constraint(self.List_NTOS, rule=active_power_balance_rule_out_a)

		def active_power_balance_rule_out_b(model, i, t, o, s):
			return (
				sum(model.Pb_out[a, j, t, o, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Plss_b_out[a, j, t, o, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Ppcc_b_out[i, t, o, s] +
				sum(model.PGb_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				sum(model.PB_dis_b[a, t] for a in data.dict_nos_bs[i]) -
				sum(model.PB_ch_b[a, t] for a in data.dict_nos_bs[i]) -
				((- data.PDb[(i,t)]*data.sd[s]) + (data.PVb[(i,t)]*data.spv[s])) * model.xd[i, t, o, s] == 0)
		model.active_power_balance_b_out = Constraint(self.List_NTOS, rule=active_power_balance_rule_out_b)

		def active_power_balance_rule_out_c(model, i, t, o, s):
			return (
				sum(model.Pc_out[a, j, t, o, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Plss_c_out[a, j, t, o, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Ppcc_c_out[i, t, o, s] +
				sum(model.PGc_out[a, t, o, s] for a in data.dict_nos_gd[i]) +
				sum(model.PB_dis_c[a, t] for a in data.dict_nos_bs[i]) -
				sum(model.PB_ch_c[a, t] for a in data.dict_nos_bs[i]) -
				((- data.PDc[(i,t)]*data.sd[s]) + (data.PVc[(i,t)]*data.spv[s])) * model.xd[i, t, o, s] == 0)
		model.active_power_balance_c_out = Constraint(self.List_NTOS, rule=active_power_balance_rule_out_c) 

		# Reactive Power Flow ----------------------------------------------------------------
		def reactive_power_balance_out_rule_out_a(model, i, t, o, s):
			return (
				sum(model.Qa_out[a, j, t, o, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Qlss_a_out[a, j, t, o, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Qpcc_a_out[i, t, o, s] +
				sum(model.QGa_out[a, t, o, s] for a in data.dict_nos_gd[i]) -
				(data.QDa[(i,t)]*data.sd[s]) * model.xd[i, t, o, s] == 0)
		model.reactive_power_balance_out_a = Constraint(self.List_NTOS, rule=reactive_power_balance_out_rule_out_a)

		def reactive_power_balance_out_rule_out_b(model, i, t, o, s):
			return (
				sum(model.Qb_out[a, j, t, o, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Qlss_b_out[a, j, t, o, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Qpcc_b_out[i, t, o, s] +
				sum(model.QGb_out[a, t, o, s] for a in data.dict_nos_gd[i]) -
				(data.QDb[(i,t)]*data.sd[s]) * model.xd[i, t, o, s] == 0)
		model.reactive_power_balance_out_b = Constraint(self.List_NTOS, rule=reactive_power_balance_out_rule_out_b)

		def reactive_power_balance_out_rule_out_c(model, i, t, o, s):
			return (
				sum(model.Qc_out[a, j, t, o, s]*data.df[(i,a,j)] for (a,j) in data.L) -
				sum(model.Qlss_c_out[a, j, t, o, s]*data.p[(i,a,j)] for (a,j) in data.L) +
				model.Qpcc_c_out[i, t, o, s] +
				sum(model.QGc_out[a, t, o, s] for a in data.dict_nos_gd[i]) -
		        (data.QDc[(i,t)]*data.sd[s]) * model.xd[i, t, o, s] == 0)
		model.reactive_power_balance_out_c = Constraint(self.List_NTOS, rule=reactive_power_balance_out_rule_out_c)

		# Voltage Droop in the Lines ----------------------------------------------------------------
		def voltage_droop_out_rule_out_a(model, i, j, t, o, s):
			return((2*(data.Raa_p[i,j]*model.Pa_out[i, j, t, o, s] + data.Xaa_p[i,j]*model.Qa_out[i, j, t, o, s])) + 
				(2*(data.Rab_p[i,j]*model.Pb_out[i, j, t, o, s] + data.Xab_p[i,j]*model.Qb_out[i, j, t, o, s])) + 
				(2*(data.Rac_p[i,j]*model.Pc_out[i, j, t, o, s] + data.Xac_p[i,j]*model.Qc_out[i, j, t, o, s])) -
				(1/data.Va_0_out[i, t, o, s]**2) * ((data.Raa_p[i,j]**2 + data.Xaa_p[i,j]**2) * (model.Pa_sqr_out[i, j, t, o, s] + 
				model.Qa_sqr_out[i, j, t, o, s])) == model.data.Va_sqr_out[i, t, o, s] - model.data.Va_sqr_out[j, t, o, s])
		model.voltage_droop_out_a = Constraint(self.List_LTOS, rule= voltage_droop_out_rule_out_a)
		
		def voltage_droop_out_rule_out_b(model, i, j, t, o, s):
			return((2*(data.Rba_p[i,j]*model.Pa_out[i, j, t, o, s] + data.Xba_p[i,j]*model.Qa_out[i, j, t, o, s])) + 
				(2*(data.Rbb_p[i,j]*model.Pb_out[i, j, t, o, s] + data.Xbb_p[i,j]*model.Qb_out[i, j, t, o, s])) + 
				(2*(data.Rbc_p[i,j]*model.Pc_out[i, j, t, o, s] + data.Xbc_p[i,j]*model.Qc_out[i, j, t, o, s])) -
				(1/data.Vb_0_out[i, t, o, s]**2) * ((data.Rbb_p[i,j]**2 + data.Xbb_p[i,j]**2) * (model.Pb_sqr_out[i, j, t, o, s] + 
				model.Qb_sqr_out[i, j, t, o, s])) == model.data.Vb_sqr_out[i, t, o, s] - model.data.Vb_sqr_out[j, t, o, s])
		model.voltage_droop_out_b = Constraint(self.List_LTOS, rule= voltage_droop_out_rule_out_b)
		
		def voltage_droop_out_rule_out_c(model, i, j, t, o, s):
			return((2*(data.Rca_p[i,j]*model.Pa_out[i, j, t, o, s] + data.Xca_p[i,j]*model.Qa_out[i, j, t, o, s])) + 
				(2*(data.Rcb_p[i,j]*model.Pb_out[i, j, t, o, s] + data.Xcb_p[i,j]*model.Qb_out[i, j, t, o, s])) + 
				(2*(data.Rcc_p[i,j]*model.Pc_out[i, j, t, o, s] + data.Xcc_p[i,j]*model.Qc_out[i, j, t, o, s])) -
				(1/data.Vc_0_out[i, t, o, s]**2) * ((data.Rcc_p[i,j]**2 + data.Xcc_p[i,j]**2) * (model.Pc_sqr_out[i, j, t, o, s] + 
				model.Qc_sqr_out[i, j, t, o, s])) == model.data.Vc_sqr_out[i, t, o, s] - model.data.Vc_sqr_out[j, t, o, s])
		model.voltage_droop_out_c = Constraint(self.List_LTOS, rule= voltage_droop_out_rule_out_c)

		# Limite máximo de fluxo de corrente e equações de linearização ----------------------------------------------------------------
		def current_limits_rule_out_a(model, i, j, t, o, s):
			return((model.Pa_sqr_out[i, j, t, o, s] + model.Qa_sqr_out[i, j, t, o, s]) <= data.Imax[i,j]**2 * (model.Va_sqr_out[i, t, o, s]))
		model.current_limits_a_out = Constraint(self.List_LTOS, rule = current_limits_rule_out_a)

		def current_limits_rule_out_b(model, i, j, t, o, s):
			return((model.Pb_sqr_out[i, j, t, o, s] + model.Qb_sqr_out[i, j, t, o, s]) <= data.Imax[i,j]**2 * (model.Vb_sqr_out[i, t, o, s]))
		model.current_limits_b_out = Constraint(self.List_LTOS, rule = current_limits_rule_out_b)

		def current_limits_rule_out_c(model, i, j, t, o, s):
			return((model.Pc_sqr_out[i, j, t, o, s] + model.Qc_sqr_out[i, j, t, o, s]) <= data.Imax[i,j]**2 * (model.Vc_sqr_out[i, t, o, s]))
		model.current_limits_c_out = Constraint(self.List_LTOS, rule = current_limits_rule_out_c)

		# Active power linearization constraints
		def pa_calculation_rule_out(model, i, j, t, o, s):
			return( model.Pa_sqr_out[i, j, t, o, s] - sum(data.S_ms[i,j,y] * model.Pa_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.Pa_calculation_out = Constraint(self.List_LTOS, rule = pa_calculation_rule_out)

		def pb_calculation_rule_out(model, i, j, t, o, s):
			return( model.Pb_sqr_out[i, j, t, o, s] - sum(data.S_ms[i,j,y] * model.Pb_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.Pb_calculation_out = Constraint(self.List_LTOS, rule = pb_calculation_rule_out)

		def pc_calculation_rule_out(model, i, j, t, o, s):
			return( model.Pc_sqr_out[i, j, t, o, s] - sum(data.S_ms[i,j,y] * model.Pc_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.Pc_calculation_out = Constraint(self.List_LTOS, rule = pc_calculation_rule_out)

		# Reactive power linearization constraints
		def qa_calculation_rule_out(model, i, j, t, o, s):
			return( model.Qa_sqr_out[i, j, t, o, s] - sum(data.S_ms[i,j,y] * model.Qa_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.Qa_calculation_out = Constraint(self.List_LTOS, rule = qa_calculation_rule_out)

		def qb_calculation_rule_out(model, i, j, t, o, s):
			return( model.Qb_sqr_out[i, j, t, o, s] - sum(data.S_ms[i,j,y] * model.Qb_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.Qb_calculation_out = Constraint(self.List_LTOS, rule = qb_calculation_rule_out)

		def qc_calculation_rule_out(model, i, j, t, o, s):
			return( model.Qc_sqr_out[i, j, t, o, s] - sum(data.S_ms[i,j,y] * model.Qc_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.Qc_calculation_out = Constraint(self.List_LTOS, rule = qc_calculation_rule_out)

		# Linearizations variables
		def pa_p_rule_out(model, i, j, t,o, s):
			return( model.Pa_p_out[i, j, t, o, s] - model.Pa_n_out[i, j, t, o, s] - model.Pa_out[i, j, t, o, s] == 0)
		model.Pa_p_constraint_out = Constraint(self.List_LTOS, rule = pa_p_rule_out)

		def pb_p_rule_out(model, i, j, t,o, s):
			return( model.Pb_p_out[i, j, t, o, s] - model.Pb_n_out[i, j, t, o, s] - model.Pb_out[i, j, t, o, s] == 0)
		model.Pb_p_constraint_out = Constraint(self.List_LTOS, rule = pb_p_rule_out)

		def pc_p_rule_out(model, i, j, t,o, s):
			return( model.Pc_p_out[i, j, t, o, s] - model.Pc_n_out[i, j, t, o, s] - model.Pc_out[i, j, t, o, s] == 0)
		model.Pc_p_constraint_out = Constraint(self.List_LTOS, rule = pc_p_rule_out)

		def qa_p_rule_out(model, i, j, t,o, s):
			return( model.Qa_p_out[i, j, t, o, s] - model.Qa_n_out[i, j, t, o, s] - model.Qa_out[i, j, t, o, s] == 0)
		model.Qa_p_constraint_out = Constraint(self.List_LTOS, rule = qa_p_rule_out)

		def qb_p_rule_out(model, i, j, t,o, s):
			return( model.Qb_p_out[i, j, t, o, s] - model.Qb_n_out[i, j, t, o, s] - model.Qb_out[i, j, t, o, s] == 0)
		model.Qb_p_constraint_out = Constraint(self.List_LTOS, rule = qb_p_rule_out)

		def qc_p_rule_out(model, i, j, t,o, s):
			return( model.Qc_p_out[i, j, t, o, s] - model.Qc_n_out[i, j, t, o, s] - model.Qc_out[i, j, t, o, s] == 0)
		model.Qc_p_constraint_out = Constraint(self.List_LTOS, rule = qc_p_rule_out)

		def pa_abs_rule_out(model, i, j, t,o, s):
			return( model.Pa_p_out[i, j, t, o, s] + model.Pa_n_out[i, j, t, o, s] - sum(model.Pa_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.pa_abs_out = Constraint(self.List_LTOS, rule = pa_abs_rule_out)

		def pb_abs_rule_out(model, i, j, t,o, s):
			return( model.Pb_p_out[i, j, t, o, s] + model.Pb_n_out[i, j, t, o, s] - sum(model.Pb_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.pb_abs_out = Constraint(self.List_LTOS, rule = pb_abs_rule_out)

		def pc_abs_rule_out(model, i, j, t,o, s):
			return( model.Pc_p_out[i, j, t, o, s] + model.Pc_n_out[i, j, t, o, s] - sum(model.Pc_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.pc_abs_out = Constraint(self.List_LTOS, rule = pc_abs_rule_out)

		def qa_abs_rule_out(model, i, j, t,o, s):
			return( model.Qa_p_out[i, j, t, o, s] + model.Qa_n_out[i, j, t, o, s] - sum(model.Qa_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.qa_abs_out = Constraint(self.List_LTOS, rule = qa_abs_rule_out)

		def qb_abs_rule_out(model, i, j, t,o, s):
			return( model.Qb_p_out[i, j, t, o, s] + model.Qb_n_out[i, j, t, o, s] - sum(model.Qb_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.qb_abs_out = Constraint(self.List_LTOS, rule = qb_abs_rule_out)

		def qc_abs_rule_out(model, i, j, t,o, s):
			return( model.Qc_p_out[i, j, t, o, s] + model.Qc_n_out[i, j, t, o, s] - sum(model.Qc_Dp_out[i, j, t, o, s, y] for y in data.Y) == 0)
		model.qc_abs_out = Constraint(self.List_LTOS, rule = qc_abs_rule_out)

		def pa_limits_rule_out(model, i, j, t, o, s, y):
			return( model.Pa_Dp_out[i, j, t, o, s, y] <= data.S_Dp_max[i,j])
		model.pa_limits_out = Constraint(self.List_LTOSY, rule = pa_limits_rule_out)

		def pb_limits_rule_out(model, i, j, t, o, s, y):
			return( model.Pb_Dp_out[i, j, t, o, s, y] <= data.S_Dp_max[i,j])
		model.pb_limits_out = Constraint(self.List_LTOSY, rule = pb_limits_rule_out)

		def pc_limits_rule_out(model, i, j, t, o, s, y):
			return( model.Pc_Dp_out[i, j, t, o, s, y] <= data.S_Dp_max[i,j])
		model.pc_limits_out = Constraint(self.List_LTOSY, rule = pc_limits_rule_out)

		def qa_limits_rule_out(model, i, j, t, o, s, y):
			return( model.Qa_Dp_out[i, j, t, o, s, y] <= data.S_Dp_max[i,j])
		model.qa_limits_out = Constraint(self.List_LTOSY, rule = qa_limits_rule_out)

		def qb_limits_rule_out(model, i, j, t, o, s, y):
			return( model.Qb_Dp_out[i, j, t, o, s, y] <= data.S_Dp_max[i,j])
		model.qb_limits_out = Constraint(self.List_LTOSY, rule = qb_limits_rule_out)

		def qc_limits_rule_out(model, i, j, t, o, s, y):
			return( model.Qc_Dp_out[i, j, t, o, s, y] <= data.S_Dp_max[i,j])
		model.qc_limits_out = Constraint(self.List_LTOSY, rule = qc_limits_rule_out)

		# Limete potência aparente fornecida pelo PCC ----------------------------------------------------------------
		def ative_power_pcc_rule_out(model, i, t, o, s):
			return(model.Ppcc_out[i, t, o, s] - model.Ppcc_a_out[i, t, o, s] - model.Ppcc_b_out[i, t, o, s] - model.Ppcc_c_out[i, t, o, s] == 0)
		model.active_power_pcc_out = Constraint(self.List_NTOS, rule = ative_power_pcc_rule_out)

		def reative_power_pcc_rule_out(model, i, t, o, s):
			return(model.Qpcc_out[i, t, o, s] - model.Qpcc_a_out[i, t, o, s] - model.Qpcc_b_out[i, t, o, s] - model.Qpcc_c_out[i, t, o, s] == 0)
		model.reactive_power_pcc_out = Constraint(self.List_NTOS, rule = reative_power_pcc_rule_out)

		def apparent_power_pcc_rule_out(model, i, t, o, s):
			return(model.Ppcc_sqr_out[i, t, o, s] + model.Qpcc_sqr_out[i, t, o, s] <= data.Smax[i]**2)
		model.apparent_power_pcc_out = Constraint(self.List_NTOS, rule = apparent_power_pcc_rule_out)

		def ppcc_calculation_rule_out(model, i, t, o, s):
			return( model.Ppcc_sqr_out[i, t, o, s] - sum(data.Spcc_ms[i,y] * model.Ppcc_Dp_out[i, t, o, s, y] for y in data.Y) == 0)
		model.Ppcc_calculation_out = Constraint(self.List_NTOS, rule = ppcc_calculation_rule_out)

		def Qpcc_calculation_rule_out(model, i, t, o, s):
			return( model.Qpcc_sqr_out[i, t, o, s] - sum(data.Spcc_ms[i,y] * model.Qpcc_Dp_out[i, t, o, s, y] for y in data.Y) == 0)
		model.Qpcc_calculation_out = Constraint(self.List_NTOS, rule = Qpcc_calculation_rule_out)

		def ppcc_p_rule_out(model, i, t, o, s):
			return( model.Ppcc_p_out[i, t, o, s] - model.Ppcc_n_out[i, t, o, s] - model.Ppcc_out[i, t, o, s] == 0)
		model.Ppcc_p_constraint_out = Constraint(self.List_NTOS, rule = ppcc_p_rule_out)

		def qpcc_p_rule_out(model, i, t, o, s):
			return( model.Qpcc_p_out[i, t, o, s] - model.Qpcc_n_out[i, t, o, s] - model.Qpcc_out[i, t, o, s] == 0)
		model.Qpcc_p_constraint_out = Constraint(self.List_NTOS, rule = qpcc_p_rule_out)

		def ppcc_abs_rule_out(model, i, t, o, s):
			return( model.Ppcc_p_out[i, t, o, s] + model.Ppcc_n_out[i, t, o, s] - sum(model.Ppcc_Dp_out[i, t, o, s, y] for y in data.Y) == 0)
		model.ppcc_abs_out = Constraint(self.List_NTOS, rule=ppcc_abs_rule_out)

		def qpcc_abs_rule_out(model, i, t, o, s):
			return( model.Qpcc_p_out[i, t, o, s] + model.Qpcc_n_out[i, t, o, s] - sum(model.Qpcc_Dp_out[i, t, o, s, y] for y in data.Y) == 0)
		model.qpcc_abs_out = Constraint(self.List_NTOS, rule=qpcc_abs_rule_out)

		def ppcc_limits_rule_out(model, i, t, o, s, y):
			return( model.Ppcc_Dp_out[i, t, o, s, y] <= data.Spcc_Dp_max[i])
		model.ppcc_limits_out = Constraint(self.List_NTOSY, rule=ppcc_limits_rule_out)

		def qpcc_limits_rule_out(model, i, t, o, s, y):
			return( model.Qpcc_Dp_out[i, t, o, s, y] <= data.Spcc_Dp_max[i])
		model.qpcc_limits_out = Constraint(self.List_NTOSY, rule=qpcc_limits_rule_out)

		# Genset --------------------------------------------------------------------
		def genset_power_rule_out(model, i, t, o, s):
			return(model.PGa_out[i, t, o, s] + model.PGb_out[i, t, o, s] + model.PGc_out[i, t, o, s] == model.PG_out[i, t, o, s])
		model.genset_power_active_out = Constraint(self.List_GDTOS, rule = genset_power_rule_out)

		def genset_power_reactive_rule_out(model, i, t, o, s):
			return(model.QGa_out[i, t, o, s] + model.QGb_out[i, t, o, s] + model.QGc_out[i, t, o, s] == model.QG_out[i, t, o, s])
		model.genset_power_reactive_out = Constraint(self.List_GDTOS, rule = genset_power_reactive_rule_out)

		def genset_power_active_limits_rule_out_1(model, i, t, o, s):
			return(model.PG_out[i, t, o, s] >= data.PG_min[i] * model.oG_out[i, t, o, s])
		model.genset_power_active_limits_1_out = Constraint(self.List_GDTOS, rule = genset_power_active_limits_rule_out_1)

		def genset_power_active_limits_rule_out_2(model, i, t, o, s):
			return(model.PG_out[i, t, o, s] <= data.PG_max[i] * model.oG_out[i, t, o, s])
		model.genset_power_active_limits_2_out = Constraint(self.List_GDTOS, rule = genset_power_active_limits_rule_out_2)

		def genset_power_reactive_limits_rule_out_1(model, i, t, o, s):
			return(model.QG_out[i, t, o, s] >= data.QG_min[i] * model.oG_out[i, t, o, s])
		model.genset_power_reactive_limits_1_out = Constraint(self.List_GDTOS, rule = genset_power_reactive_limits_rule_out_1)

		def genset_power_reactive_limits_rule_out_2(model, i, t, o, s):
			return(model.QG_out[i, t, o, s] <= data.QG_max[i] * model.oG_out[i, t, o, s])
		model.genset_power_reactive_limits_2_out = Constraint(self.List_GDTOS, rule = genset_power_reactive_limits_rule_out_2)
		
		for i in data.GD:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if int(t) < int(o) or int(t) >= int(o) + 2:
							model.genset_operation_grid_connected.add(expr = model.PGa_out[i, t, o, s] == 0)
							model.genset_operation_grid_connected.add(expr = model.PGb_out[i, t, o, s] == 0)
							model.genset_operation_grid_connected.add(expr = model.PGc_out[i, t, o, s] == 0)
							model.genset_operation_grid_connected.add(expr = model.QGa_out[i, t, o, s] == 0)
							model.genset_operation_grid_connected.add(expr = model.QGb_out[i, t, o, s] == 0)
							model.genset_operation_grid_connected.add(expr = model.QGc_out[i, t, o, s] == 0)

		# Battery --------------------------------------------------------------------
		def energy_bess_rule(model,i,t):
			if int(t) == 1:
				return model.EB[i,t] - data.EBi[i] - model.PB[i,t]*data.delta_t == 0
			else:
				return model.EB[i,t] - model.EB[i,str(int(t)-1)] - model.PB[i,t]*data.delta_t == 0
		model.energy_soc_bess = Constraint(self.List_BT, rule=energy_bess_rule)

		def power_bess_rule(model,i,t):
			return(model.PB[i,t] - model.PB_ch[i,t]*data.eta_b[i] + model.PB_dis[i,t]*(1/data.eta_b[i]) == 0)
		model.power_bess = Constraint(self.List_BT, rule=power_bess_rule)

		def operation_mode_bess_rule(model,i,t):
			return(model.b_ch[i,t] + model.b_dis[i,t] <= 1)
		model.operation_mode_bess = Constraint(self.List_BT, rule = operation_mode_bess_rule)

		def power_ch_total_rule(model, i, t):
			return(model.PB_ch[i,t] - model.PB_ch_a[i,t] - model.PB_ch_b[i,t] - model.PB_ch_c[i,t] == 0)
		model.power_ch_total_bess = Constraint(self.List_BT, rule= power_ch_total_rule)

		def power_balance_charging_1_rule(model,i,t):
			return(model.PB_ch_a[i,t] == model.PB_ch_b[i,t])
		model.power_balance_charging_1_bess = Constraint(self.List_BT, rule=power_balance_charging_1_rule)

		def power_balance_charging_2_rule(model,i,t):
			return(model.PB_ch_a[i,t] == model.PB_ch_c[i,t])
		model.power_balance_charging_2_bess = Constraint(self.List_BT, rule=power_balance_charging_2_rule)

		def power_balance_charging_3_rule(model,i,t):
			return(model.PB_ch_b[i,t] == model.PB_ch_c[i,t])
		model.power_balance_charging_3_bess = Constraint(self.List_BT, rule=power_balance_charging_3_rule)

		def power_dis_total_rule(model,i,t):
			return(model.PB_dis[i,t] - model.PB_dis_a[i,t] - model.PB_dis_b[i,t] - model.PB_dis_c[i,t] == 0)
		model.power_dis_total_bess = Constraint(self.List_BT, rule = power_dis_total_rule)

		def power_balance_discharging_1_rule(model,i,t):
			return(model.PB_dis_a[i,t] == model.PB_dis_b[i,t])
		model.power_balance_discharging_1_bess = Constraint(self.List_BT, rule=power_balance_discharging_1_rule)

		def power_balance_discharging_2_rule(model,i,t):
			return(model.PB_dis_a[i,t] == model.PB_dis_c[i,t])
		model.power_balance_discharging_2_bess = Constraint(self.List_BT, rule=power_balance_discharging_2_rule)

		def power_balance_discharging_3_rule(model,i,t):
			return(model.PB_dis_b[i,t] == model.PB_dis_c[i,t])
		model.power_balance_discharging_3_bess = Constraint(self.List_BT, rule=power_balance_discharging_3_rule)

		def power_charge_limits_rule_1(model,i,t):
			return(model.PB_ch[i,t] >= 0)
		model.power_charge_limits_1 = Constraint(self.List_BT, rule=power_charge_limits_rule_1)

		def power_charge_limits_rule_2(model,i,t):
			return(model.PB_ch[i,t] <= data.PBmax[i] * model.b_ch[i,t])
		model.power_charge_limits_2 = Constraint(self.List_BT, rule=power_charge_limits_rule_2)

		def power_discharge_limits_rule_1(model,i,t):
			return(model.PB_dis[i,t] >= 0)
		model.power_discharge_limits_1 = Constraint(self.List_BT, rule=power_discharge_limits_rule_1)

		def power_discharge_limits_rule_2(model,i,t):
			return(model.PB_dis[i,t] <= data.PBmax[i] * model.b_dis[i,t])
		model.power_discharge_limits_2 = Constraint(self.List_BT, rule = power_discharge_limits_rule_2)

		def energy_bess_limits_rule_1(model,i,t):
			return(model.EB[i,t] >= data.EBmin[i])
		model.energy_bess_limits_1 = Constraint(self.List_BT, rule = energy_bess_limits_rule_1)

		def energy_bess_limits_rule_2(model,i,t):
			return(model.EB[i,t] <= data.EBmax[i])
		model.energy_bess_limits_2 = Constraint(self.List_BT, rule = energy_bess_limits_rule_2)

		#----------------- FIX Variables --------------------------------------------------
		model.fix_active_power = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for s in data.S:
					if data.Tb[i] == 1:
						model.fix_active_power.add(expr=model.Va[i, t, s] == data.Vnom)
						model.fix_active_power.add(expr=model.Va_sqr[i, t, s] == data.Vnom**2)
						model.fix_active_power.add(expr=model.Vb[i, t, s] == data.Vnom)
						model.fix_active_power.add(expr=model.Vb_sqr[i, t, s] == data.Vnom**2)
						model.fix_active_power.add(expr=model.Vc[i, t, s] == data.Vnom)
						model.fix_active_power.add(expr=model.Vc_sqr[i, t, s] == data.Vnom**2)
					else:
						model.fix_active_power.add(expr=model.Ppcc_a[i, t, s] == 0)
						model.fix_active_power.add(expr=model.Ppcc_b[i, t, s] == 0)
						model.fix_active_power.add(expr=model.Ppcc_c[i, t, s] == 0)
						model.fix_active_power.add(expr=model.Qpcc_a[i, t, s] == 0)
						model.fix_active_power.add(expr=model.Qpcc_b[i, t, s] == 0)
						model.fix_active_power.add(expr=model.Qpcc_c[i, t, s] == 0)

		model.fix_voltage_out_1 = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if data.Tb[i] == 1 and (int(t) < int(o) or int(t) >= int(o) + 2):
							model.fix_voltage_out_1.add(expr=model.Va_out[i, t, o, s] == data.Vnom)
							model.fix_voltage_out_1.add(expr=model.Vb_out[i, t, o, s] == data.Vnom)
							model.fix_voltage_out_1.add(expr=model.Vc_out[i, t, o, s] == data.Vnom)
							model.fix_voltage_out_1.add(expr=model.Va_sqr_out[i, t, o, s] == data.Vnom**2)
							model.fix_voltage_out_1.add(expr=model.Vb_sqr_out[i, t, o, s] == data.Vnom**2)
							model.fix_voltage_out_1.add(expr=model.Vc_sqr_out[i, t, o, s] == data.Vnom**2)

		model.fix_voltage_out_2 = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if data.Tb[i] == 2 and int(t) >= int(o) and int(t) < int(o) + 2:  
							model.fix_voltage_out_2.add(expr = model.Va_out[i, t, o, s] == data.Vnom)
							model.fix_voltage_out_2.add(expr = model.Vb_out[i, t, o, s] == data.Vnom)
							model.fix_voltage_out_2.add(expr = model.Vc_out[i, t, o, s] == data.Vnom)
							model.fix_voltage_out_2.add(expr = model.Va_sqr_out[i, t, o, s] == data.Vnom**2)
							model.fix_voltage_out_2.add(expr = model.Vb_sqr_out[i, t, o, s] == data.Vnom**2)
							model.fix_voltage_out_2.add(expr = model.Vc_sqr_out[i, t, o, s] == data.Vnom**2)

		model.fix_active_power_out = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if data.Tb[i] != 1:
							model.fix_active_power_out.add(expr = model.Ppcc_a_out[i, t, o, s] == 0)
							model.fix_active_power_out.add(expr = model.Ppcc_b_out[i, t, o, s] == 0)
							model.fix_active_power_out.add(expr = model.Ppcc_c_out[i, t, o, s] == 0)

		model.fix_reactive_power_out = ConstraintList()
		for i in data.Tb:
			for t in data.T:
				for o in data.O:
					for s in data.S:
						if data.Tb[i] != 1:
							model.fix_reactive_power_out.add(expr = model.Qpcc_a_out[i, t, o, s] == 0)
							model.fix_reactive_power_out.add(expr = model.Qpcc_b_out[i, t, o, s] == 0)
							model.fix_reactive_power_out.add(expr = model.Qpcc_c_out[i, t, o, s] == 0)
		return model

	# Function to solve the model and obtain the results
	def Solving_Model(self,model):
		data = self.data

		try:
			solver = SolverFactory('cbc')
			results = solver.solve(model)
		
		except Exception as e:
			print("Error al resolver el modelo:", e)

		# Saving variables of the problem
		xd = model.xd.get_values()
		PG = model.PG.get_values()
		PG_out = model.PG_out.get_values()
		EB = model.EB.get_values()
		PB = model.PB.get_values()
		PB_ch = model.PB_ch.get_values()
		PB_dis = model.PB_dis.get_values()

		print("PB: ",PB)
