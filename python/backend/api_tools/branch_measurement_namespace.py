import sys
import http.client
from sqlalchemy import exc
from datetime import datetime
from flask_restplus import Namespace, Resource, fields, inputs, abort
from api_tools.models import branch_measurement_model, branch_information_model
from api_tools.db import db
from calendar import monthrange


def power_flow_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    return value

power_flow_rule.__schema__ = {
    "type": "number",
    "format": "power_flow_rule",
}



branch_measurement_namespace = Namespace('v1/api/branch_measurement', description='API backend EMS - Branch measurement')

branch_measurement_parser = branch_measurement_namespace.parser()
branch_measurement_parser.add_argument('time_iso',
                        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S.%f'),
                        required=True,
                        help='Datetime of the measuarement (timestamp in iso-format, p.e. 2021-07-27T14:31:00.000)')
branch_measurement_parser.add_argument('active_power_flow_a_kw', type=power_flow_rule, required=True, help='Active power flow of phase a (kW).')
branch_measurement_parser.add_argument('active_power_flow_b_kw', type=power_flow_rule, required=True, help='Active power flow of phase b (kW).')
branch_measurement_parser.add_argument('active_power_flow_c_kw', type=power_flow_rule, required=True, help='Active power flow of phase c (kW).')
branch_measurement_parser.add_argument('reactive_power_flow_a_kvar', type=power_flow_rule, required=True, help='Reactive power flow of phase a (kVar).')
branch_measurement_parser.add_argument('reactive_power_flow_b_kvar', type=power_flow_rule, required=True, help='Reactive power flow of phase b (kVar).')
branch_measurement_parser.add_argument('reactive_power_flow_c_kvar', type=power_flow_rule, required=True, help='Reactive power flow of phase c (kVar).')
branch_measurement_parser.add_argument('current_a_A', type=power_flow_rule, required=True, help='Current of phase a (A).')
branch_measurement_parser.add_argument('current_b_A', type=power_flow_rule, required=True, help='Current of phase b (A).')
branch_measurement_parser.add_argument('current_c_A', type=power_flow_rule, required=True, help='Current of phase c (A).')

model = {
    'id': fields.Integer(),
    'name': fields.String(),
    'time_iso' : fields.DateTime(),
    'active_power_flow_a_kw' : fields.Float(),
    'active_power_flow_b_kw' : fields.Float(),
    'active_power_flow_c_kw' : fields.Float(),
    'reactive_power_flow_a_kvar' : fields.Float(),
    'reactive_power_flow_b_kvar' : fields.Float(),
    'reactive_power_flow_c_kvar' : fields.Float(),
    'current_a_A' : fields.Float(),
    'current_b_A' : fields.Float(),
    'current_c_A' : fields.Float(),
}
measurement_model = branch_measurement_namespace.model('branch_measurement', model)


# ENDPOINT /v1/api/branch_measurement/ -> GET all measurements
@branch_measurement_namespace.route('/')
class branch_measurement_list(Resource):

    @branch_measurement_namespace.doc('branch_measurement')
    @branch_measurement_namespace.marshal_with(measurement_model, as_list=True)
    def get(self):
        '''
        Retrieves all measurements
        '''

        parameters = [branch_measurement_model.id, branch_information_model.name, branch_measurement_model.time_iso, branch_measurement_model.active_power_flow_a_kw, 
            branch_measurement_model.active_power_flow_b_kw, branch_measurement_model.active_power_flow_c_kw, branch_measurement_model.reactive_power_flow_a_kvar,
            branch_measurement_model.reactive_power_flow_b_kvar, branch_measurement_model.reactive_power_flow_c_kvar, branch_measurement_model.current_a_A,
            branch_measurement_model.current_b_A, branch_measurement_model.current_c_A]
        
        main_query = branch_measurement_model.query.join(branch_information_model).with_entities(*parameters)
        measurements = (main_query.all())
        # print(measurements)

        return measurements

# ENDPOINT /v1/api/branch_measurement/no/x/ -> GET all measurements from a parent branch x
@branch_measurement_namespace.route('/branch/<int:id_info_ramo>/')
class branch_measurement_ListCreateFromParent(Resource):

    @branch_measurement_namespace.doc('retrieve_measurements_from_parent')
    @branch_measurement_namespace.marshal_with(measurement_model)
    def get(self, id_info_ramo):
        '''
        Retrieves measurements from id_info_ramo
        '''

        parameters = [branch_measurement_model.id, branch_information_model.name, branch_measurement_model.time_iso, branch_measurement_model.active_power_flow_a_kw, 
            branch_measurement_model.active_power_flow_b_kw, branch_measurement_model.active_power_flow_c_kw, branch_measurement_model.reactive_power_flow_a_kvar,
            branch_measurement_model.reactive_power_flow_b_kvar, branch_measurement_model.reactive_power_flow_c_kvar, branch_measurement_model.current_a_A,
            branch_measurement_model.current_b_A, branch_measurement_model.current_c_A]

        main_query = branch_measurement_model.query.join(branch_information_model).with_entities(*parameters)
        measurements = (main_query.all())
        measurements = (main_query.filter(branch_measurement_model.id_info_ramo == id_info_ramo).all())

        if not measurements:
            # The measurements is not present
            return '', http.client.NOT_FOUND

        return measurements

    @branch_measurement_namespace.doc('create_measurement_from_parent')
    @branch_measurement_namespace.expect(branch_measurement_parser)
    @branch_measurement_namespace.marshal_with(measurement_model, code=http.client.CREATED)
    def post(self, id_info_ramo):
        '''
        Creates new measurements for id_info_ramo
        '''

        # Verify if branch exists
        branch = branch_information_model.query.get(id_info_ramo)
        if not branch:
            # The node is not present
            return '', http.client.NOT_FOUND

        args = branch_measurement_parser.parse_args()


        new_measurement = branch_measurement_model(time_iso=args['time_iso'],
                            active_power_flow_a_kw=args['active_power_flow_a_kw'],
                            active_power_flow_b_kw=args['active_power_flow_b_kw'],
                            active_power_flow_c_kw=args['active_power_flow_c_kw'],
                            reactive_power_flow_a_kvar=args['reactive_power_flow_a_kvar'],
                            reactive_power_flow_b_kvar=args['reactive_power_flow_b_kvar'],
                            reactive_power_flow_c_kvar=args['reactive_power_flow_c_kvar'],
                            current_a_A=args['current_a_A'],
                            current_b_A=args['current_b_A'],
                            current_c_A=args['current_c_A'],                   
                            id_info_ramo=id_info_ramo)

        try:
            db.session.add(new_measurement)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})
            

        parameters = [branch_measurement_model.id, branch_information_model.name, branch_measurement_model.time_iso, branch_measurement_model.active_power_flow_a_kw, 
            branch_measurement_model.active_power_flow_b_kw, branch_measurement_model.active_power_flow_c_kw, branch_measurement_model.reactive_power_flow_a_kvar,
            branch_measurement_model.reactive_power_flow_b_kvar, branch_measurement_model.reactive_power_flow_c_kvar, branch_measurement_model.current_a_A,
            branch_measurement_model.current_b_A, branch_measurement_model.current_c_A]
        main_query = branch_measurement_model.query.join(branch_information_model).with_entities(*parameters)

        measurements = (main_query.order_by(branch_measurement_model.id.desc()).first())

        result = branch_measurement_namespace.marshal(measurements, measurement_model)

        return result, http.client.CREATED

    @branch_measurement_namespace.doc('delete_measurement',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, id_info_ramo):
        '''
        Deletes all measurements from id_info_ramo
        '''
        
        parameters = [branch_measurement_model.id, branch_information_model.name, branch_measurement_model.time_iso, branch_measurement_model.active_power_flow_a_kw, 
            branch_measurement_model.active_power_flow_b_kw, branch_measurement_model.active_power_flow_c_kw, branch_measurement_model.reactive_power_flow_a_kvar,
            branch_measurement_model.reactive_power_flow_b_kvar, branch_measurement_model.reactive_power_flow_c_kvar, branch_measurement_model.current_a_A,
            branch_measurement_model.current_b_A, branch_measurement_model.current_c_A]
        main_query = branch_measurement_model.query.join(branch_information_model).with_entities(*parameters)
        measurements = (main_query.all())
        measurements = (main_query.filter(branch_measurement_model.id_info_ramo == id_info_ramo).all())

        if not measurements:
            # The branch is not present
            return '', http.client.NO_CONTENT

        # db.session.delete(measurements)
        branch_measurement_model.query.filter(branch_measurement_model.id_info_ramo == id_info_ramo).delete()
        db.session.commit()

        return '', http.client.NO_CONTENT
