import sys
import http.client
from sqlalchemy import exc
from datetime import datetime
from flask_restplus import Namespace, Resource, fields, inputs, abort
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

