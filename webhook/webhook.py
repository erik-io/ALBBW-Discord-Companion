from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_webhook():
    data = request.json
    if data['ref'] == 'refs/heads/main':
        subprocess.run(['./deploy.sh'])
        return 'OK', 200
    else:
        return 'Ignored', 200


if __name__ == '__main__':
    app.run(port=3000)
