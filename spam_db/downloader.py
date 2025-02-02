import os
import zipfile
from io import BytesIO

import requests


def download_and_extract_zip(url: str, extract_to: str) -> None:

    try:
        os.makedirs(extract_to, exist_ok=True)

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)

        print(f"ZIP file successfully downloaded and extracted to {extract_to}")
    except Exception as e:
        print(f"Error: {e}")
