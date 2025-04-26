import vsc
from vsc import (
	randobj,
	constraint,
	if_then,
	rand_bit_t,
	rand_enum_t,
	rangelist,
	rng,
)

from pyuvm import uvm_sequence_item
from APB_utils import APBType
	
@vsc.randobj
class ApbSeqItem(uvm_sequence_item):
	def __init__(self, name):  
		super().__init__(name)
		self.addr   = vsc.rand_bit_t(32)
		self.data   = vsc.rand_bit_t(32)
		self.strobe = vsc.rand_bit_t(4)
		self.type   = vsc.rand_enum_t(APBType)

	@vsc.constraint
	def data_for_reads(self):
		# Data field ignored on READ transactions
		with vsc.if_then(self.type == APBType.READ):
			self.data == 0

	@vsc.constraint
	def strobe_behavior(self):
		# On READ transactions, force strobe to 0
		with vsc.if_then(self.type == APBType.READ):
			self.strobe == 0

		# On WRITE transactions, apply the distribution
		with vsc.else_then:
			self.strobe == 15


	@vsc.constraint
	def addr_constraints(self):
		# Address aligned to 4 and within the allowed range
		self.addr.inside(vsc.rangelist(vsc.rng(0x00000000, 0x0000003C + 1)))
		self.addr % 4 == 0

	def __str__(self):
		return (
			f"\nName: {self.get_full_name()}"
			f"\nADDR: {self.addr}"
			f"\nDATA: {self.data}"
			f"\nTYPE: {self.type.name}"
		)