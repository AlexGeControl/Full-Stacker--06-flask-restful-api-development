from flask import jsonify

from . import bp

@bp.route('/')
@bp.route('/index')
@bp.route('/home')
def index():
    """ welcome to restful api development!
    """
    return jsonify({'message':'Hello, RESTful API development!'})