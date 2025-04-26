from protlib import *
from pyquesta import SVStruct


class APB_seq_item(CStruct, SVStruct):
    addr = CUInt(default=0)
    data = CUInt(default=0)
    strobe = CUChar(default=0)
    type_sv = CUChar(default=0)

    def load_sv_str(self, byte_str):
        byte_data = self.unpack_byte_data(byte_str)
        self.addr = int.from_bytes(byte_data[0:4], byteorder='big', signed=False)
        self.data = int.from_bytes(byte_data[4:8], byteorder='big', signed=False)
        self.strobe = int.from_bytes(byte_data[8:9], byteorder='big', signed=False)
        self.type_sv = int.from_bytes(byte_data[9:10], byteorder='big', signed=False)

    def __eq__(self, other):
        same = True \
            and self.addr == other.addr \
            and self.data == other.data \
            and self.strobe == other.strobe \
            and self.type_sv == other.type_sv \
            and True
        return same

    def serialize(self):
        # 4+4+1+1 = 10 bytes; format each field as hex:
        #   addr   → 8 digits
        #   data   → 8 digits
        #   strobe → 2 digits
        #   type_sv   → 2 digits
        s = (
            f"{self.addr:08x}"
            f"{self.data:08x}"
            f"{self.strobe:02x}"
            f"{self.type_sv:02x}"
        )
        return s.encode('utf-8')

