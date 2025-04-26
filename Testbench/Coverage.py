import vsc
from vsc import (
	covergroup,
	uint32_t,
	bit_t,
	enum_t,
	coverpoint,
	cross,
	bin as vsc_bin,
	report_coverage,
	write_coverage_db,
)
from pyuvm import (
	uvm_subscriber,
	uvm_tlm_analysis_fifo,
	uvm_get_port,
)
from APB_utils import APBType # your APBType enum

@vsc.covergroup
class ApbCoverGroup(object):
	def __init__(self):
		self.with_sample(
			addr=vsc.uint32_t(),
			data=vsc.uint32_t(),
			strobe=vsc.bit_t(4),
			type=vsc.enum_t(APBType)
		)

		# Transfer type coverage
		self.type_cp = vsc.coverpoint(self.type, bins=dict(
			read=vsc.bin(APBType.READ),
			write=vsc.bin(APBType.WRITE)
		))

		# Address coverage - 16 possible addresses (0x0 to 0x3C in steps of 4)
		addr_values = [i*4 for i in range(16)]
		self.addr_cp = vsc.coverpoint(self.addr, bins=dict(
			[(f"address_{hex(address)}", vsc.bin(address)) for address in addr_values]
		))

		# Write data coverage (corrected range specification)
		self.data_cp = vsc.coverpoint(self.data, bins=dict(
			zero=vsc.bin(0),
			all_ones=vsc.bin(0xFFFFFFFF)
		))

		# Cross coverage between key signals
		self.cross_rw_addr  = vsc.cross([self.type_cp, self.addr_cp])
		self.cross_rw_wdata = vsc.cross([self.type_cp, self.data_cp])

class ApbCoverage(uvm_subscriber):
	def build_phase(self):
		self.cg = ApbCoverGroup()

	def write(self, item):
		self.cg.sample(
					item.addr,
					item.data,
					item.strobe,
					item.type
				)
		self.logger.debug(f"{self.get_type_name()}: SAMPLED {item}")
		self.logger.debug(f"Instance Coverage = {self.cg.get_inst_coverage()}")

	def report_phase(self):
		self.logger.info("cg total coverage=%f" % (self.cg.get_coverage()))
		vsc.report_coverage(details=False)
		vsc.write_coverage_db(filename="../Coverage_Reports/Exported_by_PyVSC/apb_coverage.xml",  fmt='xml',      libucis=None)
		vsc.write_coverage_db(filename="../Coverage_Reports/Exported_by_PyVSC/apb_coverage.ucdb", fmt='libucis',  libucis="/home/amrelbatarny/QuestaSim/questasim/linux_x86_64/libucis.so")