__all__ = ["Owo"]

import mimetypes
from pathlib import Path
from typing import Optional

import requests

from owo.errors import ShortenUrlError, UploadDataError

API_URL = "https://api.awau.moe"
SHORTEN_PATH = "/shorten/polr"
UPLOAD_PATH = "/upload/pomf"
DEFAULT_FILENAME = "owo.txt"


class Owo:
    def __init__(
        self, key: str, domain: Optional[str] = "owo.whats-th.is"
    ) -> None:
        self.headers = {"Authorization": key}
        self.domain = f"https://{domain}"

    def shorten_url(self, url: str) -> str:
        """Shortens a URL.

        :param url: URL to shorten.
        :raises ShortenUrlError: Something went wrong shortening the URL.
        :return: Shortened URL.
        """
        resp = requests.get(
            f"{API_URL}{SHORTEN_PATH}",
            params={"action": "shorten", "url": url, "resultUrl": self.domain},
            headers=self.headers,
        )
        if resp.status_code != 200:
            raise ShortenUrlError
        return resp.text

    def upload_data(self, data: bytes, filename: str) -> str:
        """Uploads byte data. The method will try to guess the mimetype
        for the data uploaded. If you want to upload a file or text directly,
        use the wrapper methods `upload_file` and `upload_text`.

        :param data: Byte data to upload.
        :param filename: Name of the file to upload as.
        :raises UploadDataError: Something went wrong uploading the data.
        :return: URL to data uploaded.
        """
        content = [
            ["files[]", [filename, data, mimetypes.guess_type(filename)[0]]]
        ]
        resp = requests.post(
            f"{API_URL}{UPLOAD_PATH}",
            files=content,
            headers=self.headers,
        )
        if resp.status_code != 200:
            raise UploadDataError
        path = resp.json()["files"][0]["url"]
        return f"{self.domain}/{path}"

    def upload_file(self, file: Path) -> str:
        """Wrapper for `upload_data` to accept a Path to a file.

        :param file: File to upload.
        :return: URL to file uploaded.
        """
        filename = file.name
        data = file.read_bytes()
        return self.upload_data(data, filename)

    def upload_text(
        self, text: str, filename: Optional[str] = DEFAULT_FILENAME
    ) -> str:
        """Wrapper for `upload_data` to accept text.

        :param text: Text to upload.
        :param filename: Name of file to upload as.
        :return: URL to text uploaded.
        """
        data = text.encode()
        return self.upload_data(data, filename)
