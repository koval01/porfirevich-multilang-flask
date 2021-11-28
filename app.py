from flask import Flask, jsonify
from flask_cors import CORS
from requests import post

app = Flask(__name__)
CORS(app)


def translate(text: str, lang: str) -> str or None:
  resp = post("https://thetranslate.herokuapp.com/answer", json={
    "text": text, "to_lang": lang
  })
  if resp.status_code > 200 < 300:
    json_resp = resp.json()
    if json_resp["success"]:
      return json_resp["body"]["text"]
    
    
def generate(text: str, length: int) -> list or None:
  resp = post("https://pelevin.gpt.dobro.ai/generate/", json={
    "prompt": text,
    "length": length
  }, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15" 
                  "(KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Host": "pelevin.gpt.dobro.ai",
    "Origin": "https://porfirevich.ru",
    "Content-Type": "text/plain;charset=UTF-8"
  })
  if resp.status_code > 200 < 300 and len(resp.text) > 50:
    return resp.json()["replies"]
    

@app.route('/')
def index_request():
  return jsonify({"body": "Application is running!"})

  
@app.route('/generate')
def generate_request(request):
  data = request.get_json()
  if data and \
    len(data["prompt"]) > 0 < 1000 \
    and data["length"] > 0 <= 60:
    
    ru_text = translate(text=data["prompt"], lang="ru")
    ai_resp = generate(length=data["length"], text=ru_text)
    
    uk_text_array = [
      translate(text=replie, lang="uk") for replie in ai_resp if len(replie) > 10
    ]
    
    return jsonify({
      "ok": len(uk_text_array) > 0, 
      "replies": uk_text_array
    })
  
  return jsonify({"ok": False})
  
  
if __name__ == '__main__': 
  app.run(debug=True)
