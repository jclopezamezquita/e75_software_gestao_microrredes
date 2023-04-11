import http.client
from datetime import datetime, timedelta
import dateutil.relativedelta
# from flask_restplus import Namespace, Resource, fields, inputs, abort
from flask_restx import Namespace, Resource, fields, inputs, abort
from api_tools.models import milp_parameters_model
from api_tools.db import db
from sqlalchemy import exc
import requests
import json


def voltage_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value > 1.0:
        raise ValueError(' Invalid value!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

voltage_rule.__schema__ = {
    "type": "number",
    "format": "voltage_rule",
}

def nominal_voltage_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

nominal_voltage_rule.__schema__ = {
    "type": "number",
    "format": "nominal_voltage_rule",
}

def num_blocks(value):
    try:
        value = int(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= 0:
        raise ValueError(' Invalid value!')
    return value

num_blocks.__schema__ = {
    "type": "number",
    "format": "num_blocks",
}

def cost_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= 0.0:
        raise ValueError(' Invalid value!')
    return value

cost_rule.__schema__ = {
    "type": "number",
    "format": "cost_rule",
}

def max_power_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= 0.0:
        raise ValueError(' Invalid value!')
    return value

max_power_rule.__schema__ = {
    "type": "number",
    "format": "max_power_rule",
}


# Criação do milp_parameters_namespace e dos parsers
milp_parameters_namespace = Namespace('v1/api/milp_parameters', description='API backend EMS - MILP parameters')

# Parser for post
milp_parameters_parser = milp_parameters_namespace.parser()
milp_parameters_parser.add_argument('min_voltage_pu', type=voltage_rule, required=True, help='Minimum voltage [p.u.] of the microgrid.')
milp_parameters_parser.add_argument('max_voltage_pu', type=nominal_voltage_rule, required=True, help='Maximum voltage [p.u.] of the microgrid.')
milp_parameters_parser.add_argument('nominal_voltage_kv', type=nominal_voltage_rule, required=True, help='Nominal voltage [kV] of the microgrid.')
milp_parameters_parser.add_argument('num_blocks_linearization', type=num_blocks, required=True, help='Number of blocks of linearization, p.e. 20.')
milp_parameters_parser.add_argument('pcc_cost_t01', type=cost_rule, required=True, help='Cost of energy at 01h.')
milp_parameters_parser.add_argument('pcc_cost_t02', type=cost_rule, required=True, help='Cost of energy at 02h.')
milp_parameters_parser.add_argument('pcc_cost_t03', type=cost_rule, required=True, help='Cost of energy at 03h.')
milp_parameters_parser.add_argument('pcc_cost_t04', type=cost_rule, required=True, help='Cost of energy at 04h.')
milp_parameters_parser.add_argument('pcc_cost_t05', type=cost_rule, required=True, help='Cost of energy at 05h.')
milp_parameters_parser.add_argument('pcc_cost_t06', type=cost_rule, required=True, help='Cost of energy at 06h.')
milp_parameters_parser.add_argument('pcc_cost_t07', type=cost_rule, required=True, help='Cost of energy at 07h.')
milp_parameters_parser.add_argument('pcc_cost_t08', type=cost_rule, required=True, help='Cost of energy at 08h.')
milp_parameters_parser.add_argument('pcc_cost_t09', type=cost_rule, required=True, help='Cost of energy at 09h.')
milp_parameters_parser.add_argument('pcc_cost_t10', type=cost_rule, required=True, help='Cost of energy at 10h.')
milp_parameters_parser.add_argument('pcc_cost_t11', type=cost_rule, required=True, help='Cost of energy at 11h.')
milp_parameters_parser.add_argument('pcc_cost_t12', type=cost_rule, required=True, help='Cost of energy at 12h.')
milp_parameters_parser.add_argument('pcc_cost_t13', type=cost_rule, required=True, help='Cost of energy at 13h.')
milp_parameters_parser.add_argument('pcc_cost_t14', type=cost_rule, required=True, help='Cost of energy at 14h.')
milp_parameters_parser.add_argument('pcc_cost_t15', type=cost_rule, required=True, help='Cost of energy at 15h.')
milp_parameters_parser.add_argument('pcc_cost_t16', type=cost_rule, required=True, help='Cost of energy at 16h.')
milp_parameters_parser.add_argument('pcc_cost_t17', type=cost_rule, required=True, help='Cost of energy at 17h.')
milp_parameters_parser.add_argument('pcc_cost_t18', type=cost_rule, required=True, help='Cost of energy at 18h.')
milp_parameters_parser.add_argument('pcc_cost_t19', type=cost_rule, required=True, help='Cost of energy at 19h.')
milp_parameters_parser.add_argument('pcc_cost_t20', type=cost_rule, required=True, help='Cost of energy at 20h.')
milp_parameters_parser.add_argument('pcc_cost_t21', type=cost_rule, required=True, help='Cost of energy at 21h.')
milp_parameters_parser.add_argument('pcc_cost_t22', type=cost_rule, required=True, help='Cost of energy at 22h.')
milp_parameters_parser.add_argument('pcc_cost_t23', type=cost_rule, required=True, help='Cost of energy at 23h.')
milp_parameters_parser.add_argument('pcc_cost_t24', type=cost_rule, required=True, help='Cost of energy at 24h.')
milp_parameters_parser.add_argument('load_pred_error', type=voltage_rule, required=True, help='Load prediction error.')
milp_parameters_parser.add_argument('pv_generation_pred_error', type=voltage_rule, required=True, help='PV generation prediction error.')
milp_parameters_parser.add_argument('genset_cost', type=cost_rule, required=True, help='Cost of the genset.')
milp_parameters_parser.add_argument('max_power_pcc_kw', type=max_power_rule, required=True, help='Maximum power of the PCC.')
milp_parameters_parser.add_argument('load_curt_cost', type=cost_rule, required=True, help='Cost of the load curtailment.')

# Parser for put
milp_parameters_update_parser = milp_parameters_namespace.parser()
milp_parameters_update_parser.add_argument('min_voltage_pu', type=voltage_rule, required=False, help='Minimum voltage [p.u.] of the microgrid.')
milp_parameters_update_parser.add_argument('max_voltage_pu', type=nominal_voltage_rule, required=False, help='Maximum voltage [p.u.] of the microgrid.')
milp_parameters_update_parser.add_argument('nominal_voltage_kv', type=nominal_voltage_rule, required=False, help='Nominal voltage [kV] of the microgrid.')
milp_parameters_update_parser.add_argument('num_blocks_linearization', type=num_blocks, required=False, help='Number of blocks of linearization, p.e. 20.')
milp_parameters_update_parser.add_argument('pcc_cost_t01', type=cost_rule, required=False, help='Cost of energy at 01h.')
milp_parameters_update_parser.add_argument('pcc_cost_t02', type=cost_rule, required=False, help='Cost of energy at 02h.')
milp_parameters_update_parser.add_argument('pcc_cost_t03', type=cost_rule, required=False, help='Cost of energy at 03h.')
milp_parameters_update_parser.add_argument('pcc_cost_t04', type=cost_rule, required=False, help='Cost of energy at 04h.')
milp_parameters_update_parser.add_argument('pcc_cost_t05', type=cost_rule, required=False, help='Cost of energy at 05h.')
milp_parameters_update_parser.add_argument('pcc_cost_t06', type=cost_rule, required=False, help='Cost of energy at 06h.')
milp_parameters_update_parser.add_argument('pcc_cost_t07', type=cost_rule, required=False, help='Cost of energy at 07h.')
milp_parameters_update_parser.add_argument('pcc_cost_t08', type=cost_rule, required=False, help='Cost of energy at 08h.')
milp_parameters_update_parser.add_argument('pcc_cost_t09', type=cost_rule, required=False, help='Cost of energy at 09h.')
milp_parameters_update_parser.add_argument('pcc_cost_t10', type=cost_rule, required=False, help='Cost of energy at 10h.')
milp_parameters_update_parser.add_argument('pcc_cost_t11', type=cost_rule, required=False, help='Cost of energy at 11h.')
milp_parameters_update_parser.add_argument('pcc_cost_t12', type=cost_rule, required=False, help='Cost of energy at 12h.')
milp_parameters_update_parser.add_argument('pcc_cost_t13', type=cost_rule, required=False, help='Cost of energy at 13h.')
milp_parameters_update_parser.add_argument('pcc_cost_t14', type=cost_rule, required=False, help='Cost of energy at 14h.')
milp_parameters_update_parser.add_argument('pcc_cost_t15', type=cost_rule, required=False, help='Cost of energy at 15h.')
milp_parameters_update_parser.add_argument('pcc_cost_t16', type=cost_rule, required=False, help='Cost of energy at 16h.')
milp_parameters_update_parser.add_argument('pcc_cost_t17', type=cost_rule, required=False, help='Cost of energy at 17h.')
milp_parameters_update_parser.add_argument('pcc_cost_t18', type=cost_rule, required=False, help='Cost of energy at 18h.')
milp_parameters_update_parser.add_argument('pcc_cost_t19', type=cost_rule, required=False, help='Cost of energy at 19h.')
milp_parameters_update_parser.add_argument('pcc_cost_t20', type=cost_rule, required=False, help='Cost of energy at 20h.')
milp_parameters_update_parser.add_argument('pcc_cost_t21', type=cost_rule, required=False, help='Cost of energy at 21h.')
milp_parameters_update_parser.add_argument('pcc_cost_t22', type=cost_rule, required=False, help='Cost of energy at 22h.')
milp_parameters_update_parser.add_argument('pcc_cost_t23', type=cost_rule, required=False, help='Cost of energy at 23h.')
milp_parameters_update_parser.add_argument('pcc_cost_t24', type=cost_rule, required=False, help='Cost of energy at 24h.')
milp_parameters_update_parser.add_argument('load_pred_error', type=voltage_rule, required=False, help='Load prediction error.')
milp_parameters_update_parser.add_argument('pv_generation_pred_error', type=voltage_rule, required=False, help='PV generation prediction error.')
milp_parameters_update_parser.add_argument('genset_cost', type=cost_rule, required=False, help='Cost of the genset.')
milp_parameters_update_parser.add_argument('max_power_pcc_kw', type=max_power_rule, required=False, help='Maximum power of the PCC.')
milp_parameters_update_parser.add_argument('load_curt_cost', type=cost_rule, required=False, help='Cost of the load curtailment.')


model = {
    'id': fields.Integer(),
    'min_voltage_pu': fields.Float(),
    'max_voltage_pu': fields.Float(),
    'nominal_voltage_kv': fields.Float(),
    'num_blocks_linearization': fields.Integer(),
    'pcc_cost_t01': fields.Float(),
    'pcc_cost_t02': fields.Float(),
    'pcc_cost_t03': fields.Float(),
    'pcc_cost_t04': fields.Float(),
    'pcc_cost_t05': fields.Float(),
    'pcc_cost_t06': fields.Float(),
    'pcc_cost_t07': fields.Float(),
    'pcc_cost_t08': fields.Float(),
    'pcc_cost_t09': fields.Float(),
    'pcc_cost_t10': fields.Float(),
    'pcc_cost_t11': fields.Float(),
    'pcc_cost_t12': fields.Float(),
    'pcc_cost_t13': fields.Float(),
    'pcc_cost_t14': fields.Float(),
    'pcc_cost_t15': fields.Float(),
    'pcc_cost_t16': fields.Float(),
    'pcc_cost_t17': fields.Float(),
    'pcc_cost_t18': fields.Float(),
    'pcc_cost_t19': fields.Float(),
    'pcc_cost_t20': fields.Float(),
    'pcc_cost_t21': fields.Float(),
    'pcc_cost_t22': fields.Float(),
    'pcc_cost_t23': fields.Float(),
    'pcc_cost_t24': fields.Float(),
    'load_pred_error': fields.Float(),
    'pv_generation_pred_error': fields.Float(),
    'genset_cost': fields.Float(),
    'max_power_pcc_kw': fields.Float(),
    'load_curt_cost': fields.Float(),
}
parameters_model = milp_parameters_namespace.model('milp_parameters', model)

# ENDPOINT /v1/api/milp_parameters/ -> GET all and POST one parameters of the model
@milp_parameters_namespace.route('/')
class milp_parameters_ListCreate(Resource):

    @milp_parameters_namespace.doc('list_parameters')
    @milp_parameters_namespace.marshal_with(parameters_model, as_list=True)
    def get(self):
        '''
        Retrieves all parameters
        '''
        parameter = (milp_parameters_model
                    .query
                    .order_by('id')
                    .all())
        return parameter

    @milp_parameters_namespace.doc('create_parameter')
    @milp_parameters_namespace.expect(milp_parameters_parser)
    @milp_parameters_namespace.marshal_with(parameters_model, code=http.client.CREATED)
    def post(self):
        '''
        Creates a new parameter
        '''

        args = milp_parameters_parser.parse_args()

        new_parameter = milp_parameters_model(min_voltage_pu=args['min_voltage_pu'],
                            max_voltage_pu=args['max_voltage_pu'],
                            nominal_voltage_kv=args['nominal_voltage_kv'],
                            num_blocks_linearization=args['num_blocks_linearization'],
                            pcc_cost_t01=args['pcc_cost_t01'],
                            pcc_cost_t02=args['pcc_cost_t02'],
                            pcc_cost_t03=args['pcc_cost_t03'],
                            pcc_cost_t04=args['pcc_cost_t04'],
                            pcc_cost_t05=args['pcc_cost_t05'],
                            pcc_cost_t06=args['pcc_cost_t06'],
                            pcc_cost_t07=args['pcc_cost_t07'],
                            pcc_cost_t08=args['pcc_cost_t08'],
                            pcc_cost_t09=args['pcc_cost_t09'],
                            pcc_cost_t10=args['pcc_cost_t10'],
                            pcc_cost_t11=args['pcc_cost_t11'],
                            pcc_cost_t12=args['pcc_cost_t12'],
                            pcc_cost_t13=args['pcc_cost_t13'],
                            pcc_cost_t14=args['pcc_cost_t14'],
                            pcc_cost_t15=args['pcc_cost_t15'],
                            pcc_cost_t16=args['pcc_cost_t16'],
                            pcc_cost_t17=args['pcc_cost_t17'],
                            pcc_cost_t18=args['pcc_cost_t18'],
                            pcc_cost_t19=args['pcc_cost_t19'],
                            pcc_cost_t20=args['pcc_cost_t20'],
                            pcc_cost_t21=args['pcc_cost_t21'],
                            pcc_cost_t22=args['pcc_cost_t22'],
                            pcc_cost_t23=args['pcc_cost_t23'],
                            pcc_cost_t24=args['pcc_cost_t23'],
                            load_pred_error=args['load_pred_error'],
                            pv_generation_pred_error=args['pv_generation_pred_error'],
                            genset_cost=args['genset_cost'],
                            max_power_pcc_kw=args['max_power_pcc_kw'],
                            load_curt_cost=args['load_curt_cost'])


        try:
            db.session.add(new_parameter)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})

        result = milp_parameters_namespace.marshal(new_parameter, parameters_model)

        return result, http.client.CREATED

# ENDPOINT /v1/api/milp_parameters/x/ -> GET or DELETE one parameter with id=x
@milp_parameters_namespace.route('/<int:parameter_id>/')
class milp_parameters_Retrieve(Resource):

#    def options (self, parameter_id):
#        return {'Allow' : 'PUT' }, 200, \
#        { 'Access-Control-Allow-Origin': '*', \
#        {'Access-Control-Allow-Methods' : 'PUT,GET' }

    @milp_parameters_namespace.doc('retrieve_parameter')
    @milp_parameters_namespace.marshal_with(parameters_model)
    def get(self, parameter_id):
        '''
        Retrieves a parameter with parameter_id
        '''
        parameter = milp_parameters_model.query.get(parameter_id)
        if not parameter:
            # The parameter is not present
            return '', http.client.NOT_FOUND

        return parameter

    @milp_parameters_namespace.doc('delete_parameter',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, parameter_id):
        '''
        Deletes a parameter
        '''
        parameter = milp_parameters_model.query.get(parameter_id)
        if not parameter:
            # The parameter is not present
            return '', http.client.NO_CONTENT

        db.session.delete(parameter)
        db.session.commit()

        return '', http.client.NO_CONTENT

    @milp_parameters_namespace.doc('Update_milp_parameters')
    @milp_parameters_namespace.marshal_with(parameters_model)
    @milp_parameters_namespace.expect(milp_parameters_update_parser)
    def put(self, parameter_id):
        '''
        Updates milp_parameters based on name or id
        '''

        args = milp_parameters_update_parser.parse_args()

        data = {
            'min_voltage_pu': args['min_voltage_pu'],
            'max_voltage_pu': args['max_voltage_pu'],
            'nominal_voltage_kv': args['nominal_voltage_kv'],
            'num_blocks_linearization': args['num_blocks_linearization'],
            'pcc_cost_t01': args['pcc_cost_t01'],
            'pcc_cost_t02': args['pcc_cost_t02'],
            'pcc_cost_t03': args['pcc_cost_t03'],
            'pcc_cost_t04': args['pcc_cost_t04'],
            'pcc_cost_t05': args['pcc_cost_t05'],
            'pcc_cost_t06': args['pcc_cost_t06'],
            'pcc_cost_t07': args['pcc_cost_t07'],
            'pcc_cost_t08': args['pcc_cost_t08'],
            'pcc_cost_t09': args['pcc_cost_t09'],
            'pcc_cost_t10': args['pcc_cost_t10'],
            'pcc_cost_t11': args['pcc_cost_t11'],
            'pcc_cost_t12': args['pcc_cost_t12'],
            'pcc_cost_t13': args['pcc_cost_t13'],
            'pcc_cost_t14': args['pcc_cost_t14'],
            'pcc_cost_t15': args['pcc_cost_t15'],
            'pcc_cost_t16': args['pcc_cost_t16'],
            'pcc_cost_t17': args['pcc_cost_t17'],
            'pcc_cost_t18': args['pcc_cost_t18'],
            'pcc_cost_t19': args['pcc_cost_t19'],
            'pcc_cost_t20': args['pcc_cost_t20'],
            'pcc_cost_t21': args['pcc_cost_t21'],
            'pcc_cost_t22': args['pcc_cost_t22'],
            'pcc_cost_t23': args['pcc_cost_t23'],
            'pcc_cost_t24': args['pcc_cost_t24'],
            'load_pred_error': args['load_pred_error'],
            'pv_generation_pred_error': args['pv_generation_pred_error'],
            'genset_cost': args['genset_cost'],
            'max_power_pcc_kw': args['max_power_pcc_kw'],
            'load_curt_cost': args['load_curt_cost']
        }
        
        query = milp_parameters_model.query.get(parameter_id)
        if not query:
            # The query is not present
            return '', http.client.NO_CONTENT
        else:
            for key in data:
                if data[key]:
                    setattr(query, key, data[key])
            db.session.commit()
            return query
