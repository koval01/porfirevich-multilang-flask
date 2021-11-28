from flask import Flask, jsonify, request
from flask_cors import CORS
from requests import post
import logging as log

log.basicConfig(
  format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s] %(message)s', 
  level=log.INFO
)
app = Flask(__name__)
CORS(app)


def translate(text: str, lang: str) -> str or None:
  try:
    resp = post("https://thetranslate.herokuapp.com/answer", json={
      "text": text, "to_lang": lang
    })
    log.info("Translate server status code: %d" % resp.status_code)
    
    if resp.status_code >= 200 < 400:
      json_resp = resp.json()
      text_result = json_resp["body"]["text"]

      log.info("Translate server json status: %s" % json_resp["success"])
      if json_resp["success"]:
        log.info("Translate success. Result text: \"%s\". Init text: \"%s\"" % (text_result, text))
        return text_result
      
  except Exception as e:
    log.warning("Translate function internal error!")
    
    
def generate(text: str, length: int) -> list or None:
  try:
    resp = post("https://pelevin.gpt.dobro.ai/generate/", json={
      "prompt": text,
      "length": length
    }, headers={
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15" 
                    "(KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    })
    log.info("AI server status code: %d" % resp.status_code)
    
    if resp.status_code >= 200 < 300 and \
      len(resp.text) > 50:
      
      log.info("Generate success! Result text (raw): \"%s\". Init text: \"%s\"" % (
        resp.text, text
      ))
      return resp.json()["replies"]
    
  except Exception as e:
    log.warning("AI Generate function internal error!")
    

@app.route('/')
def index_request() -> jsonify:
  return jsonify({
    "body": "Application is running!"
  })

  
@app.route('/generate', methods=["POST"])
def generate_request() -> jsonify:
  data = request.get_json()
  log.info("Generate method ordered: \"%s\"" % data)
  e = jsonify({"ok": False})  # default error response
  
  if data \
    and len(data["prompt"]) > 0 < 1000 \
    and data["length"] > 0 <= 60:
    
    log.info("Generate success. Len: %d. Prompt: \"%s\"" % (
      data["length"], data["prompt"]
    ))
    
    ru_text = translate(text=data["prompt"], lang="ru")
    if not ru_text: log.error("Error translate to ru from uk."); return e
    
    ai_resp = generate(length=data["length"], text=ru_text)
    if not ai_resp: log.error("Error AI response."); return e
    
    uk_text_array = [
      translate(text=replie, lang="uk") 
      for replie in ai_resp if len(replie) > 10
    ]
    
    return jsonify({
      "ok": len(uk_text_array) > 0, 
      "replies": uk_text_array
    })
  
  return e
  
  
if __name__ == '__main__': 
  app.run(debug=True)
