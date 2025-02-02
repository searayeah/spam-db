import os
import re
import shutil
import sys

import pandas as pd
from community_database_loader import get_database_size, load_from_file
from downloader import download_and_extract_zip


def create_database(folder_path, output_csv):
    all_data = []

    for file_name in os.listdir(folder_path):
        if re.match(r"^data_slice_\d+\.dat$", file_name):
            file_path = os.path.join(folder_path, file_name)

            numbers, pos_counts, neg_counts, neu_counts, unknowns, categories = (
                load_from_file(file_path)
            )

            for i in range(len(numbers)):
                all_data.append(
                    [
                        numbers[i],
                        pos_counts[i],
                        neg_counts[i],
                        neu_counts[i],
                        unknowns[i],
                        categories[i],
                    ],
                )

    df = pd.DataFrame(
        all_data,
        columns=[
            "Number",
            "Positive Ratings",
            "Negative Ratings",
            "Neutral Ratings",
            "Unknown Data",
            "Category",
        ],
    )
    info_path = os.path.join(folder_path, "data_slice_info.dat")

    assert df.shape[0] == get_database_size(info_path)

    df.to_csv(output_csv, index=False)
    df[
        df["Number"].astype(str).str.startswith(("7", "8"))
        & (df["Number"].astype(str).str.len() == 11)
    ][["Number"]].to_csv(f"filtered_{output_csv}", index=False)
    df.sample(20).to_csv(f"example_{output_csv}", index=False)
    print(f"Data saved to {output_csv} and filtered_{output_csv}")

    shutil.rmtree(folder_path)

    print(f"The folder {folder_path} and its contents have been deleted.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_database.py <link> <folder_path> <output_csv>")
        sys.exit(1)

    link = sys.argv[1]
    folder_path = sys.argv[2]
    output_csv = sys.argv[3]
    download_and_extract_zip(link, folder_path)
    create_database(folder_path, output_csv)
