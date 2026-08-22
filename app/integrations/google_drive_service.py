from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import io


class GoogleDriveService:

    def __init__(self, access_token: str):

        credentials = Credentials(
            token=access_token
        )

        self.service = build(
            "drive",
            "v3",
            credentials=credentials
        )


    def download_file(
        self,
        file_id: str
    ) -> bytes:

        request = self.service.files().get(
            fileId=file_id,
            alt="media"
        )

        file_buffer = io.BytesIO()

        downloader = MediaIoBaseDownload(
            file_buffer,
            request
        )

        done = False

        while not done:

            status, done = downloader.next_chunk()

        file_buffer.seek(0)

        return file_buffer.read()