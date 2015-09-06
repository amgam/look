import os, sys

from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from werkzeug import secure_filename

from imageEngine.ColorDescriptor import ColorDescriptor
from imageEngine.ImageComparator import ImageComparator
import cv2

# create flask instance
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/upload")
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

INDEX = os.path.join(os.path.dirname(__file__), 'static/queryDict.json')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# main route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():

    if request.method == "POST":

        RESULTS_ARRAY = []

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = "/static/upload/" + filename

            try:
                QUERY = "static/upload/" + file.filename
                QUERYPATH = os.path.join(os.path.dirname(__file__), QUERY)
                print QUERYPATH
                queryImage = cv2.imread(QUERYPATH)
                cd = ColorDescriptor((8, 12, 3))
                queryHist = cd.extractHist(queryImage)

               # load the query image and describe it
               #  for imgPath in imgDB:
               #      image = cv2.imread(imgFileDirectory + imgPath)
               #      result = cd.extractHist(image)
               #      queryDict[imgPath] = result
               #  pickle.dump(queryDict, open("queryDict.json", "wb"))

                s = ImageComparator(INDEX)
                results = s.compare(queryHist)

                # loop over the results, displaying the score and image name
                for (score, resultID) in results:
                    RESULTS_ARRAY.append(
                        {"image": str(resultID), "score": str(score)})

                # return success
                return jsonify(results=(RESULTS_ARRAY))
            except:
                # return error
                return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
        else:
            print "EXITING"

@app.route('/imgDB/<img>')
def imageDB(img):
    return send_from_directory(app.static_folder, '/imgDB/' + img)

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
