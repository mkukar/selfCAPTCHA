# selfCAPTCHA

## DESCRIPTION
selfCAPTCHA is a variation on CAPTCHA where users upload their own photos to verify they are not a robot.

## QUICKSTART
The following steps will launch selfCAPTCHA running using a development instance on localhost.

### Requirements
- Python 3.5.1 or higher (64 bit version)

### Steps
Note1 - It is best practice to set this up in a virtual environment such as VENV. See Flask installation guide link in Note2 for more info.

Note2 - Steps written for Windows and adapted from:

https://flask.palletsprojects.com/en/1.1.x/installation/

https://github.com/OlafenwaMoses/ImageAI

1. Clone the git repo
2. Install Flask
```
pip install flask
```
3. Install ImageAI and its dependencies
```
pip install -U tensorflow keras opencv-python
pip3 install imageai --upgrade
```
4. Set Flask environment variables
```
set FLASK_APP=selfcaptcha
set FLASK_ENV=development
```
5. Launch Flask from base directory
```
python -m flask run
```
6. Load webpage http://127.0.0.1:5000

## LICENSE
MIT License

## AUTHOR
Created by Michael Kukar

August 2019

## ACKNOWLEDGEMENTS
- Icons made by Dave Gandy, Roundicons, and Freepik from http://www.flaticon.com/
- Website powered by Flask https://flask.palletsprojects.com/
- Image recognition powered by ImageAI http://imageai.org/
- Inspired by Jessica Freidin
