from requests import post
import logging as log


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
