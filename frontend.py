import tkinter as tk
from tkinter import ttk
from simulator import *

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.sim = Simulator()
        self.sim.use_default_setting()

        def start_simulating(event):
            self.sim.read_inst(path_entry.get())
            for item in self.root.winfo_children():
                item.grid_remove()
            self.draw_tomasulo()

        default_path = tk.StringVar()
        default_path.set('test0.nel')
        path_label = tk.Label(self.root, text='nel_path')
        path_label.grid(row=0, sticky=tk.W)
        path_entry = tk.Entry(self.root, textvariable=default_path)
        path_entry.grid(row=0, column=1, sticky=tk.E)
        path_entry.bind('<Return>', start_simulating)

    def init_inst(self):
        self.inst = ttk.Treeview(self.root, show='headings')

        column = ('inst', 'issue', 'exe', 'wr')
        self.inst['column'] = column
        for c in column:
            self.inst.heading(c, text=c)


        self.inst.pack()

    def init_rs(self):
        self.rs1 = ttk.Treeview(self.root, show='headings')

        column = ('ReservationStation', 'busy', 'op', 'vj', 'vk', 'qj', 'qk')
        self.rs1['column'] = column
        for c in column:
            self.rs1.heading(c, text=c)

        self.rs1.pack()

        self.rs2 = ttk.Treeview(self.root, show='headings')

        column = ('LoadBuffer', 'busy', 'address')
        self.rs2['column'] = column
        for c in column:
            self.rs2.heading(c, text=c)

        self.rs2.pack()

    def init_reg(self):
        self.reg = ttk.Treeview(self.root, show='headings')

        column = tuple(['']+['F'+ str(x+1) for x in range(len(self.sim.reg))])
        self.reg['column'] = column
        for c in column:
            self.reg.heading(c, text=c)

        self.reg.pack()


    def draw_tomasulo(self):
        step_button = tk.Button(self.root, highlightbackground='#3E4149', text='step', command=self.step)
        step_button.pack()
        step_button = tk.Button(self.root, highlightbackground='#3E4149', text='run', command=self.run)
        step_button.pack()
        step_button = tk.Button(self.root, highlightbackground='#3E4149', text='first', command=self.first)
        step_button.pack()

        self.init_inst()
        self.init_rs()
        self.init_reg()

        self.update()

    def step(self):
        self.sim.step()
        self.update()

    def run(self):
        self.sim.run()
        self.update()

    def first(self):
        for c in self.inst.get_children():
            self.inst.delete(c)

        for i, inst in enumerate(self.sim.first):
            issue = '' if inst.issue == -1 else inst.issue
            exe = '' if inst.exe == -1 else inst.exe
            wr = '' if inst.wr == -1 else inst.wr
            self.inst.insert('', i, values=(inst.inst[:-1], issue, exe, wr))

    def update(self):
        def delete_tree(tree):
            for c in tree.get_children():
                tree.delete(c)

        delete_tree(self.inst)
        delete_tree(self.rs1)
        delete_tree(self.rs2)
        delete_tree(self.reg)

        for i, inst in enumerate(self.sim.inst_status):
            issue = '' if inst.issue == -1 else inst.issue
            exe = '' if inst.exe == -1 else inst.exe
            wr = '' if inst.wr == -1 else inst.wr
            self.inst.insert('', i, values=(inst.inst[:-1], issue, exe, wr))

        for i, rs in enumerate(self.sim.rs[0]+self.sim.rs[1]):
            self.rs1.insert('', i, value=(rs.get_name(), rs.busy, rs.op, rs.vj, rs.vk, rs.qj, rs.qk))

        for i, rs in enumerate(self.sim.rs[2]):
            self.rs2.insert('', i, value=(rs.get_name(), rs.busy, rs.address))

        stat = ['stat']
        val = ['value']
        for reg in self.sim.reg:
            stat.append(reg.get_stat_string())
            val.append(reg.val)
        self.reg.insert('', 0, value=stat)
        self.reg.insert('', 1, value=val)

    def show(self):
        self.root.mainloop()

def main():
    win = Window()
    win.show()
def not_main():
    win = tk.Tk()
    tree = ttk.Treeview(win)
    tree2 = ttk.Treeview(win)
    tree['columns'] = ('1', '2')
    tree.column('1', width = 199)
    tree.heading('1', text = '1')
    tree.insert('', 0, text = 'line1', values = ('1', '1'))
    tree.pack()
    tree2['columns'] = ('1', '2')
    tree2.pack()
    win.mainloop()

if __name__ == '__main__':
    main()
