from common_imports import *
from APB_bfm import *

class APB_driver(uvm_driver):

	def build_phase(self):
		self.dut = cocotb.top
		
	def start_of_simulation_phase(self):
		self.bfm = APB_bfm()

	async def run_phase(self):
		# await Timer(10, units='ns')
		# self.logger.info("Entered the driver")
		await self.bfm.reset()
		# self.logger.info("Reset done")
		while True:
			# self.logger.info("Getting the next item...")
			stim_seq_item = await self.seq_item_port.get_next_item()
			# self.logger.info("Got the item successfully")

			self.dut.PRESETn.value = int(stim_seq_item.PRESETn)

			if stim_seq_item.PRESETn:
				await self.drive(stim_seq_item)
			
			self.seq_item_port.item_done()

			await RisingEdge(self.dut.PCLK)
			# self.logger.info("Driving done")
			# self.logger.info(stim_seq_item.__str__())

	async def drive(self, stim_seq_item):
		# self.logger.info("Driving...")

		## IDLE Phase
		await self.bfm.idle()
	
		## Drive data
		await self.bfm.prepare_data(stim_seq_item)
	
		## SETUP Phase
		await self.bfm.setup(stim_seq_item)
			
		## ACCESS Phase
		await self.bfm.access()
	
		## back to IDLE state
		self.dut.PENABLE.value = 0