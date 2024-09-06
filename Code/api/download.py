import zipfile
from pathlib import Path

from DMBotNetwork import ClientUnit, Server
from root_path import ROOT_PATH


class DownloadServerModule(Server):
    async def download_server_conent(self, cl_unit: ClientUnit):
        zip_path = self._create_zip_archive()
        await cl_unit.send_file(zip_path, "server_contet.zip")

    def _get_latest_modification_time(self, directory_path: Path) -> float:
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

    def _create_zip_archive(self) -> Path:
        """Создает ZIP-архив из папки 'Content' и возвращает путь к архиву.
        Проверяет время последней модификации файлов перед пересозданием.

        Returns:
            Path: Путь к созданному ZIP-архиву.
        """
        folder_path = Path(ROOT_PATH) / "Content"
        archive_path = Path(ROOT_PATH) / "data" / "content.zip"

        if archive_path.exists():
            if archive_path.stat().st_mtime >= self._get_latest_modification_time(
                folder_path
            ):
                return archive_path

            else:
                archive_path.unlink()

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob("*"):
                if file_path.is_file():
                    zipf.write(file_path, file_path.relative_to(folder_path))

        return archive_path
