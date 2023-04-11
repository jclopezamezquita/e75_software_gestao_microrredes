import http.client
from datetime import datetime, timedelta
import dateutil.relativedelta
# from flask_restplus import Namespace, Resource, fields, inputs, abort
from flask_restx import Namespace, Resource, fields, inputs, abort
from api_tools.models import branch_information_model
from api_tools.models import node_information_model
from api_tools.db import db
from sqlalchemy import exc
import requests
import json


def impedance_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

impedance_rule.__schema__ = {
    "type": "number",
    "format": "impedance_rule",
}

def max_current_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value <= 0.0:
        raise ValueError(' Invalid value!')
    return value

max_current_rule.__schema__ = {
    "type": "number",
    "format": "max_current_rule",
}

# Criação do branch_information_namespace e dos parsers
branch_information_namespace = Namespace('v1/api/branch_information', description='API backend EMS - Branch information')

# Parser for post
branch_information_parser = branch_information_namespace.parser()
branch_information_parser.add_argument('name', type=str, required=True, help='Name of the branch')
branch_information_parser.add_argument('initial_node', type=str, required=True, help='Initial node of the branch')
branch_information_parser.add_argument('end_node', type=str, required=True, help='End node of the branch')
branch_information_parser.add_argument('resistance_aa', type=impedance_rule, required=True, help='Resistance (Ohm) phase a')
branch_information_parser.add_argument('resistance_bb', type=impedance_rule, required=True, help='Resistance (Ohm) phase b')
branch_information_parser.add_argument('resistance_cc', type=impedance_rule, required=True, help='Resistance (Ohm) phase c')
branch_information_parser.add_argument('resistance_ab', type=impedance_rule, required=False, help='Resistance (Ohm) phase ab')
branch_information_parser.add_argument('resistance_ac', type=impedance_rule, required=False, help='Resistance (Ohm) phase ac')
branch_information_parser.add_argument('resistance_bc', type=impedance_rule, required=False, help='Resistance (Ohm) phase bc')
branch_information_parser.add_argument('reactance_aa', type=impedance_rule, required=True, help='Reactance (Ohm) phase a')
branch_information_parser.add_argument('reactance_bb', type=impedance_rule, required=True, help='Reactance (Ohm) phase b')
branch_information_parser.add_argument('reactance_cc', type=impedance_rule, required=True, help='Reactance (Ohm) phase c')
branch_information_parser.add_argument('reactance_ab', type=impedance_rule, required=False, help='Reactance (Ohm) phase ab')
branch_information_parser.add_argument('reactance_ac', type=impedance_rule, required=False, help='Reactance (Ohm) phase ac')
branch_information_parser.add_argument('reactance_bc', type=impedance_rule, required=False, help='Reactance (Ohm) phase bc')
branch_information_parser.add_argument('max_current', type=max_current_rule, required=True, help='Maximum current of the branch')

# Parser for put
branch_information_update_parser = branch_information_namespace.parser()
branch_information_update_parser.add_argument('name', type=str, required=False, help='Name of the branch')
branch_information_update_parser.add_argument('initial_node', type=str, required=False, help='Initial node of the branch')
branch_information_update_parser.add_argument('end_node', type=str, required=False, help='End node of the branch')
branch_information_update_parser.add_argument('resistance_aa', type=impedance_rule, required=False, help='Resistance (Ohm) phase a')
branch_information_update_parser.add_argument('resistance_bb', type=impedance_rule, required=False, help='Resistance (Ohm) phase b')
branch_information_update_parser.add_argument('resistance_cc', type=impedance_rule, required=False, help='Resistance (Ohm) phase c')
branch_information_update_parser.add_argument('resistance_ab', type=impedance_rule, required=False, help='Resistance (Ohm) phase ab')
branch_information_update_parser.add_argument('resistance_ac', type=impedance_rule, required=False, help='Resistance (Ohm) phase ac')
branch_information_update_parser.add_argument('resistance_bc', type=impedance_rule, required=False, help='Resistance (Ohm) phase bc')
branch_information_update_parser.add_argument('reactance_aa', type=impedance_rule, required=False, help='Reactance (Ohm) phase a')
branch_information_update_parser.add_argument('reactance_bb', type=impedance_rule, required=False, help='Reactance (Ohm) phase b')
branch_information_update_parser.add_argument('reactance_cc', type=impedance_rule, required=False, help='Reactance (Ohm) phase c')
branch_information_update_parser.add_argument('reactance_ab', type=impedance_rule, required=False, help='Reactance (Ohm) phase ab')
branch_information_update_parser.add_argument('reactance_ac', type=impedance_rule, required=False, help='Reactance (Ohm) phase ac')
branch_information_update_parser.add_argument('reactance_bc', type=impedance_rule, required=False, help='Reactance (Ohm) phase bc')
branch_information_update_parser.add_argument('max_current', type=max_current_rule, required=False, help='Maximum current of the branch')

model = {
    'id': fields.Integer(),
    'name': fields.String(),
    'initial_node': fields.String(),
    'end_node': fields.String(),
    'resistance_aa': fields.Float(),
    'resistance_bb': fields.Float(),
    'resistance_cc': fields.Float(),
    'resistance_ab': fields.Float(),
    'resistance_ac': fields.Float(),
    'resistance_bc': fields.Float(),
    'reactance_aa': fields.Float(),
    'reactance_bb': fields.Float(),
    'reactance_cc': fields.Float(),
    'reactance_ab': fields.Float(),
    'reactance_ac': fields.Float(),
    'reactance_bc': fields.Float(),
    'max_current': fields.Float(),
}
branch_model = branch_information_namespace.model('branch_information', model)


# ENDPOINT /v1/api/branch_information/ -> GET all and POST one branch
@branch_information_namespace.route('/')
class branch_information_ListCreate(Resource):

    @branch_information_namespace.doc('list_branchs')
    @branch_information_namespace.marshal_with(branch_model, as_list=True)
    def get(self):
        '''
        Retrieves all branchs
        '''
        branch = (branch_information_model
                    .query
                    .order_by('id')
                    .all())
        return branch

    @branch_information_namespace.doc('create_branch')
    @branch_information_namespace.expect(branch_information_parser)
    @branch_information_namespace.marshal_with(branch_model, code=http.client.CREATED)
    def post(self):
        '''
        Creates a new branch
        '''

        args = branch_information_parser.parse_args()

        new_branch = branch_information_model(name=args['name'],
                            initial_node=args['initial_node'],
                            end_node=args['end_node'],
                            resistance_aa=args['resistance_aa'],
                            resistance_bb=args['resistance_bb'],
                            resistance_cc=args['resistance_cc'],
                            resistance_ab=args['resistance_ab'],
                            resistance_ac=args['resistance_ac'],
                            resistance_bc=args['resistance_bc'],
                            reactance_aa=args['reactance_aa'],
                            reactance_bb=args['reactance_bb'],
                            reactance_cc=args['reactance_cc'],
                            reactance_ab=args['reactance_ab'],
                            reactance_ac=args['reactance_ac'],
                            reactance_bc=args['reactance_bc'],
                            max_current=args['max_current'])
        
        new_query = node_information_model.query.filter((node_information_model.name == new_branch.initial_node))
        if not new_query.all():
            return abort(405, 'Input payload validation failed', errors={'type' : 'initial_node has not been registered'})
        new_query = node_information_model.query.filter((node_information_model.name == new_branch.end_node))
        if not new_query.all():
            return abort(405, 'Input payload validation failed', errors={'type' : 'end_node has not been registered'})

        try:
            db.session.add(new_branch)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})

        result = branch_information_namespace.marshal(new_branch, branch_model)

        return result, http.client.CREATED


# ENDPOINT /v1/api/branch_information/x/ -> GET or DELETE one branch with id=x
@branch_information_namespace.route('/<int:branch_id>/')
class branch_information_Retrieve(Resource):

    @branch_information_namespace.doc('retrieve_branch')
    @branch_information_namespace.marshal_with(branch_model)
    def get(self, branch_id):
        '''
        Retrieves a branch with branch_id
        '''
        branch = branch_information_model.query.get(branch_id)
        if not branch:
            # The branch is not present
            return '', http.client.NOT_FOUND

        return branch

    @branch_information_namespace.doc('delete_branch',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, branch_id):
        '''
        Deletes a branch
        '''
        branch = branch_information_model.query.get(branch_id)
        if not branch:
            # The branch is not present
            return '', http.client.NO_CONTENT

        db.session.delete(branch)
        db.session.commit()

        return '', http.client.NO_CONTENT

    @branch_information_namespace.doc('Update_branch_information')
    @branch_information_namespace.marshal_with(branch_model)
    @branch_information_namespace.expect(branch_information_update_parser)
    def put(self, branch_id):
        '''
        Updates branch_information based on name or id
        '''

        args = branch_information_update_parser.parse_args()

        data = {
            'name': args['name'],
            'initial_node': args['initial_node'],
            'end_node': args['end_node'],
            'resistance_aa': args['resistance_aa'],
            'resistance_bb': args['resistance_bb'],
            'resistance_cc': args['resistance_cc'],
            'resistance_ab': args['resistance_ab'],
            'resistance_ac': args['resistance_ac'],
            'resistance_bc': args['resistance_bc'],
            'reactance_aa': args['reactance_aa'],
            'reactance_bb': args['reactance_bb'],
            'reactance_cc': args['reactance_cc'],
            'reactance_ab': args['reactance_ab'],
            'reactance_ac': args['reactance_ac'],
            'reactance_bc': args['reactance_bc'],
            'max_current': args['max_current']
        }

        query = branch_information_model.query.get(branch_id)
        if not query:
            # The query is not present
            return '', http.client.NO_CONTENT
        else:
            for key in data:
                if data[key]:
                    setattr(query, key, data[key])
            db.session.commit()
            return query
