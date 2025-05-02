"""
Author : Amr El Batarny
File   : SequenceItemCR.py
Brief  : Defines the APB sequence item class representing individual APB transactions and uses Constrainedrandom for CRV.
"""

from constrainedrandom import RandObj
from enum import IntEnum
from pyuvm import uvm_sequence_item
from APB_utils import APBType

class ApbSeqItemCR(uvm_sequence_item, RandObj):
	"""
	Constrainedrandom version of the APB sequence item.
	Fields:
	  - type   : APBType enum (READ or WRITE)
	  - addr   : 32-bit address, aligned on 4B, [0x00–0x3C]
	  - data   : 32-bit data
	  - strobe : 4-bit byte-enable mask
	"""

	def __init__(self, name):
		super().__init__(name)
		RandObj.__init__(self)

		# stype: either READ or WRITE
		self.add_rand_var('type',domain=list(APBType), order=0)
		# addr: 0x0,4,8,…,0x3C
		self.add_rand_var('addr', domain=list(range(0x00, 0x40, 4)), order=3)
		# data: 32-bit
		self.add_rand_var('data', bits=32, order=1)
		# strobe: 4-bit
		self.add_rand_var('strobe', bits=4, order=2)

		self.add_rand_var('tmp',  bits=29)
		self.add_rand_var('sq',   bits=16)
		self.add_rand_var('root', bits=16)

		# data==0 when READ, else no constraint
		def data_for_reads(txn_type, data):
			return data == 0 if txn_type == APBType.READ else True
		self.add_constraint(data_for_reads, ('type', 'data'))

		# strobe==0 when READ, else no constraint (random on WRITE)
		def strobe_for_reads(txn_type, strobe):
			return strobe == 0 if txn_type == APBType.READ else True
		self.add_constraint(strobe_for_reads, ('type', 'strobe'))

		def complex_c(data, tmp, sq, root):
			A, B = 0x1000, 0x8000
			if data < A:
				return data == 3*tmp + 5
			elif data < B:
				return sq*sq - 7 == data and root*root == data+7
			else:
				return data % 12345 == 0
		self.add_constraint(complex_c, ('data','tmp','sq','root'))


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