from flask import Flask
from flask import request
from flask import jsonify
import json

from model.statistical import statisticalModel

app = Flask(__name__)

statistical_model_gs = statisticalModel('gs')
statistical_model_jl = statisticalModel('jl')

@app.route("/convertIntoGyeongsang", methods=['POST'])
def convert_into_gyeongsang():
    data = request.json
    action = data['action']
    standard_sentence = action['parameters']['sentence']['value']

    dialect_sentence = statistical_model_gs.inference_sentence(standard_sentence)
    action['dialect_sentence'] = dialect_sentence

    response = {'version': data['version'], 'resultCode': "OK", 'output': action}
    
    return jsonify(response)

@app.route("/convertIntoJeolla", methods=['POST'])
def convert_into_jeolla():
    data = request.json
    action = data['action']
    standard_sentence = action['parameters']['sentence']['value']

    dialect_sentence = statistical_model_jl.inference_sentence(standard_sentence)
    action['dialect_sentence'] = dialect_sentence
    
    response = {'version': data['version'], 'resultCode': "OK", 'output': action}
    
    return jsonify(response)

@app.route("/health")
def health_check():
    return "200 OK"

@app.route("/initAction")
def init_action():
    return 0

if __name__ == "__main__":
    app.run(host='0.0.0.0')
