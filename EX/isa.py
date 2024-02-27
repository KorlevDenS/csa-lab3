# pylint :  disable=invalid-name
# pylint :  disable=consider-using-f-string
# pylint :  disable=missing-function-docstring
# pylint :  disable=missing-class-docstring


"""
isa
"""
import json
from enum import Enum


class IoDevice:

    counter: int

    def __init__(self):
        pass


class Opcode(str, Enum):
    """
    Opcode
    """
    LW = 'LW'  # A <- [B]
    SW = 'SW'  # [A] <- B

    JMP = 'JMP'  # unconditional transition
    # a,b,i
    BEQ = "BEQ"  # Branch if Equal (A == B)
    BNE = "BNE"  # Branch if Not Equal (A != B)
    BLT = "BLT"  # Branch if Less than (A < B)
    BGT = "BGT"  # Branch if Greater than (A > B)
    BNL = "BNL"  # Branch if Not Less than (A >= B)
    BNG = "BNG"  # Branch if less or equals then (A <= B)

    IN = "IN"  # Инструкции для обеспечения IO по порту (в качестве аргумента принимается только номер порта)
    OUT = "OUT"

    ADD = 'ADD'  # t,a,b
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    REM = "REM"

    HALT = 'HALT'

    def __str__(self):
        return str(self.value)


ops_gr = {
    "mem": {
        Opcode.LW,
        Opcode.SW,
    },
    "branch": {
        Opcode.JMP,
        Opcode.BEQ,
        Opcode.BNE,
        Opcode.BLT,
        Opcode.BNL,
        Opcode.BGT,
        Opcode.BNG,
    },
    "arith": {
        Opcode.ADD,
        Opcode.SUB,
        Opcode.MUL,
        Opcode.DIV,
        Opcode.REM,
    },
    "io": {
        Opcode.IN,
        Opcode.OUT,
    }
}

STDIN_PORT, STDOUT_PORT = 0, 1


def write_code(filename: str, memory: list):
    with open(filename, "w", encoding="utf-8") as file:
        # Почему не: `file.write(json.dumps(code, indent=4))`?
        # Чтобы одна инструкция была на одну строку.
        buf = []
        for instr in memory:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")


def read_code(filename: str):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())

    for instr in code:
        # Конвертация строки в Opcode
        if "opcode" in instr:
            instr["opcode"] = Opcode(instr["opcode"])

    return code
