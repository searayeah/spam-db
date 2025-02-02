import struct
from io import BufferedReader
from time import time


def load_from_file(
    file_path: str,
) -> tuple[list[int], list[int], list[int], list[int], list[int], list[int]]:
    print(f"load_from_file() started {file_path}")

    current_time_millis = current_millis()

    db_version = 0

    with open(file_path, "rb") as f:
        print("load_from_file() reading header")
        header_string = read_utf8_string_chars(f, 4)
        load_from_stream_check_header(header_string)

        print("load_from_file() reading post header data")
        load_from_stream_read_post_header_data(f)

        print("load_from_file() reading DB version")
        db_version = read_int(f)
        print(f"load_from_file() DB version is {db_version}")

        print("load_from_file() reading post version data")
        load_from_stream_read_post_version_data(f)

        print("load_from_file() reading number of items")
        number_of_items = read_int(f)
        print(f"load_from_file() number of items is {number_of_items}")

        positive_ratings_counts = [0] * number_of_items
        negative_ratings_counts = [0] * number_of_items
        neutral_ratings_counts = [0] * number_of_items
        unknown_data = [0] * number_of_items
        categories = [0] * number_of_items
        numbers = [0] * number_of_items
        load_from_stream_init_fields()

        print("load_from_file() reading fields")
        for i in range(number_of_items):
            numbers[i] = read_long(f)
            (
                positive_ratings_counts[i],
                negative_ratings_counts[i],
                neutral_ratings_counts[i],
                unknown_data[i],
                categories[i],
            ) = load_from_stream_load_fields(f)
        print("load_from_file() finished reading fields")

        print("load_from_file() reading CP")
        divider_string = read_utf8_string_chars(f, 2)
        if divider_string.upper() != "CP":
            raise OSError(f"CP not found. Found instead: {divider_string}")

        print("load_from_file() reading extras")
        load_from_stream_load_extras(f)

        print("load_from_file() reading endmark")
        endmark_string = read_utf8_string_chars(f, 6)
        if endmark_string.upper() not in ["YABEND", "MTZEND"]:
            raise OSError(f"Endmark not found. Found instead: {endmark_string}")

    print(
        f"load_from_file() loaded slice with {number_of_items} "
        f"items in {current_millis() - current_time_millis} ms",
    )

    return (
        numbers,
        positive_ratings_counts,
        negative_ratings_counts,
        neutral_ratings_counts,
        unknown_data,
        categories,
    )


def current_millis() -> int:
    return int(time() * 1000)


def read_byte(f: BufferedReader) -> int:
    byte = f.read(1)
    if len(byte) < 1:
        raise EOFError
    return byte[0]


def read_int(f: BufferedReader) -> int:
    buffer = f.read(4)
    if len(buffer) < 4:
        raise EOFError
    return struct.unpack("<i", buffer)[0]


def read_long(f: BufferedReader) -> int:
    buffer = f.read(8)
    if len(buffer) == 8:
        return struct.unpack("<q", buffer)[0]
    raise EOFError("Unexpected end of file")


def read_utf8_string_chars(f: BufferedReader, length: int) -> str:
    data = f.read(length)
    if len(data) < length:
        raise EOFError
    return data.decode("utf-8")


def load_from_stream_check_header(header: str) -> None:
    if header.upper() not in ["YABF", "MTZF", "MTZD"]:
        raise OSError(f"Invalid header. Actual value: {header}")


def load_from_stream_read_post_header_data(f: BufferedReader) -> None:
    b = read_byte(f)  # ignored
    print(f"load_from_stream_read_post_header_data() b={b}")


def load_from_stream_read_post_version_data(f: BufferedReader) -> None:
    s = read_utf8_string_chars(f, 2)  # ignored
    i = read_int(f)  # ignored
    print(f"load_from_stream_read_post_version_data() s={s}, i={i}")


def load_from_stream_init_fields() -> None:
    pass  # Fields are initialized globally


def load_from_stream_load_fields(f: BufferedReader) -> tuple[int, int, int, int, int]:
    return (read_byte(f) for _ in range(5))


def load_from_stream_load_extras(f: BufferedReader) -> None:
    number_of_items_to_delete = read_int(f)
    print(
        f"load_from_stream_load_extras() number_of_items_to_delete={number_of_items_to_delete}",
    )

    global numbers_to_delete
    numbers_to_delete = [read_long(f) for _ in range(number_of_items_to_delete)]


def get_database_size(data_slice_info_file: str) -> int:
    with open(data_slice_info_file) as file:
        lines = file.readlines()
        return int(lines[2].strip())


if __name__ == "__main__":
    (
        numbers,
        positive_ratings_counts,
        negative_ratings_counts,
        neutral_ratings_counts,
        unknown_data,
        categories,
    ) = load_from_file("data_slice_796729.dat")
    print(numbers)
    print(positive_ratings_counts)
    print(categories)

    print(unknown_data)

    get_database_size("data_slice_info.dat")
