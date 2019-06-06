class InstructionStatus:
    def __init__(self, inst):
       self.inst = inst
       self.issue = -1
       self.exe = -1
       self.wr = -1

class ReservationStation:
    types = 3
    ARS, MRS, LB = range(types)

    def __init__(self, rs_type):
        self.type = rs_type

        if self.type == ReservationStation.LB:
            self.busy = False
            self.address = None
        else:
            self.op = None
            self.vj = None
            self.vk = None
            self.qj = None
            self.qk = None

class Register:
    def __init__(self):
        self.stat = None
        self.val = 0x0

class FunctionUnit:
    types = 3
    ADD, MULT, LOAD = range(types)

    def __init__(self, fu_type):
        self.type = fu_type
        self.inst = None
        self.time = 0

def main():
    inst_status = InstructionStatus('LD, F1, 0x2')

if __name__ == '__main__':
    main()
