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

# Copy and rename .env.example to .env
copy_and_edit_env() {
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo ".env file created from .env.example. Please edit the .env file as needed."
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
setup_python_env
copy_and_edit_env
initialize_database

echo "Installation completed successfully!"
