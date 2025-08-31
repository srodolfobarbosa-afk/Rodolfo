from flask import Blueprint, jsonify
from supabase_client import supabase_manager

agents_bp = Blueprint("agents", __name__)

@agents_bp.route("/", methods=["GET"])
def get_agents():
    agents = supabase_manager.get_all_agents()
    return jsonify(agents)

@agents_bp.route("/<int:agent_id>", methods=["GET"])
def get_agent_by_id(agent_id):
    agent = supabase_manager.get_agent_by_id(agent_id)
    if agent:
        return jsonify(agent)
    return jsonify({"error": "Agent not found"}), 404


