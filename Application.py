import Blockchain
from textwrap import dedent
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain.Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    requires = ['sender', 'recipient', 'amount']
    if not all(k in values for k in requires):
        return "Missing Values", 400
    
    index = blockchain.new_transaction(sender=values['sender'], 
                                       recipient=values['recipient'], 
                                       amount= values['amount'])
    response = {'message' : f'transaction will beadded to Block {index}'}
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0",
                               recipient=node_identifier, 
                               amount=1)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message' : "New Block Forged",
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    
    if nodes is None:
        return "Error: Supply a valid list of Nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    
    responce = {
        'message' : "New Nodes have been added.",
        'total_nodes' : list(blockchain.nodes)
    }
    return jsonify(responce), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    
    if replaced:
        response = {
            'message' : 'Our chain was replaced!',
            'new_chain' : blockchain.chain
        }
    else:
        response = {
            'message' : 'Our chain is authoritative',
            'chain' : blockchain.chain
        }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)