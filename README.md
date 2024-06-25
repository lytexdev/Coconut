# Coconut

## Overview
A simple Dashboard to manage your server. It is built with Flask and Vue.js.

## Preview
![Preview](./preview.png)

## Features
- User Authentication
- Develope own modules
- Read System Information
- Manage Docker Containers
- Create Backup
- Shutdown
- Reboot

## Technologies
- **Backend**: Flask
- **Frontend**: Vue.js, SCSS


## Getting Started

**Clone the repository**
```bash
git clone https://github.com/ximmanuel/Coconut.git
cd Coconut
```

**Create a virtual environment**
```bash
python -m venv .venv
```

**Activate the virtual environment**

Linux
```bash
source .venv/bin/activate
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Copy .env.example to .env and edit it**
```bash
cp .env.example .env
```

**Initialize the database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Run the server**
```bash
python app.py
```

## Development

**Install frontend dependencies**
```bash
cd coconut-shell/
npm install
```

**Build frontend**
```bash
python build.py
```


## Feature Ideas
Some interesting features that could be added to - see [TODO](TODO.md) file for details.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
