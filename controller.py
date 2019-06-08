from status import *

class Controller:
    def __init__(self, sim):
        self.sim = sim
        self.time = 0
        self.eip = 0
        self.stall = False

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

        if inst_type in ['JUMP', 'ADD', 'SUB']:
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

    def __get_reg(self, reg):
        index = int(reg[1:])
        return self.sim.reg[index]

    def __get_working_fu(self):
        for fu_type in range(FunctionUnit.types):
            for fu in self.sim.fu[fu_type]:
                if fu.inst != None:
                    yield fu

    def __get_working_rs(self):
        for rs_type in range(ReservationStation.types):
            for rs in self.sim.rs[rs_type]:
                if rs.inst != None:
                    yield rs

    def __to_signed_int(self, string):
        val = int(string, 16)
        return ((val+0x80000000)&0xFFFFFFFF) - 0x80000000

    def run_one_cycle(self):
        self.time += 1
        self.run_wr()
        self.run_exe()
        self.run_issue()

    def run_issue(self):
        if self.eip >= len(self.sim.inst_status):
            return

        inst_type = self.__get_inst_type()
        assert(inst_type != -1)

        if self.now_inst_list[0] == 'JUMP':
            for i, rs in enumerate(self.sim.rs[ReservationStation.ARS]):
                if not rs.busy and not self.stall:
                    self.now_inst_status.issue = self.time
                    rs.inst = self.now_inst_status
                    rs.busy = True
                    rs.op = 'JUMP'
                    self.stall = True

                    index = int(self.now_inst_list[2][1:])
                    rs.qj = self.sim.reg[index].get_stat_string()
                    if self.sim.reg[index].stat == None:
                        rs.vj = self.sim.reg[index].val
                    break
        else:
            wr_reg =  self.__get_write_reg()
            '''
            if wr_reg.stat != None:
                return
            '''

            for i, rs in enumerate(self.sim.rs[inst_type]):
                if not rs.busy:
                    self.now_inst_status.issue = self.time
                    rs.inst = self.now_inst_status
                    rs.busy = True
                    rs.reg = wr_reg

                    if inst_type == FunctionUnit.ADD:
                        rs.update(self.now_inst_list, self.sim.reg)
                    elif inst_type == FunctionUnit.MULT:
                        rs.update(self.now_inst_list, self.sim.reg)
                    elif inst_type == FunctionUnit.LOAD:
                        rs.address = self.__get_ld_addr()
                    else:
                        assert(0)

                    self.eip += 1
                    wr_reg.stat = rs
                    break

    def run_exe(self):
        for rs in self.__get_working_rs():
            if not rs.running:
                for fu in self.sim.fu[rs.type]:
                    if fu.inst == None:
                        rs.running = True
                        fu.inst = rs.inst
                        fu.rs = rs
                        fu.time = fu.get_time()
                        break

        for fu in self.__get_working_fu():
            if fu.rs.delay:
                fu.rs.delay = False
                continue

            if fu.rs.type == ReservationStation.LB or (fu.rs.qj == '' and fu.rs.qk == ''):
                fu.time -= 1

                self.check_div(fu.rs)
                if fu.rs.div_zero:
                    fu.time = 0

                if fu.time == 0:
                    fu.inst.exe = self.time

    def run_wr(self):
        for fu in self.__get_working_fu():
            if fu.time == 0:
                fu.inst.wr = self.time

                value = self.run_code(fu.rs)
                if value == None:
                    fu.clear()
                    continue

                wr_reg = self.sim.reg[int(fu.inst.inst.split(',')[1][1:])]
                if wr_reg.stat == fu.rs:
                    wr_reg.stat = None
                    wr_reg.val = value

                for rs in self.__get_working_rs():
                    if rs.type != ReservationStation.LB:
                        if rs.qj == fu.rs.get_name():
                            rs.qj = ''
                            rs.vj = value
                            if rs.qk == '':
                                rs.delay = True
                        if rs.qk == fu.rs.get_name():
                            rs.qk = ''
                            rs.vk = value
                            if rs.qj == '':
                                rs.delay = True
                fu.clear()

    def check_div(self, rs):

        code = rs.inst.inst
        code_list = code.strip('\n').split(',')

        if code_list[0] != 'DIV':
            return

        val3 = rs.vk if rs.vk != '' else self.__get_reg(code_list[3]).val

        if val3 == 0:
            rs.div_zero = True

    def run_code(self, rs):
        code = rs.inst.inst
        code_list = code.strip('\n').split(',')

        if code_list[0] == 'LD':
            return self.__to_signed_int(code_list[2])

        elif code_list[0] == 'JUMP':
            val2 = rs.vj if rs.qj != '' else self.__get_reg(code_list[2]).val
            if val2 == self.__to_signed_int(code_list[1]):
                self.eip += self.__to_signed_int(code_list[3])

            else:
                self.eip += 1
            self.stall = False
            return None
        else:
            val2 = rs.vj if rs.vj != '' else self.__get_reg(code_list[2]).val
            val3 = rs.vk if rs.vk != '' else self.__get_reg(code_list[3]).val

            if code_list[0] == 'ADD':
                return val2 + val3
            elif code_list[0] == 'SUB':
                return val2 - val3
            elif code_list[0] == 'MUL':
                return val2 * val3
            elif code_list[0] == 'DIV':
                return val2 if rs.div_zero else val2 // val3

def main():
    print(int('0xc', 16))

if __name__ == '__main__':
    main()
