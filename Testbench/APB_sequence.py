from common_imports import *
# from APB_seq_item import *
from APB_seq_item_vsc import *
from APB_seq_itemMod import APB_seq_item
from pyquesta import SVConduit

class APB_base_sequence(uvm_sequence, uvm_report_object):
    
    def seq_print(msg: str):
        uvm_root().logger.info(msg)

    def __init__(self, name="APB_base_sequence"):
        super().__init__(name)
        # self.ral = ConfigDB().get(None, "", "regsiter_model")
        # self.map = self.ral.def_map

    # async def reg_write(self, reg_addr: int, write_data: int):
    #     target_reg = self.map.get_reg_by_offset(reg_addr)
    #     status = await target_reg.write(write_data,
    #                                     self.map,
    #                                     path_t.FRONTDOOR,
    #                                     check_t.NO_CHECK)
    #     return status
    
    async def body(self):
        raise UVMNotImplemented  


##############################################################################
# Specialized APB Test Sequences
##############################################################################

class APB_TestAll_sequence(APB_base_sequence):

    async def body(self):
        for _ in range(100):
            item = APB_seq_item_vsc.create("item")
            await self.start_item(item)
            item.randomize()
            await self.finish_item(item)

class APB_write_sequence(APB_base_sequence):

    async def body(self):
        for _ in range(100):
            item = APB_seq_item_vsc.create("item")
            await self.start_item(item)
            with item.randomize_with() as it:
                vsc.dist(it.PWRITE,  [vsc.weight(1, 95), vsc.weight(0, 5)])
            await self.finish_item(item)

class APB_read_sequence(APB_base_sequence):

    async def body(self):
        for _ in range(100):
            item = APB_seq_item_vsc.create("item")
            await self.start_item(item)
            with item.randomize_with() as it:
                vsc.dist(it.PWRITE,  [vsc.weight(1, 1), vsc.weight(0, 99)])
            await self.finish_item(item)

class APB_pyquesta_sequence(APB_base_sequence):

    async def body(self):
        for _ in range(200):
            item = APB_seq_item_vsc.create("item")
            item_vsc = SVConduit.get(APB_seq_item)
            await self.start_item(item)
            item.PRESETn = item_vsc.PRESETn
            item.PWDATA = item_vsc.PWDATA
            item.PENABLE = item_vsc.PENABLE
            item.PWRITE = item_vsc.PWRITE
            item.PADDR = item_vsc.PADDR
            await self.finish_item(item)

# class APB_reg_sequence(APB_base_sequence):

#     async def body(self):
#         status = await self.ral.reg_ADC_CTRL_REG.write(0xABCD, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)