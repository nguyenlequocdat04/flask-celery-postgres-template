from src.schemas.api import ApiMeta

from .index import bp as index_bp

from .auth import api as AuthApi


v1_bp = ApiMeta.blueprint
api = ApiMeta.api

# routing api for app
api.add_namespace(AuthApi, path='/auth')

DEFAULT_BLUEPRINTS = [
    v1_bp,
    index_bp,
]
