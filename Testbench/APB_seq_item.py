from common_imports import *

class APB_seq_item(uvm_sequence_item, Randomized):

    def presetn_dist(PRESETn):
        return 9 if PRESETn == 1 else 1

    def penable_dist(PENABLE):
        return 9 if PENABLE == 1 else 1

    def pwrite_dist(PWRITE):
        return 9 if PWRITE == 1 else 1

    def __init__(self, name):
        super().__init__(name)
        Randomized.__init__(self)
        self.PRESETn = 0
        self.PWDATA  = 0
        self.PENABLE = 0
        self.PWRITE  = 0
        self.PADDR  = 0
        self.PRDATA  = 0

        self.dut = cocotb.top

        self.add_rand("PRESETn", [0, 1])
        self.add_rand("PADDR", list(range(0x00000000, 0x0000003C + 1)))
        self.add_rand("PENABLE", [0, 1])
        self.add_rand("PWRITE", [0, 1])

        self.add_constraint(self.presetn_dist)
        self.add_constraint(lambda PADDR: PADDR % 4 == 0)
        self.add_constraint(self.penable_dist)
        self.add_constraint(self.pwrite_dist)
        
        self.PENABLE = random.randint(0, (1 << self.dut.PENABLE.value.n_bits) - 1)
        self.PWDATA  = random.randint(0, (1 << self.dut.PWDATA.value.n_bits) - 1)

    def __str__(self):
        return ((f"\nName: {self.get_full_name()} \
                \nPRESETn: {self.PRESETn} \
                \nPWDATA: {self.PWDATA} \
                \nPADDR: {self.PADDR} \
                \nPENABLE: {self.PENABLE} \
                \nPWRITE: {self.PWRITE} \
                \nPREADY: {self.PREADY} \
                \nPRDATA: {self.PRDATA}"))