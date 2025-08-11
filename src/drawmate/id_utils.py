import random

# Character list for ID generation - contains all letters (uppercase and lowercase) and numbers
ALL_CHARACTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


def generate_id(key_size: int = 20):
    key = []
    for i in range(key_size):
        rand_idx = random.randrange(0, len(ALL_CHARACTERS))
        key.append(ALL_CHARACTERS[rand_idx])
    return "".join(key)


def map_node_keys(node_key: str):
    pass

def get_adjacent_port_key(port_key_str: str) -> str:
    node_orientation = get_key_orientation(port_key_str)
    node_col = get_key_column(port_key_str)
    node_row = get_key_row(port_key_str)
    port_orientation = get_port_key_orientation(port_key_str)
    port_row = get_port_key_row(port_key_str)

    adj_orientation = ""
    adj_col = ""
    adj_node_row = ""
    adj_port_orientation = "L"
    adj_port_row = ""

    if node_orientation == "L" and node_col == 0:
        adj_orientation = "C"
        adj_col = "0"
        adj_node_row = "0"
    elif node_orientation == "L" and node_col > 0:
        adj_orientation = "L"
        adj_col = f"{node_col - 1}"
        adj_node_row = str(node_row)
    elif node_orientation == "R":
        adj_orientation = "R"
        adj_col = f"{node_col + 1}"
        adj_node_row = str(node_row)
    elif node_orientation == "C":
        adj_orientation = "R"
        adj_col = "0"
        adj_node_row = str(node_row)

    adj_port_row = str(port_row)

    return f"{adj_orientation}-{adj_col}-{adj_node_row}-{adj_port_orientation}-{adj_port_row}"

def get_key_toks(node_key: str):
    return node_key.split("-")

def get_key_column(node_key: str) -> int:
    return int(get_key_toks(node_key)[1])

def get_key_row(node_key: str) -> int:
    return int(get_key_toks(node_key)[2])

def get_key_orientation(node_key: str) -> str:
    return get_key_toks(node_key)[0]

def get_port_key_orientation(node_key) -> str:
    return get_key_toks(node_key)[3]

def get_port_key_row(node_key) -> str:
    return get_key_toks(node_key)[4]
