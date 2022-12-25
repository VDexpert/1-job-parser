import os

def del_temp_json(filename):
    path = os.path.abspath(filename)
    os.remove(path)

    return True

if __name__ == "__main__":
    del_temp_json()