"""
Author : Amr El Batarny
File   : Driver.py
Brief  : Contains the APB driver class responsible for driving transactions onto the APB interface.
"""

import cocotb
from cocotb.triggers import RisingEdge
from pyuvm import uvm_driver
from pyuvm import ConfigDB
from pyuvm import access_e
from BFM       import ApbBfm
from APB_utils import APBType

class ApbDriver(uvm_driver):

	def build_phase(self):
		self.dut = cocotb.top
		self.ral = ConfigDB().get(None, "", "REGISTER_MODEL")
		
		self.map = self.ral.def_map
		
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
			await self.bfm.write(item.addr, item.data, item.strobe)
			self.predict_regs(item.addr, item.data, item.strobe)
		else:
			item.data = await self.bfm.read(item.addr)
		self.logger.debug(f"{self.get_type_name()}: DRIVED {item.get_type_name()} item {item}")

	def predict_regs(self, addr, val, strobe):
		# Compute byte‐enable mask (32-bit value)
		mask = 0
		for byte_lane in range(4):
			if (strobe >> byte_lane) & 1:
				mask |= 0xFF << (8 * byte_lane)

		# Helper to merge old mirror and new data
		def merge(reg):
			old = reg.get_mirrored_value()
			merged = (old & ~mask) | (val & mask)
			reg.predict(merged, access_e.UVM_WRITE)

		# Dispatch based on address
		if   addr == 0x00: merge(self.ral.reg_SYS_STATUS_REG)
		elif addr == 0x04: merge(self.ral.reg_INT_CTRL_REG)
		elif addr == 0x08: merge(self.ral.reg_DEV_ID_REG)
		elif addr == 0x0C: merge(self.ral.reg_MEM_CTRL_REG)
		elif addr == 0x10: merge(self.ral.reg_TEMP_SENSOR_REG)
		elif addr == 0x14: merge(self.ral.reg_ADC_CTRL_REG)
		elif addr == 0x18: merge(self.ral.reg_DBG_CTRL_REG)
		elif addr == 0x1C: merge(self.ral.reg_GPIO_DATA_REG)
		elif addr == 0x20: merge(self.ral.reg_DAC_OUTPUT_REG)
		elif addr == 0x24: merge(self.ral.reg_VOLTAGE_CTRL_REG)
		elif addr == 0x28: merge(self.ral.reg_CLK_CONFIG_REG)
		elif addr == 0x2C: merge(self.ral.reg_TIMER_COUNT_REG)
		elif addr == 0x30: merge(self.ral.reg_INPUT_DATA_REG)
		elif addr == 0x34: merge(self.ral.reg_OUTPUT_DATA_REG)
		elif addr == 0x38: merge(self.ral.reg_DMA_CTRL_REG)
		elif addr == 0x3C: merge(self.ral.reg_SYS_CTRL_REG)
		else:
			self.logger.warning(f"Unknown register address: 0x{addr:02X}")