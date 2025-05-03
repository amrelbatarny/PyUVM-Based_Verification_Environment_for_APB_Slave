"""
Author : Amr El Batarny
File   : Tests.py
Brief  : Defines test cases for verifying the functionality of the APB slave using the testbench.
"""

# ----------------------------------------------------------------------------
# Configuration Parameters (via ConfigDB)
#
# NUM_TRANSACTIONS       : integer  
#   – Number of APB transactions each sequence should generate.
#
# ENABLE_SV_RANDOMIZATION: bool  
#   – If True, *all* sequences bypass Python-side randomization and
#     call SVConduit.get() to retrieve randomized items from SystemVerilog.
#   – Overrides any VSC/CR/CCVG randomization flags; only one mode allowed.
#
# ENABLE_VSC_RANDOMIZATION: bool  
#   – If True (and all other randomization flags False), sequences use
#     PyVSC’s randomize() on ApbSeqItemVSC.
#
# ENABLE_CR_RANDOMIZATION : bool  
#   – If True (and all other randomization flags False), sequences use
#     constrainedrandom on ApbSeqItemCR.
#
# ENABLE_CCVG_RANDOMIZATION: bool  
#   – If True (and all other randomization flags False), sequences use
#     cocotb-coverage CRV on ApbSeqItemCCVG.
#
# ENABLE_SV_COVERAGE      : bool  
#   – If True, the monitor invokes SVConduit.put() to sample coverage
#     in SystemVerilog (sv_put). The PyVSC coverage component is not built.
#
# ENABLE_VSC_COVERAGE     : bool  
#   – If True (and SV coverage False), the PyVSC-based coverage subscriber
#     (ApbCoverage) is instantiated and receives transactions via the
#     analysis port. SVConduit.put() is not used.
#
# Notes:
#   * Exactly one randomization mode flag (SV, VSC, CR, or CCVG) must be True.
#   * Coverage flags are independent: you may enable either SV or VSC coverage,
#     but not both simultaneously.
# ----------------------------------------------------------------------------

import vsc
import cocotb
import pyuvm
from pyuvm import uvm_test, uvm_factory
from pyuvm import ConfigDB
from Environment		import ApbEnv
from SequenceItemVSC	import ApbSeqItemVSC
from SequenceItemCR		import ApbSeqItemCR
from SequenceItemCCVG import ApbSeqItemCCVG
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
		self.logger.info(f"================================ Start of {self.get_type_name()} ================================")

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
		self.logger.info(f"================================ End of {self.get_type_name()} ================================")
		
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
		# Override with the TestAll sequence
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbTestAllSequence)
		
		# Test Configuration (You can read the descriptions in the top for details)
		ConfigDB().set(None, "*", "NUM_TRANSACTIONS", 5)
		ConfigDB().set(None, "*", "ENABLE_SV_RANDOMIZATION", False)
		ConfigDB().set(None, "*", "ENABLE_VSC_RANDOMIZATION", False)
		ConfigDB().set(None, "*", "ENABLE_CR_RANDOMIZATION", True)
		ConfigDB().set(None, "*", "ENABLE_CCVG_RANDOMIZATION", False)
		ConfigDB().set(None, "*", "ENABLE_SV_COVERAGE", False)
		ConfigDB().set(None, "*", "ENABLE_VSC_COVERAGE", False)

		super().build_phase()
	
# @pyuvm.test(stage=1)
class ApbRegTest(ApbBaseTest):
	
	def build_phase(self):
		uvm_factory().set_type_override_by_type(ApbBaseSequence, ApbRegSequence)
		ConfigDB().set(None, "*", "ENABLE_SV_COVERAGE", True)
		super().build_phase()