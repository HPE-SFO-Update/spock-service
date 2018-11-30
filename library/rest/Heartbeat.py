from flask import jsonify
from flask_restful import Resource
from library.multithreads.Scheduler import check_spock_map


class HeartbeatV1(Resource):
    """
    The class for heartbeat version 1 uri
    """
    @check_spock_map
    def get(self):
        """
        This is a heartbeat message
        :return: text message -> "Smart Fabric Orchestrator Update Service"
        """
        return jsonify({"message": "Smart Fabric Orchestrator Update Service"})
