from flask import Flask, jsonify
from views import adverView, userView
from errors import ApiException

advApp = Flask('advertisement')

@advApp.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify({
        'status': error.status_code,
        'message': error.message
    })
    response.status_code = error.status_code
    return response

advApp.add_url_rule('/advertisement', view_func=adverView.as_view('advertisement'), methods=['GET'])
advApp.add_url_rule('/users/<int:user_id>', view_func=userView.as_view('user_view'), methods=['GET'])
advApp.add_url_rule('/users', view_func=userView.as_view('user_create'), methods=['POST'])

if __name__ == '__main__':
    advApp.run(host='127.0.0.1', port=5000)
