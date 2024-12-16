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

class APB_TestAll_sequence(APB_base_sequence):

    async def body(self):
        def pwrite_dist(PWRITE):
            return 5

        # Create seq_item
        for _ in range(100):
            item = APB_seq_item.create("item")
            await self.start_item(item)
            # item.del_constraint(pwrite_dist)
            item.randomize_with(pwrite_dist)
            # item.populate()
            await self.finish_item(item)

class APB_write_sequence(APB_base_sequence):

    async def body(self):

        # Create seq_item
        for _ in range(100):
            item = APB_seq_item.create("item")
            await self.start_item(item)
            item.randomize()
            # item.populate()
            await self.finish_item(item)

class APB_read_sequence(APB_base_sequence):

    async def body(self):
        def pwrite_dist(PWRITE):
            return 9 if PWRITE == 0 else 2

        # Create seq_item
        for _ in range(100):
            item = APB_seq_item.create("item")
            await self.start_item(item)
            item.randomize_with(pwrite_dist)
            # item.populate()
            await self.finish_item(item)

class APB_reg_sequence(APB_base_sequence):

    async def body(self):
        status = await self.ral.reg_ADC_CTRL_REG.write(0xABCD, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)