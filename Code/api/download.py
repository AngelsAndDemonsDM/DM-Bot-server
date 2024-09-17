import zipfile
from pathlib import Path

from DMBotNetwork import ClUnit
from root_path import ROOT_PATH


class DownloadServerModule:
    @staticmethod
    async def net_download_server_conent(cl_unit: ClUnit):
        zip_path = DownloadServerModule._create_zip_archive()
        await cl_unit.send_file(zip_path, "server_contet.zip")

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
