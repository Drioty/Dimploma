from flask import Flask, jsonify, request

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

@app.route('/settings/<int:setting_id>', methods=['GET'])
def get_setting(setting_id):
    setting = (filter(lambda t: t['id'] == setting_id, settings))
    if len(setting) == 0:
        abort(404)
    return jsonify({'setting': setting[0]})

@app.route('/userinfo', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/userinfo/<int:user_id>', methods=['GET'])
def get_userinfo(user_id):
    user = filter(lambda t: t['id'] == user_id, users)
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/auth', methods=['GET'])
def get_auth():
    return jsonify({'auth': auth})

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/auth/registration', methods=['POST'])
def registration():
    if not request.json or not 'Login' in request.json or not 'Password' in request.json:
        abort(400)
    new_auth = {
        'id': auth[-1]['id'] + 1,
        'Password': request.json.get('Password', ""),
        'Login': request.json.get('Login', ""),
        'User_id': users[-1]['id'] + 1
    }
    auth.append(new_auth)
    return jsonify({'auth': new_auth}), 201
   
@app.route('/settings', methods=['POST'])
def add_setting():
    if not request.json or not 'Login' in request.json:
        abort(400)
    new_setting = {
        'id': settings[-1]['id'] + 1,
        'Login': request.json['Login'],
        'Setting': request.json.get('Setting', "")
    }
    settings.append(new_setting)
    return jsonify({'setting': new_setting}), 201

@app.route('/userinfo', methods=['POST'])
def add_userinfo():
    if not request.json or not 'Username' in request.json:
        abort(400)
    new_user = {
        'id': users[-1]['id'] + 1,
        'Username': request.json.get('Username', ""),
        'Age': request.json.get('Age', ""),
        'Weight': request.json.get('Weight', ""),
        'High': request.json.get('High', ""),
        'Email': request.json.get('Email', "")
    }
    users.append(new_user)
    return jsonify({'userinfo': new_user}), 201



@app.route('/settings/<int:setting_id>', methods=['PUT'])
def update_settings(setting_id):
    new_setting = filter(lambda t: t['id'] == setting_id, settings)
    if len(new_setting) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Login' in request.json and type(request.json['Login']) is not unicode:
        abort(400)
    if 'Setting' in request.json and type(request.json['Setting']) is not unicode:
        abort(400)
    new_setting[0]['Login'] = request.json.get('Login', new_setting[0]['Login'])
    new_setting[0]['Setting'] = request.json.get('Setting', new_setting[0]['Setting'])
    return jsonify({'settings': new_setting[0]})

if __name__ == '__main__':
    app.run(debug=True)
