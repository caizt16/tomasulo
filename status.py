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
        self.reg = None
        self.clear()

    def clear(self):
        self.reg = None
        self.inst = None

        self.busy = False
        self.running = False

        self.delay = False
        self.div_zero = False

        if self.type == ReservationStation.LB:
            self.address = ''
        else:
            self.op = ''
            self.vj = ''
            self.vk = ''
            self.qj = ''
            self.qk = ''

    def update(self, inst_list, reg_list):
        self.op = inst_list[0]

        index = int(inst_list[2][1:])
        self.qj = reg_list[index].get_stat_string()
        if reg_list[index].stat == None:
            self.vj = reg_list[index].val

        index = int(inst_list[3][1:])
        self.qk = reg_list[index].get_stat_string()
        if reg_list[index].stat == None:
            self.vk = reg_list[index].val

    def get_name(self):
        return ReservationStation.name[self.type]+str(self.index)

class Register:
    def __init__(self):
        self.clear()

    def clear(self):
        self.stat = None
        self.val = 0x0

    def get_stat_string(self):
        return '' if self.stat == None else self.stat.get_name()

class FunctionUnit:
    types = 3
    ADD, MULT, LOAD = range(types)

    def __init__(self, fu_type):
        self.type = fu_type
        self.rs = None
        self.clear()

    def clear(self):
        self.inst = None
        if self.rs != None:
            self.rs.clear()
        self.rs = None
        self.time = 0

    def get_time(self):
        inst_type = self.inst.inst.split(',')[0]
        if inst_type == 'JUMP':
            return 1
        if inst_type == 'MUL':
            return 4
            return 12
        if inst_type == 'DIV':
            return 4
            return 40
        if inst_type in ['LD', 'ADD', 'SUB']:
            return 3

def main():
    inst_status = InstructionStatus('LD, F1, 0x2')

if __name__ == '__main__':
    main()
