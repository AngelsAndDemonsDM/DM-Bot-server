from typing import Optional, Tuple

from main_impt import auth_manager
from quart import jsonify
from systems.access_system import AuthError
from systems.access_system.access_flags import AccessFlags

HEADER_FOR_TOKEN: str = 'user_token'

class MissingFieldsError(Exception):
    """Ошибка вызываемая при недостающих полях.
    """
    pass

def catch_MissingFilds_Auth_Exception(func):
    """Функция ловит AuthError и другие Exception которые долетели до функции. Возвращает 403 и 500 клиенту соответственно.
    
    Args:
        func (Callable): Функция, которую нужно обернуть.

    Returns:
        Callable: Обернутая функция.
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except MissingFieldsError as err:
            return jsonify({'message': f'Field(s) {err} are required'}), 400
        
        except AuthError:
            return jsonify({"message": "Access denied"}), 403
        
        except Exception as err:
            return jsonify({"message": "An unexpected error occurred", "error": str(err)}), 500
    
    return wrapper

async def get_requester_info(header: dict) -> Tuple[str, str, AccessFlags]:
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

def check_required_fields(data: dict, *args: str) -> Optional[str]: #TODO: Возвращать просто список аргсов которое запросили. Если аргов каких то нет - кинуть MissingFieldsError. Упрощаем код. Мяф.
    """Проверяет, что все необходимые поля присутствуют в данных.

    Args:
        data (dict): Словарь данных, в котором проверяются поля.
        *args (str): Переменное количество строковых аргументов, представляющих имена необходимых полей.

    Returns:
        Optional[str]: None, если все необходимые поля присутствуют, иначе строка с перечислением отсутствующих полей.
    """
    missing_fields = [field for field in args if field not in data]
    return ", ".join(missing_fields) if missing_fields else None
