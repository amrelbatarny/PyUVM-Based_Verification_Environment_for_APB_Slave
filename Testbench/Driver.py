import cocotb
from cocotb.triggers import RisingEdge
from pyuvm import uvm_driver
from BFM       import ApbBfm
from APB_utils import APBType

class ApbDriver(uvm_driver):

	def build_phase(self):
		self.dut = cocotb.top
		
	def start_of_simulation_phase(self):
		self.bfm = ApbBfm()

	async def run_phase(self):
		self.logger.debug("Entered the driver")
		await self.bfm.reset()
		self.logger.info("Reset done")
		while True:
			await RisingEdge(self.dut.PCLK)
			stim_seq_item = await self.seq_item_port.get_next_item()
			await self.drive(stim_seq_item)
			self.seq_item_port.item_done()

	async def drive(self, item):
		self.logger.debug("Driving...")
		if(item.type == APBType.WRITE):
			await self.bfm.write(item.addr, item.data)
		else:
			item.data = await self.bfm.read(item.addr)