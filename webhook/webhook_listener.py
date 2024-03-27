"""from flask import Flask, request, jsonify
import subprocess
import logging

logging.basicConfig(filename='webhook.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)


@app.route('/')
def index():
    return '<p>Webhook Listener is running!</p>'


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    logging.info("Webhook received %s", data)
    if data['event'] == 'push':
        subprocess.call(['./update.sh'])
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
"""

from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)

# Konfiguriere das Logging
logging.basicConfig(level=logging.INFO, filename='git_webhooks.log', format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/webhook', methods=['POST'])
def git_webhook():
    # Verarbeite die Webhook-Daten
    data = request.json
    logging.info('Webhook received with data: %s', data)

    # Versuche, ein 'git pull' Kommando auszuführen
    try:
        # Definiere den Pfad zum Repository
        repo_path = '/home/ubuntu/pythonDiscordBot'
        # Führe 'git pull' aus
        subprocess.check_output(['git', '-C', repo_path, 'pull'])
        logging.info('Git pull erfolgreich ausgeführt.')
        return jsonify({'status': 'Git pull erfolgreich.'}), 200
    except subprocess.CalledProcessError as e:
        logging.error('Fehler beim Git pull: %s', e.output)
        return jsonify({'status': 'Fehler beim Git pull.'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
