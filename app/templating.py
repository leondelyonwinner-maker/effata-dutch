"""Single shared Jinja2Templates instance so custom filters/globals are
registered exactly once and every router renders through the same
environment."""
import json

from fastapi.templating import Jinja2Templates

from app.config import get_settings

templates = Jinja2Templates(directory="app/templates")
templates.env.filters["fromjson"] = json.loads
templates.env.globals["session_cookie_name"] = get_settings().session_cookie_name
