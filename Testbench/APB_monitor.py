from common_imports import *
from APB_seq_item_vsc import *
from APB_seq_itemMod import APB_seq_item
from pyquesta import SVConduit

class APB_monitor(uvm_monitor):

	def build_phase(self):
		self.mon_ap = uvm_analysis_port.create("mon_ap", self)
		self.dut = cocotb.top

	async def run_phase(self):
		while True:

			await RisingEdge(self.dut.PCLK)
			# await First(RisingEdge(self.dut.PENABLE), RisingEdge(self.dut.PREADY)) # Either at SETUP phase or ACCESS phase or at end of transfer
			# await Combine(FallingEdge(self.dut.PENABLE), FallingEdge(self.dut.PREADY)) # Wait for end of transfer

			rsp_seq_item = APB_seq_item_vsc.create("rsp_seq_item")

			rsp_seq_item.PRESETn	=	self.dut.PRESETn.value
			rsp_seq_item.PWDATA		=	self.dut.PWDATA.value
			rsp_seq_item.PRDATA		=	self.dut.PRDATA.value
			rsp_seq_item.PADDR		=	self.dut.PADDR.value
			rsp_seq_item.PENABLE	=	self.dut.PENABLE.value
			rsp_seq_item.PWRITE		=	self.dut.PWRITE.value
			rsp_seq_item.PREADY		=	self.dut.PREADY.value
			
			self.logger.debug(f"{self.get_type_name()}: MONITORED {rsp_seq_item}")

			self.mon_ap.write(rsp_seq_item)
			
			item_sv = APB_seq_item()

			item_sv.PRESETn		=	rsp_seq_item.PRESETn
			item_sv.PWDATA		=	rsp_seq_item.PWDATA
			item_sv.PRDATA		=	rsp_seq_item.PRDATA
			item_sv.PADDR		=	rsp_seq_item.PADDR
			item_sv.PENABLE		=	rsp_seq_item.PENABLE
			item_sv.PWRITE		=	rsp_seq_item.PWRITE
			item_sv.PREADY		=	rsp_seq_item.PREADY

			self.logger.debug(f"{self.get_type_name()}: Monitor sent to SVConduit's put: {item_sv}")
			
			SVConduit.put(item_sv)