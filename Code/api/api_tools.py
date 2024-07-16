from typing import Optional

HEADER_FOR_TOKEN: str = 'user_token'

def get_requester_token(header: dict) -> Optional[str]:
    """Получает токен пользователя из заголовков запроса.

    Args:
        header (dict): Словарь заголовков запроса.

    Returns:
        Optional[str]: Значение токена, если найдено, иначе None.
    """
    return header.get(HEADER_FOR_TOKEN, None)

def check_required_fields(data: dict, *args: str) -> Optional[str]:
    """
    Проверяет, что все необходимые поля присутствуют в данных.

    Args:
        data (dict): Словарь данных, в котором проверяются поля.
        *args (str): Переменное количество строковых аргументов, представляющих имена необходимых полей.

    Returns:
        Optional[str]: None, если все необходимые поля присутствуют, иначе строка с перечислением отсутствующих полей.
    """
    missing_fields = [field for field in args if field not in data]
    return ", ".join(missing_fields) if missing_fields else None
