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
    ApbPyquestaSequence,
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

@pyuvm.test()
class ApbTestAllTest(ApbBaseTest):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbTestAllSequence)
		ConfigDB().set(None, "*", "ENABLE_SV_RANDOMIZATION", True)
		ConfigDB().set(None, "*", "ENABLE_SV_Coverage", True)
		ConfigDB().set(None, "*", "NUM_TRANSACTIONS", 300)
		super().build_phase()
	
# @pyuvm.test(stage=1)
class ApbRegTest(ApbBaseTest):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbRegSequence)
		super().build_phase()


# Cocotb entry point coroutine
# @cocotb.test()
# async def run_uvm_test(dut):
#     test_name = cocotb.plusargs["UVM_TEST"]
#     await uvm_root().run_test(test_name)
#     # Add coverage save after test completes
#     await Timer(100, units="ns")  # Allow final operations
#     dut._log.info("Saving coverage...")
#     await cocotb.decorators.RunningTask.await_tasks()

# # Pytest parameterized test function
# @pytest.mark.parametrize("uvm_test", [
#     "APB_write_test",
#     "APB_read_test", 
#     "APB_TestAll_test"
# ])
# APB_test.py (revised)