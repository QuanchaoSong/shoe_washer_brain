import random
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
# 最大16M
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["TIMEOUT"] = 120
CORS(app)


@app.route("/", methods=["POST", "GET"])
def hello_world():
    toBrainDataList = request.json.get("toBrainDataList")
    print("toBrainDataList:", toBrainDataList[0])
    return {"hi": random.randint(0, 100)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="26686", debug=True, threaded=True)
