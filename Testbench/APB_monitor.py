from common_imports import *
from APB_seq_item import *

class APB_monitor(uvm_monitor):

	def build_phase(self):
		self.mon_ap = uvm_analysis_port.create("mon_ap", self)
		self.dut = cocotb.top

	async def run_phase(self):
		while True:

			await RisingEdge(self.dut.PCLK)
			await First(RisingEdge(self.dut.PENABLE), RisingEdge(self.dut.PREADY)) # Either at SETUP phase or ACCESS phase or at end of transfer
			await Combine(FallingEdge(self.dut.PENABLE), FallingEdge(self.dut.PREADY)) # Wait for end of transfer

			rsp_seq_item = APB_seq_item.create("rsp_seq_item")

			rsp_seq_item.PRESETn	=	self.dut.PRESETn.value
			rsp_seq_item.PWDATA		=	self.dut.PWDATA.value
			rsp_seq_item.PRDATA		=	self.dut.PRDATA.value
			rsp_seq_item.PADDR		=	self.dut.PADDR.value
			rsp_seq_item.PENABLE	=	self.dut.PENABLE.value
			rsp_seq_item.PWRITE		=	self.dut.PWRITE.value
			rsp_seq_item.PREADY		=	self.dut.PREADY.value
			
			self.mon_ap.write(rsp_seq_item)
			self.logger.debug(f"{self.get_type_name()}: MONITORED {rsp_seq_item.__str__()}")