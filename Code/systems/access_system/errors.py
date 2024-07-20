class AuthError(Exception):
    """Общая ошибка выбрасываемая при ошибке получения авторизации
    """
    pass

class AccessError(Exception):
    """Общая ошибка выбрасываемая при ошибке получения доступа
    """
    pass
