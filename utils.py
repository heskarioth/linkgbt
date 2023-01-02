import os 

def find_file_in_app(file_name : str):
    """ Given file name this function will return it's location in the application """
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if name == file_name:
                return os.path.abspath(os.path.join(root, name))
