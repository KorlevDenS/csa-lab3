import re
import sys

from typing import Tuple, List
from isa import write_code


def translate_stage_1(raw: str) -> str:
    raws = raw.split("\n")
    cleaned_raws = []

    for r in raws:
        r = r.partition(";")[0]
        cleaned_raws.append(r.strip())

    text = " ".join(cleaned_raws)
    text = re.sub(r" +", " ", text)  # remove extra whitespaces

    return text


def translate_stage_2(text) -> Tuple[list, list]:
    text = re.sub(r"'.*'", lambda match: f'{",".join(map(lambda char: str(ord(char)), match.group()[1:-1]))}', text)
    data_section_index = text.find("section data:")
    text_section_index = text.find("section text:")

    data_tokens = re.split("[, ]", text[data_section_index + len("section data:"): text_section_index])
    data_tokens = list(filter(lambda token: token, data_tokens))
    data_tokens = list(map(lambda token: (token[:-1],) if token[-1] == ':' else token, data_tokens))

    instruction_tokens = re.split("[, ]", text[text_section_index + len("section text:"):])
    instruction_tokens = list(filter(lambda token: token, instruction_tokens))
    instruction_tokens = list(map(lambda token: (token[:-1],) if token[-1] == ':' else token, instruction_tokens))

    return data_tokens, instruction_tokens


def translate_stage_3(data_tokens: List[str], instruction_tokens: List[str]):
    data = []
    data_labels = {}
    code = []
    code_labels = {}

    for data_token in data_tokens:
        if isinstance(data_token, tuple):
            data_labels[data_token[0]] = len(data)
        elif data_token.isdigit():
            data.append(data_token)

    i = 0
    while i < len(instruction_tokens):
        token = instruction_tokens[i]
        if isinstance(token, tuple):
            code_labels[token[0]] = len(code)
            i += 1
            continue

        pre_opcode = instruction_tokens[i].upper()
        if pre_opcode in ["HALT"]:
            code.append({"opcode": pre_opcode, "args": []})
            i += 1
            pass
        elif pre_opcode in ["JMP"]:
            code.append({"opcode": pre_opcode, "args": [instruction_tokens[i + 1]]})
            i += 2
            pass
        elif pre_opcode in ["IN", "OUT"]:
            code.append({"opcode": pre_opcode, "args": [instruction_tokens[i + 1], instruction_tokens[i + 2]]})
            i += 3
            pass
        elif pre_opcode in ["SW", "LW"]:
            addr_type = detect_addr_type(instruction_tokens[i + 2])
            code.append(
                {"opcode": pre_opcode, "addr_type": addr_type if addr_type != 0 else 1,
                 "args": [instruction_tokens[i + 1].strip("[]"), instruction_tokens[i + 2]]})
            i += 3
            pass
        elif pre_opcode in ["JMP", "BEQ", "BNE", "BLT", "BGT", "BNL", "BNG"]:
            code.append({"opcode": pre_opcode, "args": [instruction_tokens[i + 1], instruction_tokens[i + 2], instruction_tokens[i + 3]]})
            i += 4
            pass
        elif pre_opcode in ["ADD", "SUB", "MUL", "DIV", "REM"]:
            addr_type = detect_addr_type(instruction_tokens[i + 3])
            code.append(
                {"opcode": pre_opcode, "addr_type": addr_type,
                 "args": [instruction_tokens[i + 1], instruction_tokens[i + 2].strip("[]"), instruction_tokens[i + 3]]})
            i += 4
            pass
        else:
            raise SyntaxError(f"Unknown instruction: {pre_opcode}")

    return data, data_labels, code, code_labels


def detect_addr_type(arg: str) -> int:
    if re.fullmatch(r'r\d{1,2}', arg):
        return 0
    if re.fullmatch(r'\[r\d{1,2}\\]', arg):
        return 1
    return 2


def translate_stage_4(program: list, data: list) -> list:
    for i in range(len(program)):
        if "addr_type" in program[i]:
            program[i]["args"].append(program[i]["addr_type"])

        for arg in range(len(program[i]["args"])):
            if isinstance(program[i]["args"][arg], str):
                program[i]["args"][arg] = program[i]["args"][arg].replace("r", "")

    united_memory = program
    for i in range(len(data)):
        united_memory.append({"data": data[i]})
    return united_memory


def translate_to_struct(text) -> list:
    text = translate_stage_1(text)

    data_tokens, instruction_tokens = translate_stage_2(text)

    data, data_labels, code, code_labels = translate_stage_3(data_tokens, instruction_tokens)

    program = code
    for word_idx, word in enumerate(program):
        if isinstance(word, dict):
            for arg_idx, arg in enumerate(word["args"]):
                if arg in data_labels:
                    program[word_idx]["args"][arg_idx] = data_labels[arg] + len(code)
                elif arg in code_labels:
                    program[word_idx]["args"][arg_idx] = code_labels[arg]

    united_memory = translate_stage_4(program, data)
    return united_memory


# def translate_to_binary(data: list, program: List[dict]) -> Tuple[List[str], List[str], List[str]]:
#     hex_program = list()
#     hex_program_with_mnemonics = list()
#     for instr in program:
#         hex_instr = translate_instruction_to_hex_str(instr)
#         hex_program_with_mnemonics.append(f"{hex_instr} {instr}")
#         hex_program.append(hex_instr)
#
#     hex_data_bytes = list()
#     for i in data:
#         hex_data_bytes.append(to_bytes_str(int(i), 4))
#
#     return hex_data_bytes, hex_program, hex_program_with_mnemonics


# def translate_instruction_to_hex_str(instr: dict) -> str:
#     hex_instr = ""  # hex-предстваление 32битной инструкции (в виде строки)
#     _instr_type = ""  # для вывода ошибок
#     opcode = Opcode(instr["opcode"])
#
#     if opcode in ops_gr["arith"]:  # addr instruction
#         _instr_type = "arith"
#         hex_instr = "{0}{1}{2}{3}".format(
#             get_lower_nibble(addr_instruction_code[opcode]),
#             get_lower_nibble(int(instr["addr_type"])),
#             get_lower_nibble(register_to_number[instr["args"][0]]),
#             get_lower_nibble(register_to_number[instr["args"][1]]))
#         if int(instr["addr_type"]) == 2:
#             hex_instr += to_bytes_str(int(instr["args"][2]), 4)
#         else:
#             hex_instr += get_lower_nibble(register_to_number[instr["args"][2]])
#             hex_instr += "0" * 3
#
#     elif opcode in ops_gr["mem"]:  # addr instruction
#         _instr_type = "mem"
#         hex_instr = "{0}{1}{2}".format(
#             get_lower_nibble(addr_instruction_code[opcode]),
#             get_lower_nibble(int(instr["addr_type"])),
#             get_lower_nibble(register_to_number[instr["args"][0]]))
#         if int(instr["addr_type"]) == 2:
#             hex_instr += "0" \
#                          + to_bytes_str(instr["args"][1], 4)
#         else:
#             hex_instr += get_lower_nibble(register_to_number[instr["args"][1]]) \
#                          + "0" * 4
#
#     elif opcode is Opcode.HALT:
#         _instr_type = "halt"
#         hex_instr = "00000010"
#
#     elif opcode in ops_gr["branch"]:
#         _instr_type = "branch"
#         hex_instr = "{0}{1}".format(
#             get_lower_nibble(int("1111", 2)),
#             get_lower_nibble(branch_instruction_code[opcode]))
#         if opcode is Opcode.JMP:
#             hex_instr += "00{0}".format(to_bytes_str(int(instr["args"][0]), 4))
#         else:
#             hex_instr += "{0}{1}{2}".format(
#                 get_lower_nibble(register_to_number[instr["args"][0]]),
#                 get_lower_nibble(register_to_number[instr["args"][1]]),
#                 to_bytes_str(int(instr["args"][2]), 4))
#
#     elif opcode in ops_gr["io"]:
#         _instr_type = "io"
#         hex_instr = "{0}{1}{2}0{3}".format(
#             get_lower_nibble(int("0001", 2)),
#             get_lower_nibble(io_instruction_code[opcode]),
#             get_lower_nibble(register_to_number[instr["args"][0]]),
#             to_bytes_str(int(instr["args"][1]), 4))
#
#     assert len(hex_instr) == 8, f"Error in translate {_instr_type}-instruction to binary: {str(instr)},\n " \
#                                 f"result: {hex_instr}"
#
#     return hex_instr


# def get_lower_nibble(byte: int) -> str:
#     return to_bytes_str(byte, 1)


# def to_bytes_str(number: int, len_in_nibbles: int) -> str:
#     hex_num = hex(number).replace("0x", "")
#
#     if len(hex_num) >= len_in_nibbles:
#         return hex_num[len(hex_num) - len_in_nibbles:]
#
#     return (len_in_nibbles - len(hex_num)) * "0" + hex_num


def main(args):
    assert len(args) == 2, \
        "Wrong arguments: translator.py <input_file> <target_code_file>"

    source, target = args
    with open(source, "rt", encoding="utf-8") as f:
        source = f.read()

    united_memory = translate_to_struct(source)
    write_code(target, united_memory)


if __name__ == '__main__':
    main(sys.argv[1:])
