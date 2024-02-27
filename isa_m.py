"""
Представление исходного и машинного кода
"""
import json
from enum import Enum
from typing import List
from collections import namedtuple


class Opcode(str, Enum):

    LW = 'LW'  # lw rd, rs: load from [rs] to rd
    SW = 'SW'  # sw rd, rs: load from to [rd]

    # arithmetics
    # rd, rs1, rs2
    ADD = 'ADD'
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    REM = "REM"  # remainder of the division

    JMP = 'JMP'  # Jump without condition
    # A, B, imm
    BEQ = "BEQ"  # Branch imm if A == B
    BNE = "BNE"  # Branch imm if A != B
    BNL = "BNL"  # Branch imm if A >= B
    BNG = "BNG"  # Branch imm if A <= B
    BLT = "BLT"  # Branch imm if A < B
    BGT = "BGT"  # Branch imm if A > B

    IN = "IN"    # Read to A
    OUT = "OUT"  # Write to A

    # exit
    HALT = "HALT"

    def __str__(self):
        """Переопределение стандартного поведения `__str__` для `Enum`: вместо
        `Opcode.INC` вернуть `increment`.
        """
        return str(self.value)


class AddrType(int, Enum):

    VAL = 0
    ADDR = 1

    def __str__(self):
        return int(self.value)


class Term(namedtuple("Term", "line pos symbol")):
    """Описание выражения из исходного текста программы.

        Сделано через класс, чтобы был docstring.
        """


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
    }
}


def write_code(filename, code):
    """Записать машинный код в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        # Почему не: `file.write(json.dumps(code, indent=4))`?
        # Чтобы одна инструкция была на одну строку.
        buf = []
        for instr in code:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")

def read_code(filename):
    """Прочесть машинный код из файла.

    Так как в файле хранятся не только простейшие типы (`Opcode`, `Term`), мы
    также выполняем конвертацию в объекты классов вручную (возможно, следует
    переписать через `JSONDecoder`, но это скорее усложнит код).

    """
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())

    for instr in code:
        # Конвертация строки в Opcode
        instr["opcode"] = Opcode(instr["opcode"])

        # Конвертация списка term в класс Term
        if "term" in instr:
            assert len(instr["term"]) == 3
            instr["term"] = Term(instr["term"][0], instr["term"][1], instr["term"][2])

    return code

