"""
File   : SequenceLibrary.py
Author : Amr El Batarny
Brief  : Contains various APB sequences for generating different types of APB transactions during simulation.
"""

import cocotb
import vsc
from cocotb.triggers import RisingEdge, FallingEdge
from pyuvm import uvm_sequence, uvm_report_object, ConfigDB, uvm_root, path_t, check_t
from SequenceItem import ApbSeqItem
from APB_seq_itemMod import APB_seq_item
from pyquesta import SVConduit
from APB_utils import APBType

class ApbBaseSequence(uvm_sequence, uvm_report_object):
	
	def seq_print(msg: str):
		uvm_root().logger.info(msg)

	def __init__(self, name="ApbBaseSequence"):
		super().__init__(name)
		self.ral = ConfigDB().get(None, "", "regsiter_model")
		self.map = self.ral.def_map
	
	async def pre_body(self):
		print("Entered pre_body")
		self.item = ApbSeqItem.create("item")

	async def body(self):
		raise UVMNotImplemented  


##############################################################################
# Specialized APB Test Sequences
##############################################################################

class ApbTestAllSequence(ApbBaseSequence):

	async def body(self):
		for _ in range(100):
			await self.start_item(self.item)
			self.item.randomize()
			await self.finish_item(self.item)

class ApbWriteSequence(ApbBaseSequence):

	async def body(self):
		for _ in range(100):
			await self.start_item(self.item)
			with self.item.randomize_with() as it:
				vsc.dist(it.type, [
					vsc.weight(APBType.WRITE, 95),
					vsc.weight(APBType.READ, 5)
					])
			await self.finish_item(self.item)

class ApbReadSequence(ApbBaseSequence):

	async def body(self):
		for _ in range(100):
			await self.start_item(self.item)
			with self.item.randomize_with() as it:
				vsc.dist(it.type, [
					vsc.weight(APBType.WRITE, 5),
					vsc.weight(APBType.READ, 95)
					])
			await self.finish_item(self.item)

class ApbPyquestaSequence(ApbBaseSequence):

	async def body(self):
		for _ in range(300):
			item_sv = SVConduit.get(APB_seq_item)
			await self.start_item(self.item)
			self.item.data = item_sv.data
			self.item.type = APBType.WRITE if item_sv.type_sv else APBType.READ
			self.item.addr = item_sv.addr
			self.item.strobe = item_sv.strobe
			await self.finish_item(self.item)

class ApbRegSequence(ApbBaseSequence):

	async def body(self):
		status = await self.ral.reg_INPUT_DATA_REG.write(0x1F2C9A0D, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_DMA_CTRL_REG.write(0xF1C3422A, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_INT_CTRL_REG.write(0xABCDEF12, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_DEV_ID_REG.write(0x34578967, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_ADC_CTRL_REG.write(0x78954806, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_VOLTAGE_CTRL_REG.write(0x2347AEBC, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_TEMP_SENSOR_REG.write(0x218390FA, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_DAC_OUTPUT_REG.write(0x908CD2AB, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_SYS_STATUS_REG.write(0x12345678, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_CLK_CONFIG_REG.write(0x15A4B8CD, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_DBG_CTRL_REG.write(0xEA5B7C12, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)
		status = await self.ral.reg_OUTPUT_DATA_REG.write(0xC9D287A3, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)

		await RisingEdge(cocotb.top.PCLK)
		
		# self.ral.reg_ADC_CTRL_REG.ADC_READY.field_set(0xAB)
		# whole_reg_value = self.ral.reg_ADC_CTRL_REG.get_desired()
		# status = await self.ral.reg_ADC_CTRL_REG.write(whole_reg_value, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)

		# status = await self.ral.reg_MEM_CTRL_REG.write(0xFD12AB45, self.map, path_t.FRONTDOOR, check_t.NO_CHECK)