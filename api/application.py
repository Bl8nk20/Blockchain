from flask import Flask, jsonify, request
from uuid import uuid4
from src.blockchain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

# Restliche Routen wie in deiner Datei
# ... (mine, new_transaction, full_chain, register_nodes, consensus)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)