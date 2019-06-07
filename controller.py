from status import *

class Controller:
    def __init__(self, sim):
        self.sim = sim
        self.time = 0
        self.eip = 0

    @property
    def now_inst_status(self):
        return self.sim.inst_status[self.eip]

    @property
    def now_inst(self):
        return self.now_inst_status.inst

    @property
    def now_inst_list(self):
        return self.now_inst.strip('\n').split(',')

    def __get_inst_type(self):
        inst_type = self.now_inst_list[0]

        if inst_type in ['ADD', 'SUB']:
            return FunctionUnit.ADD
        elif inst_type in ['MUL', 'DIV']:
            return FunctionUnit.MULT
        elif inst_type == 'LD':
            return FunctionUnit.LOAD
        return -1

    def __get_ld_addr(self):
        return self.now_inst_list[2]

    def __get_write_reg(self):
        index = int(self.now_inst_list[1][1:])
        return self.sim.reg[index]

    def run_one_cycle(self):
        self.time += 1
        self.run_issue()
        self.run_exe()
        self.run_wr()

    def run_issue(self):
        inst_type = self.__get_inst_type()
        assert(inst_type != -1)


        wr_reg =  self.__get_write_reg()
        if wr_reg.stat != None:
            return

        for i, rs in enumerate(self.sim.rs[inst_type]):
            if not rs.busy:
                self.now_inst_status.issue = self.time
                rs.busy = True

                if inst_type == FunctionUnit.LOAD:
                    rs.address = self.__get_ld_addr()

                self.eip += 1
                wr_reg.stat = rs
                break

    def run_exe(self):
        pass

    def run_wr(self):
        pass
