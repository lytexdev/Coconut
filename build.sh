#!/bin/bash

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

run_npm_build
copy_images
move_and_rename_files
