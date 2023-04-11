import http.client
from datetime import datetime, timedelta
import dateutil.relativedelta
# from flask_restplus import Namespace, Resource, fields, inputs, abort
from flask_restx import Namespace, Resource, fields, inputs, abort
from api_tools.models import economic_dispatch_model
from api_tools.db import db
from sqlalchemy import exc
import requests
import json

def bat_power_rule(value):
    try:
        value = float(value)
        if abs(value) < 0.1:
            value = 0.0
    except:
        raise ValueError(' Invalid format!')
    return value

bat_power_rule.__schema__ = {
    "type": "number",
    "format": "bat_power_rule",
}

def curt_rule(value):
    try:
        value = float(value)
    except:
        raise ValueError(' Invalid format!')
    if value < 0:
        raise ValueError(' Invalid value!')
    return value

curt_rule.__schema__ = {
    "type": "number",
    "format": "curt_rule",
}


# Criação do economic_dispatch_namespace e dos parsers
economic_dispatch_namespace = Namespace('v1/api/economic_dispatch', description='API backend EMS - Economic dispatch')

# Parser for post
economic_dispatch_parser = economic_dispatch_namespace.parser()
economic_dispatch_parser.add_argument('bat_power_t00', type=bat_power_rule, required=True, help='BESS dispatch at 00h.')
economic_dispatch_parser.add_argument('bat_power_t01', type=bat_power_rule, required=True, help='BESS dispatch at 01h.')
economic_dispatch_parser.add_argument('bat_power_t02', type=bat_power_rule, required=True, help='BESS dispatch at 02h.')
economic_dispatch_parser.add_argument('bat_power_t03', type=bat_power_rule, required=True, help='BESS dispatch at 03h.')
economic_dispatch_parser.add_argument('bat_power_t04', type=bat_power_rule, required=True, help='BESS dispatch at 04h.')
economic_dispatch_parser.add_argument('bat_power_t05', type=bat_power_rule, required=True, help='BESS dispatch at 05h.')
economic_dispatch_parser.add_argument('bat_power_t06', type=bat_power_rule, required=True, help='BESS dispatch at 06h.')
economic_dispatch_parser.add_argument('bat_power_t07', type=bat_power_rule, required=True, help='BESS dispatch at 07h.')
economic_dispatch_parser.add_argument('bat_power_t08', type=bat_power_rule, required=True, help='BESS dispatch at 08h.')
economic_dispatch_parser.add_argument('bat_power_t09', type=bat_power_rule, required=True, help='BESS dispatch at 09h.')
economic_dispatch_parser.add_argument('bat_power_t10', type=bat_power_rule, required=True, help='BESS dispatch at 10h.')
economic_dispatch_parser.add_argument('bat_power_t11', type=bat_power_rule, required=True, help='BESS dispatch at 11h.')
economic_dispatch_parser.add_argument('bat_power_t12', type=bat_power_rule, required=True, help='BESS dispatch at 12h.')
economic_dispatch_parser.add_argument('bat_power_t13', type=bat_power_rule, required=True, help='BESS dispatch at 13h.')
economic_dispatch_parser.add_argument('bat_power_t14', type=bat_power_rule, required=True, help='BESS dispatch at 14h.')
economic_dispatch_parser.add_argument('bat_power_t15', type=bat_power_rule, required=True, help='BESS dispatch at 15h.')
economic_dispatch_parser.add_argument('bat_power_t16', type=bat_power_rule, required=True, help='BESS dispatch at 16h.')
economic_dispatch_parser.add_argument('bat_power_t17', type=bat_power_rule, required=True, help='BESS dispatch at 17h.')
economic_dispatch_parser.add_argument('bat_power_t18', type=bat_power_rule, required=True, help='BESS dispatch at 18h.')
economic_dispatch_parser.add_argument('bat_power_t19', type=bat_power_rule, required=True, help='BESS dispatch at 19h.')
economic_dispatch_parser.add_argument('bat_power_t20', type=bat_power_rule, required=True, help='BESS dispatch at 20h.')
economic_dispatch_parser.add_argument('bat_power_t21', type=bat_power_rule, required=True, help='BESS dispatch at 21h.')
economic_dispatch_parser.add_argument('bat_power_t22', type=bat_power_rule, required=True, help='BESS dispatch at 22h.')
economic_dispatch_parser.add_argument('bat_power_t23', type=bat_power_rule, required=True, help='BESS dispatch at 23h.')
economic_dispatch_parser.add_argument('genset_power_t00', type=bat_power_rule, required=True, help='Genset dispatch at 00h.')
economic_dispatch_parser.add_argument('genset_power_t01', type=bat_power_rule, required=True, help='Genset dispatch at 01h.')
economic_dispatch_parser.add_argument('genset_power_t02', type=bat_power_rule, required=True, help='Genset dispatch at 02h.')
economic_dispatch_parser.add_argument('genset_power_t03', type=bat_power_rule, required=True, help='Genset dispatch at 03h.')
economic_dispatch_parser.add_argument('genset_power_t04', type=bat_power_rule, required=True, help='Genset dispatch at 04h.')
economic_dispatch_parser.add_argument('genset_power_t05', type=bat_power_rule, required=True, help='Genset dispatch at 05h.')
economic_dispatch_parser.add_argument('genset_power_t06', type=bat_power_rule, required=True, help='Genset dispatch at 06h.')
economic_dispatch_parser.add_argument('genset_power_t07', type=bat_power_rule, required=True, help='Genset dispatch at 07h.')
economic_dispatch_parser.add_argument('genset_power_t08', type=bat_power_rule, required=True, help='Genset dispatch at 08h.')
economic_dispatch_parser.add_argument('genset_power_t09', type=bat_power_rule, required=True, help='Genset dispatch at 09h.')
economic_dispatch_parser.add_argument('genset_power_t10', type=bat_power_rule, required=True, help='Genset dispatch at 10h.')
economic_dispatch_parser.add_argument('genset_power_t11', type=bat_power_rule, required=True, help='Genset dispatch at 11h.')
economic_dispatch_parser.add_argument('genset_power_t12', type=bat_power_rule, required=True, help='Genset dispatch at 12h.')
economic_dispatch_parser.add_argument('genset_power_t13', type=bat_power_rule, required=True, help='Genset dispatch at 13h.')
economic_dispatch_parser.add_argument('genset_power_t14', type=bat_power_rule, required=True, help='Genset dispatch at 14h.')
economic_dispatch_parser.add_argument('genset_power_t15', type=bat_power_rule, required=True, help='Genset dispatch at 15h.')
economic_dispatch_parser.add_argument('genset_power_t16', type=bat_power_rule, required=True, help='Genset dispatch at 16h.')
economic_dispatch_parser.add_argument('genset_power_t17', type=bat_power_rule, required=True, help='Genset dispatch at 17h.')
economic_dispatch_parser.add_argument('genset_power_t18', type=bat_power_rule, required=True, help='Genset dispatch at 18h.')
economic_dispatch_parser.add_argument('genset_power_t19', type=bat_power_rule, required=True, help='Genset dispatch at 19h.')
economic_dispatch_parser.add_argument('genset_power_t20', type=bat_power_rule, required=True, help='Genset dispatch at 20h.')
economic_dispatch_parser.add_argument('genset_power_t21', type=bat_power_rule, required=True, help='Genset dispatch at 21h.')
economic_dispatch_parser.add_argument('genset_power_t22', type=bat_power_rule, required=True, help='Genset dispatch at 22h.')
economic_dispatch_parser.add_argument('genset_power_t23', type=bat_power_rule, required=True, help='Genset dispatch at 23h.')
economic_dispatch_parser.add_argument('load_curt_t00', type=curt_rule, required=True, help='Load curtailment dispatch at 00h.')
economic_dispatch_parser.add_argument('load_curt_t01', type=curt_rule, required=True, help='Load curtailment dispatch at 01h.')
economic_dispatch_parser.add_argument('load_curt_t02', type=curt_rule, required=True, help='Load curtailment dispatch at 02h.')
economic_dispatch_parser.add_argument('load_curt_t03', type=curt_rule, required=True, help='Load curtailment dispatch at 03h.')
economic_dispatch_parser.add_argument('load_curt_t04', type=curt_rule, required=True, help='Load curtailment dispatch at 04h.')
economic_dispatch_parser.add_argument('load_curt_t05', type=curt_rule, required=True, help='Load curtailment dispatch at 05h.')
economic_dispatch_parser.add_argument('load_curt_t06', type=curt_rule, required=True, help='Load curtailment dispatch at 06h.')
economic_dispatch_parser.add_argument('load_curt_t07', type=curt_rule, required=True, help='Load curtailment dispatch at 07h.')
economic_dispatch_parser.add_argument('load_curt_t08', type=curt_rule, required=True, help='Load curtailment dispatch at 08h.')
economic_dispatch_parser.add_argument('load_curt_t09', type=curt_rule, required=True, help='Load curtailment dispatch at 09h.')
economic_dispatch_parser.add_argument('load_curt_t10', type=curt_rule, required=True, help='Load curtailment dispatch at 10h.')
economic_dispatch_parser.add_argument('load_curt_t11', type=curt_rule, required=True, help='Load curtailment dispatch at 11h.')
economic_dispatch_parser.add_argument('load_curt_t12', type=curt_rule, required=True, help='Load curtailment dispatch at 12h.')
economic_dispatch_parser.add_argument('load_curt_t13', type=curt_rule, required=True, help='Load curtailment dispatch at 13h.')
economic_dispatch_parser.add_argument('load_curt_t14', type=curt_rule, required=True, help='Load curtailment dispatch at 14h.')
economic_dispatch_parser.add_argument('load_curt_t15', type=curt_rule, required=True, help='Load curtailment dispatch at 15h.')
economic_dispatch_parser.add_argument('load_curt_t16', type=curt_rule, required=True, help='Load curtailment dispatch at 16h.')
economic_dispatch_parser.add_argument('load_curt_t17', type=curt_rule, required=True, help='Load curtailment dispatch at 17h.')
economic_dispatch_parser.add_argument('load_curt_t18', type=curt_rule, required=True, help='Load curtailment dispatch at 18h.')
economic_dispatch_parser.add_argument('load_curt_t19', type=curt_rule, required=True, help='Load curtailment dispatch at 19h.')
economic_dispatch_parser.add_argument('load_curt_t20', type=curt_rule, required=True, help='Load curtailment dispatch at 20h.')
economic_dispatch_parser.add_argument('load_curt_t21', type=curt_rule, required=True, help='Load curtailment dispatch at 21h.')
economic_dispatch_parser.add_argument('load_curt_t22', type=curt_rule, required=True, help='Load curtailment dispatch at 22h.')
economic_dispatch_parser.add_argument('load_curt_t23', type=curt_rule, required=True, help='Load curtailment dispatch at 23h.')
economic_dispatch_parser.add_argument('pv_curt_t00', type=curt_rule, required=True, help='PV disconnect dispatch at 00h.')
economic_dispatch_parser.add_argument('pv_curt_t01', type=curt_rule, required=True, help='PV disconnect dispatch at 01h.')
economic_dispatch_parser.add_argument('pv_curt_t02', type=curt_rule, required=True, help='PV disconnect dispatch at 02h.')
economic_dispatch_parser.add_argument('pv_curt_t03', type=curt_rule, required=True, help='PV disconnect dispatch at 03h.')
economic_dispatch_parser.add_argument('pv_curt_t04', type=curt_rule, required=True, help='PV disconnect dispatch at 04h.')
economic_dispatch_parser.add_argument('pv_curt_t05', type=curt_rule, required=True, help='PV disconnect dispatch at 05h.')
economic_dispatch_parser.add_argument('pv_curt_t06', type=curt_rule, required=True, help='PV disconnect dispatch at 06h.')
economic_dispatch_parser.add_argument('pv_curt_t07', type=curt_rule, required=True, help='PV disconnect dispatch at 07h.')
economic_dispatch_parser.add_argument('pv_curt_t08', type=curt_rule, required=True, help='PV disconnect dispatch at 08h.')
economic_dispatch_parser.add_argument('pv_curt_t09', type=curt_rule, required=True, help='PV disconnect dispatch at 09h.')
economic_dispatch_parser.add_argument('pv_curt_t10', type=curt_rule, required=True, help='PV disconnect dispatch at 10h.')
economic_dispatch_parser.add_argument('pv_curt_t11', type=curt_rule, required=True, help='PV disconnect dispatch at 11h.')
economic_dispatch_parser.add_argument('pv_curt_t12', type=curt_rule, required=True, help='PV disconnect dispatch at 12h.')
economic_dispatch_parser.add_argument('pv_curt_t13', type=curt_rule, required=True, help='PV disconnect dispatch at 13h.')
economic_dispatch_parser.add_argument('pv_curt_t14', type=curt_rule, required=True, help='PV disconnect dispatch at 14h.')
economic_dispatch_parser.add_argument('pv_curt_t15', type=curt_rule, required=True, help='PV disconnect dispatch at 15h.')
economic_dispatch_parser.add_argument('pv_curt_t16', type=curt_rule, required=True, help='PV disconnect dispatch at 16h.')
economic_dispatch_parser.add_argument('pv_curt_t17', type=curt_rule, required=True, help='PV disconnect dispatch at 17h.')
economic_dispatch_parser.add_argument('pv_curt_t18', type=curt_rule, required=True, help='PV disconnect dispatch at 18h.')
economic_dispatch_parser.add_argument('pv_curt_t19', type=curt_rule, required=True, help='PV disconnect dispatch at 19h.')
economic_dispatch_parser.add_argument('pv_curt_t20', type=curt_rule, required=True, help='PV disconnect dispatch at 20h.')
economic_dispatch_parser.add_argument('pv_curt_t21', type=curt_rule, required=True, help='PV disconnect dispatch at 21h.')
economic_dispatch_parser.add_argument('pv_curt_t22', type=curt_rule, required=True, help='PV disconnect dispatch at 22h.')
economic_dispatch_parser.add_argument('pv_curt_t23', type=curt_rule, required=True, help='PV disconnect dispatch at 23h.')

# Parser for put
economic_dispatch_update_parser = economic_dispatch_namespace.parser()
economic_dispatch_update_parser.add_argument('bat_power_t00', type=bat_power_rule, required=False, help='BESS dispatch at 00h.')
economic_dispatch_update_parser.add_argument('bat_power_t01', type=bat_power_rule, required=False, help='BESS dispatch at 01h.')
economic_dispatch_update_parser.add_argument('bat_power_t02', type=bat_power_rule, required=False, help='BESS dispatch at 02h.')
economic_dispatch_update_parser.add_argument('bat_power_t03', type=bat_power_rule, required=False, help='BESS dispatch at 03h.')
economic_dispatch_update_parser.add_argument('bat_power_t04', type=bat_power_rule, required=False, help='BESS dispatch at 04h.')
economic_dispatch_update_parser.add_argument('bat_power_t05', type=bat_power_rule, required=False, help='BESS dispatch at 05h.')
economic_dispatch_update_parser.add_argument('bat_power_t06', type=bat_power_rule, required=False, help='BESS dispatch at 06h.')
economic_dispatch_update_parser.add_argument('bat_power_t07', type=bat_power_rule, required=False, help='BESS dispatch at 07h.')
economic_dispatch_update_parser.add_argument('bat_power_t08', type=bat_power_rule, required=False, help='BESS dispatch at 08h.')
economic_dispatch_update_parser.add_argument('bat_power_t09', type=bat_power_rule, required=False, help='BESS dispatch at 09h.')
economic_dispatch_update_parser.add_argument('bat_power_t10', type=bat_power_rule, required=False, help='BESS dispatch at 10h.')
economic_dispatch_update_parser.add_argument('bat_power_t11', type=bat_power_rule, required=False, help='BESS dispatch at 11h.')
economic_dispatch_update_parser.add_argument('bat_power_t12', type=bat_power_rule, required=False, help='BESS dispatch at 12h.')
economic_dispatch_update_parser.add_argument('bat_power_t13', type=bat_power_rule, required=False, help='BESS dispatch at 13h.')
economic_dispatch_update_parser.add_argument('bat_power_t14', type=bat_power_rule, required=False, help='BESS dispatch at 14h.')
economic_dispatch_update_parser.add_argument('bat_power_t15', type=bat_power_rule, required=False, help='BESS dispatch at 15h.')
economic_dispatch_update_parser.add_argument('bat_power_t16', type=bat_power_rule, required=False, help='BESS dispatch at 16h.')
economic_dispatch_update_parser.add_argument('bat_power_t17', type=bat_power_rule, required=False, help='BESS dispatch at 17h.')
economic_dispatch_update_parser.add_argument('bat_power_t18', type=bat_power_rule, required=False, help='BESS dispatch at 18h.')
economic_dispatch_update_parser.add_argument('bat_power_t19', type=bat_power_rule, required=False, help='BESS dispatch at 19h.')
economic_dispatch_update_parser.add_argument('bat_power_t20', type=bat_power_rule, required=False, help='BESS dispatch at 20h.')
economic_dispatch_update_parser.add_argument('bat_power_t21', type=bat_power_rule, required=False, help='BESS dispatch at 21h.')
economic_dispatch_update_parser.add_argument('bat_power_t22', type=bat_power_rule, required=False, help='BESS dispatch at 22h.')
economic_dispatch_update_parser.add_argument('bat_power_t23', type=bat_power_rule, required=False, help='BESS dispatch at 23h.')
economic_dispatch_update_parser.add_argument('genset_power_t00', type=bat_power_rule, required=False, help='Genset dispatch at 00h.')
economic_dispatch_update_parser.add_argument('genset_power_t01', type=bat_power_rule, required=False, help='Genset dispatch at 01h.')
economic_dispatch_update_parser.add_argument('genset_power_t02', type=bat_power_rule, required=False, help='Genset dispatch at 02h.')
economic_dispatch_update_parser.add_argument('genset_power_t03', type=bat_power_rule, required=False, help='Genset dispatch at 03h.')
economic_dispatch_update_parser.add_argument('genset_power_t04', type=bat_power_rule, required=False, help='Genset dispatch at 04h.')
economic_dispatch_update_parser.add_argument('genset_power_t05', type=bat_power_rule, required=False, help='Genset dispatch at 05h.')
economic_dispatch_update_parser.add_argument('genset_power_t06', type=bat_power_rule, required=False, help='Genset dispatch at 06h.')
economic_dispatch_update_parser.add_argument('genset_power_t07', type=bat_power_rule, required=False, help='Genset dispatch at 07h.')
economic_dispatch_update_parser.add_argument('genset_power_t08', type=bat_power_rule, required=False, help='Genset dispatch at 08h.')
economic_dispatch_update_parser.add_argument('genset_power_t09', type=bat_power_rule, required=False, help='Genset dispatch at 09h.')
economic_dispatch_update_parser.add_argument('genset_power_t10', type=bat_power_rule, required=False, help='Genset dispatch at 10h.')
economic_dispatch_update_parser.add_argument('genset_power_t11', type=bat_power_rule, required=False, help='Genset dispatch at 11h.')
economic_dispatch_update_parser.add_argument('genset_power_t12', type=bat_power_rule, required=False, help='Genset dispatch at 12h.')
economic_dispatch_update_parser.add_argument('genset_power_t13', type=bat_power_rule, required=False, help='Genset dispatch at 13h.')
economic_dispatch_update_parser.add_argument('genset_power_t14', type=bat_power_rule, required=False, help='Genset dispatch at 14h.')
economic_dispatch_update_parser.add_argument('genset_power_t15', type=bat_power_rule, required=False, help='Genset dispatch at 15h.')
economic_dispatch_update_parser.add_argument('genset_power_t16', type=bat_power_rule, required=False, help='Genset dispatch at 16h.')
economic_dispatch_update_parser.add_argument('genset_power_t17', type=bat_power_rule, required=False, help='Genset dispatch at 17h.')
economic_dispatch_update_parser.add_argument('genset_power_t18', type=bat_power_rule, required=False, help='Genset dispatch at 18h.')
economic_dispatch_update_parser.add_argument('genset_power_t19', type=bat_power_rule, required=False, help='Genset dispatch at 19h.')
economic_dispatch_update_parser.add_argument('genset_power_t20', type=bat_power_rule, required=False, help='Genset dispatch at 20h.')
economic_dispatch_update_parser.add_argument('genset_power_t21', type=bat_power_rule, required=False, help='Genset dispatch at 21h.')
economic_dispatch_update_parser.add_argument('genset_power_t22', type=bat_power_rule, required=False, help='Genset dispatch at 22h.')
economic_dispatch_update_parser.add_argument('genset_power_t23', type=bat_power_rule, required=False, help='Genset dispatch at 23h.')
economic_dispatch_update_parser.add_argument('load_curt_t00', type=curt_rule, required=False, help='Load curtailment dispatch at 00h.')
economic_dispatch_update_parser.add_argument('load_curt_t01', type=curt_rule, required=False, help='Load curtailment dispatch at 01h.')
economic_dispatch_update_parser.add_argument('load_curt_t02', type=curt_rule, required=False, help='Load curtailment dispatch at 02h.')
economic_dispatch_update_parser.add_argument('load_curt_t03', type=curt_rule, required=False, help='Load curtailment dispatch at 03h.')
economic_dispatch_update_parser.add_argument('load_curt_t04', type=curt_rule, required=False, help='Load curtailment dispatch at 04h.')
economic_dispatch_update_parser.add_argument('load_curt_t05', type=curt_rule, required=False, help='Load curtailment dispatch at 05h.')
economic_dispatch_update_parser.add_argument('load_curt_t06', type=curt_rule, required=False, help='Load curtailment dispatch at 06h.')
economic_dispatch_update_parser.add_argument('load_curt_t07', type=curt_rule, required=False, help='Load curtailment dispatch at 07h.')
economic_dispatch_update_parser.add_argument('load_curt_t08', type=curt_rule, required=False, help='Load curtailment dispatch at 08h.')
economic_dispatch_update_parser.add_argument('load_curt_t09', type=curt_rule, required=False, help='Load curtailment dispatch at 09h.')
economic_dispatch_update_parser.add_argument('load_curt_t10', type=curt_rule, required=False, help='Load curtailment dispatch at 10h.')
economic_dispatch_update_parser.add_argument('load_curt_t11', type=curt_rule, required=False, help='Load curtailment dispatch at 11h.')
economic_dispatch_update_parser.add_argument('load_curt_t12', type=curt_rule, required=False, help='Load curtailment dispatch at 12h.')
economic_dispatch_update_parser.add_argument('load_curt_t13', type=curt_rule, required=False, help='Load curtailment dispatch at 13h.')
economic_dispatch_update_parser.add_argument('load_curt_t14', type=curt_rule, required=False, help='Load curtailment dispatch at 14h.')
economic_dispatch_update_parser.add_argument('load_curt_t15', type=curt_rule, required=False, help='Load curtailment dispatch at 15h.')
economic_dispatch_update_parser.add_argument('load_curt_t16', type=curt_rule, required=False, help='Load curtailment dispatch at 16h.')
economic_dispatch_update_parser.add_argument('load_curt_t17', type=curt_rule, required=False, help='Load curtailment dispatch at 17h.')
economic_dispatch_update_parser.add_argument('load_curt_t18', type=curt_rule, required=False, help='Load curtailment dispatch at 18h.')
economic_dispatch_update_parser.add_argument('load_curt_t19', type=curt_rule, required=False, help='Load curtailment dispatch at 19h.')
economic_dispatch_update_parser.add_argument('load_curt_t20', type=curt_rule, required=False, help='Load curtailment dispatch at 20h.')
economic_dispatch_update_parser.add_argument('load_curt_t21', type=curt_rule, required=False, help='Load curtailment dispatch at 21h.')
economic_dispatch_update_parser.add_argument('load_curt_t22', type=curt_rule, required=False, help='Load curtailment dispatch at 22h.')
economic_dispatch_update_parser.add_argument('load_curt_t23', type=curt_rule, required=False, help='Load curtailment dispatch at 23h.')
economic_dispatch_update_parser.add_argument('pv_curt_t00', type=curt_rule, required=False, help='PV disconnect dispatch at 00h.')
economic_dispatch_update_parser.add_argument('pv_curt_t01', type=curt_rule, required=False, help='PV disconnect dispatch at 01h.')
economic_dispatch_update_parser.add_argument('pv_curt_t02', type=curt_rule, required=False, help='PV disconnect dispatch at 02h.')
economic_dispatch_update_parser.add_argument('pv_curt_t03', type=curt_rule, required=False, help='PV disconnect dispatch at 03h.')
economic_dispatch_update_parser.add_argument('pv_curt_t04', type=curt_rule, required=False, help='PV disconnect dispatch at 04h.')
economic_dispatch_update_parser.add_argument('pv_curt_t05', type=curt_rule, required=False, help='PV disconnect dispatch at 05h.')
economic_dispatch_update_parser.add_argument('pv_curt_t06', type=curt_rule, required=False, help='PV disconnect dispatch at 06h.')
economic_dispatch_update_parser.add_argument('pv_curt_t07', type=curt_rule, required=False, help='PV disconnect dispatch at 07h.')
economic_dispatch_update_parser.add_argument('pv_curt_t08', type=curt_rule, required=False, help='PV disconnect dispatch at 08h.')
economic_dispatch_update_parser.add_argument('pv_curt_t09', type=curt_rule, required=False, help='PV disconnect dispatch at 09h.')
economic_dispatch_update_parser.add_argument('pv_curt_t10', type=curt_rule, required=False, help='PV disconnect dispatch at 10h.')
economic_dispatch_update_parser.add_argument('pv_curt_t11', type=curt_rule, required=False, help='PV disconnect dispatch at 11h.')
economic_dispatch_update_parser.add_argument('pv_curt_t12', type=curt_rule, required=False, help='PV disconnect dispatch at 12h.')
economic_dispatch_update_parser.add_argument('pv_curt_t13', type=curt_rule, required=False, help='PV disconnect dispatch at 13h.')
economic_dispatch_update_parser.add_argument('pv_curt_t14', type=curt_rule, required=False, help='PV disconnect dispatch at 14h.')
economic_dispatch_update_parser.add_argument('pv_curt_t15', type=curt_rule, required=False, help='PV disconnect dispatch at 15h.')
economic_dispatch_update_parser.add_argument('pv_curt_t16', type=curt_rule, required=False, help='PV disconnect dispatch at 16h.')
economic_dispatch_update_parser.add_argument('pv_curt_t17', type=curt_rule, required=False, help='PV disconnect dispatch at 17h.')
economic_dispatch_update_parser.add_argument('pv_curt_t18', type=curt_rule, required=False, help='PV disconnect dispatch at 18h.')
economic_dispatch_update_parser.add_argument('pv_curt_t19', type=curt_rule, required=False, help='PV disconnect dispatch at 19h.')
economic_dispatch_update_parser.add_argument('pv_curt_t20', type=curt_rule, required=False, help='PV disconnect dispatch at 20h.')
economic_dispatch_update_parser.add_argument('pv_curt_t21', type=curt_rule, required=False, help='PV disconnect dispatch at 21h.')
economic_dispatch_update_parser.add_argument('pv_curt_t22', type=curt_rule, required=False, help='PV disconnect dispatch at 22h.')
economic_dispatch_update_parser.add_argument('pv_curt_t23', type=curt_rule, required=False, help='PV disconnect dispatch at 23h.')


model = {
    'id': fields.Integer(),
    'bat_power_t00': fields.Float(),
    'bat_power_t01': fields.Float(),
    'bat_power_t02': fields.Float(),
    'bat_power_t03': fields.Float(),
    'bat_power_t04': fields.Float(),
    'bat_power_t05': fields.Float(),
    'bat_power_t06': fields.Float(),
    'bat_power_t07': fields.Float(),
    'bat_power_t08': fields.Float(),
    'bat_power_t09': fields.Float(),
    'bat_power_t10': fields.Float(),
    'bat_power_t11': fields.Float(),
    'bat_power_t12': fields.Float(),
    'bat_power_t13': fields.Float(),
    'bat_power_t14': fields.Float(),
    'bat_power_t15': fields.Float(),
    'bat_power_t16': fields.Float(),
    'bat_power_t17': fields.Float(),
    'bat_power_t18': fields.Float(),
    'bat_power_t19': fields.Float(),
    'bat_power_t20': fields.Float(),
    'bat_power_t21': fields.Float(),
    'bat_power_t22': fields.Float(),
    'bat_power_t23': fields.Float(),
    'genset_power_t00': fields.Float(),
    'genset_power_t01': fields.Float(),
    'genset_power_t02': fields.Float(),
    'genset_power_t03': fields.Float(),
    'genset_power_t04': fields.Float(),
    'genset_power_t05': fields.Float(),
    'genset_power_t06': fields.Float(),
    'genset_power_t07': fields.Float(),
    'genset_power_t08': fields.Float(),
    'genset_power_t09': fields.Float(),
    'genset_power_t10': fields.Float(),
    'genset_power_t11': fields.Float(),
    'genset_power_t12': fields.Float(),
    'genset_power_t13': fields.Float(),
    'genset_power_t14': fields.Float(),
    'genset_power_t15': fields.Float(),
    'genset_power_t16': fields.Float(),
    'genset_power_t17': fields.Float(),
    'genset_power_t18': fields.Float(),
    'genset_power_t19': fields.Float(),
    'genset_power_t20': fields.Float(),
    'genset_power_t21': fields.Float(),
    'genset_power_t22': fields.Float(),
    'genset_power_t23': fields.Float(),
    'load_curt_t00': fields.Float(),
    'load_curt_t01': fields.Float(),
    'load_curt_t02': fields.Float(),
    'load_curt_t03': fields.Float(),
    'load_curt_t04': fields.Float(),
    'load_curt_t05': fields.Float(),
    'load_curt_t06': fields.Float(),
    'load_curt_t07': fields.Float(),
    'load_curt_t08': fields.Float(),
    'load_curt_t09': fields.Float(),
    'load_curt_t10': fields.Float(),
    'load_curt_t11': fields.Float(),
    'load_curt_t12': fields.Float(),
    'load_curt_t13': fields.Float(),
    'load_curt_t14': fields.Float(),
    'load_curt_t15': fields.Float(),
    'load_curt_t16': fields.Float(),
    'load_curt_t17': fields.Float(),
    'load_curt_t18': fields.Float(),
    'load_curt_t19': fields.Float(),
    'load_curt_t20': fields.Float(),
    'load_curt_t21': fields.Float(),
    'load_curt_t22': fields.Float(),
    'load_curt_t23': fields.Float(),
    'pv_curt_t00': fields.Float(),
    'pv_curt_t01': fields.Float(),
    'pv_curt_t02': fields.Float(),
    'pv_curt_t03': fields.Float(),
    'pv_curt_t04': fields.Float(),
    'pv_curt_t05': fields.Float(),
    'pv_curt_t06': fields.Float(),
    'pv_curt_t07': fields.Float(),
    'pv_curt_t08': fields.Float(),
    'pv_curt_t09': fields.Float(),
    'pv_curt_t10': fields.Float(),
    'pv_curt_t11': fields.Float(),
    'pv_curt_t12': fields.Float(),
    'pv_curt_t13': fields.Float(),
    'pv_curt_t14': fields.Float(),
    'pv_curt_t15': fields.Float(),
    'pv_curt_t16': fields.Float(),
    'pv_curt_t17': fields.Float(),
    'pv_curt_t18': fields.Float(),
    'pv_curt_t19': fields.Float(),
    'pv_curt_t20': fields.Float(),
    'pv_curt_t21': fields.Float(),
    'pv_curt_t22': fields.Float(),
    'pv_curt_t23': fields.Float(),
}
dispatch_model = economic_dispatch_namespace.model('economic_dispatch', model)

# ENDPOINT /v1/api/economic_dispatch/ -> GET all and POST one Dispatch
@economic_dispatch_namespace.route('/')
class economic_dispatch_ListCreate(Resource):

    @economic_dispatch_namespace.doc('list_dispatches')
    @economic_dispatch_namespace.marshal_with(dispatch_model, as_list=True)
    def get(self):
        '''
        Retrieves all dispatches
        '''
        dispatch = (economic_dispatch_model
                    .query
                    .order_by('id')
                    .all())
        return dispatch

    @economic_dispatch_namespace.doc('create_dispatch')
    @economic_dispatch_namespace.expect(economic_dispatch_parser)
    @economic_dispatch_namespace.marshal_with(dispatch_model, code=http.client.CREATED)
    def post(self):
        '''
        Creates a new dispatch
        '''

        args = economic_dispatch_parser.parse_args()

        new_dispatch = economic_dispatch_model(bat_power_t00=args['bat_power_t00'],
                            bat_power_t01=args['bat_power_t01'],
                            bat_power_t02=args['bat_power_t02'],
                            bat_power_t03=args['bat_power_t03'],
                            bat_power_t04=args['bat_power_t04'],
                            bat_power_t05=args['bat_power_t05'],
                            bat_power_t06=args['bat_power_t06'],
                            bat_power_t07=args['bat_power_t07'],
                            bat_power_t08=args['bat_power_t08'],
                            bat_power_t09=args['bat_power_t09'],
                            bat_power_t10=args['bat_power_t10'],
                            bat_power_t11=args['bat_power_t11'],
                            bat_power_t12=args['bat_power_t12'],
                            bat_power_t13=args['bat_power_t13'],
                            bat_power_t14=args['bat_power_t14'],
                            bat_power_t15=args['bat_power_t15'],
                            bat_power_t16=args['bat_power_t16'],
                            bat_power_t17=args['bat_power_t17'],
                            bat_power_t18=args['bat_power_t18'],
                            bat_power_t19=args['bat_power_t19'],
                            bat_power_t20=args['bat_power_t20'],
                            bat_power_t21=args['bat_power_t21'],
                            bat_power_t22=args['bat_power_t22'],
                            bat_power_t23=args['bat_power_t23'],
                            genset_power_t00=args['genset_power_t00'],
                            genset_power_t01=args['genset_power_t01'],
                            genset_power_t02=args['genset_power_t02'],
                            genset_power_t03=args['genset_power_t03'],
                            genset_power_t04=args['genset_power_t04'],
                            genset_power_t05=args['genset_power_t05'],
                            genset_power_t06=args['genset_power_t06'],
                            genset_power_t07=args['genset_power_t07'],
                            genset_power_t08=args['genset_power_t08'],
                            genset_power_t09=args['genset_power_t09'],
                            genset_power_t10=args['genset_power_t10'],
                            genset_power_t11=args['genset_power_t11'],
                            genset_power_t12=args['genset_power_t12'],
                            genset_power_t13=args['genset_power_t13'],
                            genset_power_t14=args['genset_power_t14'],
                            genset_power_t15=args['genset_power_t15'],
                            genset_power_t16=args['genset_power_t16'],
                            genset_power_t17=args['genset_power_t17'],
                            genset_power_t18=args['genset_power_t18'],
                            genset_power_t19=args['genset_power_t19'],
                            genset_power_t20=args['genset_power_t20'],
                            genset_power_t21=args['genset_power_t21'],
                            genset_power_t22=args['genset_power_t22'],
                            genset_power_t23=args['genset_power_t23'],
                            load_curt_t00=args['load_curt_t00'],
                            load_curt_t01=args['load_curt_t01'],
                            load_curt_t02=args['load_curt_t02'],
                            load_curt_t03=args['load_curt_t03'],
                            load_curt_t04=args['load_curt_t04'],
                            load_curt_t05=args['load_curt_t05'],
                            load_curt_t06=args['load_curt_t06'],
                            load_curt_t07=args['load_curt_t07'],
                            load_curt_t08=args['load_curt_t08'],
                            load_curt_t09=args['load_curt_t09'],
                            load_curt_t10=args['load_curt_t10'],
                            load_curt_t11=args['load_curt_t11'],
                            load_curt_t12=args['load_curt_t12'],
                            load_curt_t13=args['load_curt_t13'],
                            load_curt_t14=args['load_curt_t14'],
                            load_curt_t15=args['load_curt_t15'],
                            load_curt_t16=args['load_curt_t16'],
                            load_curt_t17=args['load_curt_t17'],
                            load_curt_t18=args['load_curt_t18'],
                            load_curt_t19=args['load_curt_t19'],
                            load_curt_t20=args['load_curt_t20'],
                            load_curt_t21=args['load_curt_t21'],
                            load_curt_t22=args['load_curt_t22'],
                            load_curt_t23=args['load_curt_t23'],
                            pv_curt_t00=args['pv_curt_t00'],
                            pv_curt_t01=args['pv_curt_t01'],
                            pv_curt_t02=args['pv_curt_t02'],
                            pv_curt_t03=args['pv_curt_t03'],
                            pv_curt_t04=args['pv_curt_t04'],
                            pv_curt_t05=args['pv_curt_t05'],
                            pv_curt_t06=args['pv_curt_t06'],
                            pv_curt_t07=args['pv_curt_t07'],
                            pv_curt_t08=args['pv_curt_t08'],
                            pv_curt_t09=args['pv_curt_t09'],
                            pv_curt_t10=args['pv_curt_t10'],
                            pv_curt_t11=args['pv_curt_t11'],
                            pv_curt_t12=args['pv_curt_t12'],
                            pv_curt_t13=args['pv_curt_t13'],
                            pv_curt_t14=args['pv_curt_t14'],
                            pv_curt_t15=args['pv_curt_t15'],
                            pv_curt_t16=args['pv_curt_t16'],
                            pv_curt_t17=args['pv_curt_t17'],
                            pv_curt_t18=args['pv_curt_t18'],
                            pv_curt_t19=args['pv_curt_t19'],
                            pv_curt_t20=args['pv_curt_t20'],
                            pv_curt_t21=args['pv_curt_t21'],
                            pv_curt_t22=args['pv_curt_t22'],
                            pv_curt_t23=args['pv_curt_t23'])


        try:
            db.session.add(new_dispatch)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args
            print('Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1])
            return abort(403, 'Input payload validation failed', errors={'type' : 'Database update was rejected', 'info' : 'Database error ' + str(errorInfo[0]) + ': ' + errorInfo[1]})

        result = economic_dispatch_namespace.marshal(new_dispatch, dispatch_model)

        return result, http.client.CREATED


# ENDPOINT /v1/api/economic_dispatch/x/ -> GET or DELETE one dispatch with id=x
@economic_dispatch_namespace.route('/<int:dispatch_id>/')
class economic_dispatch_Retrieve(Resource):

    @economic_dispatch_namespace.doc('retrieve_dispatch')
    @economic_dispatch_namespace.marshal_with(dispatch_model)
    def get(self, dispatch_id):
        '''
        Retrieves a dispatch with dispatch_id
        '''
        dispatch = economic_dispatch_model.query.get(dispatch_id)
        if not dispatch:
            # The dispatch is not present
            return '', http.client.NOT_FOUND

        return dispatch

    @economic_dispatch_namespace.doc('delete_dispatch',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, dispatch_id):
        '''
        Deletes a dispatch
        '''
        dispatch = economic_dispatch_model.query.get(dispatch_id)
        if not dispatch:
            # The dispatch is not present
            return '', http.client.NO_CONTENT

        db.session.delete(dispatch)
        db.session.commit()

        return '', http.client.NO_CONTENT


    @economic_dispatch_namespace.doc('Update_economic_dispatch')
    @economic_dispatch_namespace.marshal_with(dispatch_model)
    @economic_dispatch_namespace.expect(economic_dispatch_update_parser)
    def put(self, dispatch_id):
        '''
        Updates economic_dispatch based on name or id
        '''

        args = economic_dispatch_update_parser.parse_args()

        data = {
            'bat_power_t00': args['bat_power_t00'],
            'bat_power_t01': args['bat_power_t01'],
            'bat_power_t02': args['bat_power_t02'],
            'bat_power_t03': args['bat_power_t03'],
            'bat_power_t04': args['bat_power_t04'],
            'bat_power_t05': args['bat_power_t05'],
            'bat_power_t06': args['bat_power_t06'],
            'bat_power_t07': args['bat_power_t07'],
            'bat_power_t08': args['bat_power_t08'],
            'bat_power_t09': args['bat_power_t09'],
            'bat_power_t10': args['bat_power_t10'],
            'bat_power_t11': args['bat_power_t11'],
            'bat_power_t12': args['bat_power_t12'],
            'bat_power_t13': args['bat_power_t13'],
            'bat_power_t14': args['bat_power_t14'],
            'bat_power_t15': args['bat_power_t15'],
            'bat_power_t16': args['bat_power_t16'],
            'bat_power_t17': args['bat_power_t17'],
            'bat_power_t18': args['bat_power_t18'],
            'bat_power_t19': args['bat_power_t19'],
            'bat_power_t20': args['bat_power_t20'],
            'bat_power_t21': args['bat_power_t21'],
            'bat_power_t22': args['bat_power_t22'],
            'bat_power_t23': args['bat_power_t23'],
            'genset_power_t00': args['genset_power_t00'],
            'genset_power_t01': args['genset_power_t01'],
            'genset_power_t02': args['genset_power_t02'],
            'genset_power_t03': args['genset_power_t03'],
            'genset_power_t04': args['genset_power_t04'],
            'genset_power_t05': args['genset_power_t05'],
            'genset_power_t06': args['genset_power_t06'],
            'genset_power_t07': args['genset_power_t07'],
            'genset_power_t08': args['genset_power_t08'],
            'genset_power_t09': args['genset_power_t09'],
            'genset_power_t10': args['genset_power_t10'],
            'genset_power_t11': args['genset_power_t11'],
            'genset_power_t12': args['genset_power_t12'],
            'genset_power_t13': args['genset_power_t13'],
            'genset_power_t14': args['genset_power_t14'],
            'genset_power_t15': args['genset_power_t15'],
            'genset_power_t16': args['genset_power_t16'],
            'genset_power_t17': args['genset_power_t17'],
            'genset_power_t18': args['genset_power_t18'],
            'genset_power_t19': args['genset_power_t19'],
            'genset_power_t20': args['genset_power_t20'],
            'genset_power_t21': args['genset_power_t21'],
            'genset_power_t22': args['genset_power_t22'],
            'genset_power_t23': args['genset_power_t23'],
            'load_curt_t00': args['load_curt_t00'],
            'load_curt_t01': args['load_curt_t01'],
            'load_curt_t02': args['load_curt_t02'],
            'load_curt_t03': args['load_curt_t03'],
            'load_curt_t04': args['load_curt_t04'],
            'load_curt_t05': args['load_curt_t05'],
            'load_curt_t06': args['load_curt_t06'],
            'load_curt_t07': args['load_curt_t07'],
            'load_curt_t08': args['load_curt_t08'],
            'load_curt_t09': args['load_curt_t09'],
            'load_curt_t10': args['load_curt_t10'],
            'load_curt_t11': args['load_curt_t11'],
            'load_curt_t12': args['load_curt_t12'],
            'load_curt_t13': args['load_curt_t13'],
            'load_curt_t14': args['load_curt_t14'],
            'load_curt_t15': args['load_curt_t15'],
            'load_curt_t16': args['load_curt_t16'],
            'load_curt_t17': args['load_curt_t17'],
            'load_curt_t18': args['load_curt_t18'],
            'load_curt_t19': args['load_curt_t19'],
            'load_curt_t20': args['load_curt_t20'],
            'load_curt_t21': args['load_curt_t21'],
            'load_curt_t22': args['load_curt_t22'],
            'load_curt_t23': args['load_curt_t23'],
            'pv_curt_t00': args['pv_curt_t00'],
            'pv_curt_t01': args['pv_curt_t01'],
            'pv_curt_t02': args['pv_curt_t02'],
            'pv_curt_t03': args['pv_curt_t03'],
            'pv_curt_t04': args['pv_curt_t04'],
            'pv_curt_t05': args['pv_curt_t05'],
            'pv_curt_t06': args['pv_curt_t06'],
            'pv_curt_t07': args['pv_curt_t07'],
            'pv_curt_t08': args['pv_curt_t08'],
            'pv_curt_t09': args['pv_curt_t09'],
            'pv_curt_t10': args['pv_curt_t10'],
            'pv_curt_t11': args['pv_curt_t11'],
            'pv_curt_t12': args['pv_curt_t12'],
            'pv_curt_t13': args['pv_curt_t13'],
            'pv_curt_t14': args['pv_curt_t14'],
            'pv_curt_t15': args['pv_curt_t15'],
            'pv_curt_t16': args['pv_curt_t16'],
            'pv_curt_t17': args['pv_curt_t17'],
            'pv_curt_t18': args['pv_curt_t18'],
            'pv_curt_t19': args['pv_curt_t19'],
            'pv_curt_t20': args['pv_curt_t20'],
            'pv_curt_t21': args['pv_curt_t21'],
            'pv_curt_t22': args['pv_curt_t22'],
            'pv_curt_t23': args['pv_curt_t23']
        }
        
        query = economic_dispatch_model.query.get(dispatch_id)
        if not query:
            # The query is not present
            return '', http.client.NO_CONTENT
        else:
            for key in data:
                if data[key]:
                    setattr(query, key, data[key])
                elif data[key] == 0.0:
                    setattr(query, key, data[key])
            db.session.commit()
            return query
