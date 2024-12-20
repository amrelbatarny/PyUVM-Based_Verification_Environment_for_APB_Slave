from common_imports import *
from APB_env import *
from APB_sequence import *

@pyuvm.test()
class APB_TestAll_test(uvm_test):

	def build_phase(self):
		self.env = APB_env.create("env", self)

	def end_of_elaboration_phase(self):
		self.seq = APB_TestAll_sequence.create("seq")

	async def run_phase(self):
		self.raise_objection()

		# Clock generation
		c = Clock(cocotb.top.PCLK, 2, 'ps')
		await cocotb.start(c.start())

		# Starting the sequence
		self.logger.info(f"{self.get_type_name()}, Starting sequence, {self.seq.get_type_name()}")
		await self.seq.start(self.env.agt.sqr)
		self.logger.info(f"{self.get_type_name()}, Finished sequence, {self.seq.get_type_name()}")

		self.drop_objection()

	def final_phase(self):
		uvm_factory().print(0)

@pyuvm.test()
class APB_write_test(APB_TestAll_test):

	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_TestAll_sequence, APB_write_sequence)
		super().build_phase()

@pyuvm.test()
class APB_read_test(APB_TestAll_test):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_TestAll_sequence, APB_read_sequence)
		super().build_phase()

# @pyuvm.test()
class APB_reg_test(APB_TestAll_test):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(APB_TestAll_sequence, APB_reg_sequence)
		super().build_phase()