import os
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
    pattern = r"def\s+([^\s\(]+)\s*\([^:]*\):\s*(['\"]{3})(.*?)\2|class\s+([^\s\(]+)\s*:\s*(['\"]{3})(.*?)\5"
    matches = re.findall(pattern, file_content, re.MULTILINE | re.DOTALL)

    for match in matches:
        function_name, _, docstring, class_name, _, class_docstring = match
        if function_name and docstring:
            docstrings[function_name] = docstring.strip()
        if class_name and class_docstring:
            docstrings[class_name] = class_docstring.strip()

    return docstrings

def generate_documentation(logger):
    """
    Генерирует документацию по файлам в указанной папке.

    Args:
        input_folder (str): Папка с исходными файлами.
        output_folder (str): Папка для сохранения документации.
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
                            doc_file.write("# Документация по файлу {}\n\n".format(module_name))
                            for name, docstring in docstrings.items():
                                doc_file.write(f"## {name}\n\n")
                                doc_file.write(f"{docstring}\n\n")
