import http.client
from datetime import datetime, timedelta
import dateutil.relativedelta
# from flask_restplus import Namespace, Resource, fields, inputs, abort
from flask_restx import Namespace, Resource, fields, inputs, abort
from api_tools.models import ev_parameters_model
from api_tools.db import db
from sqlalchemy import exc
import requests
import json


def time_rule(value):
    try:
        value = int(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= -0.1:
        raise ValueError(' Invalid time!')
    if value >= 24.1:
        raise ValueError(' Invalid time!')
    return value

time_rule.__schema__ = {
    "type": "number",
    "format": "time_rule",
}

def power_and_energy_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= -0.000000001:
        raise ValueError(' Invalid Power or Energy!')
    return value

power_and_energy_rule.__schema__ = {
    "type": "number",
    "format": "power_and_energy",
}

def soc_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= -0.000000001:
        raise ValueError(' Invalid SoC!')
    if value >= 100.00000001:
        raise ValueError(' Invalid SoC!')
    return value

soc_rule.__schema__ = {
    "type": "number",
    "format": "soc_rule",
}


# Criação do ev_parameters_namespace e dos parsers
ev_parameters_namespace = Namespace('v1/api/ev_parameters', description='API backend EMS - EV parameters')

# Parser for post
ev_parameters_parser = ev_parameters_namespace.parser()
ev_parameters_parser.add_argument('EV_battery_size_1', type=power_and_energy_rule, required=True, help='Size of the battery 1.')
ev_parameters_parser.add_argument('EV_power_size_1', type=power_and_energy_rule, required=True, help='Power of the charger 1.')
ev_parameters_parser.add_argument('EV_initial_SoC_1', type=soc_rule, required=True, help='Initial SoC of EV 1.')
ev_parameters_parser.add_argument('EV_arrival_time_1', type=time_rule, required=True, help='Time of arrival EV 1.')
ev_parameters_parser.add_argument('EV_departure_time_1', type=time_rule, required=True, help='Time of departure EV 1.')
ev_parameters_parser.add_argument('EV_battery_size_2', type=power_and_energy_rule, required=True, help='Size of the battery 2.')
ev_parameters_parser.add_argument('EV_power_size_2', type=power_and_energy_rule, required=True, help='Power of the charger 2.')
ev_parameters_parser.add_argument('EV_initial_SoC_2', type=soc_rule, required=True, help='Initial SoC of EV 2.')
ev_parameters_parser.add_argument('EV_arrival_time_2', type=time_rule, required=True, help='Time of arrival EV 2.')
ev_parameters_parser.add_argument('EV_departure_time_2', type=time_rule, required=True, help='Time of departure EV 2.')

# Parser for put
ev_parameters_update_parser = ev_parameters_namespace.parser()
ev_parameters_update_parser.add_argument('EV_battery_size_1', type=power_and_energy_rule, required=False, help='Size of the battery 1')
ev_parameters_update_parser.add_argument('EV_power_size_1', type=power_and_energy_rule, required=False, help='Power of the charger 1.')
ev_parameters_update_parser.add_argument('EV_initial_SoC_1', type=soc_rule, required=False, help='Initial SoC of EV 1.')
ev_parameters_update_parser.add_argument('EV_arrival_time_1', type=time_rule, required=False, help='Time of arrival EV 1.')
ev_parameters_update_parser.add_argument('EV_departure_time_1', type=time_rule, required=False, help='Time of departure EV 1.')
ev_parameters_update_parser.add_argument('EV_battery_size_2', type=power_and_energy_rule, required=False, help='Size of the battery 2.')
ev_parameters_update_parser.add_argument('EV_power_size_2', type=power_and_energy_rule, required=False, help='Power of the charger 2.')
ev_parameters_update_parser.add_argument('EV_initial_SoC_2', type=soc_rule, required=False, help='Initial SoC of EV 2.')
ev_parameters_update_parser.add_argument('EV_arrival_time_2', type=time_rule, required=False, help='Time of arrival EV 2.')
ev_parameters_update_parser.add_argument('EV_departure_time_2', type=time_rule, required=False, help='Time of departure EV 2.')


model = {
    'id': fields.Integer(),
    'EV_battery_size_1': fields.Float(),
    'EV_power_size_1': fields.Float(),
    'EV_initial_SoC_1': fields.Float(),
    'EV_arrival_time_1': fields.Integer(),
    'EV_departure_time_1': fields.Integer(),
    'EV_battery_size_2': fields.Float(),
    'EV_power_size_2': fields.Float(),
    'EV_initial_SoC_2': fields.Float(),
    'EV_arrival_time_2': fields.Integer(),
    'EV_departure_time_2': fields.Integer(),
}
parameters_model = ev_parameters_namespace.model('ev_parameters', model)

# ENDPOINT /v1/api/ev_parameters/ -> GET all and POST one parameters of the model
@ev_parameters_namespace.route('/')
class ev_parameters_ListCreate(Resource):

    @ev_parameters_namespace.doc('list_parameters')
    @ev_parameters_namespace.marshal_with(parameters_model, as_list=True)
    def get(self):
        '''
        Retrieves all parameters
        '''
        parameter = (ev_parameters_model
                    .query
                    .order_by('id')
                    .all())
        return parameter

    @ev_parameters_namespace.doc('create_parameter')
    @ev_parameters_namespace.expect(ev_parameters_parser)
    @ev_parameters_namespace.marshal_with(parameters_model, code=http.client.CREATED)
    def post(self):
        '''
        Creates a new parameter
        '''

        args = ev_parameters_parser.parse_args()

        new_parameter = ev_parameters_model(EV_battery_size_1=args['EV_battery_size_1'],
                            EV_power_size_1=args['EV_power_size_1'],
                            EV_initial_SoC_1=args['EV_initial_SoC_1'],
                            EV_arrival_time_1=args['EV_arrival_time_1'],
                            EV_departure_time_1=args['EV_departure_time_1'],
                            EV_battery_size_2=args['EV_battery_size_2'],
                            EV_power_size_2=args['EV_power_size_2'],
                            EV_initial_SoC_2=args['EV_initial_SoC_2'],
                            EV_arrival_time_2=args['EV_arrival_time_2'],
                            EV_departure_time_2=args['EV_departure_time_2'])


        try:
            db.session.add(new_parameter)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})

        result = ev_parameters_namespace.marshal(new_parameter, parameters_model)

        return result, http.client.CREATED

# ENDPOINT /v1/api/ev_parameters/x/ -> GET or DELETE one parameter with id=x
@ev_parameters_namespace.route('/<int:parameter_id>/')
class ev_parameters_Retrieve(Resource):

#    def options (self, parameter_id):
#        return {'Allow' : 'PUT' }, 200, \
#        { 'Access-Control-Allow-Origin': '*', \
#        {'Access-Control-Allow-Methods' : 'PUT,GET' }

    @ev_parameters_namespace.doc('retrieve_parameter')
    @ev_parameters_namespace.marshal_with(parameters_model)
    def get(self, parameter_id):
        '''
        Retrieves a parameter with parameter_id
        '''
        parameter = ev_parameters_model.query.get(parameter_id)
        if not parameter:
            # The parameter is not present
            return '', http.client.NOT_FOUND

        return parameter

    @ev_parameters_namespace.doc('delete_parameter',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, parameter_id):
        '''
        Deletes a parameter
        '''
        parameter = ev_parameters_model.query.get(parameter_id)
        if not parameter:
            # The parameter is not present
            return '', http.client.NO_CONTENT

        db.session.delete(parameter)
        db.session.commit()

        return '', http.client.NO_CONTENT

    @ev_parameters_namespace.doc('Update_ev_parameters')
    @ev_parameters_namespace.marshal_with(parameters_model)
    @ev_parameters_namespace.expect(ev_parameters_update_parser)
    def put(self, parameter_id):
        '''
        Updates ev_parameters based on name or id
        '''

        args = ev_parameters_update_parser.parse_args()

        data = {
            'EV_battery_size_1' : args['EV_battery_size_1'],
            'EV_power_size_1': args['EV_power_size_1'],
            'EV_initial_SoC_1' : args['EV_initial_SoC_1'],
            'EV_arrival_time_1' : args['EV_arrival_time_1'],
            'EV_departure_time_1' : args['EV_departure_time_1'],
            'EV_battery_size_2' : args['EV_battery_size_2'],
            'EV_power_size_2' : args['EV_power_size_2'],
            'EV_initial_SoC_2' : args['EV_initial_SoC_2'],
            'EV_arrival_time_2' : args['EV_arrival_time_2'],
            'EV_departure_time_2' : args['EV_departure_time_2']
        }
        
        query = ev_parameters_model.query.get(parameter_id)
        if not query:
            # The query is not present
            return '', http.client.NO_CONTENT
        else:
            for key in data:
                if data[key]:
                    setattr(query, key, data[key])
            db.session.commit()
            return query
