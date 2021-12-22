from collections import defaultdict
from functools import cache, reduce
from math import inf
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import prettyprinter as pp

with open("input.txt", "r") as f:
    content = f.read().strip()

# content = "C200B40A82"

bits = ""
for c in content:
    binary_repr = bin(eval(f"0x{c}"))[2:]
    bits += "0" * (4 - len(binary_repr))
    bits += binary_repr


def binary_parse(bitstring):
    return eval(f"0b{bitstring}")


@dataclass
class Packet:
    version: int
    type_id: int
    num_bits_encoded: int
    value: Optional[int] = None
    children: Optional[list] = None


def parse_packet(packet):
    version = binary_parse(packet[:3])
    type_id = binary_parse(packet[3:6])
    if type_id == 4:
        encoded_literal = packet[6:]
        literal_bits = ""
        i = 0
        while True:
            literal_bits += encoded_literal[i + 1 : i + 5]
            if encoded_literal[i] == "0":
                break
            i += 5
        return Packet(
            version=version,
            type_id=type_id,
            num_bits_encoded=i + 11,
            value=binary_parse(literal_bits),
        )
    else:
        length_type_id = int(packet[6])
        children = []
        if length_type_id:
            num_subpacket_bits = packet[7:18]
            assert len(num_subpacket_bits) == 11
            num_subpackets = binary_parse(num_subpacket_bits)
            num_bits_encoded = 18
            while len(children) < num_subpackets:
                children.append(parse_packet(packet[num_bits_encoded:]))
                num_bits_encoded += children[-1].num_bits_encoded
        else:
            subpackets_size_bits = packet[7:22]
            assert len(subpackets_size_bits) == 15
            subpackets_size = binary_parse(subpackets_size_bits)
            prefix_bits = 22
            num_bits_encoded = prefix_bits
            while num_bits_encoded - prefix_bits < subpackets_size:
                children.append(parse_packet(packet[num_bits_encoded:]))
                num_bits_encoded += children[-1].num_bits_encoded
        return Packet(
            version=version,
            type_id=type_id,
            num_bits_encoded=num_bits_encoded,
            children=children
        )

def evaluate(packet):
    if packet.type_id == 4:
        return packet.value

    subpacket_values = list(map(evaluate, packet.children))
    match packet.type_id:
        case 0:
            return sum(subpacket_values)
        case 1:
            return reduce(lambda a, b: a * b, subpacket_values, 1)
        case 2:
            return min(subpacket_values)
        case 3:
            return max(subpacket_values)
        case 5:
            return int(subpacket_values[0] > subpacket_values[1])
        case 6:
            return int(subpacket_values[0] < subpacket_values[1])
        case 7:
            return int(subpacket_values[0] == subpacket_values[1])

    for child in (packet.children or []):
        res += version_sum(child)
    return res

packet_parsed = parse_packet(bits)
# pp.install_extras()
# pp.pprint(packet_parsed, width=1)
print( evaluate( packet_parsed ) )
