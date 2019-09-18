from flask import Flask, request, redirect, render_template
from flask_cors import CORS
import show_routes as sr

app = Flask(__name__)
CORS(app) #cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #(see https://flask-cors.readthedocs.io/en/latest/)

@app.route('/')
def web_page():
    id = str(request.args['id'])
    try:
        num = int(request.args['num'])
    except:
        num = 1000000
    try:
        if id == "query":
            return str(sr.get_list(num))
        else:
            return str(sr.show_routes(id))
    except:
    	return "id not found"
