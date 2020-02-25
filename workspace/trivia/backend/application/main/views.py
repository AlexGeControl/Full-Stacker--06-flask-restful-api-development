from flask import jsonify
from . import bp

@bp.route('/')
def index():
    """ welcome to restful api development!
    """
    response = jsonify(
        {'message':'Hello, RESTful API development!'}
    )
    
    return response, 200