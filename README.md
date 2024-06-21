# Coconut

## Overview
Lightweight and self-hosted Server management tool. It is designed to be simple and easy to use. It is built with Flask and Vue.js.

## Preview
![Preview](./preview.png)

## Features
- User Authentication
- Read System Information
- Manage Docker Containers
- Create Backup
- Shutdown
- Reboot

## Technologies
- **Backend**: Flask
- **Frontend**: Vue.js, SCSS

## Requirements
- Python 3.8+
- Node.js 20+

## Installation

### Docker
***Soon***


### Manual Installation
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

Fish
```bash
source .venv/bin/activate.fish
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


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
