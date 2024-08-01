from api.admin import (admin_bp, api_change_access, api_change_password,
                       api_delete_user)
from api.auth import api_login, api_logout, api_register, auth_bp
from api.server import api_check_status, api_download_server_content, server_bp

__all__ = ['admin_bp', 'auth_bp', 'server_bp', 'api_change_access', 'api_change_password', 'api_delete_user', 'api_login', 'api_logout', 'api_register', 'api_check_status', 'api_download_server_content']