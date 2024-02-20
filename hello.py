from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/get-all-rounds")
def get_all_rounds():
    pass

@app.route("/add-new-round", methods=["POST"])
def add_new_round():
    pass

@app.route("/delete-one-round/<int:round_id>", methods=["DELETE"])
def delete_one_round():
    pass