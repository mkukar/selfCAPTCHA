# selfCAPTCHA

## DESCRIPTION
selfCAPTCHA is a variation on CAPTCHA where users upload their own photos to verify they are not a robot, rather than clicking on existing images.

## QUICKSTART
The following steps will launch selfCAPTCHA running using a development instance on localhost.

### Requirements
- Python 3.5.1 or higher (64 bit version)

### Steps
Note 1 - It is best practice to set this up in a virtual environment such as VENV. See Flask installation guide link in Note 2 for more info.

Note 2 - Steps written for Windows and adapted from:

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

## DEMO GIF
https://gfycat.com/circularmaturehalcyon

## LICENSE
MIT License

## AUTHOR
Created by Michael Kukar

August 2019

## ACKNOWLEDGEMENTS
- Filmed by and original idea from Jessica Freidin
- Icons made by Dave Gandy, Roundicons, and Freepik from http://www.flaticon.com/
- Website powered by Flask https://flask.palletsprojects.com/
- Image recognition powered by ImageAI http://imageai.org/
- Project created for 1st Programmer Humor Hackathon - Overengineering https://www.programmerhumor.org/Hackathon
