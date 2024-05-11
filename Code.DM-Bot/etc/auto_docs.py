import ast
import logging
import os
import re
import shutil


class AutoDocs:
    def __init__(self, input_folder: str = None, output_folder: str = None) -> None:
        if input_folder is None:
            self._input_folder = os.path.join(os.getcwd(), 'Code.DM-Bot')
        else:
            self._input_folder = os.path.join(os.getcwd(), input_folder)
        
        if output_folder is None:
            self._output_folder = os.path.join(os.getcwd(), 'Docs.DM-Bot')
        else:
            self._output_folder = os.path.join(os.getcwd(), output_folder)
        
    def extract_docstrings(self, file_content):
        """
        Извлекает документационные строки из содержимого файла.

        Args:
            file_content (str): Содержимое файла.

        Returns:
            dict: Словарь, где ключи - имена методов/атрибутов, значения - их документация.
        """
        docstrings = {}
        tree = ast.parse(file_content)
        current_class = None

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                current_class = node.name
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith('_') or node.name.endswith('__'):
                    if current_class is not None:
                        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                            docstrings.setdefault(f"{current_class}.{node.name}", []).append(node.body[0].value.s)
                    else:
                        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                            docstrings.setdefault(node.name, []).append(node.body[0].value.s)

        return docstrings

    def format_docstring(self, name, docstring) -> str:
        """
        Форматирует документацию для отображения в файле Markdown.

        Args:
            name (str): Имя метода/атрибута.
            docstring (str или list): Документация, представленная в виде строки или списка строк.

        Returns:
            str: Отформатированная документация.
        """
        if isinstance(docstring, list):
            docstring = "\n".join(docstring)

        formatted_docstring = "\n".join(line.lstrip() for line in docstring.splitlines())

        if formatted_docstring:
            formatted_docstring = f"## `{name}`\n{formatted_docstring}\n\n"
        else:
            formatted_docstring = f"## `{name}`\n*Документация отсутствует*\n\n"

        formatted_docstring = re.sub(r'(Args|Attributes|Examples|Parameters|Raises|Returns):\n', r'**\1:**\n', formatted_docstring)
        formatted_docstring = re.sub(r'\n', r'<br>\n', formatted_docstring)
        formatted_docstring = re.sub(r'<br>\n<br>\n', r'<br>\n', formatted_docstring)
        
        formatted_docstring = re.sub(r'```py.*?```<br>', lambda match: match.group().replace('<br>', ''), formatted_docstring, flags=re.DOTALL)
        formatted_docstring = re.sub(r'```py', r'\n```py', formatted_docstring)
        formatted_docstring = re.sub(r'```(?!py)', r'```\n', formatted_docstring)

        formatted_docstring = re.sub(r'##(?=[^\n])', r'\n##', formatted_docstring)
        formatted_docstring = re.sub(r'\n\n', r'\n', formatted_docstring)

        return formatted_docstring

    def generate_documentation(self):
        """
        Генерирует документацию по файлам в указанной папке.
        """

        if os.path.exists(self._output_folder):
            shutil.rmtree(self._output_folder)
            logging.debug(f"Удаление содержимого папки {self._output_folder}")

        for root, dirs, files in os.walk(self._input_folder):
            for file in files:
                if file.endswith(".py"):
                    module_name = file[:-3]
                    module_path = os.path.join(root, file)
                    relative_folder = os.path.relpath(root, self._input_folder)
                    doc_folder = os.path.join(self._output_folder, relative_folder)
                    os.makedirs(doc_folder, exist_ok=True)
                    logging.debug(f"Обработка файла: {module_name}")
                    with open(module_path, "r", encoding="utf-8") as f:
                        module_content = f.read()
                        docstrings = self.extract_docstrings(module_content)
                        if docstrings:
                            with open(os.path.join(doc_folder, f"{module_name}.md"), "w", encoding="utf-8") as doc_file:
                                doc_file.write(f"# Документация по файлу `{file}`\n\n")
                                for name, docstring in docstrings.items():
                                    formatted_docstring = self.format_docstring(name, docstring)
                                    doc_file.write(formatted_docstring)
        logging.info("Создание документации завершено")

if __name__ == "__main__":
    main_code = AutoDocs("Code.DM-Bot", "Docs.DM-Bot")
    main_code.generate_documentation()
