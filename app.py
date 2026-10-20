import sys, os, shutil
from wasteDetection.pipeline.training_pipeline import TrainPipeline
from wasteDetection.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin
from wasteDetection.constant.application import APP_HOST, APP_PORT

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        
        
@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return "Training Successful!"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST", "GET"])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)
        
        weights = "my_model.pt" if os.path.exists("yolov5/my_model.pt") else ("best.pt" if os.path.exists("yolov5/best.pt") else "yolov5s.pt")
        
        # Clean runs/detect folder before detecting
        shutil.rmtree("yolov5/runs/detect", ignore_errors=True)
        
        cmd = f'cd yolov5 && "{sys.executable}" detect.py --weights {weights} --img 416 --conf 0.5 --source ../data/inputImage.jpg'
        os.system(cmd)
        
        exp_dir = "yolov5/runs/detect/exp"
        output_image = os.path.join(exp_dir, "inputImage.jpg")
        if os.path.exists(output_image):
            opencodebase64 = encodeImageIntoBase64(output_image)
            result = {'image': opencodebase64.decode('utf-8')}
        else:
            result = {'error': 'No output generated from detection model'}
        
        shutil.rmtree("yolov5/runs", ignore_errors=True)
    except ValueError as val:
        print(val)
        return Response("Value not found inside json data", status=400)
    except KeyError:
        return Response("Key value error incorrect key passed", status=400)
    except Exception as e:
        print(e)
        result = {"error": "Invalid input"}
        
    return jsonify(result)        
        
@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        weights = "my_model.pt" if os.path.exists("yolov5/my_model.pt") else ("best.pt" if os.path.exists("yolov5/best.pt") else "yolov5s.pt")
        os.system(f'cd yolov5 && "{sys.executable}" detect.py --weights {weights} --img 416 --conf 0.5 --source 0')
        shutil.rmtree("yolov5/runs", ignore_errors=True)
        return "Camera started" 
    except ValueError as val:
        print(val)
        return Response("Value not found inside json data", status=400)       
        
clApp = ClientApp()

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)