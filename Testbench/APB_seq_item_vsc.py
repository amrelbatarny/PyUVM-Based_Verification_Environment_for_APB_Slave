from common_imports import *

@vsc.randobj
class APB_seq_item_vsc(uvm_sequence_item):

    def __init__(self, name):
        super().__init__(name)
        self.PRESETn = vsc.rand_bit_t(1)
        self.PWDATA  = vsc.rand_bit_t(32)
        self.PENABLE = vsc.rand_bit_t(32)
        self.PWRITE  = vsc.rand_bit_t(1)
        self.PADDR   = vsc.rand_bit_t(32)
        
        self.PREADY  = 0
        self.PDATA   = 0

        self.pwrite_weight = 90

    @vsc.constraint
    def dist(self):
        vsc.dist(self.PRESETn, [vsc.weight(1, 90), vsc.weight(0, 10)])
        vsc.dist(self.PENABLE, [vsc.weight(1, 90), vsc.weight(0, 10)])
        vsc.dist(self.PWDATA, [
            vsc.weight(0x00000000,                    20),
            vsc.weight((0x00000001, 0xFFFFFFFF - 1),  60),
            vsc.weight(0xFFFFFFFF,                    20)])

    @vsc.constraint
    def pwrite_data_constraints(self):
        with vsc.if_then(self.PWRITE == 0):
            self.PWDATA == 0  # Driver ignores PWDATA for reads

    @vsc.constraint
    def PADDR_constr(self):
        self.PADDR.inside(vsc.rangelist(vsc.rng(0x00000000, 0x0000003C + 1)))
        self.PADDR % 4 == 0
        
    def __str__(self):
        return ((f"\nName: {self.get_full_name()} \
                \nPRESETn: {self.PRESETn} \
                \nPWDATA:  {self.PWDATA} \
                \nPADDR:   {self.PADDR} \
                \nPENABLE: {self.PENABLE} \
                \nPWRITE:  {self.PWRITE} \
                \nPREADY:  {self.PREADY} \
                \nPRDATA:  {self.PRDATA}"))

# print("start")
# item = APB_seq_item_vsc()
# item.randomize()
# print(item.PRESETn, item.PWDATA, item.PENABLE, item.PWRITE, item.PADDR)