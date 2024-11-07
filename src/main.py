import os
import shutil
from typing import TextIO

def main():
    delete_files("public")
    copy_files(src = "static", dest = "public")
    

def delete_files(src = "public"):
    if os.path.exists(src):
        shutil.rmtree(src)


def copy_files(src = "static", dest = "public"):
    if os.path.exists(src) == False:
        raise ValueError(f"source folder not found {src}")
    
    os.mkdir(dest)
    for path in os.listdir(src):
        cur_path = os.path.join(src, path)
        if os.path.isfile(cur_path):
            shutil.copy(cur_path, dest)
        else:
            next_dest = os.path.join(dest, path)
            copy_files(cur_path, next_dest)
        


if __name__ == "__main__":
    main()