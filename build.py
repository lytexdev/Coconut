import os
import shutil
import subprocess


def run_npm_build():
    cange_dir = os.chdir("./coconut-shell")
    result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error during npm run build:")
        print(result.stderr)
        exit(1)
    else:
        print("npm run build completed successfully.")


def move_and_rename_files():
    dist_folder = "./dist/assets"
    static_folder = "../static/assets"

    os.makedirs(static_folder, exist_ok=True)

    try:
        for filename in os.listdir(dist_folder):
            file_path = os.path.join(dist_folder, filename)
            if filename.endswith(".css"):
                new_name = "main.css"
            elif filename.endswith(".js"):
                new_name = "main.js"
            else:
                new_name = filename

            new_file_path = os.path.join(static_folder, new_name)

            print(f"Moving {file_path} to {new_file_path}")
            shutil.move(file_path, new_file_path)
    except Exception as e:
        print(f"Error moving files: {e}")

    shutil.rmtree(dist_folder)

    print("\nFrontend build completed successfully!\n")


if __name__ == "__main__":
    run_npm_build()
    move_and_rename_files()
