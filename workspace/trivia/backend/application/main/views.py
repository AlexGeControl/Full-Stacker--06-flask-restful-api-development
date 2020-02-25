from flask import jsonify

from . import bp

@bp.route('/')
@bp.route('/index')
@bp.route('/home')
def index():
    """ welcome to restful api development!
    """
    response = jsonify(
        {'message':'Hello, RESTful API development!'}
    )

    return response, 200