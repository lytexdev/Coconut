# Coconut

## Overview
[Coconut](https://lytexmedia.com/coconut) is a selfhosted and simple Dashboard to manage your server. It's built with Flask and Vue.js.
**It's still in development and not ready for production.**

## Documentation
[lytexmedia.com/coconut](https://lytexmedia.com/coconut)

## Preview
![Preview](./preview.png)

## Technologies
- **Backend**: Flask
- **Frontend**: Vue.js, SCSS

## Requirements
- Unix-based OS (Linux, macOS, etc. - Windows is not supported)
- Python 3.6+
- Node.js & npm

## Getting Started

**Clone the repository**
```bash
git clone https://github.com/ximmanuel/Coconut.git
cd Coconut
```

**Install Coconut**
```bash
chmod +x install.sh
./install.sh
```

**Activate venv**
```bash
source .venv/bin/activate
```

**Run the server**
```bash
python3 app.py
```

## Development

**Build frontend**
```bash
chmod +x build.sh
./build.sh
```

**Initialize the database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```


## Feature Ideas
Some interesting features that could be added to - see [TODO](TODO.md) file for details.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
