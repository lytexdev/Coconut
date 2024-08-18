from flask import Blueprint, render_template

setup_bp = Blueprint("setup", __name__)

from .user import *
from .modules import *
from .backup import *
from .status import *


@setup_bp.route("/", methods=["GET"])
def setup_index():
    return render_template("index.html")