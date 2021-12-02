from flask import Flask, jsonify, request
from flask_cors import CORS

from reqproc import translate, generate
from other_code import available_lang

import logging as log

log.basicConfig(
  format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s] %(message)s', 
  level=log.INFO
)
app = Flask(__name__)
CORS(app)
    

@app.route('/')
def index_request() -> jsonify:
  return jsonify({"body": "Application is running!"})

  
@app.route('/generate', methods=["POST"])
def generate_request() -> jsonify:
  data = request.get_json()
  log.info("Generate method ordered: \"%s\"" % data)
  e = jsonify({"ok": False})  # default error response
  
  if data \
    and (len(data["prompt"]) > 0 < 1000) \
    and (data["length"] > 0 <= 60) \
    and (data["lang"] in available_lang):
    
    log.info("Generate success. Len: %d. Prompt: \"%s\"" % (
      data["length"], data["prompt"]
    ))
    
    ru_text = translate(text=data["prompt"], lang="ru")
    if not ru_text: log.error("Error translate to ru from uk."); return e
    
    ai_resp = generate(length=data["length"], text=ru_text)
    if not ai_resp: log.error("Error AI response."); return e
    
    userLang_text_array = [
      translate(text=replie, lang=data["lang"]) 
      for replie in ai_resp if len(replie) > 10
    ]
    
    return jsonify({
      "ok": len(userLang_text_array) > 0, 
      "replies": userLang_text_array
    })
  
  return e
  
  
if __name__ == '__main__': 
  app.run(debug=True)
