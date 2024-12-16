from common_imports import *
from APB_seq_item import *

class APB_reg_adapter(uvm_reg_adapter, uvm_report_object):
		def __init__(self, name="APB_reg_adapter"):
			super().__init__(name)

		def reg2bus(self, rw: uvm_reg_bus_op) -> uvm_sequence_item:
			# uvm_root().logger.info(f"Entered the adapter: rw.addr = {rw.addr}, rw.data = {rw.data:#x}")
			item = APB_seq_item("item")
			if (rw.kind == access_e.UVM_READ):
				item.PWRITE = 0
			else:
				item.PWRITE = 1
			item.PENABLE = 1
			item.PADDR = rw.addr
			item.PWDATA = rw.data
			if (rw.status == status_t.IS_OK):
				item.PREADY = 1
			else:
				item.PREADY = 0
			return item
		
		def bus2reg(self, bus_item: uvm_sequence_item, rw: uvm_reg_bus_op):
			rw.kind = access_e.UVM_READ if bus_item.PWRITE == 0 else access_e.UVM_WRITE
			rw.addr = bus_item.PADDR
			rw.data = bus_item.PRDATA if bus_item.PWRITE == 0 else bus_item.PWDATA
			rw.status = status_t.IS_OK if bus_item.PREADY == 1 else status_t.IS_NOT_OK