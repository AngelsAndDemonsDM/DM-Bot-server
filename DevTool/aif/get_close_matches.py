from difflib import get_close_matches

valid_commands = ['install', 'uninstall', 'search', 'list', 'freeze', 'show']

def suggest_command(command): # Получаем наиболее близкие совпадения среди допустимых команд
    suggestions = get_close_matches(command, valid_commands)
    if suggestions:
        return f"Unknown command '{command}' - maybe you meant '{suggestions[0]}'"
    else:
        return f"Unknown command '{command}'"

