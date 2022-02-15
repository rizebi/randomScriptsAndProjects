import split
from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


exemptedIPs = ['192.168.100.11']

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["15 per minute"]
)

@app.errorhandler(429)
def errorAPILimitReached(e):
    # API ;imit reached
    # Return 429
    return Response("{'responseCode':'429', 'message': 'API limit reached. Try again in few minutes'}", status=429, mimetype='application/json')

def exemptFuction():
  currentIP = get_remote_address()
  if currentIP in exemptedIPs:
    return True
  return False

@app.route('/wordsplit', methods=['GET'])
@limiter.limit("15 per minute", exempt_when=exemptFuction)
def wordSplit():
  if 'search_term' in request.args:
    search_term = str(request.args['search_term'])

  elif request.json is not None:
    request.json
    if 'search_term' not in request.json:
      # Bad JSON
      # Return 400
      return Response("{'responseCode':'400', 'message': 'JSON provided, but it does not contain <search_term> key'}", status=400, mimetype='application/json')
    else:
      search_term = str(request.json["search_term"])
  else:
    # Nor parameter or JSON provided
    # Return 400
    return Response("{'responseCode':'400', 'message': 'Nor parameter search_term or JSON provided'}", status=400, mimetype='application/json')

  # Now process search_term and respond accordingly
  responseList = split.Infer_Spaces(search_term)[::-1]
  if len(responseList) == 0:
    # No content found
    # Return 204
    return Response("{'responseCode':'204', 'message': 'No content found'}", status=204, mimetype='application/json')

  returnJSON = {"entry_term" : search_term, 'responseCode':'200', 'message': 'OK'}
  i = 1
  while i <= len(responseList):
    returnJSON["part" + str(i)] = responseList[i - 1]
    i += 1

  return Response(str(returnJSON), status=200, mimetype='application/json')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
