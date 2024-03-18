from flask import Flask
# from flask_restplus import Api
from flask_restx import Api


def create_app():
    from api_tools.node_information_namespace import node_information_namespace
    from api_tools.node_measurement_namespace import node_measurement_namespace
    from api_tools.branch_information_namespace import branch_information_namespace
    from api_tools.branch_measurement_namespace import branch_measurement_namespace
    from api_tools.economic_dispatch_namespace import economic_dispatch_namespace
    from api_tools.milp_parameters_namespace import milp_parameters_namespace


    application = Flask(__name__)
    #api = Api(application, version='0.1', title='E75_EMS_LabREI Backend API',
    api = Api(application, version='0.1', title='API EMS Backend',
              description='A CRUD API')

    from api_tools.db import db, db_config
    application.config['RESTPLUS_MASK_SWAGGER'] = False
    application.config.update(db_config)
    db.init_app(application)
    application.db = db

    api.add_namespace(node_information_namespace)
    api.add_namespace(node_measurement_namespace)
    api.add_namespace(branch_information_namespace)
    api.add_namespace(branch_measurement_namespace)
    api.add_namespace(economic_dispatch_namespace)
    api.add_namespace(milp_parameters_namespace)


    return application
