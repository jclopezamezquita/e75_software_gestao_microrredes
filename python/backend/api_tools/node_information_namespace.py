import http.client
from datetime import datetime, timedelta
import dateutil.relativedelta
# from flask_restplus import Namespace, Resource, fields, inputs, abort
from flask_restx import Namespace, Resource, fields, inputs, abort
from api_tools.models import node_information_model
from api_tools.db import db
from sqlalchemy import exc
import requests
import json


def node_type_rule(value):
    try:
        value = str(value)
    except:
        raise ValueError('-> Invalid format!')
    # Lista os tipos de nós
    data = json.load(open('config/node_types.json'))
    # type_list = ["PQ", "PCC", "Ref"]
    # PQ - barra de potencia ativa e reativa constante (carga ou renovável)
    # PCC - Nó do ponto de acoplamento com a rede principal
    # Ref - Nó que vira referência quando a microrrede opera ilhada
    type_list = data['node_types']
    if value not in type_list:
        raise ValueError('-> Invalid value! Please use: \'PQ\', \'PCC\', \'Ref\'')
    return value

node_type_rule.__schema__ = {
    "type": "string",
    "format": "node_type_rule",
}

def der_type_rule(value):
    try:
        value = str(value)
    except:
        raise ValueError('-> Invalid format!')
    # Lista os tipos de DERs
    data = json.load(open('config/der_types.json'))
    # type_list = ["none", "load", "bess", "pv", "genset", "pcc", "ev"]
    type_list = data['der_types']
    if value not in type_list:
        raise ValueError('-> Invalid value! Please use: \'none\', \'load\', \'bess\', \'pv\', \'genset\', \'pcc\', \'ev\'')
    return value

der_type_rule.__schema__ = {
    "type": "string",
    "format": "der_type_rule",
}

def nominal_kva_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

nominal_kva_rule.__schema__ = {
    "type": "number",
    "format": "nominal_kva_rule",
}

def power_factor_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value > 1.0:
        raise ValueError(' Invalid value!')
    if value < -1.0:
        raise ValueError(' Invalid value!')
    return value

power_factor_rule.__schema__ = {
    "type": "number",
    "format": "power_factor_rule",
}

def soc_min_bat_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value > 1.0:
        raise ValueError(' Invalid value!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

soc_min_bat_rule.__schema__ = {
    "type": "number",
    "format": "soc_min_bat_rule",
}

def bat_nom_energy_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

bat_nom_energy_rule.__schema__ = {
    "type": "number",
    "format": "bat_nom_energy_rule",
}

def soc_min_ev_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value > 1.0:
        raise ValueError(' Invalid value!')
    if value < 0.0:
        raise ValueError(' Invalid value!')
    return value

soc_min_ev_rule.__schema__ = {
    "type": "number",
    "format": "soc_min_ev_rule",
}


# Criação do node_information_namespace e dos parsers
node_information_namespace = Namespace('v1/api/node_information', description='API backend EMS - Node information')

# Parser for post
node_information_parser = node_information_namespace.parser()
node_information_parser.add_argument('name', type=str, required=True, help='Name of the node')
node_information_parser.add_argument('type', type=node_type_rule, required=True, help='Type of node')
node_information_parser.add_argument('der', type=der_type_rule, required=True, help='Type of DER')
node_information_parser.add_argument('nominal_kva', type=nominal_kva_rule, required=True, help='Nominal kVA of the DER')
node_information_parser.add_argument('minimum_kva', type=nominal_kva_rule, required=True, help='Minimum kVA of the DER')
node_information_parser.add_argument('maximum_kva', type=nominal_kva_rule, required=True, help='Maximum kVA of the DER')
node_information_parser.add_argument('power_factor', type=power_factor_rule, required=True, help='Power factor of the DER')
node_information_parser.add_argument('soc_min_bat', type=soc_min_bat_rule, required=False, help='Minimum SOC of the BESS')
node_information_parser.add_argument('soc_max_bat', type=soc_min_bat_rule, required=False, help='Maximum SOC of the BESS')
node_information_parser.add_argument('bat_nom_energy', type=bat_nom_energy_rule, required=False, help='Nominal energy of the BESS')
node_information_parser.add_argument('soc_min_ev', type=soc_min_ev_rule, required=False, help='Minimum SOC of the EV')
node_information_parser.add_argument('soc_max_ev', type=soc_min_ev_rule, required=False, help='Maximum SOC of the EV')

# Parser for put
node_information_update_parser = node_information_namespace.parser()
node_information_update_parser.add_argument('name', type=str, required=False, help='Name of the node')
node_information_update_parser.add_argument('type', type=node_type_rule, required=False, help='Type of node')
node_information_update_parser.add_argument('der', type=der_type_rule, required=False, help='Type of DER')
node_information_update_parser.add_argument('nominal_kva', type=nominal_kva_rule, required=False, help='Nominal kVA of the DER')
node_information_update_parser.add_argument('minimum_kva', type=nominal_kva_rule, required=False, help='Minimum kVA of the DER')
node_information_update_parser.add_argument('maximum_kva', type=nominal_kva_rule, required=False, help='Maximum kVA of the DER')
node_information_update_parser.add_argument('power_factor', type=power_factor_rule, required=False, help='Power factor of the DER')
node_information_update_parser.add_argument('soc_min_bat', type=soc_min_bat_rule, required=False, help='Minimum SOC of the BESS')
node_information_update_parser.add_argument('soc_max_bat', type=soc_min_bat_rule, required=False, help='Maximum SOC of the BESS')
node_information_update_parser.add_argument('bat_nom_energy', type=bat_nom_energy_rule, required=False, help='Nominal energy of the BESS')
node_information_update_parser.add_argument('soc_min_ev', type=soc_min_ev_rule, required=False, help='Minimum SOC of the EV')
node_information_update_parser.add_argument('soc_max_ev', type=soc_min_ev_rule, required=False, help='Maximum SOC of the EV')

model = {
    'id': fields.Integer(),
    'name': fields.String(),
    'type': fields.String(),
    'der': fields.String(),
    'nominal_kva': fields.Float(),
    'minimum_kva': fields.Float(),
    'maximum_kva': fields.Float(),
    'power_factor': fields.Float(),
    'soc_min_bat': fields.Float(),
    'soc_max_bat': fields.Float(),
    'bat_nom_energy': fields.Float(),
    'soc_min_ev': fields.Float(),
    'soc_max_ev': fields.Float(),
}
node_model = node_information_namespace.model('node_information', model)


# ENDPOINT /v1/api/node_information/ -> GET all and POST one DER
@node_information_namespace.route('/')
class node_information_ListCreate(Resource):

    @node_information_namespace.doc('list_nodes')
    @node_information_namespace.marshal_with(node_model, as_list=True)
    def get(self):
        '''
        Retrieves all nodes
        '''
        node = (node_information_model
                    .query
                    .order_by('id')
                    .all())
        return node

    @node_information_namespace.doc('create_node')
    @node_information_namespace.expect(node_information_parser)
    @node_information_namespace.marshal_with(node_model, code=http.client.CREATED)
    def post(self):
        '''
        Creates a new node
        '''

        args = node_information_parser.parse_args()

        new_node = node_information_model(name=args['name'],
                            type=args['type'],
                            der=args['der'],
                            nominal_kva=args['nominal_kva'],
                            minimum_kva=args['minimum_kva'],
                            maximum_kva=args['maximum_kva'],
                            power_factor=args['power_factor'],
                            soc_min_bat=args['soc_min_bat'],
                            soc_max_bat=args['soc_max_bat'],
                            bat_nom_energy=args['bat_nom_energy'],
                            soc_min_ev=args['soc_min_ev'],
                            soc_max_ev=args['soc_max_ev'])

        if (new_node.der == 'bess') and new_node.bat_nom_energy is None:
            return abort(405, 'Input bess validation failed', errors={'der' : 'BESS has no bat_nom_energy attribute'})

        try:
            db.session.add(new_node)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})

        result = node_information_namespace.marshal(new_node, node_model)

        return result, http.client.CREATED


# ENDPOINT /v1/api/node_information/x/ -> GET or DELETE one DER with id=x
@node_information_namespace.route('/<int:node_id>/')
class node_information_Retrieve(Resource):

    @node_information_namespace.doc('retrieve_node')
    @node_information_namespace.marshal_with(node_model)
    def get(self, node_id):
        '''
        Retrieves a node with node_id
        '''
        node = node_information_model.query.get(node_id)
        if not node:
            # The node is not present
            return '', http.client.NOT_FOUND

        return node

    @node_information_namespace.doc('delete_node',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, node_id):
        '''
        Deletes a node
        '''
        node = node_information_model.query.get(node_id)
        if not node:
            # The node is not present
            return '', http.client.NO_CONTENT

        db.session.delete(node)
        db.session.commit()

        return '', http.client.NO_CONTENT
    

    @node_information_namespace.doc('Update_node_information')
    @node_information_namespace.marshal_with(node_model)
    @node_information_namespace.expect(node_information_update_parser)
    def put(self, node_id):
        '''
        Updates node_information based on name or id
        '''

        args = node_information_update_parser.parse_args()

        data = {
            'name': args['name'],
            'type': args['der'],
            'nominal_kva': args['nominal_kva'],
            'minimum_kva': args['minimum_kva'],
            'maximum_kva': args['maximum_kva'],
            'power_factor': args['power_factor'],
            'soc_min_bat': args['soc_min_bat'],
            'soc_max_bat': args['soc_max_bat'],
            'bat_nom_energy': args['bat_nom_energy'],
            'soc_min_ev': args['soc_min_ev'],
            'soc_max_ev': args['soc_max_bat']
        }

        query = node_information_model.query.get(node_id)
        if not query:
            # The query is not present
            return '', http.client.NO_CONTENT
        else:
            for key in data:
                if data[key]:
                    setattr(query, key, data[key])
            db.session.commit()
            return query

