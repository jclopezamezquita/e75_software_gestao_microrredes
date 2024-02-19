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
		'''
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
		'''
		#return (self.List_NTS, self.List_NTOS, self.List_LTS, self.List_LTOS, self.List_SETS, self.List_SETOS, self.List_sPDTS, self.List_sQDTS, self.List_sPDTOS, self.List_sQDTOS, self.List_GDTS, self.List_GDTOS, self.List_sPVT, self.List_sPVTO, self.List_BT, self.List_LTSY, self.List_LTOSY, self.List_SETSY, self.List_SETOSY, self.List_GDTSY, self.List_GDTOSY)

	def ProblemFormultion_ColdStart(self):
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
		Pa_0 = model_cs.Pa.get_values()
		Pb_0 = model_cs.Pb.get_values()
		Pc_0 = model_cs.Pc.get_values()
		Qa_0 = model_cs.Qa.get_values()
		Qb_0 = model_cs.Qb.get_values()
		Qc_0 = model_cs.Qc.get_values()
		Va_0 = model_cs.Va.get_values()
		Vb_0 = model_cs.Vb.get_values()
		Vc_0 = model_cs.Vc.get_values()

		Pa_0_out = model_cs.Pa_out.get_values()
		Pb_0_out = model_cs.Pb_out.get_values()
		Pc_0_out = model_cs.Pc_out.get_values()
		Qa_0_out = model_cs.Qa_out.get_values()
		Qb_0_out = model_cs.Qb_out.get_values()
		Qc_0_out = model_cs.Qc_out.get_values()
		Va_0_out = model_cs.Va_out.get_values()
		Vb_0_out = model_cs.Vb_out.get_values()
		Vc_0_out = model_cs.Vc_out.get_values()
		
	def ProblemFormulation(self):
		data = self.data

		# Type of problem
		model = ConcreteModel("Modelo_EMS_PYOMO")

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
		def current_limits_rule_a(model, i, j, t, s):
			return((model.Pa_sqr[i, j, t, s] + model.Qa_sqr[i, j, t, s]) <= data.Imax[i,j]**2 * (model.Va_sqr[i, t, s]))
		model.current_limits_a = Constraint(self.List_LTS, rule=current_limits_rule_a)

		def current_limits_rule_b(model, i, j, t, s):
			return((model.Pb_sqr[i, j, t, s] + model.Qb_sqr[i, j, t, s]) <= data.Imax[i,j]**2 * (model.Vb_sqr[i, t, s]))
		model.current_limits_b = Constraint(self.List_LTS, rule=current_limits_rule_b)

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
		def current_limits_rule_out_a(model, i, j, t, o, s):
			return((model.Pa_sqr_out[i, j, t, o, s] + model.Qa_sqr_out[i, j, t, o, s]) <= data.Imax[i,j]**2 * (model.Va_sqr_out[i, t, o, s]))
		model.current_limits_a_out = Constraint(self.List_LTOS, rule = current_limits_rule_out_a)

		def current_limits_rule_out_b(model, i, j, t, o, s):
			return((model.Pb_sqr_out[i, j, t, o, s] + model.Qb_sqr_out[i, j, t, o, s]) <= data.Imax[i,j]**2 * (model.Vb_sqr_out[i, t, o, s]))
		model.current_limits_b_out = Constraint(self.List_LTOS, rule = current_limits_rule_out_b)

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

		# Energy Storage System -----------------------------------------------------------
		for (i,t) in self.List_BT:
			if int(t) == 1:
				return model.EB[i,t] - data.EBi[i] - model.PB[i,t]*data.delta_t == 0
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
