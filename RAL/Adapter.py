from pyuvm import uvm_reg_adapter
from pyuvm import uvm_reg_bus_op
from pyuvm import uvm_sequence_item
from pyuvm.s24_uvm_reg_includes import access_e
from SequenceItem import ApbSeqItem
from APB_utils import APBType

class ApbRegAdapter(uvm_reg_adapter):
		def __init__(self, name="APB_reg_adapter"):
			super().__init__(name)

		def reg2bus(self, rw: uvm_reg_bus_op) -> uvm_sequence_item:
			item = ApbSeqItem("item")
			item.type = APBType.READ if rw.kind == access_e.UVM_READ else APBType.WRITE
			item.data = rw.data
			item.addr = int(rw.addr, 16)  # Convert '0x14' to integer 20
			return item
		
		def bus2reg(self, bus_item: uvm_sequence_item, rw: uvm_reg_bus_op):
			rw.kind = access_e.UVM_READ if bus_item.type == APBType.READ else access_e.UVM_WRITE
			rw.data = bus_item.data
			rw.addr = bus_item.addr