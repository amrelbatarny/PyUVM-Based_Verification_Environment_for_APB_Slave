from common_imports import *
from APB_agent import *
from APB_reg_adapter import *
from APB_reg_block import *

class APB_env(uvm_env):

	def build_phase(self):
		self.agt = APB_agent.create("agt", self)
		self.reg_adapter = APB_reg_adapter("reg_adapter")
		self.reg_block   = APB_reg_block("reg_block")

	def connect_phase(self):
		self.reg_block.def_map.set_sequencer(self.agt.sqr)
		self.reg_block.def_map.set_adapter(self.reg_adapter)
		# share SEQR and RAL across the TB if needed
		ConfigDB().set(None, "*", "SQR", self.agt.sqr)
		ConfigDB().set(None, "*", "regsiter_model", self.reg_block)