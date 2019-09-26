import os
from flask import Blueprint, request, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from flask_restplus import Api, Namespace, Resource

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main import metrics


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

metrics_ns = Namespace('metrics', description='prometheus metrics collector endpoints')

@metrics.do_not_track()
@metrics_ns.route('/')
class PrometheusMetricsEndpoint(Resource):

    def get(self):
      from prometheus_client import multiprocess, CollectorRegistry

      if 'prometheus_multiproc_dir' in os.environ:
          registry = CollectorRegistry()
      else:
          registry = metrics.registry

      if 'name[]' in request.args:
          registry = registry.restricted_registry(request.args.getlist('name[]'))

      if 'prometheus_multiproc_dir' in os.environ:
          multiprocess.MultiProcessCollector(registry)
  
      headers = {'Content-Type': CONTENT_TYPE_LATEST}
      return generate_latest(metrics.registry), 200, headers

api.add_namespace(metrics_ns, path='/metrics')
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)