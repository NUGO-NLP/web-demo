from flask import Flask
from flask import request
from flask import jsonify
import json
import os

from model.statistical import statisticalModel
from evaluate import word_accuracy, sentence_accuracy, word_accuracy_oov

current_path = os.path.dirname(os.path.abspath( __file__ ))
sent_gs_valid_filename = os.path.join(current_path, 'data/sent_gs_test.json')
sent_jl_valid_filename = os.path.join(current_path, 'data/sent_jl_test.json')
result_gs_filename = os.path.join(current_path, 'output/sent_result_gs.json')
result_jl_filename = os.path.join(current_path, 'output/sent_result_jl.json')
word_dict_gs_filename = os.path.join(current_path, 'model/save/statistical_word_dict_gs.json')
word_dict_jl_filename = os.path.join(current_path, 'model/save/statistical_word_dict_jl.json')

statistical_model_gs = statisticalModel('gs')
statistical_model_jl = statisticalModel('jl')

app = Flask(__name__)

@app.route("/convertIntoGyeongsang", methods=['POST'])
def f1():
    data = request.json	#
    version = data['version']
    action = data['action']
    resultCode = "OK"
    src = action['parameters']['sentence']['value']
    # dialect_sentence = translate_sentence(model, SRC, TRG, src, INPUT_LEVEL, device)
    dialect_sentence = statistical_model_gs.inference_sentence(src)
    print('gyeongsang before :', src)
    print('gyeongsang after :', dialect_sentence)
    action['dialect_sentence'] = dialect_sentence
    response = {'version': version, 'resultCode': resultCode, 'output': action}
    
    return jsonify(response)

@app.route("/convertIntoJeolla", methods=['POST'])
def f2():
    data = request.json
    version = data['version']
    action = data['action']
    resultCode = "OK"
    src = action['parameters']['sentence']['value']
    dialect_sentence = statistical_model_jl.inference_sentence(src)
    action['dialect_sentence'] = dialect_sentence
    response = {'version': version, 'resultCode': resultCode, 'output': action}
    
    return jsonify(response) 

@app.route("/health")
def f3():
    return "200 OK"

@app.route("/initAction")
def f4():
    print("--- Start ---")
    return 0

if __name__ == "__main__":
    app.run(host='0.0.0.0')
