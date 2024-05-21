from flask import Flask, jsonify

app = Flask(__name__)

# Пример списка пользователей
users = ['user1', 'user2', 'user3']

@app.route('/api/v1/accounts', methods=['GET'])
def get_users():
    return jsonify({'users': users})

if __name__ == '__main__':
    app.run(port=5432)
