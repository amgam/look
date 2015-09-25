import os, sys, glob

from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from werkzeug import secure_filename

from imageEngine.PreProcessor import PreProcessor
from imageEngine.QueryAnalyzer import QueryAnalyzer
from imageEngine.ImageComparator import ImageComparator

# create flask instance
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/upload")
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#File paths
IMG_INFO = 'static/data/imgInfo.json'
TRAINED_DATA = 'static/data/bof.pkl'


IMG_DATA_LOAD = os.path.join(os.path.dirname(__file__), IMG_INFO)
TRAINED_DATA = os.path.join(os.path.dirname(__file__), TRAINED_DATA)

IMG_DB_FOLDER = os.path.join(os.path.dirname(__file__), 'static/imgDB/')
TAGS_FILE = os.path.join(os.path.dirname(__file__), 'static/tags/train_tags.txt')


# Run pre-processor
preProcessor = PreProcessor(IMG_DATA_LOAD, TRAINED_DATA)

if(preProcessor.isDBMissing()):
    preProcessor.processImages(IMG_DB_FOLDER) #need to generate processed imageInfo

# if(preProcessor.isModelUntrained()):
#     #train model
#     preProcessor.trainData(IMG_DB_FOLDER)

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
            #upload incoming image
            filename = secure_filename(file.filename)

            #clear contents
            dirPath = UPLOAD_FOLDER
            fileList = os.listdir(dirPath)
            for fileName in fileList:
                os.remove(dirPath+"/"+fileName)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            # img = "/static/upload/" + filename

            try:
                QUERY = "static/upload/" + file.filename
                QUERY_PATH = os.path.join(os.path.dirname(__file__), QUERY)

                analyzer = QueryAnalyzer(QUERY_PATH) #analyze incoming image

                queryHistVisual = analyzer.analyze("visual")
                # print "VIZ:", type(queryHistVisual)
                queryHistColor = analyzer.analyze("color")
                # print "COL:", type(queryHistColor)
                scoresText = analyzer.processImageTags(queryTags, TAGS_FILE)

                imageComparator = ImageComparator(IMG_DATA_LOAD)

                resultsVectorVisual = imageComparator.compareAgainstDB(queryHistVisual, "visual")
                resultsVectorColor = imageComparator.compareAgainstDB(queryHistColor, "color")


                results = imageComparator.combineResults(resultsVectorColor, resultsVectorVisual)
                print "\nBINGO\n"

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
