from flask import Flask, redirect, request
from onnxruntime import InferenceSession
from prepocessing import preprocessing
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=["GET"])
def index():
    return redirect("https://github.com/podolnayaa/antiFaker")  # TODO: redirect to addition`s page


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    try:
        inputs = preprocessing(**dict(request.get_json()))
        # print(inputs)
        result = model.run(None, {'X': [inputs]})[0][0][0]
        # TODO: get results from MongoDB or save new
        if result < 0.40:
            return {"response": "<font color=\"#FF033E\" style = \"font-weight: 600;\"> Низкая <br>" + str(round(result * 100)) + " % </font>" }
        elif result < 0.60:
            return {"response": "<font color=\"#FFB02E\" style = \"font-weight: 600;\"> Средняя <br>" + str(round(result * 100)) + " % </font>"}
        return {"response": "<font color=\"#30BA8F\" style = \"font-weight: 600;\"> Высокая <br>" + str(round(result * 100)) + " % </font>"}
    except Exception as e:
        return {"response": "<font style = \"font-size: small; font-weight: 600;\"> Извинете, не достаточно данных для определения достоверности </font>"}


if __name__ == "__main__":
    app.run(debug=True)