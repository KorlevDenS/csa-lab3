from types import FunctionType
from typing import Tuple, List

from isa_m import Opcode


class RegisterUnit:
    r0: int
    rd: int
    rs1: int
    rs2: int
    rin: FunctionType
    rout: FunctionType

    def __init__(self, input_mapping, output_mapping):
        self.r0 = 0
        self.rd = 0
        self.rs1 = 0
        self.rs2 = 0
        self.rin = input_mapping
        self.rout = output_mapping

    def latch_sel_rd(self, number: int):
        self.rd = number

    def latch_sel_rs1(self, number: int):
        self.rs1 = number

    def latch_sel_rs2(self, number: int):
        self.rs2 = number

    def get_rd_data(self):
        return self.rd

    def get_rs1_data(self):
        return self.rs1

    def get_rs2_data(self):
        return self.rs2

    def get_input(self):
        return self.rin()

    def set_output(self, data):
        self.rout(data)


class ALU:
    output: int
    a: int
    b: int
    _operations_ = {
        Opcode.ADD: lambda a, b: a + b,
        Opcode.SUB: lambda a, b: a - b,
        Opcode.MUL: lambda a, b: a * b,
        Opcode.DIV: lambda a, b: a // b,
        Opcode.REM: lambda a, b: a % b,
    }

    def __init__(self):
        self.output = 0
        self.a = 0
        self.b = 0

    def load(self, a: int, b: int):
        self.a = a
        self.b = b

    def compute(self, operation: Opcode) -> int:
        self.output = int(self._operations_[operation](self.a, self.b))
        return self.output


class BranchComparator:
    a: int
    b: int

    def __init__(self):
        self.a = 0
        self.b = 0

    def load(self, a: int, b: int):
        self.a = a
        self.b = b

    def compare(self) -> Tuple[bool, bool]:
        return self.a == self.b, self.a < self.b


class DataPath:
    memory: List
    data_memory_size: int
    current_address: int
    instruction_pointer: int
    register_unit: RegisterUnit
    alu: ALU
    branch_comparator: BranchComparator

    current_instruction: None

    current_data: None
    immediately_generator: int

    def __init__(self, data: List, data_memory_size: int, input_mapping, output_mapping):
        assert data_memory_size > 0, "Data_memory size should be non-zero"
        self.data_memory_size = data_memory_size
        self.memory = data
        self.instruction_pointer = 0
        self.current_address = 0
        self.immediately_generator = 0
        self.register_unit = RegisterUnit(input_mapping, output_mapping)
        self.alu = ALU()
        self.branch_comparator = BranchComparator()

    def select_instruction(self):
        # self.current_instruction = self.memory[self.instruction_pointer + ..]
        # opcode, args = self.current_instruction
        # self.args = deque(args)
        self.instruction_pointer += 1
        return None


    def latch_dest_reg_from_instr(self):
        # arg = self.args.popleft()
        self.register_unit.latch_sel_rd(int(arg))




    