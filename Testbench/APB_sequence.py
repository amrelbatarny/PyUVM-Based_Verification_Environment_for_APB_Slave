from common_imports import *
from APB_seq_item import *

class APB_base_sequence(uvm_sequence, uvm_report_object):
    
    def seq_print(self, msg: str):
        # self.logger.info(msg)
        uvm_root().logger.info(msg)

    def __init__(self, name="APB_base_sequence"):
        super().__init__(name)
        self.ral = ConfigDB().get(None, "", "regsiter_model")
        self.map = self.ral.def_map

    async def reg_write(self, reg_addr: int, write_data: int):
        target_reg = self.map.get_reg_by_offset(reg_addr)
        status = await target_reg.write(write_data,
                                        self.map,
                                        path_t.FRONTDOOR,
                                        check_t.NO_CHECK)
        return status
    
    async def body(self):
        raise UVMNotImplemented  


##############################################################################
# Specialized APB Test Sequences
##############################################################################

class APB_TestAll_sequence(APB_base_sequence):

    async def body(self):

        for _ in range(100):
            item = APB_seq_item.create("item")
            await self.start_item(item)
            item.del_constraint(item.pwrite_dist)
            item.randomize()
            await self.finish_item(item)

class APB_write_sequence(APB_base_sequence):

    async def body(self):

        for _ in range(100):
            item = APB_seq_item.create("item")
            await self.start_item(item)
            item.randomize()
            await self.finish_item(item)

class APB_read_sequence(APB_base_sequence):

    async def body(self):
        def my_pwrite_dist(PWRITE):
            return 9 if PWRITE == 0 else 1

        for _ in range(100):
            item = APB_seq_item.create("item")
            await self.start_item(item)
            item.randomize_with(my_pwrite_dist)
            await self.finish_item(item)

class APB_reg_sequence(APB_base_sequence):

    async def body(self):
        status = await self.ral.reg_ADC_CTRL_REG.write(0xABCD, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)