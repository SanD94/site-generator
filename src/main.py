from create_blog import (
    delete_files,
    copy_files,
    generate_pages_recursive
)

dir_path_static = "./static"
dir_path_public = "./public"
template_path = "./template.html"
content_path = "./content"
dest_path = "./public"

def main():
    print("Deleting public directory...")
    delete_files(dir_path_public)

    print("Copying static files to public directory...")
    copy_files(src = dir_path_static, dest = dir_path_public)

    print("Generating page...")
    generate_pages_recursive(content_path, template_path, dest_path)
    


if __name__ == "__main__":
    main()