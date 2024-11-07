from create_template import delete_files, copy_files

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    delete_files(dir_path_public)
    copy_files(src = dir_path_static, dest = dir_path_public)
    


if __name__ == "__main__":
    main()