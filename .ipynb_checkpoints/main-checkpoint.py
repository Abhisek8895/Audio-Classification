from flask import Flask, render_template, request
import os
from runtime import main_function
from flask import send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'audios/'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_file_in_folder(folder_path):
    # Iterate over all the files in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        # Check if the item is a file
        if os.path.isfile(item_path):
            # Remove the file
            os.remove(item_path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/uploaded', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['audioFile']
    
    if file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file or no file selected.', 400
    
    default_filename = 'sample' + os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_FOLDER, default_filename)
    file.save(file_path)
    
    return render_template("uploaded.html", audio_filename=default_filename)

@app.route("/prediction", methods=['POST'])
def prediction():
    audio_folder = "audios"
    # print(audio_filename)
    # audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    for file in os.listdir(audio_folder):
        audio_filename = audio_folder+ "/" + file
    try:
        predicted_result = main_function(audio_file=audio_filename)
    except Exception as e:
        return "Please upload the file again"
    # predicted_result = main_function(audio_file=audio_filename)
    try:
        delete_file_in_folder(UPLOAD_FOLDER)
    except Exception as e:
        pass
    return render_template("uploaded.html", predicted_result=predicted_result, audio_filename=audio_filename)

@app.route("/record_prediction", methods=['POST'])
def recorded_prediction():
    audio_folder = "audios"
    # print(audio_filename)
    # audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    # for file in os.listdir(audio_folder):
    #     audio_filename = audio_folder+ "/" + file
    # try:
    #     predicted_result = main_function(audio_file=audio_filename)
    # except Exception as e:
    #     return "Please upload the file again"
    # # predicted_result = main_function(audio_file=audio_filename)
    # try:
    #     delete_file_in_folder(UPLOAD_FOLDER)
    # except Exception as e:
    #     pass
    return render_template("record_prediction.html")
@app.route('/audios/<filename>')
def audios(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
