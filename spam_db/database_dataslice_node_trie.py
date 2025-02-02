class DatabaseDataSliceNode:
    def __init__(self) -> None:
        self.slice_tree = [None] * 10

    def init(self, data: str, offset: int) -> int:
        for i in range(10):
            if data[offset] in ("*", "+"):
                offset += 1
                continue

            node = DatabaseDataSliceNode()
            offset = node.init(data, offset + 1)
            self.slice_tree[i] = node

        return offset

    def get_slice_id(self, current_number: int, number: str) -> int:
        if not number:
            return 0

        current_digit = int(number[0])
        number = number[1:]
        current_number = current_number * 10 + current_digit

        if self.slice_tree[current_digit] is None:
            return current_number

        return (
            self.slice_tree[current_digit].get_slice_id(current_number, number)
            if len(number) > 0
            else 0
        )

    def get_all_keys(self, prefix: str = "") -> list:
        keys = []

        for digit in range(10):
            if self.slice_tree[digit] is not None:
                new_prefix = prefix + str(digit)
                keys.append(new_prefix)
                keys.extend(self.slice_tree[digit].get_all_keys(new_prefix))

        return keys


def load_database_data_slice_node(file_name: str) -> DatabaseDataSliceNode:
    with open(file_name) as file:
        nodes = file.readline().strip()

    db_root_node = DatabaseDataSliceNode()
    db_root_node.init(nodes, 0)
    return db_root_node


if __name__ == "__main__":
    node = load_database_data_slice_node("data_slice_list.dat")
    numbers = node.get_all_keys()
    print(numbers)
    print(len(numbers))
    print(node.get_slice_id(0, "796729"))
