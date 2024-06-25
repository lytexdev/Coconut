import os
import shutil
import subprocess


def run_npm_build():
    os.chdir("./coconut-shell")
    result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error during npm run build:")
        print(result.stderr)
        exit(1)
    else:
        print("npm run build completed successfully.")
    os.chdir("..")


def copy_images():
    src_images_folder = "./coconut-shell/src/assets/images"
    dist_images_folder = "./coconut-shell/dist/assets/images"
    
    if os.path.exists(src_images_folder):
        os.makedirs(dist_images_folder, exist_ok=True)
        
        for filename in os.listdir(src_images_folder):
            src_file = os.path.join(src_images_folder, filename)
            dest_file = os.path.join(dist_images_folder, filename)
            shutil.copy(src_file, dest_file)


def move_and_rename_files():
    dist_folder = "./coconut-shell/dist/assets"
    static_folder = "./static/assets"

    os.makedirs(static_folder, exist_ok=True)

    try:
        for root, dirs, files in os.walk(dist_folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, dist_folder)
                new_file_path = os.path.join(static_folder, relative_path)

                # Rename CSS and JS files
                if filename.endswith(".css"):
                    new_file_path = os.path.join(static_folder, "main.css")
                elif filename.endswith(".js"):
                    new_file_path = os.path.join(static_folder, "main.js")

                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

                print(f"Moving {file_path} to {new_file_path}")
                shutil.move(file_path, new_file_path)
    except Exception as e:
        print(f"Error moving files: {e}")

    shutil.rmtree(dist_folder)

    print("\nFrontend build completed successfully!\n")


if __name__ == "__main__":
    run_npm_build()
    copy_images()
    move_and_rename_files()
