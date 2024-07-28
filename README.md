# Coconut

## Overview
[Coconut](https://lytexmedia.com/coconut) is a selfhosted and simple Dashboard to manage your server. It's built with Flask and Vue.js.
**It's still in development and not ready for production.**

## Documentation
[lytexmedia.com/coconut](https://lytexmedia.com/coconut)

## Technologies
- **Backend**: Flask
- **Frontend**: Vue.js, SCSS
- **Database**: SQLite

## Requirements
- Unix-based OS
    - Recommended: Linux (Arch, Debian, Ubuntu etc.)
- Python 3.8+
- Node.js & npm

## Getting Started

**Clone the repository**
```bash
git clone https://github.com/ximmanuel/Coconut.git
cd Coconut
```

**Run Coconut**
```bash
./coco run
```

## Development

**Build frontend**
```bash
./coco build
```

**Create custom modules**
```bash
./coco create module [name] [VueComponentName]
```
*Example:*
```bash
./coco create module 'My Module' MyModule
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
