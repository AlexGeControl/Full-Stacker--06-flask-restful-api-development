from flask import jsonify

from . import main

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    """ welcome to restful api development!
    """
    return jsonify({'message':'Hello, RESTful API development!'})