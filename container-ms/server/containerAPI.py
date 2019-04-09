from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from confluent_kafka import KafkaError, Producer, Consumer
import psycopg2

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/container')
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(blueprint, version='1.0', title='Container MS API',
    description='API for checking container data', doc='/api/'
)
app.register_blueprint(blueprint)

ns = api.namespace('container', description='Operations to get container data.')
nsg = api.namespace('general', description='General application checks')

container = api.model('container', {
	'ID': fields.String(required = True, description = 'Container ID'),
	'Latitude': fields.Integer(required = True,description = 'Container current latitude'),
	'Longitude': fields.Integer(required = True,description = 'Container current longitude'),
	'Type': fields.String(required = True, description = 'Container type'),
	'Status': fields.String(required = True, description = 'Container status'),
	'CurrentCity': fields.String(required = True, description = 'City container is currently in'),
	'Brand': fields.String(required = True, description = 'Brand of the container'),
    'Capacity': fields.Integer(required = True,description = 'Capacity of the container')
})

class containerActions(object):
    def __init__(self):
        self.counter = 0

    def getAllContainers(self):
        conn = databaseActions.createConnection(self)
        cur = conn.cursor()
        cur.execute("SELECT * FROM containers;")
        containers=cur.fetchall()
        cur.close()
        conn.close()
        if len(containers) == 0:
            return 'There are no containers there.'
        else:
            return containers

    def getContainerByID(self, id):
        conn = databaseActions.createConnection(self)
        cur = conn.cursor()
        cur.execute("SELECT * from container WHERE id=%s", (id))
        containers=cur.fetchall()
        cur.close()
        conn.close()
        if len(containers) == 0:
            return 'There is no container with that ID.'
        else:
            return containers

    def getCityContainers(self, city):
        conn = databaseActions.createConnection(self)
        cur = conn.cursor()
        cur.execute("SELECT * from container WHERE city=%s", (city))
        containers=cur.fetchall()
        cur.close()
        conn.close()
        if len(containers) == 0:
            return 'There is no containers in the specified city.'
        else:
            return containers

class databaseActions(object):
    def __init__(self):
        self.counter = 0

@ns.route('/')
class containerList(Resource):
    '''Shows a list of all the containers in the system.'''
    @ns.doc('list_containers')
    def get(self):
        '''Lists Containers'''
        return cActions.getAllContainers()

@ns.route('/<int:id>')
@ns.response(404, 'Container not found')
@ns.param('id', 'Container ID')
class Container(Resource):
    '''Funtions to set the status of a container'''
    @ns.expect(container)
    def get(self, id):
        '''Returns data about a specified container.'''
        return  cActions.getContainerByID(id)

@ns.route('/<string:city>')
@ns.response(404, 'City not found')
@ns.param('city', 'Container ID')
class Container(Resource):
    '''Funtions to set the status of a container'''
    @ns.expect(container)
    def get(self, city):
        '''Returns containers in the city specified.'''
        return cActions.getCityContainers(city)

@nsg.route('/healthcheck')
class generalChecks(Resource):
    '''Basic Application Checks'''
    @nsg.doc('healthcheck')
    def get(self):
        '''Runs a basic health check'''
        return {'status': 'UP'}, 200

if __name__ == '__main__':
    app.run(debug=True)
