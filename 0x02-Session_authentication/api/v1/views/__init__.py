from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import routes after defining the Blueprint to avoid circular imports
from api.v1.views.users import *
from api.v1.views.index import *