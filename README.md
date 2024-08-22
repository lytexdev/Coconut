# Coconut

## Overview
Coconut is a self-hosted and simple Dashboard to manage your server. It's built with Flask and Vue.js.
**It's still in development and not ready for production.**

## Technologies
- **Backend**: Flask
- **Frontend**: Vue.js, SCSS
- **Database**: SQLite

## Requirements
- Unix-based OS
- Python 3.8+
- Node.js & npm

## Installation

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

**Create custom module**
```bash
./coco create module [name] [VueComponentName]
```
*Example:*
```bash
./coco create module 'System Info' SystemInfo
```

**Initialize the database**
```bash
./coco create db
```

## Feature Ideas
Some interesting features that could be added to - see [TODO](TODO.md) file for details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
