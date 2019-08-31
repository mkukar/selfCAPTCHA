# selfCAPTCHA Project
# CB: Michael Kukar 2019
# MIT License

import functools, os, random
from pprint import pprint

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from imageai.Prediction import ImagePrediction
from werkzeug.utils import secure_filename

bp = Blueprint('iamnotarobot', __name__, url_prefix="/iamnotarobot")

SAVE_IMAGE_PATH = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# image recognition trained to imagenet1000 images, goal images must be in list
# example list: https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a
GOAL_IMAGES = [
    'purse',
    'bus',
    'burrito',
    'screwdriver',
    'shopping basket',
    'cheeseburger',
    'hotdog',
    'tarantula',
    'bee',
    'hammer',
    'umbrella',
    'pretzel',
    'banana',
    'soccer ball',
    'school bus',
    'cup'
]


REQUIRED_IMAGE_COUNT = 3

# assigns a random goal image
# if lastImage is assigned, then we make sure the new image != lastImage
def getGoalImage(lastImage = None):
    newImage = random.choice(GOAL_IMAGES)

    if lastImage is not None:
        # makes sure not a duplicate of the last image
        while newImage == lastImage:
            newImage = random.choice(GOAL_IMAGES)
    return newImage


# makes sure the file is one of the allowed extensions (is an image)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# validates the image by checking if we can recognize it using imageai
# predictionImage is path to image user uploaded
# goal image is the name of the goal image from GOAL_IMAGES
def validateImage(predictionImage, goalImage):
    # load image here, not best practice but does load fast enough (less than a few seconds)
    prediction = ImagePrediction()
    prediction.setModelTypeAsSqueezeNet()
    prediction.setModelPath("selfcaptcha/static/algorithms/squeezenet_weights_tf_dim_ordering_tf_kernels.h5")
    prediction.loadModel()

    # converts goal image name to lowercase with underscores to match algo
    goalImage = goalImage.lower().replace(' ', '_')

    # tries top 5 predictions to see if they match (also must meet minimum probability requirement)
    bestGuesses, probabilities = prediction.predictImage(predictionImage, result_count=5 )
    foundMatch = False
    foundMatchProbability = 0
    for bestGuess, probability in zip(bestGuesses, probabilities):
        if bestGuess == goalImage and probability > 1: # must meet min probability of 1% to consider
            foundMatch = True
            foundMatchProbability = probability

    return (foundMatch, foundMatchProbability) # we use probability to determine if images are duplicates


@bp.route('/selfcaptcha', methods=('GET', 'POST'))
def splash():
    if request.method == 'POST':
        # if we click the checkbox, load a captcha
        # checkbox uses submit.x and submit.y since it is an image, that is how we recognize it here
        if 'submit.x' in request.form:
            return render_template('iamnotarobot/captcha.html', required_image=getGoalImage(), required_image_count=REQUIRED_IMAGE_COUNT)
        # the other submit button is from the captcha, so handle the captcha page here
        elif request.form['submit'] == 'Submit':
            # saves the images, or fails and renders a new captcha
            filenames = []
            for imageNumber in range(1, REQUIRED_IMAGE_COUNT+1):
                if 'image' + str(imageNumber) not in request.files: # image not found
                    return render_template('iamnotarobot/captcha.html', required_image=getGoalImage(request.form['required_image_name']), required_image_count=REQUIRED_IMAGE_COUNT)
                file = request.files['image' + str(imageNumber)]
                if file.filename == '': # image is empty or not selected
                    return render_template('iamnotarobot/captcha.html', required_image=getGoalImage(request.form['required_image_name']), required_image_count=REQUIRED_IMAGE_COUNT)
                if not allowed_file(file.filename): # photo is not valid format (incorrect extension)
                    return render_template('iamnotarobot/captcha.html', required_image=getGoalImage(request.form['required_image_name']), required_image_count=REQUIRED_IMAGE_COUNT)
                if file: # makes sure it is a secure filename and saves it
                    filename = str(imageNumber) + secure_filename(file.filename) # prepend the number to make unique
                    file.save(os.path.join(SAVE_IMAGE_PATH, filename))
                    filenames.append(filename)

            # checks if all the images were validated using image recognition algorithm
            allValid = True
            probabilitiesSet = set() # set will not allow duplicates so we can check length to ensure all photos were unique (not the exact same probability)
            for savedFile in filenames:
                validatedImageData = validateImage(os.path.join(SAVE_IMAGE_PATH, savedFile), request.form['required_image_name'])
                allValid = allValid and validatedImageData[0]
                probabilitiesSet.add(validatedImageData[1])

            # if we detected duplicate images return False (probabilities are exactly equal between 2 or more images)
            if len(probabilitiesSet) != REQUIRED_IMAGE_COUNT:
                allValid = False

            if not allValid:
                # if not valid, load another captcha (cannot be same as old captcha)
                return render_template('iamnotarobot/captcha.html', required_image=getGoalImage(request.form['required_image_name']), required_image_count=REQUIRED_IMAGE_COUNT)
            else:
                # if valid, we go to the splash page with a green checkmark now
                return render_template('iamnotarobot/splash.html', submit_button='green', is_disabled='disabled')

        # this case should not happen as the button should be disabled when green
        # however, if it does happen just refresh
        elif request.form['submit'] == 'green':
            return render_template('iamnotarobot/splash.html', submit_button='green', is_disabled = '')

    # default renders splash screen
    return render_template('iamnotarobot/splash.html', submit_button='checkbox', is_disabled = '')
