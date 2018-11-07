from flask_restful import reqparse, abort, Api, Resource


class HeartbeatV1(Resource):

    def get(self):
        return "Smart Fabric Orchestrator Update Service"
