from typing import Annotated
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pydantic import BaseModel, Field, ValidationError

app = Flask(__name__)
api = Api(app)


# DTO using Pydantic
class MathOperationDTO(BaseModel):
    x: Annotated[int, Field(strict=True)]
    y: Annotated[int, Field(strict=True)]

    model_config = {"extra": "forbid"}


# Common parser function using Pydantic
def parse_input():
    try:
        data = MathOperationDTO(**request.get_json())
        return data, None
    except ValidationError as e:
        return None, {
            "Message": "Invalid input",
            "Errors": e.errors(),
            "Status Code": 400,
        }


class Add(Resource):
    def post(self):
        data, error = parse_input()
        if error:
            return jsonify(error)
        result = data.x + data.y
        return jsonify({"Message": result, "Status Code": 200})


class Subtract(Resource):
    def post(self):
        data, error = parse_input()
        if error:
            return jsonify(error)
        result = data.x - data.y
        return jsonify({"Message": result, "Status Code": 200})


class Multiply(Resource):
    def post(self):
        data, error = parse_input()
        if error:
            return jsonify(error)
        result = data.x * data.y
        return jsonify({"Message": result, "Status Code": 200})


class Divide(Resource):
    def post(self):
        data, error = parse_input()
        if error:
            return jsonify(error)

        if data.y == 0:
            return jsonify(
                {"Message": "Division by zero is not allowed", "Status Code": 400}
            )

        result = data.x / data.y
        return jsonify({"Message": result, "Status Code": 200})


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0")
    # app.run(host="127.0.0.1", port=80)
