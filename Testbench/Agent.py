"""
Author : Amr El Batarny
File   : Agent.py
Brief  : Implements the APB agent, integrating the driver, monitor, and sequencer components for the verification environment.
"""

from pyuvm import (
    uvm_agent,
    uvm_sequencer,
    uvm_analysis_port,
    ConfigDB,
)
from Driver import ApbDriver
from Monitor import ApbMonitor

class ApbAgent(uvm_agent):

	def build_phase(self):
		self.sqr = uvm_sequencer("sqr", self)
		self.drv = ApbDriver.create("drv", self)
		self.mon = ApbMonitor.create("mon", self)
		self.agt_ap = uvm_analysis_port.create("agt_ap", self)

		# share SEQR across the TB if needed
		ConfigDB().set(None, "*", "SQR", self.sqr)

	def connect_phase(self):
		self.drv.seq_item_port.connect(self.sqr.seq_item_export)
		self.mon.mon_ap.connect(self.agt_ap)