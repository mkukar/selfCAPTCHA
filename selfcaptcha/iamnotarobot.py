import functools, os, random
from pprint import pprint

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from imageai.Prediction import ImagePrediction
from werkzeug.utils import secure_filename

bp = Blueprint('iamnotarobot', __name__, url_prefix="/iamnotarobot")

SAVE_IMAGE_PATH = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

GOAL_IMAGES = [
    'purse',
    'bus',
    'street sign',
    'burrito',
    'screwdriver',
    'shopping basket',
    'cheeseburger',
    'hotdog'
]

# assigns a random goal image
def getGoalImage():
    return random.choice(GOAL_IMAGES)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

# validates the image by checking if we can recognize it using
def validateImage(predictionImage, goalImage):
    # load image here, will make very slow (not great)
    # TODO - change this
    prediction = ImagePrediction()
    prediction.setModelTypeAsSqueezeNet()
    prediction.setModelPath("selfcaptcha/static/algorithms/squeezenet_weights_tf_dim_ordering_tf_kernels.h5")
    # THIS IS MUCH SLOWER BUT MORE ACCURATE
    #prediction.setModelTypeAsDenseNet()
    #prediction.setModelPath("selfcaptcha/static/algorithms/DenseNet-BC-121-32.h5")
    prediction.loadModel()

    # converts goal image name to lowercase with underscores to match algo
    goalImage = goalImage.lower().replace(' ', '_')


    bestGuesses, probabilities = prediction.predictImage(predictionImage, result_count=5 ) # if in first 5 results that is good enough
    foundMatch = False
    for bestGuess, probability in zip(bestGuesses, probabilities):
        print(bestGuess + ":" + str(probability)) # debug line, erase this
        if bestGuess == goalImage:
            foundMatch = True

    return foundMatch


# initial splash screen (I am not a robot checkbox)
@bp.route('/selfcaptcha', methods=('GET', 'POST'))
def slash():
    if request.method == 'POST':
        # if we click the checkbox, render the captcha
        if request.form['submit'] == 'checkbox':
            return render_template('iamnotarobot/captcha.html', required_image=getGoalImage())
        # if we submit from the captcha, then we want to validate it
        elif request.form['submit'] == 'Submit':
            print(request.form, flush=True)
            print(request.files, flush=True)

            # saves the image, or fails and then we can error out
            if 'image' not in request.files:
                flash('No photo found')
                return render_template('iamnotarobot/captcha.html', required_image=request.form['required_image_name'])
            file = request.files['image']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No photo uploaded')
                return render_template('iamnotarobot/captcha.html', required_image=request.form['required_image_name'])
            if not allowed_file(file.filename):
                flash('Invalid photo format')
                return render_template('iamnotarobot/captcha.html', required_image=request.form['required_image_name'])
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(SAVE_IMAGE_PATH, filename))

            # checks if the image was validated. if so, we go back to splash and say we're all good
            valid = validateImage(os.path.join(SAVE_IMAGE_PATH, filename), request.form['required_image_name'])
            # if not, we just refresh with a new required image
            if not valid:
                return render_template('iamnotarobot/captcha.html', required_image=getGoalImage())
            else:
                return render_template('iamnotarobot/splash.html', submit_button='green')
        # for green we don't want to do anything, just refresh the page I guess
        elif request.form['submit'] == 'green':
            return render_template('iamnotarobot/splash.html', submit_button='green')

    return render_template('iamnotarobot/splash.html', submit_button='checkbox')
