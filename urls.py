from views.auth import auth_bp
from views.setup import setup_bp
from api.system_info import system_info_bp
from api.backup import backup_bp
import logging
import importlib
import os

# List of blueprints to be registered with their prefixes
blueprints = [
    (auth_bp, ""),
    (setup_bp, "/setup"),
    (system_info_bp, "/api"),
    (backup_bp, "/api"),
]

# List of routes/endpoints that require login
require_login_endpoints = [
    "auth.login",
    "setup.create_user",
    "setup.set_modules",
    "setup.get_setup_status",
    "setup.finish_setup",
    "setup.setup_index",
    "setup.get_available_modules",
    "setup.create_backup",
    "setup.get_backups",
    "setup.delete_backup",
    "csrf_token",
]

# List of routes/endpoints allowed during setup without login
allowed_endpoints = [
    "setup.create_user",
    "setup.set_modules",
    "setup.get_setup_status",
    "setup.finish_setup",
    "setup.setup_index",
    "setup.get_available_modules",
    "setup.create_backup",
    "setup.get_backups",
    "setup.delete_backup",
    "csrf_token",
]

def register_blueprints(app):
    """Register all blueprints listed in the blueprints variable."""
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)

    register_custom_modules(app)

def register_custom_modules(app):
    """Register custom modules dynamically from the custom_modules directory."""
    custom_modules_dir = os.path.join(os.path.dirname(__file__), 'custom_modules')

    if not os.path.exists(custom_modules_dir):
        logging.info(f"No custom modules directory found at {custom_modules_dir}")
        return

    for module_name in os.listdir(custom_modules_dir):
        module_path = os.path.join(custom_modules_dir, module_name)
        if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, '__init__.py')):
            try:
                module = importlib.import_module(f'custom_modules.{module_name}')
                expected_bp_name = f'{module_name}_bp'
                
                if hasattr(module, expected_bp_name):
                    blueprint = getattr(module, expected_bp_name)
                    app.register_blueprint(blueprint, url_prefix="/api")
                    logging.info(f"Registered custom module: {module_name}")
                else:
                    logging.warning(f"No blueprint found in custom module {module_name}")

            except ImportError as e:
                logging.error(f"Failed to import custom module {module_name}: {e}")
