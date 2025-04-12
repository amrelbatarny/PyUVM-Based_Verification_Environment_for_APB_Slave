from protlib import *
from pyquesta import SVStruct


class APB_seq_item(CStruct, SVStruct):
    PRESETn = CUInt(default=0)
    PWDATA = CUInt(default=0)
    PENABLE = CUInt(default=0)
    PWRITE = CUInt(default=0)
    PADDR = CUInt(default=0)

    def load_sv_str(self, byte_str):
        byte_data = self.unpack_byte_data(byte_str)
        self.PRESETn = int.from_bytes(byte_data[0:4], byteorder='big', signed=False)
        self.PWDATA = int.from_bytes(byte_data[4:8], byteorder='big', signed=False)
        self.PENABLE = int.from_bytes(byte_data[8:12], byteorder='big', signed=False)
        self.PWRITE = int.from_bytes(byte_data[12:16], byteorder='big', signed=False)
        self.PADDR = int.from_bytes(byte_data[16:20], byteorder='big', signed=False)

    def __eq__(self, other):
        same = True \
            and self.PRESETn == other.PRESETn \
            and self.PWDATA == other.PWDATA \
            and self.PENABLE == other.PENABLE \
            and self.PWRITE == other.PWRITE \
            and self.PADDR == other.PADDR \
            and True
        return same
