import hashlib
import zipfile
from pathlib import Path

from DMBotNetwork import ClUnit
from root_path import ROOT_PATH


class DownloadServerModule:
    @staticmethod
    async def net_get_server_content_hash(cl_unit: ClUnit):
        try:
            zip_path = DownloadServerModule._create_zip_archive()
            return DownloadServerModule._calculate_file_hash(zip_path)
        
        except Exception as err:
            return str(err)

    @staticmethod
    async def net_download_server_content(cl_unit: ClUnit):
        try:
            zip_path = DownloadServerModule._create_zip_archive()
            await cl_unit.send_file(zip_path, "server_content.zip")
            return "done"

        except Exception as err:
            return str(err)

    @staticmethod
    def _get_latest_modification_time(directory_path: Path) -> float:
        """Получает время последней модификации файлов в директории.

        Args:
            directory_path (Path): Путь к директории.

        Returns:
            float: Время последней модификации в формате timestamp.
        """
        latest_time = 0
        for file_path in directory_path.rglob("*"):
            if file_path.is_file():
                file_time = file_path.stat().st_mtime
                if file_time > latest_time:
                    latest_time = file_time

        return latest_time

    @staticmethod
    def _create_zip_archive() -> Path:
        """Создает ZIP-архив из папки 'Content' и возвращает путь к архиву.
        Проверяет время последней модификации файлов перед пересозданием.

        Returns:
            Path: Путь к созданному ZIP-архиву.
        """
        folder_path = Path(ROOT_PATH) / "Content"
        archive_path = Path(ROOT_PATH) / "data" / "content.zip"

        if archive_path.exists():
            if (
                archive_path.stat().st_mtime
                >= DownloadServerModule._get_latest_modification_time(folder_path)
            ):
                return archive_path

            else:
                archive_path.unlink()

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob("*"):
                if file_path.is_file():
                    zipf.write(file_path, file_path.relative_to(folder_path))

        return archive_path

    @staticmethod
    def _calculate_file_hash(file_path: Path, hash_algo="sha256") -> str:
        """Вычисляет хеш для переданного файла.

        Args:
            file_path (Path): Путь к файлу.
            hash_algo (str): Алгоритм хеширования (по умолчанию 'sha256').

        Returns:
            str: Хеш файла в виде шестнадцатеричной строки.
        """
        hash_function = hashlib.new(hash_algo)
        with file_path.open("rb") as f:
            while chunk := f.read(8192):
                hash_function.update(chunk)

        return hash_function.hexdigest()
