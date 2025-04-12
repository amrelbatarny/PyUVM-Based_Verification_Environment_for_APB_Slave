# © 2022 Siemens.

#  This material may only be used with products of Siemens Industry Software Inc.
#  or its affiliates, and for no other purpose.

# If you have a signed license agreement with Siemens for the product with which
# this Software will be used, your use of this Software is subject to the scope of
# license and the software protection and security provisions of that agreement.
# If you do not have such a signed license agreement, your use is subject to the
# Siemens Universal Customer Agreement, which may be viewed at
# https://www.sw.siemens.com/en-US/sw-terms/base/uca/, as supplemented by the
# electronic design automation (EDA) specific terms which may be viewed at
# https://www.sw.siemens.com/en-US/sw-terms/supplements/.

# NOTWITHSTANDING ANYTHING TO THE CONTRARY IN YOUR SIGNED LICENSE AGREMENT WITH
# SISW OR THE SISW END USER LICENSE AGREEMENT, THIS SOFTWARE IS BEING PROVIDED “AS
# IS;” SISW MAKES NO WARRANTY OF ANY KIND WITH REGARD TO THIS SOFTWARE INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE, AND NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. SISW SHALL
# NOT BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, CONSEQUENTIAL OR PUNITIVE
# DAMAGES, LOST DATA OR PROFITS, EVEN IF SUCH DAMAGES WERE FORESEEABLE, ARISING
# OUT OF OR RELATED TO THIS SOFTWARE OR THE INFORMATION CONTAINED IN IT, EVEN IF
# SISW HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

# Unless agreed in writing, SISW has no obligation to support or otherwise
# maintain this Software.

from protlib import CStruct
import ctypes
import pathlib


class SVStruct:
    def unpack_byte_data(self, byte_arr):
        byte_str = byte_arr.decode('utf-8')
        byte_data = bytearray.fromhex(byte_str)
        return byte_data


class SVConduitData(CStruct, SVStruct):
    """Data to and from SystemVerilog"""
    ...


class SVConduit:
    try:
        c_lib = ctypes.CDLL(pathlib.Path().absolute() / "sv_conduit.so")
    except OSError:
        c_lib = None

    def __pkg_path(data_class):
        pkg_str = data_class.__name__+"_pkg"
        pkg_path = ctypes.c_char_p(pkg_str.encode("utf-8"))
        return pkg_path

    @classmethod
    def get(cls, data_class):
        cls.c_lib.get.restype = ctypes.c_char_p
        obj_str = cls.c_lib.get(cls.__pkg_path(data_class))
        obj = data_class()
        obj.load_sv_str(obj_str)
        return obj

    @classmethod
    def put(cls, obj):
        cls.c_lib.put(cls.__pkg_path(type(obj)), obj.serialize())
        return None

    @classmethod
    def transport(cls, obj):
        cls.c_lib.transport.restype = ctypes.c_char_p
        obj_str = cls.c_lib.transport(cls.__pkg_path(type(obj)), obj.serialize())
        new_obj = type(obj)()
        new_obj.load_sv_str(obj_str)
        return new_obj
