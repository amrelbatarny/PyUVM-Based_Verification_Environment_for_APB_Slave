"""
Author : Amr El Batarny
File   : Monitor.py
Brief  : Implements the APB monitor class that observes and records transactions from the APB interface.
"""
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from pyuvm import uvm_monitor, uvm_analysis_port
from pyuvm import ConfigDB
from pyuvm import UVMConfigItemNotFound

from SequenceItem import ApbSeqItem
from APB_utils import APBType
from APB_seq_itemMod import APB_seq_item
from pyquesta import SVConduit

class ApbMonitor(uvm_monitor):

	def build_phase(self):
		self.mon_ap = uvm_analysis_port.create("mon_ap", self)
		self.dut = cocotb.top
		self.monitor_count = 0

	def start_of_simulation_phase(self):
		# Read the coverage-mode flag from the ConfigDB (default to False)
		try:
			self.sv_coverage_en = ConfigDB().get(self, "", "ENABLE_SV_COVERAGE")
		except UVMConfigItemNotFound:
			self.sv_coverage_en = False

	async def run_phase(self):
		# Wait until reset is deasserted before sampling begins
		await RisingEdge(self.dut.PRESETn)

		while True:
			# Create a new sequence item for each transaction
			item = ApbSeqItem.create("item")

			# Align to start of a new APB cycle
			await FallingEdge(self.dut.PCLK)
			
			# Wait until setup phase: PSELx, PENABLE, PRESETn all high
			while not (
				int(self.dut.PSELx.value)   == 1 and
				int(self.dut.PENABLE.value) == 1 and
				int(self.dut.PRESETn.value) == 1
			):
				await FallingEdge(self.dut.PCLK)
			
			self.logger.debug("Now, it's the setup phase, we can sample addr, type and data(for write)")

			item.addr = self.dut.PADDR

			if (self.dut.PWRITE.value):
				item.type = APBType.WRITE
				item.data = self.dut.PWDATA.value
			else:
				# For reads, wait until PREADY asserts, then capture PRDATA on next cycle
				while not (self.dut.PREADY):
					await FallingEdge(self.dut.PCLK)
				self.logger.debug("PREADY is asserted, now we can sample PRDATA")
				await FallingEdge(self.dut.PCLK)
				item.data = self.dut.PRDATA.value

				self.mon_ap.write(item)
				self.logger.debug(f"{self.get_type_name()}: MONITORED PyVSC's item {item}")
			
			# Route transactions to the chosen coverage backend:
			# - If SV coverage is enabled, serialize and send to SystemVerilog via SVConduit.put()
			if self.sv_coverage_en == True:
				# SystemVerilog coverage via SVConduit
				item_sv = APB_seq_item()

				# Populating SystemVerilog's item
				item_sv.addr		=	item.addr
				item_sv.data		=	item.data
				item_sv.strobe		=	item.strobe
				item_sv.type_sv		=	1 if item.type == APBType.WRITE else 0

				SVConduit.put(item_sv)
				self.logger.debug(f"{self.get_type_name()}: Monitor sent to SVConduit's put: {item_sv}")
			
			self.monitor_count += 1

	def report_phase(self):
		# Report how many transactions were monitored
		self.logger.info(f"{self.get_type_name()}: Total transactions monitored = {self.monitor_count}")