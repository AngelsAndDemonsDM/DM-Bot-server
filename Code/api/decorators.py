from functools import wraps

from quart import jsonify
from systems.network import AccessError, AuthError


def server_exception_handler(func):
    """Декоратор для обработки исключений в асинхронных маршрутах Quart. В случае возникновения исключения возвращает JSON-ответ с сообщением об ошибке.

    Args:
        func (function): Асинхронная функция маршрута, которую необходимо обернуть декоратором.

    Returns:
        function: Асинхронная функция-обертка, которая обрабатывает исключения.
    """
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        """
        Обертка для обработки исключений, возникающих в обернутой функции.

        Args:
            *args: Позиционные аргументы, передаваемые в обернутую функцию.
            **kwargs: Именованные аргументы, передаваемые в обернутую функцию.

        Returns:
            object: JSON-ответ обернутой функции или ответ с сообщением об ошибке.
        """
        try:
            return await func(*args, **kwargs)
        
        except AuthError:
            return jsonify({"message": "Unauthorized access"}), 401
        
        except AccessError:
            return jsonify({"message": "Forbidden access"}), 403

        except ValueError as err:
            return jsonify({"message": "Bad arguments", "details": str(err)}), 400
        
        except Exception as err:
            return jsonify({"message": "Server got exception", "details": str(err)}), 500
    
    return decorated_function
