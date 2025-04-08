from common_imports import *
from APB_seq_item_vsc import *

@vsc.covergroup
class APBCoverGroup(object):
    def __init__(self):
        self.with_sample(
            PRESETn=vsc.bit_t(1),
            PWRITE=vsc.bit_t(1),
            PENABLE=vsc.bit_t(1),
            PREADY=vsc.bit_t(1),
            PADDR=vsc.uint32_t(),
            PWDATA=vsc.uint32_t(),
            PRDATA=vsc.uint32_t()
        )

        # Reset state coverage
        self.cp_preset = vsc.coverpoint(self.PRESETn, bins=dict(
            reset_active=vsc.bin(0),
            reset_inactive=vsc.bin(1)
        ))

        # Transfer type coverage
        self.cp_pwrite = vsc.coverpoint(self.PWRITE, bins=dict(
            read=vsc.bin(0),
            write=vsc.bin(1)
        ))

        # Enable signal coverage
        self.cp_penable = vsc.coverpoint(self.PENABLE, bins=dict(
            enabled=vsc.bin(1),
            disabled=vsc.bin(0)
        ))

        # Address coverage - 16 possible addresses (0x0 to 0x3C in steps of 4)
        addr_values = [i*4 for i in range(16)]
        self.cp_paddr = vsc.coverpoint(self.PADDR, bins=dict(
            [(f"addr_{hex(addr)}", vsc.bin(addr)) for addr in addr_values]
        ))

        # Write data coverage (corrected range specification)
        self.cp_pwdata = vsc.coverpoint(self.PWDATA, bins=dict(
            zero=vsc.bin(0),
            all_ones=vsc.bin(0xFFFFFFFF)
        ))

        # Cross coverage between key signals
        self.cross_rw_addr  = vsc.cross([self.cp_pwrite, self.cp_paddr])
        self.cross_rw_wdata = vsc.cross([self.cp_pwrite, self.cp_pwdata])

class APB_coverage(uvm_component):
    def build_phase(self):
        self.cov_fifo = uvm_tlm_analysis_fifo("cov_fifo", self)
        self.cov_get_port = uvm_get_port("cov_get_port", self)
        self.cov_export = self.cov_fifo.analysis_export
        self.cg = APBCoverGroup()

    def connect_phase(self):
        self.cov_get_port.connect(self.cov_fifo.get_export)

    async def run_phase(self):
        while True:
            try:
                item = await self.cov_get_port.get()
                self.cg.sample(
                    item.PRESETn,
                    item.PWRITE,
                    item.PENABLE,
                    item.PREADY,
                    item.PADDR,
                    item.PWDATA,
                    item.PRDATA
                )
                self.logger.debug(f"{self.get_type_name()}: SAMPLED {item}")
                self.logger.debug(f"Instance Coverage = {self.cg.get_inst_coverage()}")
            except Exception as e:
                pass

    def report_phase(self):
        self.logger.info("cg total coverage=%f" % (self.cg.get_coverage()))
        vsc.report_coverage(details=False)
        vsc.write_coverage_db(filename="../Coverage_Reports/Exported_by_PyVSC/apb_coverage.xml",  fmt='xml',      libucis=None)
        vsc.write_coverage_db(filename="../Coverage_Reports/Exported_by_PyVSC/apb_coverage.ucdb", fmt='libucis',  libucis="/home/amrelbatarny/QuestaSim/questasim/linux_x86_64/libucis.so")