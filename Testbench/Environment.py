"""
Author : Amr El Batarny
File   : Environment.py
Brief  : Top-level UVM environment composing agent, scoreboard, and coverage for APB.
"""

import sys
# Add the RAL directory to sys.path
directory_path = "../RAL"
sys.path.append(directory_path)
from pyuvm import (
    uvm_env,
    ConfigDB,
)
from pyuvm import uvm_factory, UVMConfigItemNotFound, UVMFatalError

from Agent          import ApbAgent
from Coverage       import ApbCoverage
from Scoreboard     import ApbScoreboard
from Adapter        import ApbRegAdapter
from RegisterBlock  import ApbRegBlock
from SequenceItemVSC import ApbSeqItemVSC
from SequenceItemCR import ApbSeqItemCR
from SequenceItemCCVG import ApbSeqItemCCVG


class ApbEnv(uvm_env):

	def build_phase(self):
		try:
			self.sv_coverage_en 	= ConfigDB().get(self, "", "ENABLE_SV_COVERAGE")
			self.vsc_coverage_en 	= ConfigDB().get(self, "", "ENABLE_VSC_COVERAGE")
			self.sv_rand_en 		= ConfigDB().get(self, "", "ENABLE_SV_RANDOMIZATION")
			self.vsc_rand_en 		= ConfigDB().get(self, "", "ENABLE_VSC_RANDOMIZATION")
			self.cr_rand_en 		= ConfigDB().get(self, "", "ENABLE_CR_RANDOMIZATION")
			self.ccvg_rand_en 		= ConfigDB().get(self, "", "ENABLE_CCVG_RANDOMIZATION")
		except UVMConfigItemNotFound:
			self.sv_coverage_en 	= False
			self.vsc_coverage_en 	= False
			self.vsc_rand_en 		= False
			self.cr_rand_en 		= False
			self.ccvg_rand_en 		= False

		# Exactly one mode must be true
		if	 self.sv_rand_en:
			# Bypass Python-side randomization
			pass
		elif self.vsc_rand_en and not self.cr_rand_en and not self.ccvg_rand_en:
			# Default: using ApbSeqItemVSC, no override needed
			pass
		elif not self.vsc_rand_en and self.cr_rand_en and not self.ccvg_rand_en:
			# Override VSC item with constrainedrandom item
			uvm_factory().set_type_override_by_type(ApbSeqItemVSC, ApbSeqItemCR)
		elif not self.vsc_rand_en and not self.cr_rand_en and self.ccvg_rand_en:
			# Override VSC item with cocotb-coverage CRV item
			uvm_factory().set_type_override_by_type(ApbSeqItemVSC, ApbSeqItemCCVG)
		else:
			# Invalid combination: must choose exactly one
			raise UVMFatalError(
				f"{self.get_type_name()}: "
				"Exactly one randomization mode must be enabled "
				"(VSC, CR, or CCVG). "
				"Please check your ConfigDB settings."
				)

		self.agt = ApbAgent.create("agt", self)

		# Only create the PyVSC coverage component when SV-based coverage is disabled
		if self.sv_coverage_en == False:
			if self.vsc_coverage_en == True:
				self.logger.info("Building coverage component")
				self.cvg = ApbCoverage.create("cvg", self)

		self.sb = ApbScoreboard.create("sb", self)
		self.adapter = ApbRegAdapter("adapter")
		self.block = ApbRegBlock("block")

		# Share RAL across the TB if needed
		ConfigDB().set(None, "*", "REGISTER_MODEL", self.block)

	def connect_phase(self):
		# self.agt.agt_ap.connect(self.cvg.cov_export)
		self.agt.agt_ap.connect(self.sb.analysis_export)
		if self.sv_coverage_en == False:
			if self.vsc_coverage_en == True:
				self.agt.agt_ap.connect(self.cvg.analysis_export)
		self.block.def_map.set_sequencer(self.agt.sqr)
		self.block.def_map.set_adapter(self.adapter)
		# self.sb.ral = self.block