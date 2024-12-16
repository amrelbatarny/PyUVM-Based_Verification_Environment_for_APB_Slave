from common_imports import *
from APB_driver import *
from APB_monitor import *
from APB_seq_item import *

class APB_agent(uvm_agent):

	def build_phase(self):
		self.sqr = uvm_sequencer("sqr", self)
		self.drv = APB_driver.create("drv", self)
		self.mon = APB_monitor.create("mon", self)
		self.agt_ap = uvm_analysis_port.create("agt_ap", self)

	def connect_phase(self):
		self.drv.seq_item_port.connect(self.sqr.seq_item_export)
		self.mon.mon_ap.connect(self.agt_ap)