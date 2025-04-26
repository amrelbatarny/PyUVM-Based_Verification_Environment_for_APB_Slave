import sys
# Add the RAL directory to sys.path
directory_path = "../RAL"
sys.path.append(directory_path)
from pyuvm import (
    uvm_env,
    ConfigDB,
)
from Agent          import ApbAgent
from Coverage       import ApbCoverage
from Scoreboard     import ApbScoreboard
from Adapter        import ApbRegAdapter
from RegisterBlock  import ApbRegBlock


class ApbEnv(uvm_env):

	def build_phase(self):
		self.agt = ApbAgent.create("agt", self)
		self.cvg = ApbCoverage.create("cvg", self)
		self.sb = ApbScoreboard.create("sb", self)
		self.adapter = ApbRegAdapter("adapter")
		self.block = ApbRegBlock("block")

	def connect_phase(self):
		# self.agt.agt_ap.connect(self.cvg.cov_export)
		self.agt.agt_ap.connect(self.sb.analysis_export)
		self.agt.agt_ap.connect(self.cvg.analysis_export)
		self.block.def_map.set_sequencer(self.agt.sqr)
		self.block.def_map.set_adapter(self.adapter)
		self.sb.ral = self.block
		ConfigDB().set(None, "*", "SQR", self.agt.sqr) # share SEQR and RAL across the TB if needed
		ConfigDB().set(None, "*", "regsiter_model", self.block)