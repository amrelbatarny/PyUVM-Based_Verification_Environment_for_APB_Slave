"""
Author : Amr El Batarny
File   : SequenceItemVSC.py
Brief  : Defines the APB sequence item class representing individual APB transactions and uses PyVSC for CRV.
"""

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
class ApbSeqItemVSC(uvm_sequence_item):
	"""
	PyVSC version of the APB sequence item.
	Fields:
	  - type   : APBType enum (READ or WRITE)
	  - addr   : 32-bit address, aligned on 4B, [0x00–0x3C]
	  - data   : 32-bit data
	  - strobe : 4-bit byte-enable mask
	"""

	def __init__(self, name):
		super().__init__(name)
		self.type   = vsc.rand_enum_t(APBType)
		self.addr   = vsc.rand_bit_t(32)
		self.data   = vsc.rand_bit_t(32)
		self.strobe = vsc.rand_bit_t(4)

		self.tmp	= vsc.rand_bit_t(29)
		self.sq		= vsc.rand_bit_t(16)
		self.root	= vsc.rand_bit_t(16)

	@vsc.constraint
	def complex_c(self):
		# Choose two thresholds
		A = 0x1000
		B = 0x8000

		# Branch 1: data < A → use tmp
		with vsc.if_then(self.data < A):
			self.data == self.tmp * 3 + 5

		# Branch 2: A ≤ data < B
		with vsc.else_if(self.data < B):
			self.sq * self.sq - 7 == self.data and self.root * self.root == self.data + 7

		# Branch 3: data ≥ B
		with vsc.else_then:
			self.data % 12345 == 0

	@vsc.constraint
	def strobe_dist(self):
		vsc.dist(self.strobe, [
			vsc.weight(1,  10), vsc.weight(2,  10), vsc.weight(3,  10),
			vsc.weight(4,  10), vsc.weight(5,  10),  # 1–5 @10
			vsc.weight(6,  20), vsc.weight(7,  20), vsc.weight(8,  20),
			vsc.weight(9,  20), vsc.weight(10, 20),  # 6–10 @20
			vsc.weight(11, 70), vsc.weight(12, 70), vsc.weight(13, 70), vsc.weight(14, 70),  # 11–14 @70
			vsc.weight(15, 90)  # 15 @90
		])
			
	@vsc.constraint
	def addr_constraints(self):
		# Address aligned to 4 and within the allowed range
		self.addr.inside(vsc.rangelist(vsc.rng(0x00000000, 0x0000003C + 1)))
		self.addr % 4 == 0

	# Override do_copy() to perform deep copying
	def do_copy(self, rhs):
		super().do_copy(rhs)
		self.addr   = rhs.addr
		self.data   = rhs.data
		self.strobe = rhs.strobe
		self.type   = rhs.type

	def __str__(self):
		return (
			f"\nName:	{self.get_full_name()}"
			f"\nADDR:	{self.addr}"
			f"\nDATA: 	{self.data}"
			f"\nSTROBE:	{self.strobe}"
			f"\nTYPE:	{self.type.name}"
		)