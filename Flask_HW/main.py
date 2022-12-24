from flask import jsonify
from views import adverView, userView, allUserView, allAdverView
from errors import ApiException
from app import advApp


@advApp.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify({
        'status': error.status_code,
        'message': error.message
    })
    response.status_code = error.status_code
    return response

# создаём правила обращения к нашим функциям
advApp.add_url_rule('/users', view_func=allUserView.as_view('users_views'), methods=['GET'])
advApp.add_url_rule('/users/<int:user_id>', view_func=userView.as_view('user_view'), methods=['GET'])
advApp.add_url_rule('/users', view_func=userView.as_view('user_create'), methods=['POST'])
advApp.add_url_rule('/users/<int:user_id>', view_func=userView.as_view('user_update'), methods=['PATCH'])
advApp.add_url_rule('/users/<int:user_id>', view_func=userView.as_view('user_delete'), methods=['DELETE'])
advApp.add_url_rule('/advertisement', view_func=allAdverView.as_view('advertisement_view'), methods=['GET'])
advApp.add_url_rule('/advertisement/<int:adver_id>', view_func=adverView.as_view('advertisements_view'), methods=['GET'])
advApp.add_url_rule('/advertisement', view_func=adverView.as_view('advertisement_create'), methods=['POST'])




if __name__ == '__main__':
    advApp.run(host='127.0.0.1', port=5000)
