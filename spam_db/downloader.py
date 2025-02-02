import os
import zipfile
from io import BytesIO

import requests


def download_and_extract_zip(url: str, extract_to: str) -> None:

    try:
        os.makedirs(extract_to, exist_ok=True)

        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)

        print(f"ZIP file successfully downloaded and extracted to {extract_to}")
    except Exception as e:
        print(f"Error: {e}")


# https://yacb.lom.name/srvapp/get-database/sia.zip
# https://gitlab.com/xynngh/YetAnotherCallBlocker_data/raw/zip_v1/archives/sia.zip
