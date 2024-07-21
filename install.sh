#!/bin/bash

# Install npm dependencies
install_npm_dependencies() {
    cd ./coconut-shell || exit
    if ! npm install; then
        echo "Error during npm install."
        exit 1
    else
        echo "npm dependencies installed successfully."
    fi
    cd ..
}

# Build the frontend (coconut-shell)
run_npm_build() {
    cd ./coconut-shell || exit
    if ! npm run build; then
        echo "Error during npm run build:"
        exit 1
    else
        echo "npm run build completed successfully."
    fi
    cd ..
}

# Copy images from src to dist folder
copy_images() {
    src_images_folder="./coconut-shell/src/assets/images"
    dist_images_folder="./coconut-shell/dist/assets/images"

    if [ -d "$src_images_folder" ]; then
        mkdir -p "$dist_images_folder"
        cp -r "$src_images_folder/"* "$dist_images_folder/"
    fi
}

# Move and rename files in dist folder
move_and_rename_files() {
    dist_folder="./coconut-shell/dist/assets"
    static_folder="./static/assets"

    mkdir -p "$static_folder"

    find "$dist_folder" -type f | while read -r file; do
        relative_path="${file#$dist_folder/}"
        new_file_path="$static_folder/$relative_path"

        # Rename CSS and JS files
        if [[ $file == *.css ]]; then
            new_file_path="$static_folder/main.css"
        elif [[ $file == *.js ]]; then
            new_file_path="$static_folder/main.js"
        fi

        mkdir -p "$(dirname "$new_file_path")"
        echo "Moving $file to $new_file_path"
        mv "$file" "$new_file_path"
    done

    rm -rf "$dist_folder"
    echo -e "\nFrontend build completed successfully!\n"
}

# Setup Python virtual environment and install dependencies
setup_python_env() {
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 could not be found"
        exit 1
    fi

    if ! command -v pip3 &> /dev/null; then
        echo "pip for Python 3 could not be found"
        exit 1
    fi

    if [ -d ".venv" ]; then
        echo "Virtual environment already exists."
    else
        python3 -m venv .venv
    fi

    source .venv/bin/activate

    if ! pip install -r requirements.txt; then
        echo "Error during pip install."
        deactivate
        exit 1
    else
        echo "Python dependencies installed successfully."
    fi

    deactivate
}

# Generate a random Flask SECRET_KEY
generate_secret_key() {
    python3 -c "import os; print(os.urandom(24).hex())"
}

# Copy and rename .env.example to .env and set a random SECRET_KEY
copy_and_edit_env() {
    if [ ! -f ".env" ]; then
        cp .env.example .env
        SECRET_KEY=$(generate_secret_key)
        sed -i "s/^SECRET_KEY=.*/SECRET_KEY=\"$SECRET_KEY\"/" .env
        echo ".env file created from .env.example with a random SECRET_KEY."
    else
        echo ".env file already exists."
    fi
}

# Initialize database
initialize_database() {
    source .venv/bin/activate

    if ! flask db init; then
        echo "Database already initialized."
    fi

    if ! flask db migrate -m "Initial migration"; then
        echo "Error during database migration."
        deactivate
        exit 1
    fi

    if ! flask db upgrade; then
        echo "Error during database upgrade."
        deactivate
        exit 1
    fi

    echo "Database initialized successfully."

    deactivate
}

install_npm_dependencies
run_npm_build
copy_images
move_and_rename_files
setup_python_env
copy_and_edit_env
initialize_database

echo "\nInstallation completed successfully!\n"
