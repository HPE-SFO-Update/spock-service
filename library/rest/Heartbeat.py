from flask import jsonify
from flask_restful import Resource



class HeartbeatV1(Resource):
    """
    The class for heartbeat version 1 uri
    """
    def get(self):
        """
        This is a heartbeat message
        :return: text message -> "Smart Fabric Orchestrator Update Service"
        """
        return jsonify({"message": "Smart Fabric Orchestrator Update Service"});
