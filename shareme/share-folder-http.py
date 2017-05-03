from flask import Flask, request, render_template, send_from_directory
from collections import namedtuple
import os

MAIN_FOLDER = '/shareme'

FileType = namedtuple('FileType', 'path is_file name relative_path')

app = Flask(__name__, template_folder='.', static_folder='static', static_url_path='')

@app.route("/")
def show_file():

    if is_file(MAIN_FOLDER):
        return serve_file(MAIN_FOLDER)

    requested_file = calculate_path(request.args.get('f', ''))
   
    if not is_folder_location_valid(requested_file):
        return show_error_message('Invalid requested folder')
   
    if is_file(requested_file):
        return serve_file(requested_file) 

    relative_path = get_relative_path(requested_file)
    root_path = get_relative_path(calculate_path(os.path.join(relative_path, '..')))

    root_folder = [] if '.' == relative_path else [FileType(path=root_path, is_file=False, name='..', relative_path=root_path)]
    folders = root_folder + get_items(requested_file)

    return render_template('content.html', found_files=folders, path=relative_path)

def serve_file(requested_file):
    if is_file(requested_file):
        base_dir, filename = os.path.split(requested_file)
        return send_from_directory(directory=base_dir, filename=filename, as_attachment=True)
    return None

def calculate_path(path):
    return os.path.abspath(os.path.join(MAIN_FOLDER, path))

def get_relative_path(path):
    return os.path.relpath(path, start=MAIN_FOLDER)

def is_file(path):
    return os.path.isfile(path)

def show_error_message(message):
    return message

def is_folder_location_valid(folder):
    return os.path.commonprefix([MAIN_FOLDER, folder]) == MAIN_FOLDER

def get_items(path):
    items = []
    for item in os.listdir(path):
        file_path = os.path.join(path, item)
        items.append(FileType(path=file_path, is_file=os.path.isfile(file_path), name=item, relative_path=get_relative_path(file_path)))
    return items


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)

