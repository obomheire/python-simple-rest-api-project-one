# from flask import Flask, jsonify, request
# from flask_restful import Api, Resource
# from pydantic import BaseModel, ValidationError, constr

# app = Flask(__name__)
# api = Api(app)


# def checkPostedData(postedData, functionName):
#     if (
#         functionName == "add"
#         or functionName == "subtract"
#         or functionName == "multiply"
#     ):
#         if "x" not in postedData or "y" not in postedData:
#             return 301  # Missing parameter
#         else:
#             return 200
#     elif functionName == "division":
#         if "x" not in postedData or "y" not in postedData:
#             return 301
#         elif int(postedData["y"]) == 0:
#             return 302
#         else:
#             return 200


# class Add(Resource):
#     def post(self):

#         # Step 1: Get posted data:
#         postedData = request.get_json()

#         # Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "add")
#         if status_code != 200:
#             retJson = {"Message": "An error happened", "Status Code": status_code}
#             return jsonify(retJson)

#         # If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)

#         # Step 2: Add the posted data
#         ret = x + y
#         retMap = {"Message": ret, "Status Code": 200}
#         return jsonify(retMap)


# class Subtract(Resource):
#     def post(self):
#         # If I am here, then the resouce Subtract was requested using the method POST

#         # Step 1: Get posted data:
#         postedData = request.get_json()

#         # Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "subtract")

#         if status_code != 200:
#             retJson = {"Message": "An error happened", "Status Code": status_code}
#             return jsonify(retJson)

#         # If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)

#         # Step 2: Subtract the posted data
#         ret = x - y
#         retMap = {"Message": ret, "Status Code": 200}
#         return jsonify(retMap)


# class Multiply(Resource):
#     def post(self):
#         # If I am here, then the resouce Multiply was requested using the method POST

#         # Step 1: Get posted data:
#         postedData = request.get_json()

#         # Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "multiply")

#         if status_code != 200:
#             retJson = {"Message": "An error happened", "Status Code": status_code}
#             return jsonify(retJson)

#         # If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)

#         # Step 2: Multiply the posted data
#         ret = x * y
#         retMap = {"Message": ret, "Status Code": 200}
#         return jsonify(retMap)


# class Divide(Resource):
#     def post(self):
#         # If I am here, then the resouce Divide was requested using the method POST

#         # Step 1: Get posted data:
#         postedData = request.get_json()

#         # Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "division")

#         if status_code != 200:
#             retJson = {"Message": "An error happened", "Status Code": status_code}
#             return jsonify(retJson)

#         # If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)

#         # Step 2: Multiply the posted data
#         ret = (x * 1.0) / y
#         retMap = {"Message": ret, "Status Code": 200}
#         return jsonify(retMap)


# api.add_resource(Add, "/add")
# api.add_resource(Subtract, "/subtract")
# api.add_resource(Multiply, "/multiply")
# api.add_resource(Divide, "/division")


# @app.route("/")
# def hello_world():
#     return "Hello World!"


# if __name__ == "__main__":
#     app.run(debug=True)
#     # app.run(host="0.0.0.0")
#     # app.run(host="127.0.0.1", port=80)

from typing import Annotated

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pydantic import BaseModel, Field, ValidationError, conint

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
