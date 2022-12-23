# main.py

import os
import subprocess
from PIL import Image
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint('main', __name__)

def executeCommand(command):
  error = ""
  output = ""
  print("Executing: " + command)
  try:
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
  except subprocess.CalledProcessError as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e.output).replace("\\n", "\n")  # to get the output even when error
  except Exception as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e)  # to get the output even when error
  #print("Output: " + output)
  return output, error

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/image')
@login_required
def image():
    return render_template('image.html')


@main.route('/profile', methods=['POST'])
def profile_post():

    imagefile = request.files.get('picture', '')
    if imagefile.filename == "":
        flash('Picture not selected. Try again.')
        return redirect(url_for('main.profile_post'))

    filter = request.form.get('filter')
    if filter == "Select filter":
        flash('Filter not selected. Try again.')
        return redirect(url_for('main.profile_post'))

    # Open the picture and save it
    filepath = os.path.join('image_processor/static', imagefile.filename)
    pic = Image.open(imagefile)
    pic.save(filepath)

    command = "which python3"
    output, error = executeCommand(command)
    print("output = " + str(output))
    print("error = " + str(error))

    command = "python3 ./image_processor/image_filter/image_filter.py -f " + filter + " -i " + filepath + " -o image_processor/static/processed.jpg"
    output, error = executeCommand(command)
    print("output = " + str(output))
    print("error = " + str(error))

    command = "rm " + filepath
    output, error = executeCommand(command)

    return redirect(url_for('main.image'))
