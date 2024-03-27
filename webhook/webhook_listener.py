from flask import Flask, request, jsonify
import subprocess
import logging

logging.basicConfig(filename='webhook.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)


@app.route('/')
def index():
    return 'Webhook Listener is running!'


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    logging.info("Webhook received %s", data)
    if data['event'] == 'push':
        subprocess.call(['./update.sh'])
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
