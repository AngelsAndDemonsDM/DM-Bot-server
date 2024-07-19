from typing import Optional, Tuple

from main_impt import auth_manager
from systems.access_system import AuthError
from systems.access_system.access_flags import AccessFlags

HEADER_FOR_TOKEN: str = 'user_token'

async def get_requester_info(header: dict) -> Tuple[str, str, AccessFlags]: #TODO: Декоратор чтобы не ловить постоянно ошибки на подобии 500 и AuthError
    """_summary_

    Args:
        header (dict): _description_

    Raises:
        AuthError: _description_

    Returns:
        Tuple[str, str, AccessFlags]: _description_
    """
    requester_token = header.get(HEADER_FOR_TOKEN, None)
    
    if not requester_token:
        raise AuthError("Token not provided")
    
    try:
        requester_login, requester_accsess = await auth_manager.get_user_login_and_access_by_token(requester_token)
    
    except ValueError:
        raise AuthError("Error while get info about requester")
        
    return (requester_token, requester_login, requester_accsess)

def check_required_fields(data: dict, *args: str) -> Optional[str]:
    """Проверяет, что все необходимые поля присутствуют в данных.

    Args:
        data (dict): Словарь данных, в котором проверяются поля.
        *args (str): Переменное количество строковых аргументов, представляющих имена необходимых полей.

    Returns:
        Optional[str]: None, если все необходимые поля присутствуют, иначе строка с перечислением отсутствующих полей.
    """
    missing_fields = [field for field in args if field not in data]
    return ", ".join(missing_fields) if missing_fields else None
