class InstructionStatus:
    def __init__(self, inst):
       self.inst = inst
       self.issue = -1
       self.exe = -1
       self.wr = -1

class ReservationStation:
    types = 3
    ARS, MRS, LB = range(types)
    name = ['ARS', 'MRS', 'LB']
    cnt = [0 for _ in range(types)]

    def __init__(self, rs_type):
        ReservationStation.cnt[rs_type] += 1

        self.index = ReservationStation.cnt[rs_type]
        self.type = rs_type
        self.busy = False

        if self.type == ReservationStation.LB:
            self.address = None
        else:
            self.op = None
            self.vj = None
            self.vk = None
            self.qj = None
            self.qk = None

    def get_name(self):
        return ReservationStation.name[self.type]+str(self.index)

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
