from flask import Flask, jsonify, request
from datetime import datetime as dt
from inference.engine import Model
import os

INDIC_LANG_CODES = ["as", "bn", "gu", "hi",
                     "kn", "ml", "mr", "or", "pa", "ta", "te"]
INDIC_LANGS = ["Assamese", "Bengali", "Gujarati",
               "Hindi", "Kannada", "Malayalam", "Marathi",
               "Odia", "Punjabi", "Tamil", "Telugu"]

app = Flask(__name__)

# load model
model = Model(expdir=os.environ.get('model_path'))


@app.route('/', methods=["GET"])
def get_status():
    return jsonify({"Status": "OK"})


@app.route('/list-indic', methods=["GET"])
def get_indic_lang_list():
    return jsonify({
        "indic-languages": [{
            "code": INDIC_LANG_CODES[i],
            "name": INDIC_LANGS[i]
        } for i in range(len(INDIC_LANGS))]}
    )


@app.route('/translate', methods=['POST'])
def get_translation():
    try:
        text = request.json.get('text')
        source_lang = request.json.get('source_lang')
        target_lang = request.json.get('target_lang')
        start_time = dt.now()

        if text is None or len(text) == 0:
            return jsonify({"msg": "text should not be empty."}), 400
        if source_lang != 'en':
            return jsonify({"msg": "source langauge should be \'en\'."}), 400
        if target_lang not in INDIC_LANG_CODES:
            return jsonify({"msg": f"target langauge should be one of {INDIC_LANG_CODES}."}), 400

        translation = model.translate_paragraph(text, source_lang, target_lang)

        return jsonify({
            "translation": translation,
            "model_mttr": int((dt.now() - start_time).total_seconds() * 1000),
        })
    except:
        return jsonify({"msg": "Something went wrong.", }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
