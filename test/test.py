ARROW = 0 << 1
MX_ARRAY = 1 << 1
HAS_LABEL = 1 << 2

def toggle_bit(value, bit_flag):
    value ^= bit_flag

node_attrib: int = 0

toggle_bit(node_attrib, ARROW | MX_ARRAY)
print(node_attrib)