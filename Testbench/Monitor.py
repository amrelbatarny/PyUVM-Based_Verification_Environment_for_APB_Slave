import cocotb                                         # access cocotb.top and scheduler :contentReference[oaicite:3]{index=3}
from cocotb.triggers import RisingEdge                # await clock/reset edges :contentReference[oaicite:4]{index=4}
from pyuvm import uvm_monitor, uvm_analysis_port      # UVM monitor base & analysis port :contentReference[oaicite:5]{index=5}
from SequenceItem import ApbSeqItem                   # your sequence item definition
from APB_utils import APBType
from APB_seq_itemMod import APB_seq_item
from pyquesta import SVConduit

class ApbMonitor(uvm_monitor):

	def build_phase(self):
		self.mon_ap = uvm_analysis_port.create("mon_ap", self)
		self.dut = cocotb.top

	async def run_phase(self):
		await RisingEdge(self.dut.PRESETn)

		while True:
			await RisingEdge(self.dut.PCLK)
			if self.dut.PSELx and self.dut.PENABLE and self.dut.PRESETn:
				item = ApbSeqItem.create("item")
				item.addr = self.dut.PADDR
				if (self.dut.PWRITE.value):
					item.data = self.dut.PWDATA.value
					item.type = APBType.WRITE
				else:
					item.data = self.dut.PRDATA.value
					item.type = APBType.READ
				self.mon_ap.write(item)

			self.logger.debug(f"{self.get_type_name()}: MONITORED {item}")
			
			# Populating SystemVerilog's item
			# item_sv = APB_seq_item()

			# item_sv.PRESETn		=	item.PRESETn
			# item_sv.PWDATA		=	item.PWDATA
			# item_sv.PRDATA		=	item.PRDATA
			# item_sv.PADDR		=	item.PADDR
			# item_sv.PENABLE		=	item.PENABLE
			# item_sv.PWRITE		=	item.PWRITE
			# item_sv.PREADY		=	item.PREADY

			# self.logger.debug(f"{self.get_type_name()}: Monitor sent to SVConduit's put: {item_sv}")
			
			# SVConduit.put(item_sv)