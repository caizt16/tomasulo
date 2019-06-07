from utils import *
from status import *
from controller import *

class Simulator:
    def __init__(self):
        self.inst_status = None
        self.rs = None
        self.reg = None
        self.fu = None
        self.controller = Controller(self)

    def __check_runnable(self):
        assert(type(self.inst_status) == list)
        for stat in self.inst_status:
            assert(type(stat) == InstructionStatus)

        assert(type(self.rs) == list)
        assert(len(self.rs) == ReservationStation.types)
        for type_list in self.rs:
            assert(type(type_list) == list)
            for rs in type_list:
                assert(type(rs) == ReservationStation)

        assert(type(self.reg) == list)
        for reg in self.reg:
            assert(type(reg) == Register)

        assert(type(self.fu) == list)
        assert(len(self.fu) == FunctionUnit.types)
        for fu_list in self.fu:
            assert(type(fu_list) == list)
            for fu in fu_list:
                assert(type(fu) == FunctionUnit)

    def read_inst(self, filename):
        self.inst_status = list()
        with open(filename, 'r') as f:
            for line in f.readlines():
                self.inst_status.append(InstructionStatus(line))

    def add_rs(self, rs_type, num):
        if self.rs == None:
            self.rs = [[] for _ in range(ReservationStation.types)]

        for _ in range(num):
            self.rs[rs_type].append(ReservationStation(rs_type))

    def init_rs(self, ars_n, mrs_n, lb_n):
        self.add_rs(ReservationStation.ARS, ars_n)
        self.add_rs(ReservationStation.MRS, mrs_n)
        self.add_rs(ReservationStation.LB, lb_n)

    def add_reg(self, num):
        if self.reg == None:
            self.reg = list()

        for _ in range(num):
            self.reg.append(Register())

    def add_fu(self, fu_type, num):
        if self.fu == None:
            self.fu = [[] for _ in range(FunctionUnit.types)]

        self.fu[fu_type].append(FunctionUnit(fu_type))

    def init_fu(self, add_n, mult_n, load_n):
        self.add_fu(FunctionUnit.ADD, add_n)
        self.add_fu(FunctionUnit.MULT, mult_n)
        self.add_fu(FunctionUnit.LOAD, load_n)

    def __step(self):
        self.controller.run_one_cycle()

    def is_finished(self):
        return False

    def run(self, cycles:int=-1):
        self.__check_runnable()

        cnt = 0
        while cycles:
            if self.is_finished():
                return cnt
            self.__step()
            cnt += 1
            cycles -= 1
        return cnt

    def step(self):
        self.__check_runnable()
        if self.is_finished():
            return False
        self.__step()

    def print_inst_status(self):
        print('\t\t\t\tissue\texe\twr\n')
        for inst in self.inst_status:
            print('%30s\t%d\t%d\t%d\n' % (inst.inst[:-1], inst.issue, inst.exe, inst.wr))

    def print_rs_status(self):
        print('\tBusy\top\tvj\tvk\tqj\tqk\n')
        for i, rs in enumerate(self.rs[0]):
            print('%s\t%s\n' % (rs.get_name(), rs.busy))
        for i, rs in enumerate(self.rs[1]):
            print('%s\t%s\n' % (rs.get_name(), rs.busy))
        print('\tBusy\tAddress\n')
        for i, rs in enumerate(self.rs[2]):
            print('%s\t%s\t%s\n' % (rs.get_name(), rs.busy, rs.address))

    def print_reg_status(self):
        print('\t', end = '')
        for _ in range(5):
            print('F%d\t' % (_), end = '')
        print('\n')

        print('State\t', end = '')
        for _ in range(5):
            name = '' if self.reg[_].stat == None else self.reg[_].stat.get_name()
            print('%s\t' % name, end = '')
        print('\n')

    def print_status(self):
        self.print_inst_status()
        self.print_rs_status()
        self.print_reg_status()

def main():
    sim = Simulator()
    sim.init_rs(6, 3, 3)
    sim.init_fu(3, 2, 2)
    sim.add_reg(32)
    sim.read_inst('test0.nel')
    for _ in range(4):
        sim.step()
    sim.print_status()

if __name__ == '__main__':
    main()
