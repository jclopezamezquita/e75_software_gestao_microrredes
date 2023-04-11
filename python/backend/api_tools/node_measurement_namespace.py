import sys
import http.client
from sqlalchemy import exc
from datetime import datetime, timedelta
# from flask_restplus import Namespace, Resource, fields, inputs, abort
from flask_restx import Namespace, Resource, fields, inputs, abort
from api_tools.models import node_measurement_model, node_information_model
from api_tools.db import db
from calendar import monthrange


def power_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    return value

power_rule.__schema__ = {
    "type": "number",
    "format": "power_rule",
}

def voltage_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

voltage_rule.__schema__ = {
    "type": "number",
    "format": "voltage_rule",
}

def soc_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

soc_rule.__schema__ = {
    "type": "number",
    "format": "soc_rule",
}


node_measurement_namespace = Namespace('v1/api/node_measurement', description='API backend EMS - Node measurement')

node_measurement_parser = node_measurement_namespace.parser()
node_measurement_parser.add_argument('time_iso',
                        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S.%f'),
                        required=True,
                        help='Datetime of the measuarement (timestamp in iso-format, p.e. 2021-07-27T14:31:00.000)')
node_measurement_parser.add_argument('active_power_a_kw', type=power_rule, required=True, help='Active power of phase a (kW).')
node_measurement_parser.add_argument('active_power_b_kw', type=power_rule, required=True, help='Active power of phase b (kW).')
node_measurement_parser.add_argument('active_power_c_kw', type=power_rule, required=True, help='Active power of phase c (kW).')
node_measurement_parser.add_argument('reactive_power_a_kvar', type=power_rule, required=True, help='Reactive power of phase a (kVar).')
node_measurement_parser.add_argument('reactive_power_b_kvar', type=power_rule, required=True, help='Reactive power of phase b (kVar).')
node_measurement_parser.add_argument('reactive_power_c_kvar', type=power_rule, required=True, help='Reactive power of phase c (kVar).')
node_measurement_parser.add_argument('voltage_a_kv', type=voltage_rule, required=True, help='Voltage of phase a (kV).')
node_measurement_parser.add_argument('voltage_b_kv', type=voltage_rule, required=True, help='Voltage of phase b (kV).')
node_measurement_parser.add_argument('voltage_c_kv', type=voltage_rule, required=True, help='Voltage of phase c (kV).')
node_measurement_parser.add_argument('soc_kwh', type=soc_rule, required=False, help='State of charge of BESS (kWh).')


model = {
    'id': fields.Integer(),
    'name': fields.String(), 
    'time_iso' : fields.DateTime(),
    'active_power_a_kw' : fields.Float(),
    'active_power_b_kw' : fields.Float(),
    'active_power_c_kw' : fields.Float(),
    'reactive_power_a_kvar' : fields.Float(),
    'reactive_power_b_kvar' : fields.Float(),
    'reactive_power_c_kvar' : fields.Float(),
    'voltage_a_kv' : fields.Float(),
    'voltage_b_kv' : fields.Float(),
    'voltage_c_kv' : fields.Float(),
    'soc_kwh' : fields.Float(),
}
measurement_model = node_measurement_namespace.model('node_measurement', model)

model_2 = {
    'pcc_t00': fields.Float(default=0.0),
    'pcc_t01': fields.Float(default=0.0),
    'pcc_t02': fields.Float(default=0.0),
    'pcc_t03': fields.Float(default=0.0),
    'pcc_t04': fields.Float(default=0.0),
    'pcc_t05': fields.Float(default=0.0),
    'pcc_t06': fields.Float(default=0.0),
    'pcc_t07': fields.Float(default=0.0),
    'pcc_t08': fields.Float(default=0.0),
    'pcc_t09': fields.Float(default=0.0),
    'pcc_t10': fields.Float(default=0.0),
    'pcc_t11': fields.Float(default=0.0),
    'pcc_t12': fields.Float(default=0.0),
    'pcc_t13': fields.Float(default=0.0),
    'pcc_t14': fields.Float(default=0.0),
    'pcc_t15': fields.Float(default=0.0),
    'pcc_t16': fields.Float(default=0.0),
    'pcc_t17': fields.Float(default=0.0),
    'pcc_t18': fields.Float(default=0.0),
    'pcc_t19': fields.Float(default=0.0),
    'pcc_t20': fields.Float(default=0.0),
    'pcc_t21': fields.Float(default=0.0),
    'pcc_t22': fields.Float(default=0.0),
    'pcc_t23': fields.Float(default=0.0),

    'pv_t00': fields.Float(default=0.0),
    'pv_t01': fields.Float(default=0.0),
    'pv_t02': fields.Float(default=0.0),
    'pv_t03': fields.Float(default=0.0),
    'pv_t04': fields.Float(default=0.0),
    'pv_t05': fields.Float(default=0.0),
    'pv_t06': fields.Float(default=0.0),
    'pv_t07': fields.Float(default=0.0),
    'pv_t08': fields.Float(default=0.0),
    'pv_t09': fields.Float(default=0.0),
    'pv_t10': fields.Float(default=0.0),
    'pv_t11': fields.Float(default=0.0),
    'pv_t12': fields.Float(default=0.0),
    'pv_t13': fields.Float(default=0.0),
    'pv_t14': fields.Float(default=0.0),
    'pv_t15': fields.Float(default=0.0),
    'pv_t16': fields.Float(default=0.0),
    'pv_t17': fields.Float(default=0.0),
    'pv_t18': fields.Float(default=0.0),
    'pv_t19': fields.Float(default=0.0),
    'pv_t20': fields.Float(default=0.0),
    'pv_t21': fields.Float(default=0.0),
    'pv_t22': fields.Float(default=0.0),
    'pv_t23': fields.Float(default=0.0),

    'genset_t00': fields.Float(default=0.0),
    'genset_t01': fields.Float(default=0.0),
    'genset_t02': fields.Float(default=0.0),
    'genset_t03': fields.Float(default=0.0),
    'genset_t04': fields.Float(default=0.0),
    'genset_t05': fields.Float(default=0.0),
    'genset_t06': fields.Float(default=0.0),
    'genset_t07': fields.Float(default=0.0),
    'genset_t08': fields.Float(default=0.0),
    'genset_t09': fields.Float(default=0.0),
    'genset_t10': fields.Float(default=0.0),
    'genset_t11': fields.Float(default=0.0),
    'genset_t12': fields.Float(default=0.0),
    'genset_t13': fields.Float(default=0.0),
    'genset_t14': fields.Float(default=0.0),
    'genset_t15': fields.Float(default=0.0),
    'genset_t16': fields.Float(default=0.0),
    'genset_t17': fields.Float(default=0.0),
    'genset_t18': fields.Float(default=0.0),
    'genset_t19': fields.Float(default=0.0),
    'genset_t20': fields.Float(default=0.0),
    'genset_t21': fields.Float(default=0.0),
    'genset_t22': fields.Float(default=0.0),
    'genset_t23': fields.Float(default=0.0),

    'bess_t00': fields.Float(default=0.0),
    'bess_t01': fields.Float(default=0.0),
    'bess_t02': fields.Float(default=0.0),
    'bess_t03': fields.Float(default=0.0),
    'bess_t04': fields.Float(default=0.0),
    'bess_t05': fields.Float(default=0.0),
    'bess_t06': fields.Float(default=0.0),
    'bess_t07': fields.Float(default=0.0),
    'bess_t08': fields.Float(default=0.0),
    'bess_t09': fields.Float(default=0.0),
    'bess_t10': fields.Float(default=0.0),
    'bess_t11': fields.Float(default=0.0),
    'bess_t12': fields.Float(default=0.0),
    'bess_t13': fields.Float(default=0.0),
    'bess_t14': fields.Float(default=0.0),
    'bess_t15': fields.Float(default=0.0),
    'bess_t16': fields.Float(default=0.0),
    'bess_t17': fields.Float(default=0.0),
    'bess_t18': fields.Float(default=0.0),
    'bess_t19': fields.Float(default=0.0),
    'bess_t20': fields.Float(default=0.0),
    'bess_t21': fields.Float(default=0.0),
    'bess_t22': fields.Float(default=0.0),
    'bess_t23': fields.Float(default=0.0),

    'bess_soc_t00': fields.Float(default=0.0),
    'bess_soc_t01': fields.Float(default=0.0),
    'bess_soc_t02': fields.Float(default=0.0),
    'bess_soc_t03': fields.Float(default=0.0),
    'bess_soc_t04': fields.Float(default=0.0),
    'bess_soc_t05': fields.Float(default=0.0),
    'bess_soc_t06': fields.Float(default=0.0),
    'bess_soc_t07': fields.Float(default=0.0),
    'bess_soc_t08': fields.Float(default=0.0),
    'bess_soc_t09': fields.Float(default=0.0),
    'bess_soc_t10': fields.Float(default=0.0),
    'bess_soc_t11': fields.Float(default=0.0),
    'bess_soc_t12': fields.Float(default=0.0),
    'bess_soc_t13': fields.Float(default=0.0),
    'bess_soc_t14': fields.Float(default=0.0),
    'bess_soc_t15': fields.Float(default=0.0),
    'bess_soc_t16': fields.Float(default=0.0),
    'bess_soc_t17': fields.Float(default=0.0),
    'bess_soc_t18': fields.Float(default=0.0),
    'bess_soc_t19': fields.Float(default=0.0),
    'bess_soc_t20': fields.Float(default=0.0),
    'bess_soc_t21': fields.Float(default=0.0),
    'bess_soc_t22': fields.Float(default=0.0),
    'bess_soc_t23': fields.Float(default=0.0)
}

measurement_model_2 = node_measurement_namespace.model('node_measurement_2', model_2)

# ENDPOINT /v1/api/node_measurement/ -> GET all measurements
@node_measurement_namespace.route('/')
class node_measurement_list(Resource):

    @node_measurement_namespace.doc('node_measurement')
    @node_measurement_namespace.marshal_with(measurement_model, as_list=True)
    def get(self):
        '''
        Retrieves all measurements
        '''

        parameters = [node_measurement_model.id, node_information_model.name, node_measurement_model.time_iso, node_measurement_model.active_power_a_kw, 
            node_measurement_model.active_power_b_kw, node_measurement_model.active_power_c_kw, node_measurement_model.reactive_power_a_kvar,
            node_measurement_model.reactive_power_b_kvar, node_measurement_model.reactive_power_c_kvar, node_measurement_model.voltage_a_kv,
            node_measurement_model.voltage_b_kv, node_measurement_model.voltage_c_kv, node_measurement_model.soc_kwh]
        
        main_query = node_measurement_model.query.join(node_information_model).with_entities(*parameters)
        measurements = (main_query.all())

        return measurements

# ENDPOINT /v1/api/node_measurement/last_24h/ -> GET last 24 hours measurements
@node_measurement_namespace.route('/last_24h/')
class node_measurement_list(Resource):

    @node_measurement_namespace.doc('last_node_measurement')
    @node_measurement_namespace.marshal_with(measurement_model_2)
    def get(self):
        '''
        Retrieves last node measurement
        '''

        parameters = [node_measurement_model.id, node_information_model.der, node_measurement_model.time_iso, node_measurement_model.active_power_a_kw, 
            node_measurement_model.active_power_b_kw, node_measurement_model.active_power_c_kw, node_measurement_model.reactive_power_a_kvar,
            node_measurement_model.reactive_power_b_kvar, node_measurement_model.reactive_power_c_kvar, node_measurement_model.voltage_a_kv,
            node_measurement_model.voltage_b_kv, node_measurement_model.voltage_c_kv, node_measurement_model.soc_kwh]
        
        main_query = node_measurement_model.query.join(node_information_model).with_entities(*parameters)
        
        data = {
            'pcc_t00': 0.0,
            'pcc_t01': 0.0,
            'pcc_t02': 0.0,
            'pcc_t03': 0.0,
            'pcc_t04': 0.0,
            'pcc_t05': 0.0,
            'pcc_t06': 0.0,
            'pcc_t07': 0.0,
            'pcc_t08': 0.0,
            'pcc_t09': 0.0,
            'pcc_t10': 0.0,
            'pcc_t11': 0.0,
            'pcc_t12': 0.0,
            'pcc_t13': 0.0,
            'pcc_t14': 0.0,
            'pcc_t15': 0.0,
            'pcc_t16': 0.0,
            'pcc_t17': 0.0,
            'pcc_t18': 0.0,
            'pcc_t19': 0.0,
            'pcc_t20': 0.0,
            'pcc_t21': 0.0,
            'pcc_t22': 0.0,
            'pcc_t23': 0.0,
            'pv_t00': 0.0,
            'pv_t01': 0.0,
            'pv_t02': 0.0,
            'pv_t03': 0.0,
            'pv_t04': 0.0,
            'pv_t05': 0.0,
            'pv_t06': 0.0,
            'pv_t07': 0.0,
            'pv_t08': 0.0,
            'pv_t09': 0.0,
            'pv_t10': 0.0,
            'pv_t11': 0.0,
            'pv_t12': 0.0,
            'pv_t13': 0.0,
            'pv_t14': 0.0,
            'pv_t15': 0.0,
            'pv_t16': 0.0,
            'pv_t17': 0.0,
            'pv_t18': 0.0,
            'pv_t19': 0.0,
            'pv_t20': 0.0,
            'pv_t21': 0.0,
            'pv_t22': 0.0,
            'pv_t23': 0.0,
            'genset_t00': 0.0,
            'genset_t01': 0.0,
            'genset_t02': 0.0,
            'genset_t03': 0.0,
            'genset_t04': 0.0,
            'genset_t05': 0.0,
            'genset_t06': 0.0,
            'genset_t07': 0.0,
            'genset_t08': 0.0,
            'genset_t09': 0.0,
            'genset_t10': 0.0,
            'genset_t11': 0.0,
            'genset_t12': 0.0,
            'genset_t13': 0.0,
            'genset_t14': 0.0,
            'genset_t15': 0.0,
            'genset_t16': 0.0,
            'genset_t17': 0.0,
            'genset_t18': 0.0,
            'genset_t19': 0.0,
            'genset_t20': 0.0,
            'genset_t21': 0.0,
            'genset_t22': 0.0,
            'genset_t23': 0.0,
            'bess_t00': 0.0,
            'bess_t01': 0.0,
            'bess_t02': 0.0,
            'bess_t03': 0.0,
            'bess_t04': 0.0,
            'bess_t05': 0.0,
            'bess_t06': 0.0,
            'bess_t07': 0.0,
            'bess_t08': 0.0,
            'bess_t09': 0.0,
            'bess_t10': 0.0,
            'bess_t11': 0.0,
            'bess_t12': 0.0,
            'bess_t13': 0.0,
            'bess_t14': 0.0,
            'bess_t15': 0.0,
            'bess_t16': 0.0,
            'bess_t17': 0.0,
            'bess_t18': 0.0,
            'bess_t19': 0.0,
            'bess_t20': 0.0,
            'bess_t21': 0.0,
            'bess_t22': 0.0,
            'bess_t23': 0.0,
            'bess_soc_t00': 0.0,
            'bess_soc_t01': 0.0,
            'bess_soc_t02': 0.0,
            'bess_soc_t03': 0.0,
            'bess_soc_t04': 0.0,
            'bess_soc_t05': 0.0,
            'bess_soc_t06': 0.0,
            'bess_soc_t07': 0.0,
            'bess_soc_t08': 0.0,
            'bess_soc_t09': 0.0,
            'bess_soc_t10': 0.0,
            'bess_soc_t11': 0.0,
            'bess_soc_t12': 0.0,
            'bess_soc_t13': 0.0,
            'bess_soc_t14': 0.0,
            'bess_soc_t15': 0.0,
            'bess_soc_t16': 0.0,
            'bess_soc_t17': 0.0,
            'bess_soc_t18': 0.0,
            'bess_soc_t19': 0.0,
            'bess_soc_t20': 0.0,
            'bess_soc_t21': 0.0,
            'bess_soc_t22': 0.0,
            'bess_soc_t23': 0.0
        }

        counters = {
            'counter_pcc_t00': 0,
            'counter_pcc_t01': 0,
            'counter_pcc_t02': 0,
            'counter_pcc_t03': 0,
            'counter_pcc_t04': 0,
            'counter_pcc_t05': 0,
            'counter_pcc_t06': 0,
            'counter_pcc_t07': 0,
            'counter_pcc_t08': 0,
            'counter_pcc_t09': 0,
            'counter_pcc_t10': 0,
            'counter_pcc_t11': 0,
            'counter_pcc_t12': 0,
            'counter_pcc_t13': 0,
            'counter_pcc_t14': 0,
            'counter_pcc_t15': 0,
            'counter_pcc_t16': 0,
            'counter_pcc_t17': 0,
            'counter_pcc_t18': 0,
            'counter_pcc_t19': 0,
            'counter_pcc_t20': 0,
            'counter_pcc_t21': 0,
            'counter_pcc_t22': 0,
            'counter_pcc_t23': 0,
            'counter_pv_t00': 0,
            'counter_pv_t01': 0,
            'counter_pv_t02': 0,
            'counter_pv_t03': 0,
            'counter_pv_t04': 0,
            'counter_pv_t05': 0,
            'counter_pv_t06': 0,
            'counter_pv_t07': 0,
            'counter_pv_t08': 0,
            'counter_pv_t09': 0,
            'counter_pv_t10': 0,
            'counter_pv_t11': 0,
            'counter_pv_t12': 0,
            'counter_pv_t13': 0,
            'counter_pv_t14': 0,
            'counter_pv_t15': 0,
            'counter_pv_t16': 0,
            'counter_pv_t17': 0,
            'counter_pv_t18': 0,
            'counter_pv_t19': 0,
            'counter_pv_t20': 0,
            'counter_pv_t21': 0,
            'counter_pv_t22': 0,
            'counter_pv_t23': 0,
            'counter_genset_t00': 0,
            'counter_genset_t01': 0,
            'counter_genset_t02': 0,
            'counter_genset_t03': 0,
            'counter_genset_t04': 0,
            'counter_genset_t05': 0,
            'counter_genset_t06': 0,
            'counter_genset_t07': 0,
            'counter_genset_t08': 0,
            'counter_genset_t09': 0,
            'counter_genset_t10': 0,
            'counter_genset_t11': 0,
            'counter_genset_t12': 0,
            'counter_genset_t13': 0,
            'counter_genset_t14': 0,
            'counter_genset_t15': 0,
            'counter_genset_t16': 0,
            'counter_genset_t17': 0,
            'counter_genset_t18': 0,
            'counter_genset_t19': 0,
            'counter_genset_t20': 0,
            'counter_genset_t21': 0,
            'counter_genset_t22': 0,
            'counter_genset_t23': 0,
            'counter_bess_t00': 0,
            'counter_bess_t01': 0,
            'counter_bess_t02': 0,
            'counter_bess_t03': 0,
            'counter_bess_t04': 0,
            'counter_bess_t05': 0,
            'counter_bess_t06': 0,
            'counter_bess_t07': 0,
            'counter_bess_t08': 0,
            'counter_bess_t09': 0,
            'counter_bess_t10': 0,
            'counter_bess_t11': 0,
            'counter_bess_t12': 0,
            'counter_bess_t13': 0,
            'counter_bess_t14': 0,
            'counter_bess_t15': 0,
            'counter_bess_t16': 0,
            'counter_bess_t17': 0,
            'counter_bess_t18': 0,
            'counter_bess_t19': 0,
            'counter_bess_t20': 0,
            'counter_bess_t21': 0,
            'counter_bess_t22': 0,
            'counter_bess_t23': 0
        }
        
        SP_timezone = 3 # Timezone at SP - Brazil (improve this code please!!!)
        for i in range(24):

            final_time = datetime.today() - timedelta(hours=(int(i) + SP_timezone)) 
            initial_time = datetime.today() - timedelta(hours=(int(i) + SP_timezone + 1))

            measurements = main_query.filter(node_measurement_model.time_iso >= initial_time).filter(node_measurement_model.time_iso < final_time)

            for meas in measurements.all():
                if meas.der == "pcc":
                    if i == 23:
                        data["pcc_t00"] = data["pcc_t00"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t00"] = counters["counter_pcc_t00"] + 1
                    if i == 22:
                        data["pcc_t01"] = data["pcc_t01"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t01"] = counters["counter_pcc_t01"] + 1
                    if i == 21:
                        data["pcc_t02"] = data["pcc_t02"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t02"] = counters["counter_pcc_t02"] + 1
                    if i == 20:
                        data["pcc_t03"] = data["pcc_t03"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t03"] = counters["counter_pcc_t03"] + 1
                    if i == 19:
                        data["pcc_t04"] = data["pcc_t04"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t04"] = counters["counter_pcc_t04"] + 1
                    if i == 18:
                        data["pcc_t05"] = data["pcc_t05"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t05"] = counters["counter_pcc_t05"] + 1
                    if i == 17:
                        data["pcc_t06"] = data["pcc_t06"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t06"] = counters["counter_pcc_t06"] + 1
                    if i == 16:
                        data["pcc_t07"] = data["pcc_t07"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t07"] = counters["counter_pcc_t07"] + 1
                    if i == 15:
                        data["pcc_t08"] = data["pcc_t08"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t08"] = counters["counter_pcc_t08"] + 1
                    if i == 14:
                        data["pcc_t09"] = data["pcc_t09"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t09"] = counters["counter_pcc_t09"] + 1
                    if i == 13:
                        data["pcc_t10"] = data["pcc_t10"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t10"] = counters["counter_pcc_t10"] + 1
                    if i == 12:
                        data["pcc_t11"] = data["pcc_t11"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t11"] = counters["counter_pcc_t11"] + 1
                    if i == 11:
                        data["pcc_t12"] = data["pcc_t12"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t12"] = counters["counter_pcc_t12"] + 1
                    if i == 10:
                        data["pcc_t13"] = data["pcc_t13"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t13"] = counters["counter_pcc_t13"] + 1
                    if i == 9:
                        data["pcc_t14"] = data["pcc_t14"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t14"] = counters["counter_pcc_t14"] + 1
                    if i == 8:
                        data["pcc_t15"] = data["pcc_t15"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t15"] = counters["counter_pcc_t15"] + 1
                    if i == 7:
                        data["pcc_t16"] = data["pcc_t16"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t16"] = counters["counter_pcc_t16"] + 1
                    if i == 6:
                        data["pcc_t17"] = data["pcc_t17"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t17"] = counters["counter_pcc_t17"] + 1
                    if i == 5:
                        data["pcc_t18"] = data["pcc_t18"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t18"] = counters["counter_pcc_t18"] + 1
                    if i == 4:
                        data["pcc_t19"] = data["pcc_t19"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t19"] = counters["counter_pcc_t19"] + 1
                    if i == 3:
                        data["pcc_t20"] = data["pcc_t20"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t20"] = counters["counter_pcc_t20"] + 1
                    if i == 2:
                        data["pcc_t21"] = data["pcc_t21"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t21"] = counters["counter_pcc_t21"] + 1
                    if i == 1:
                        data["pcc_t22"] = data["pcc_t22"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t22"] = counters["counter_pcc_t22"] + 1
                    if i == 0:
                        data["pcc_t23"] = data["pcc_t23"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pcc_t23"] = counters["counter_pcc_t23"] + 1
                if meas.der == "bess":
                    if i == 23:
                        data["bess_t00"] = data["bess_t00"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t00"] = data["bess_soc_t00"] + meas.soc_kwh
                        counters["counter_bess_t00"] = counters["counter_bess_t00"] + 1
                    if i == 22:
                        data["bess_t01"] = data["bess_t01"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t01"] = data["bess_soc_t01"] + meas.soc_kwh
                        counters["counter_bess_t01"] = counters["counter_bess_t01"] + 1
                    if i == 21:
                        data["bess_t02"] = data["bess_t02"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t02"] = data["bess_soc_t02"] + meas.soc_kwh
                        counters["counter_bess_t02"] = counters["counter_bess_t02"] + 1
                    if i == 20:
                        data["bess_t03"] = data["bess_t03"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t03"] = data["bess_soc_t03"] + meas.soc_kwh
                        counters["counter_bess_t03"] = counters["counter_bess_t03"] + 1
                    if i == 19:
                        data["bess_t04"] = data["bess_t04"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t04"] = data["bess_soc_t04"] + meas.soc_kwh
                        counters["counter_bess_t04"] = counters["counter_bess_t04"] + 1
                    if i == 18:
                        data["bess_t05"] = data["bess_t05"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t05"] = data["bess_soc_t05"] + meas.soc_kwh
                        counters["counter_bess_t05"] = counters["counter_bess_t05"] + 1
                    if i == 17:
                        data["bess_t06"] = data["bess_t06"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t06"] = data["bess_soc_t06"] + meas.soc_kwh
                        counters["counter_bess_t06"] = counters["counter_bess_t06"] + 1
                    if i == 16:
                        data["bess_t07"] = data["bess_t07"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t07"] = data["bess_soc_t07"] + meas.soc_kwh
                        counters["counter_bess_t07"] = counters["counter_bess_t07"] + 1
                    if i == 15:
                        data["bess_t08"] = data["bess_t08"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t08"] = data["bess_soc_t08"] + meas.soc_kwh
                        counters["counter_bess_t08"] = counters["counter_bess_t08"] + 1
                    if i == 14:
                        data["bess_t09"] = data["bess_t09"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t09"] = data["bess_soc_t09"] + meas.soc_kwh
                        counters["counter_bess_t09"] = counters["counter_bess_t09"] + 1
                    if i == 13:
                        data["bess_t10"] = data["bess_t10"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t10"] = data["bess_soc_t10"] + meas.soc_kwh
                        counters["counter_bess_t10"] = counters["counter_bess_t10"] + 1
                    if i == 12:
                        data["bess_t11"] = data["bess_t11"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t11"] = data["bess_soc_t11"] + meas.soc_kwh
                        counters["counter_bess_t11"] = counters["counter_bess_t11"] + 1
                    if i == 11:
                        data["bess_t12"] = data["bess_t12"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t12"] = data["bess_soc_t12"] + meas.soc_kwh
                        counters["counter_bess_t12"] = counters["counter_bess_t12"] + 1
                    if i == 10:
                        data["bess_t13"] = data["bess_t13"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t13"] = data["bess_soc_t13"] + meas.soc_kwh
                        counters["counter_bess_t13"] = counters["counter_bess_t13"] + 1
                    if i == 9:
                        data["bess_t14"] = data["bess_t14"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t14"] = data["bess_soc_t14"] + meas.soc_kwh
                        counters["counter_bess_t14"] = counters["counter_bess_t14"] + 1
                    if i == 8:
                        data["bess_t15"] = data["bess_t15"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t15"] = data["bess_soc_t15"] + meas.soc_kwh
                        counters["counter_bess_t15"] = counters["counter_bess_t15"] + 1
                    if i == 7:
                        data["bess_t16"] = data["bess_t16"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t16"] = data["bess_soc_t16"] + meas.soc_kwh
                        counters["counter_bess_t16"] = counters["counter_bess_t16"] + 1
                    if i == 6:
                        data["bess_t17"] = data["bess_t17"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t17"] = data["bess_soc_t17"] + meas.soc_kwh
                        counters["counter_bess_t17"] = counters["counter_bess_t17"] + 1
                    if i == 5:
                        data["bess_t18"] = data["bess_t18"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t18"] = data["bess_soc_t18"] + meas.soc_kwh
                        counters["counter_bess_t18"] = counters["counter_bess_t18"] + 1
                    if i == 4:
                        data["bess_t19"] = data["bess_t19"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t19"] = data["bess_soc_t19"] + meas.soc_kwh
                        counters["counter_bess_t19"] = counters["counter_bess_t19"] + 1
                    if i == 3:
                        data["bess_t20"] = data["bess_t20"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t20"] = data["bess_soc_t20"] + meas.soc_kwh
                        counters["counter_bess_t20"] = counters["counter_bess_t20"] + 1
                    if i == 2:
                        data["bess_t21"] = data["bess_t21"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t21"] = data["bess_soc_t21"] + meas.soc_kwh
                        counters["counter_bess_t21"] = counters["counter_bess_t21"] + 1
                    if i == 1:
                        data["bess_t22"] = data["bess_t22"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t22"] = data["bess_soc_t22"] + meas.soc_kwh
                        counters["counter_bess_t22"] = counters["counter_bess_t22"] + 1
                    if i == 0:
                        data["bess_t23"] = data["bess_t23"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        data["bess_soc_t23"] = data["bess_soc_t23"] + meas.soc_kwh
                        counters["counter_bess_t23"] = counters["counter_bess_t23"] + 1
                if meas.der == "pv":
                    if i == 23:
                        data["pv_t00"] = data["pv_t00"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t00"] = counters["counter_pv_t00"] + 1
                    if i == 22:
                        data["pv_t01"] = data["pv_t01"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t01"] = counters["counter_pv_t01"] + 1
                    if i == 21:
                        data["pv_t02"] = data["pv_t02"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t02"] = counters["counter_pv_t02"] + 1
                    if i == 20:
                        data["pv_t03"] = data["pv_t03"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t03"] = counters["counter_pv_t03"] + 1
                    if i == 19:
                        data["pv_t04"] = data["pv_t04"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t04"] = counters["counter_pv_t04"] + 1
                    if i == 18:
                        data["pv_t05"] = data["pv_t05"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t05"] = counters["counter_pv_t05"] + 1
                    if i == 17:
                        data["pv_t06"] = data["pv_t06"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t06"] = counters["counter_pv_t06"] + 1
                    if i == 16:
                        data["pv_t07"] = data["pv_t07"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t07"] = counters["counter_pv_t07"] + 1
                    if i == 15:
                        data["pv_t08"] = data["pv_t08"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t08"] = counters["counter_pv_t08"] + 1
                    if i == 14:
                        data["pv_t09"] = data["pv_t09"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t09"] = counters["counter_pv_t09"] + 1
                    if i == 13:
                        data["pv_t10"] = data["pv_t10"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t10"] = counters["counter_pv_t10"] + 1
                    if i == 12:
                        data["pv_t11"] = data["pv_t11"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t11"] = counters["counter_pv_t11"] + 1
                    if i == 11:
                        data["pv_t12"] = data["pv_t12"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t12"] = counters["counter_pv_t12"] + 1
                    if i == 10:
                        data["pv_t13"] = data["pv_t13"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t13"] = counters["counter_pv_t13"] + 1
                    if i == 9:
                        data["pv_t14"] = data["pv_t14"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t14"] = counters["counter_pv_t14"] + 1
                    if i == 8:
                        data["pv_t15"] = data["pv_t15"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t15"] = counters["counter_pv_t15"] + 1
                    if i == 7:
                        data["pv_t16"] = data["pv_t16"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t16"] = counters["counter_pv_t16"] + 1
                    if i == 6:
                        data["pv_t17"] = data["pv_t17"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t17"] = counters["counter_pv_t17"] + 1
                    if i == 5:
                        data["pv_t18"] = data["pv_t18"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t18"] = counters["counter_pv_t18"] + 1
                    if i == 4:
                        data["pv_t19"] = data["pv_t19"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t19"] = counters["counter_pv_t19"] + 1
                    if i == 3:
                        data["pv_t20"] = data["pv_t20"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t20"] = counters["counter_pv_t20"] + 1
                    if i == 2:
                        data["pv_t21"] = data["pv_t21"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t21"] = counters["counter_pv_t21"] + 1
                    if i == 1:
                        data["pv_t22"] = data["pv_t22"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t22"] = counters["counter_pv_t22"] + 1
                    if i == 0:
                        data["pv_t23"] = data["pv_t23"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_pv_t23"] = counters["counter_pv_t23"] + 1
                if meas.der == "genset":
                    if i == 23:
                        data["genset_t00"] = data["genset_t00"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t00"] = counters["counter_genset_t00"] + 1
                    if i == 22:
                        data["genset_t01"] = data["genset_t01"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t01"] = counters["counter_genset_t01"] + 1
                    if i == 21:
                        data["genset_t02"] = data["genset_t02"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t02"] = counters["counter_genset_t02"] + 1
                    if i == 20:
                        data["genset_t03"] = data["genset_t03"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t03"] = counters["counter_genset_t03"] + 1
                    if i == 19:
                        data["genset_t04"] = data["genset_t04"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t04"] = counters["counter_genset_t04"] + 1
                    if i == 18:
                        data["genset_t05"] = data["genset_t05"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t05"] = counters["counter_genset_t05"] + 1
                    if i == 17:
                        data["genset_t06"] = data["genset_t06"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t06"] = counters["counter_genset_t06"] + 1
                    if i == 16:
                        data["genset_t07"] = data["genset_t07"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t07"] = counters["counter_genset_t07"] + 1
                    if i == 15:
                        data["genset_t08"] = data["genset_t08"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t08"] = counters["counter_genset_t08"] + 1
                    if i == 14:
                        data["genset_t09"] = data["genset_t09"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t09"] = counters["counter_genset_t09"] + 1
                    if i == 13:
                        data["genset_t10"] = data["genset_t10"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t10"] = counters["counter_genset_t10"] + 1
                    if i == 12:
                        data["genset_t11"] = data["genset_t11"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t11"] = counters["counter_genset_t11"] + 1
                    if i == 11:
                        data["genset_t12"] = data["genset_t12"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t12"] = counters["counter_genset_t12"] + 1
                    if i == 10:
                        data["genset_t13"] = data["genset_t13"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t13"] = counters["counter_genset_t13"] + 1
                    if i == 9:
                        data["genset_t14"] = data["genset_t14"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t14"] = counters["counter_genset_t14"] + 1
                    if i == 8:
                        data["genset_t15"] = data["genset_t15"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t15"] = counters["counter_genset_t15"] + 1
                    if i == 7:
                        data["genset_t16"] = data["genset_t16"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t16"] = counters["counter_genset_t16"] + 1
                    if i == 6:
                        data["genset_t17"] = data["genset_t17"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t17"] = counters["counter_genset_t17"] + 1
                    if i == 5:
                        data["genset_t18"] = data["genset_t18"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t18"] = counters["counter_genset_t18"] + 1
                    if i == 4:
                        data["genset_t19"] = data["genset_t19"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t19"] = counters["counter_genset_t19"] + 1
                    if i == 3:
                        data["genset_t20"] = data["genset_t20"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t20"] = counters["counter_genset_t20"] + 1
                    if i == 2:
                        data["genset_t21"] = data["genset_t21"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t21"] = counters["counter_genset_t21"] + 1
                    if i == 1:
                        data["genset_t22"] = data["genset_t22"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t22"] = counters["counter_genset_t22"] + 1
                    if i == 0:
                        data["genset_t23"] = data["genset_t23"] + meas.active_power_a_kw + meas.active_power_b_kw + meas.active_power_c_kw
                        counters["counter_genset_t23"] = counters["counter_genset_t23"] + 1

        if counters["counter_pcc_t00"] > 1:
            data["pcc_t00"] = data["pcc_t00"] / counters["counter_pcc_t00"]
        if counters["counter_pcc_t01"] > 1:
            data["pcc_t01"] = data["pcc_t01"] / counters["counter_pcc_t01"]
        if counters["counter_pcc_t02"] > 1:
            data["pcc_t02"] = data["pcc_t02"] / counters["counter_pcc_t02"]
        if counters["counter_pcc_t03"] > 1:
            data["pcc_t03"] = data["pcc_t03"] / counters["counter_pcc_t03"]
        if counters["counter_pcc_t04"] > 1:
            data["pcc_t04"] = data["pcc_t04"] / counters["counter_pcc_t04"]
        if counters["counter_pcc_t05"] > 1:
            data["pcc_t05"] = data["pcc_t05"] / counters["counter_pcc_t05"]
        if counters["counter_pcc_t06"] > 1:
            data["pcc_t06"] = data["pcc_t06"] / counters["counter_pcc_t06"]
        if counters["counter_pcc_t07"] > 1:
            data["pcc_t07"] = data["pcc_t07"] / counters["counter_pcc_t07"]
        if counters["counter_pcc_t08"] > 1:
            data["pcc_t08"] = data["pcc_t08"] / counters["counter_pcc_t08"]
        if counters["counter_pcc_t09"] > 1:
            data["pcc_t09"] = data["pcc_t09"] / counters["counter_pcc_t09"]
        if counters["counter_pcc_t10"] > 1:
            data["pcc_t10"] = data["pcc_t10"] / counters["counter_pcc_t10"]
        if counters["counter_pcc_t11"] > 1:
            data["pcc_t11"] = data["pcc_t11"] / counters["counter_pcc_t11"]
        if counters["counter_pcc_t12"] > 1:
            data["pcc_t12"] = data["pcc_t12"] / counters["counter_pcc_t12"]
        if counters["counter_pcc_t13"] > 1:
            data["pcc_t13"] = data["pcc_t13"] / counters["counter_pcc_t13"]
        if counters["counter_pcc_t14"] > 1:
            data["pcc_t14"] = data["pcc_t14"] / counters["counter_pcc_t14"]
        if counters["counter_pcc_t15"] > 1:
            data["pcc_t15"] = data["pcc_t15"] / counters["counter_pcc_t15"]
        if counters["counter_pcc_t16"] > 1:
            data["pcc_t16"] = data["pcc_t16"] / counters["counter_pcc_t16"]
        if counters["counter_pcc_t17"] > 1:
            data["pcc_t17"] = data["pcc_t17"] / counters["counter_pcc_t17"]
        if counters["counter_pcc_t18"] > 1:
            data["pcc_t18"] = data["pcc_t18"] / counters["counter_pcc_t18"]
        if counters["counter_pcc_t19"] > 1:
            data["pcc_t19"] = data["pcc_t19"] / counters["counter_pcc_t19"]
        if counters["counter_pcc_t20"] > 1:
            data["pcc_t20"] = data["pcc_t20"] / counters["counter_pcc_t20"]
        if counters["counter_pcc_t21"] > 1:
            data["pcc_t21"] = data["pcc_t21"] / counters["counter_pcc_t21"]
        if counters["counter_pcc_t22"] > 1:
            data["pcc_t22"] = data["pcc_t22"] / counters["counter_pcc_t22"]
        if counters["counter_pcc_t23"] > 1:
            data["pcc_t23"] = data["pcc_t23"] / counters["counter_pcc_t23"]

        if counters["counter_bess_t00"] > 1:
            data["bess_t00"] = data["bess_t00"] / counters["counter_bess_t00"]
            data["bess_soc_t00"] = data["bess_soc_t00"] / counters["counter_bess_t00"]
        if counters["counter_bess_t01"] > 1:
            data["bess_t01"] = data["bess_t01"] / counters["counter_bess_t01"]
            data["bess_soc_t01"] = data["bess_soc_t01"] / counters["counter_bess_t01"]
        if counters["counter_bess_t02"] > 1:
            data["bess_t02"] = data["bess_t02"] / counters["counter_bess_t02"]
            data["bess_soc_t02"] = data["bess_soc_t02"] / counters["counter_bess_t02"]
        if counters["counter_bess_t03"] > 1:
            data["bess_t03"] = data["bess_t03"] / counters["counter_bess_t03"]
            data["bess_soc_t03"] = data["bess_soc_t03"] / counters["counter_bess_t03"]
        if counters["counter_bess_t04"] > 1:
            data["bess_t04"] = data["bess_t04"] / counters["counter_bess_t04"]
            data["bess_soc_t04"] = data["bess_soc_t04"] / counters["counter_bess_t04"]
        if counters["counter_bess_t05"] > 1:
            data["bess_t05"] = data["bess_t05"] / counters["counter_bess_t05"]
            data["bess_soc_t05"] = data["bess_soc_t05"] / counters["counter_bess_t05"]
        if counters["counter_bess_t06"] > 1:
            data["bess_t06"] = data["bess_t06"] / counters["counter_bess_t06"]
            data["bess_soc_t06"] = data["bess_soc_t06"] / counters["counter_bess_t06"]
        if counters["counter_bess_t07"] > 1:
            data["bess_t07"] = data["bess_t07"] / counters["counter_bess_t07"]
            data["bess_soc_t07"] = data["bess_soc_t07"] / counters["counter_bess_t07"]
        if counters["counter_bess_t08"] > 1:
            data["bess_t08"] = data["bess_t08"] / counters["counter_bess_t08"]
            data["bess_soc_t08"] = data["bess_soc_t08"] / counters["counter_bess_t08"]
        if counters["counter_bess_t09"] > 1:
            data["bess_t09"] = data["bess_t09"] / counters["counter_bess_t09"]
            data["bess_soc_t09"] = data["bess_soc_t09"] / counters["counter_bess_t09"]
        if counters["counter_bess_t10"] > 1:
            data["bess_t10"] = data["bess_t10"] / counters["counter_bess_t10"]
            data["bess_soc_t10"] = data["bess_soc_t10"] / counters["counter_bess_t10"]
        if counters["counter_bess_t11"] > 1:
            data["bess_t11"] = data["bess_t11"] / counters["counter_bess_t11"]
            data["bess_soc_t11"] = data["bess_soc_t11"] / counters["counter_bess_t11"]
        if counters["counter_bess_t12"] > 1:
            data["bess_t12"] = data["bess_t12"] / counters["counter_bess_t12"]
            data["bess_soc_t12"] = data["bess_soc_t12"] / counters["counter_bess_t12"]
        if counters["counter_bess_t13"] > 1:
            data["bess_t13"] = data["bess_t13"] / counters["counter_bess_t13"]
            data["bess_soc_t13"] = data["bess_soc_t13"] / counters["counter_bess_t13"]
        if counters["counter_bess_t14"] > 1:
            data["bess_t14"] = data["bess_t14"] / counters["counter_bess_t14"]
            data["bess_soc_t14"] = data["bess_soc_t14"] / counters["counter_bess_t14"]
        if counters["counter_bess_t15"] > 1:
            data["bess_t15"] = data["bess_t15"] / counters["counter_bess_t15"]
            data["bess_soc_t15"] = data["bess_soc_t15"] / counters["counter_bess_t15"]
        if counters["counter_bess_t16"] > 1:
            data["bess_t16"] = data["bess_t16"] / counters["counter_bess_t16"]
            data["bess_soc_t16"] = data["bess_soc_t16"] / counters["counter_bess_t16"]
        if counters["counter_bess_t17"] > 1:
            data["bess_t17"] = data["bess_t17"] / counters["counter_bess_t17"]
            data["bess_soc_t17"] = data["bess_soc_t17"] / counters["counter_bess_t17"]
        if counters["counter_bess_t18"] > 1:
            data["bess_t18"] = data["bess_t18"] / counters["counter_bess_t18"]
            data["bess_soc_t18"] = data["bess_soc_t18"] / counters["counter_bess_t18"]
        if counters["counter_bess_t19"] > 1:
            data["bess_t19"] = data["bess_t19"] / counters["counter_bess_t19"]
            data["bess_soc_t19"] = data["bess_soc_t19"] / counters["counter_bess_t19"]
        if counters["counter_bess_t20"] > 1:
            data["bess_t20"] = data["bess_t20"] / counters["counter_bess_t20"]
            data["bess_soc_t20"] = data["bess_soc_t20"] / counters["counter_bess_t20"]
        if counters["counter_bess_t21"] > 1:
            data["bess_t21"] = data["bess_t21"] / counters["counter_bess_t21"]
            data["bess_soc_t21"] = data["bess_soc_t21"] / counters["counter_bess_t21"]
        if counters["counter_bess_t22"] > 1:
            data["bess_t22"] = data["bess_t22"] / counters["counter_bess_t22"]
            data["bess_soc_t22"] = data["bess_soc_t22"] / counters["counter_bess_t22"]
        if counters["counter_bess_t23"] > 1:
            data["bess_t23"] = data["bess_t23"] / counters["counter_bess_t23"]
            data["bess_soc_t23"] = data["bess_soc_t23"] / counters["counter_bess_t23"]

        if counters["counter_pv_t00"] > 1:
            data["pv_t00"] = data["pv_t00"] / counters["counter_pv_t00"]
        if counters["counter_pv_t01"] > 1:
            data["pv_t01"] = data["pv_t01"] / counters["counter_pv_t01"]
        if counters["counter_pv_t02"] > 1:
            data["pv_t02"] = data["pv_t02"] / counters["counter_pv_t02"]
        if counters["counter_pv_t03"] > 1:
            data["pv_t03"] = data["pv_t03"] / counters["counter_pv_t03"]
        if counters["counter_pv_t04"] > 1:
            data["pv_t04"] = data["pv_t04"] / counters["counter_pv_t04"]
        if counters["counter_pv_t05"] > 1:
            data["pv_t05"] = data["pv_t05"] / counters["counter_pv_t05"]
        if counters["counter_pv_t06"] > 1:
            data["pv_t06"] = data["pv_t06"] / counters["counter_pv_t06"]
        if counters["counter_pv_t07"] > 1:
            data["pv_t07"] = data["pv_t07"] / counters["counter_pv_t07"]
        if counters["counter_pv_t08"] > 1:
            data["pv_t08"] = data["pv_t08"] / counters["counter_pv_t08"]
        if counters["counter_pv_t09"] > 1:
            data["pv_t09"] = data["pv_t09"] / counters["counter_pv_t09"]
        if counters["counter_pv_t10"] > 1:
            data["pv_t10"] = data["pv_t10"] / counters["counter_pv_t10"]
        if counters["counter_pv_t11"] > 1:
            data["pv_t11"] = data["pv_t11"] / counters["counter_pv_t11"]
        if counters["counter_pv_t12"] > 1:
            data["pv_t12"] = data["pv_t12"] / counters["counter_pv_t12"]
        if counters["counter_pv_t13"] > 1:
            data["pv_t13"] = data["pv_t13"] / counters["counter_pv_t13"]
        if counters["counter_pv_t14"] > 1:
            data["pv_t14"] = data["pv_t14"] / counters["counter_pv_t14"]
        if counters["counter_pv_t15"] > 1:
            data["pv_t15"] = data["pv_t15"] / counters["counter_pv_t15"]
        if counters["counter_pv_t16"] > 1:
            data["pv_t16"] = data["pv_t16"] / counters["counter_pv_t16"]
        if counters["counter_pv_t17"] > 1:
            data["pv_t17"] = data["pv_t17"] / counters["counter_pv_t17"]
        if counters["counter_pv_t18"] > 1:
            data["pv_t18"] = data["pv_t18"] / counters["counter_pv_t18"]
        if counters["counter_pv_t19"] > 1:
            data["pv_t19"] = data["pv_t19"] / counters["counter_pv_t19"]
        if counters["counter_pv_t20"] > 1:
            data["pv_t20"] = data["pv_t20"] / counters["counter_pv_t20"]
        if counters["counter_pv_t21"] > 1:
            data["pv_t21"] = data["pv_t21"] / counters["counter_pv_t21"]
        if counters["counter_pv_t22"] > 1:
            data["pv_t22"] = data["pv_t22"] / counters["counter_pv_t22"]
        if counters["counter_pv_t23"] > 1:
            data["pv_t23"] = data["pv_t23"] / counters["counter_pv_t23"]

        if counters["counter_genset_t00"] > 1:
            data["genset_t00"] = data["genset_t00"] / counters["counter_genset_t00"]
        if counters["counter_genset_t01"] > 1:
            data["genset_t01"] = data["genset_t01"] / counters["counter_genset_t01"]
        if counters["counter_genset_t02"] > 1:
            data["genset_t02"] = data["genset_t02"] / counters["counter_genset_t02"]
        if counters["counter_genset_t03"] > 1:
            data["genset_t03"] = data["genset_t03"] / counters["counter_genset_t03"]
        if counters["counter_genset_t04"] > 1:
            data["genset_t04"] = data["genset_t04"] / counters["counter_genset_t04"]
        if counters["counter_genset_t05"] > 1:
            data["genset_t05"] = data["genset_t05"] / counters["counter_genset_t05"]
        if counters["counter_genset_t06"] > 1:
            data["genset_t06"] = data["genset_t06"] / counters["counter_genset_t06"]
        if counters["counter_genset_t07"] > 1:
            data["genset_t07"] = data["genset_t07"] / counters["counter_genset_t07"]
        if counters["counter_genset_t08"] > 1:
            data["genset_t08"] = data["genset_t08"] / counters["counter_genset_t08"]
        if counters["counter_genset_t09"] > 1:
            data["genset_t09"] = data["genset_t09"] / counters["counter_genset_t09"]
        if counters["counter_genset_t10"] > 1:
            data["genset_t10"] = data["genset_t10"] / counters["counter_genset_t10"]
        if counters["counter_genset_t11"] > 1:
            data["genset_t11"] = data["genset_t11"] / counters["counter_genset_t11"]
        if counters["counter_genset_t12"] > 1:
            data["genset_t12"] = data["genset_t12"] / counters["counter_genset_t12"]
        if counters["counter_genset_t13"] > 1:
            data["genset_t13"] = data["genset_t13"] / counters["counter_genset_t13"]
        if counters["counter_genset_t14"] > 1:
            data["genset_t14"] = data["genset_t14"] / counters["counter_genset_t14"]
        if counters["counter_genset_t15"] > 1:
            data["genset_t15"] = data["genset_t15"] / counters["counter_genset_t15"]
        if counters["counter_genset_t16"] > 1:
            data["genset_t16"] = data["genset_t16"] / counters["counter_genset_t16"]
        if counters["counter_genset_t17"] > 1:
            data["genset_t17"] = data["genset_t17"] / counters["counter_genset_t17"]
        if counters["counter_genset_t18"] > 1:
            data["genset_t18"] = data["genset_t18"] / counters["counter_genset_t18"]
        if counters["counter_genset_t19"] > 1:
            data["genset_t19"] = data["genset_t19"] / counters["counter_genset_t19"]
        if counters["counter_genset_t20"] > 1:
            data["genset_t20"] = data["genset_t20"] / counters["counter_genset_t20"]
        if counters["counter_genset_t21"] > 1:
            data["genset_t21"] = data["genset_t21"] / counters["counter_genset_t21"]
        if counters["counter_genset_t22"] > 1:
            data["genset_t22"] = data["genset_t22"] / counters["counter_genset_t22"]
        if counters["counter_genset_t23"] > 1:
            data["genset_t23"] = data["genset_t23"] / counters["counter_genset_t23"]

        # print(data)
        # print(counters)

        return data


# ENDPOINT /v1/api/node_measurement/no/x/ -> GET all measurements from a parent node x
@node_measurement_namespace.route('/no/<int:id_info_no>/')
class node_measurement_ListCreateFromParent(Resource):

    @node_measurement_namespace.doc('retrieve_measurements_from_parent')
    @node_measurement_namespace.marshal_with(measurement_model)
    def get(self, id_info_no):
        '''
        Retrieves measurements from id_info_no
        '''

        parameters = [node_measurement_model.id, node_information_model.name, node_measurement_model.time_iso, node_measurement_model.active_power_a_kw, 
            node_measurement_model.active_power_b_kw, node_measurement_model.active_power_c_kw, node_measurement_model.reactive_power_a_kvar,
            node_measurement_model.reactive_power_b_kvar, node_measurement_model.reactive_power_c_kvar, node_measurement_model.voltage_a_kv,
            node_measurement_model.voltage_b_kv, node_measurement_model.voltage_c_kv, node_measurement_model.soc_kwh]

        main_query = node_measurement_model.query.join(node_information_model).with_entities(*parameters)
        measurements = (main_query.all())
        measurements = (main_query.filter(node_measurement_model.id_info_no == id_info_no).all())

        if not measurements:
            # The measurements is not present
            return '', http.client.NOT_FOUND

        return measurements

    @node_measurement_namespace.doc('create_measurement_from_parent')
    @node_measurement_namespace.expect(node_measurement_parser)
    @node_measurement_namespace.marshal_with(measurement_model, code=http.client.CREATED)
    def post(self, id_info_no):
        '''
        Creates new measurements for id_info_no
        '''

        # Verify if node exists
        node = node_information_model.query.get(id_info_no)
        if not node:
            # The node is not present
            return '', http.client.NOT_FOUND

        args = node_measurement_parser.parse_args()


        new_measurement = node_measurement_model(time_iso=args['time_iso'],
                            active_power_a_kw=args['active_power_a_kw'],
                            active_power_b_kw=args['active_power_b_kw'],
                            active_power_c_kw=args['active_power_c_kw'],
                            reactive_power_a_kvar=args['reactive_power_a_kvar'],
                            reactive_power_b_kvar=args['reactive_power_b_kvar'],
                            reactive_power_c_kvar=args['reactive_power_c_kvar'],
                            voltage_a_kv=args['voltage_a_kv'],
                            voltage_b_kv=args['voltage_b_kv'],
                            voltage_c_kv=args['voltage_c_kv'],
                            soc_kwh=args['soc_kwh'],                        
                            id_info_no=id_info_no)

        if (node.der == 'bess') and new_measurement.soc_kwh is None:
            return abort(405, 'Input bess validation failed', errors={'soc_kwh' : 'BESS measurement has no soc_kwh attribute'})
        
        try:
            db.session.add(new_measurement)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})
            

        parameters = [node_measurement_model.id, node_information_model.name, node_measurement_model.time_iso, node_measurement_model.active_power_a_kw, 
            node_measurement_model.active_power_b_kw, node_measurement_model.active_power_c_kw, node_measurement_model.reactive_power_a_kvar,
            node_measurement_model.reactive_power_b_kvar, node_measurement_model.reactive_power_c_kvar, node_measurement_model.voltage_a_kv,
            node_measurement_model.voltage_b_kv, node_measurement_model.voltage_c_kv, node_measurement_model.soc_kwh]
        main_query = node_measurement_model.query.join(node_information_model).with_entities(*parameters)

        measurements = (main_query.order_by(node_measurement_model.id.desc()).first())

        result = node_measurement_namespace.marshal(measurements, measurement_model)

        return result, http.client.CREATED

    @node_measurement_namespace.doc('delete_measurement',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, id_info_no):
        '''
        Deletes all measurements from id_info_no
        '''

        parameters = [node_measurement_model.id, node_information_model.name, node_measurement_model.time_iso, node_measurement_model.active_power_a_kw, 
            node_measurement_model.active_power_b_kw, node_measurement_model.active_power_c_kw, node_measurement_model.reactive_power_a_kvar,
            node_measurement_model.reactive_power_b_kvar, node_measurement_model.reactive_power_c_kvar, node_measurement_model.voltage_a_kv,
            node_measurement_model.voltage_b_kv, node_measurement_model.voltage_c_kv, node_measurement_model.soc_kwh]
        main_query = node_measurement_model.query.join(node_information_model).with_entities(*parameters)
        measurements = (main_query.all())
        measurements = (main_query.filter(node_measurement_model.id_info_no == id_info_no).all())

        if not measurements:
            # The node is not present
            return '', http.client.NO_CONTENT

        # db.session.delete(measurements)
        node_measurement_model.query.filter(node_measurement_model.id_info_no == id_info_no).delete()
        db.session.commit()

        return '', http.client.NO_CONTENT


# ENDPOINT /v1/api/node_measurement/DateTimeMax/ -> DELETE all measurements before DateTimeMax
@node_measurement_namespace.route('/<DateTimeMax>/')
class node_measurement_DeleteFromDateTime(Resource):

    @node_measurement_namespace.doc('delete_measurement',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, DateTimeMax):
        '''
        DELETE all measurements before DateTimeMax
        '''

        datetime_max_trans = datetime.strptime(DateTimeMax,'%Y-%m-%dT%H:%M:%S.%f')
        
        parameters = [node_measurement_model.id, node_information_model.name, node_measurement_model.time_iso, node_measurement_model.active_power_a_kw, 
            node_measurement_model.active_power_b_kw, node_measurement_model.active_power_c_kw, node_measurement_model.reactive_power_a_kvar,
            node_measurement_model.reactive_power_b_kvar, node_measurement_model.reactive_power_c_kvar, node_measurement_model.voltage_a_kv,
            node_measurement_model.voltage_b_kv, node_measurement_model.voltage_c_kv, node_measurement_model.soc_kwh]
        main_query = node_measurement_model.query.join(node_information_model).with_entities(*parameters)
        measurements = (main_query.all())
        measurements = (main_query.filter(node_measurement_model.time_iso <= datetime_max_trans).all())

        if not measurements:
            # The node is not present
            return '', http.client.NO_CONTENT

        # db.session.delete(measurements)
        node_measurement_model.query.filter(node_measurement_model.time_iso <= datetime_max_trans).delete()
        db.session.commit()

        return '', http.client.NO_CONTENT
