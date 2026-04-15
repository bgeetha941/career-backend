from flask import Blueprint, jsonify, request
from services.stream_service import StreamService

stream_bp = Blueprint('stream_bp', __name__)
stream_service = StreamService()

@stream_bp.route('/', methods=['GET'])
def get_all_streams():
    streams = stream_service.get_all_streams()
    return jsonify(streams), 200

@stream_bp.route('/<stream_id>', methods=['GET'])
def get_stream_details(stream_id):
    stream = stream_service.get_stream_by_id(stream_id)
    if not stream:
        return jsonify({'error': 'Stream not found'}), 404
    return jsonify(stream), 200

@stream_bp.route('/<stream_id>/sub-streams', methods=['GET'])
def get_sub_streams(stream_id):
    sub_streams = stream_service.get_sub_streams(stream_id)
    if sub_streams is None:
        return jsonify({'error': 'Stream not found'}), 404
    return jsonify(sub_streams), 200

@stream_bp.route('/<stream_id>/<sub_stream_id>', methods=['GET'])
def get_sub_stream_details(stream_id, sub_stream_id):
    details = stream_service.get_sub_stream_details(stream_id, sub_stream_id)
    if not details:
        return jsonify({'error': 'Sub-stream not found'}), 404
    return jsonify(details), 200
