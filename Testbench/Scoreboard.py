"""
Author : Amr El Batarny
File   : Scoreboard.py
Brief  : Implements the scoreboard for checking the correctness of APB transactions against expected behavior.
"""

from pyuvm import uvm_subscriber
from SequenceItem import ApbSeqItem
from APB_utils import APBType

class ApbScoreboard(uvm_subscriber):
	
	def write(self, item):
		item_in = ApbSeqItem.create("item_in")
		item_in.copy(item)
		if item_in.type == APBType.READ:
			addr = item_in.addr
			# Mirror-read from the RAL model
			if   addr == 0x0:
				result = self.ral.reg_SYS_STATUS_REG.get_mirrored_value()
			elif addr == 0x4:
				result = self.ral.reg_INT_CTRL_REG.get_mirrored_value()
			elif addr == 0x8:
				result = self.ral.reg_DEV_ID_REG.get_mirrored_value()
			elif addr == 0xC:
				result = self.ral.reg_MEM_CTRL_REG.get_mirrored_value()
			elif addr == 0x10:
				result = self.ral.reg_TEMP_SENSOR_REG.get_mirrored_value()
			elif addr == 0x14:
				result = self.ral.reg_ADC_CTRL_REG.get_mirrored_value()
			elif addr == 0x18:
				result = self.ral.reg_DBG_CTRL_REG.get_mirrored_value()
			elif addr == 0x1C:
				result = self.ral.reg_GPIO_DATA_REG.get_mirrored_value()
			elif addr == 0x20:
				result = self.ral.reg_DAC_OUTPUT_REG.get_mirrored_value()
			elif addr == 0x24:
				result = self.ral.reg_VOLTAGE_CTRL_REG.get_mirrored_value()
			elif addr == 0x28:
				result = self.ral.reg_CLK_CONFIG_REG.get_mirrored_value()
			elif addr == 0x2C:
				result = self.ral.reg_TIMER_COUNT_REG.get_mirrored_value()
			elif addr == 0x30:
				result = self.ral.reg_INPUT_DATA_REG.get_mirrored_value()
			elif addr == 0x34:
				result = self.ral.reg_OUTPUT_DATA_REG.get_mirrored_value()
			elif addr == 0x38:
				result = self.ral.reg_DMA_CTRL_REG.get_mirrored_value()
			elif addr == 0x3C:
				result = self.ral.reg_SYS_CTRL_REG.get_mirrored_value()
			else:
				# address not recognized
				result = None

			# Compare and report
			if result == item_in.data:
				self.logger.debug("MATCH, [MATCH] read-back value matches expected")
			else:
				self.logger.info(f"REGISTER_ERROR, [MISMATCH] Expected 0x{result:08X} but got 0x{item_in.data:08X}")