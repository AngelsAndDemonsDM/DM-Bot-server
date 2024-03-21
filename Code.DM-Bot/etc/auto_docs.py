import os
import re

import re

def extract_docstrings(file_content):
    """
    Извлекает документационные строки из содержимого файла.

    Args:
        file_content (str): Содержимое файла.

    Returns:
        dict: Словарь, где ключи - имена методов/атрибутов, значения - их документация.
    """
    docstrings = {}
    pattern = r"(?:async\s+def\s+([^\s\(]+)\s*\([^:]*\):\s*(['\"]{3})(.*?)\2)|(?:def\s+([^\s\(]+)\s*\([^:]*\):\s*(['\"]{3})(.*?)\5)|(?:class\s+([^\s\(]+)\s*:\s*(['\"]{3})(.*?)\7)"
    matches = re.findall(pattern, file_content, re.MULTILINE | re.DOTALL)

    for match in matches:
        async_func_name, async_quote, async_docstring, def_func_name, def_quote, def_docstring, class_name, class_quote, class_docstring = match
        if async_func_name:
            docstrings[async_func_name] = async_docstring.strip()
        elif def_func_name:
            docstrings[def_func_name] = def_docstring.strip()
        elif class_name:
            docstrings[class_name] = class_docstring.strip()

    return docstrings

def format_docstring(name, docstring):
    """
    Форматирует документацию для отображения в файле Markdown.

    Args:
        name (str): Имя метода/атрибута.
        docstring (str): Документация.

    Returns:
        str: Отформатированная документация.
    """
    formatted_docstring = f"## {name}\n{docstring}\n\n"
    formatted_docstring = re.sub(r'(Args|Returns|Raises):\n', r'**\1:**\n\n', formatted_docstring)
    return formatted_docstring

def generate_documentation(logger):
    """
    Генерирует документацию по файлам в указанной папке.

    Args:
        logger: Логгер для записи информации о процессе генерации документации.
    """
    input_folder = os.path.join(os.getcwd(), 'Code.DM-Bot')
    output_folder = os.path.join(os.getcwd(), 'Docs.DM-Bot')

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join(root, file)
                logger.debug(f"Обработка файла: {module_name}")
                with open(module_path, "r", encoding="utf-8") as f:
                    module_content = f.read()
                    docstrings = extract_docstrings(module_content)
                    if docstrings:
                        with open(os.path.join(output_folder, f"{module_name}.md"), "w", encoding="utf-8") as doc_file:
                            doc_file.write(f"# Документация по файлу {module_name}\n\n")
                            for name, docstring in docstrings.items():
                                formatted_docstring = format_docstring(name, docstring)
                                doc_file.write(formatted_docstring)
    logger.info("Создание документации завершено")
