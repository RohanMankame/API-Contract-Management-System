from flask import jsonify, make_response

def _envelope(success, message=None, data=None, errors=None, meta=None, status=200):
    body = {"success": success, "message": message or "", "data": data, "errors": errors, "meta": meta}
    return make_response(jsonify(body), status)

def ok(data=None, message="OK", meta=None): 
    return _envelope(True, message, data, None, meta, 200)

def created(data=None, message="Created"): 
    return _envelope(True, message, data, None, None, 201)

def bad_request(message="Bad request", errors=None): 
    return _envelope(False, message, None, errors, None, 400)

def not_found(message="Not found"): 
    return _envelope(False, message, None, None, None, 404)

def server_error(message="Server error", errors=None): 
    return _envelope(False, message, None, errors, None, 500)