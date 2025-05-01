"""
Author : Amr El Batarny
File   : Tests.py
Brief  : Defines test cases for verifying the functionality of the APB slave using the testbench.
"""

import vsc
import cocotb
import pyuvm
from pyuvm import uvm_test, uvm_factory
from pyuvm import ConfigDB
from Environment		import ApbEnv
from SequenceLibrary	import (
    ApbBaseSequence,
    ApbWriteSequence,
    ApbReadSequence,
    ApbTestAllSequence,
    ApbRegSequence,
)
from BFM				import ApbBfm


class ApbBaseTest(uvm_test):
	def build_phase(self):
		vsc.vsc_solvefail_debug(1)
		self.env = ApbEnv.create("env", self)

	def end_of_elaboration_phase(self):
		self.seq = ApbBaseSequence.create("seq")

	def start_of_simulation_phase(self):
		self.bfm = ApbBfm()
		self.logger.info(f"==================== Start of {self.get_type_name()} ====================")

	async def run_phase(self):
		self.raise_objection()

		# Clock generation
		await self.bfm.generate_clock()

		# Starting the sequence
		self.logger.info(f"{self.get_type_name()}, Starting sequence, {self.seq.get_type_name()}")
		await self.seq.start(self.env.agt.sqr)
		self.logger.info(f"{self.get_type_name()}, Finished sequence, {self.seq.get_type_name()}")

		self.drop_objection()

	def final_phase(self):
		uvm_factory().print(0)
		self.logger.info(f"==================== End of {self.get_type_name()} ====================")
		
# @pyuvm.test()
class ApbWriteTest(ApbBaseTest):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbWriteSequence)
		super().build_phase()

# @pyuvm.test()
class ApbReadTest(ApbBaseTest):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbReadSequence)
		super().build_phase()

# @pyuvm.test()
class ApbTestAllTest(ApbBaseTest):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbTestAllSequence)
		ConfigDB().set(None, "*", "ENABLE_SV_RANDOMIZATION", True)
		ConfigDB().set(None, "*", "ENABLE_SV_COVERAGE", True)
		ConfigDB().set(None, "*", "NUM_TRANSACTIONS", 300)
		super().build_phase()
	
@pyuvm.test(stage=1)
class ApbRegTest(ApbBaseTest):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbRegSequence)
		ConfigDB().set(None, "*", "ENABLE_SV_COVERAGE", True)
		super().build_phase()