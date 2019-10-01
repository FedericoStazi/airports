from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
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
            sr.show_routes(id)
            file = "files/"+id+".png"
            if id[1:] != "0":
                make_transparent(file)
            return send_file(file)
    except:
    	return "id not found"


def make_transparent(file):

    img = Image.open(file)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        elif item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(file, "PNG")
