from common_imports import *
from APB_env import *
from APB_sequence import *
from APB_bfm import *

class APB_base_test(uvm_test):
	def build_phase(self):
		vsc.vsc_solvefail_debug(1)
		self.env = APB_env.create("env", self)

	def end_of_elaboration_phase(self):
		self.seq = APB_base_sequence.create("seq")

	def start_of_simulation_phase(self):
		self.bfm = APB_bfm()

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
		self.logger.info("----------------------------------------------------------------------")
		self.logger.info(f"End of {self.get_type_name()}")
		self.logger.info("----------------------------------------------------------------------")

# @pyuvm.test()
class APB_write_test(APB_base_test):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_base_sequence, APB_write_sequence)
		super().build_phase()

# @pyuvm.test()
class APB_read_test(APB_base_test):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_base_sequence, APB_read_sequence)
		super().build_phase()

# @pyuvm.test()
class APB_TestAll_test(APB_base_test):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_base_sequence, APB_TestAll_sequence)
		super().build_phase()

@pyuvm.test()
class APB_pyquesta_test(APB_base_test):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_base_sequence, APB_pyquesta_sequence)
		super().build_phase()

# @pyuvm.test()
class APB_reg_test(APB_base_test):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_base_sequence, APB_reg_sequence)
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
