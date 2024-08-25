from flask import Flask, request, jsonify

# Constants
PORT = 9000
HOST = '0.0.0.0'
REQUEST_ID_HEADER = 'x-fc-request-id'

app = Flask(__name__)

@app.route('/initialize', methods=['POST'])
def initialize():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print(f"FC Initialize Start RequestId: {rid}")
    # do your things
    print(f"FC Initialize End RequestId: {rid}")
    return 'Hello FunctionCompute, initialize \n', 200

@app.route('/invoke', methods=['POST'])
def invoke():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print(f"FC Invoke Start RequestId: {rid}")
    try:
        # get body to do your things
        body_str = request.data.decode('utf-8')
        print(body_str)
        json.loads(body_str)  # Parsing JSON to ensure it's valid
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 404

    print(f"FC Invoke End RequestId: {rid}")
    return 'OK', 200

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)

