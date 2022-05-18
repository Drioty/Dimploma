from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {
        'id': 1,
        'Username': u'Pavel',
        'Age': 20,
        'Weight': 60,
        'High': 172,
        'Email': u'qqq@mail.ru'
    },
    {
        'id': 2,
        'Username': u'Ivan',
        'Age': 21,
        'Weight': 65,
        'High': 175,
        'Email': u'ppp@mail.ru'
    }
]

auth = [
    {
        'id': 1,
        'Password': u't3tt2g3t',
        'Login': u'user1',
        'User_id': 1
    },
    {
        'id': 2,
        'Password': u'j4j3kk4j',
        'Login': u'user2',
        'User_id': 2
    }
]

settings = [
    {
        'Login': u'user1',
        'id': 1,
        'Setting': u'json'
    },
    {
        'Login': u'user2',
        'id': 2,
        'Setting': u'json'
    }
]

recommendations = [
    {
        'Login': u'user1',
        'recommendation_id': 1,
        'recommendation': u'text'
    },
    {
        'Login': u'user2',
        'recommendation_id': 2,
        'recommendation': u'text'
    }
]

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    return jsonify({'recommendations': recommendations})

from flask import abort

@app.route('/recommendations/<int:recommendation_id>', methods=['GET'])
def get_recommendation(recommendation_id):
    recommendation = filter(lambda t: t['recommendation_id'] == recommendation_id, recommendations)
    if len(recommendation) == 0:
        abort(404)
    return jsonify({'recommendation': recommendation[0]})

@app.route('/settings', methods=['GET'])
def get_settings():
    return jsonify({'settings': settings})

@app.route('/userinfo/<int:user_id>', methods=['GET'])
def get_userinfo(user_id):
    user = filter(lambda t: t['id'] == user_id, users)
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/auth/registration', methods=['POST'])
def registration():
    if not request.json:
        abort(400)
    new_auth = {
        'id': auth[-1]['id'] + 1,
        'Password': request.json['Password'],
        'Login': request.json['Login'],
        'User_id': None
    }
    auth.append(new_auth)
    return jsonify({'auth': new_auth}), 201
    
@app.route('/userinfo', methods=['POST'])
def add_userinfo():
    if not request.json:
        abort(400)
    new_user = {
        'id': [-1]['id'] + 1,
        'Username': u'Misha',
        'Age': 19,
        'Weight': 68,
        'High': 168,
        'Email': u'www@mail.ru'
    }
    users.append(new_user)
    return jsonify({'userinfo': new_user}), 201

@app.route('/settings/<int:setting_id>', methods=['PUT'])
def update_settings(setting_id):
    new_setting = filter(lambda t: t['id'] == setting_id, settings)
    if len(task) == 0:
        abort(404)
    new_setting[0]['setting'] = request.json.get('setting', new_setting[0]['setting'])
    return jsonify({'settings': new_setting[0]})

if __name__ == '__main__':
    app.run(debug=True)
