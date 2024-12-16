# Makefile

# defaults
GUI=1
WAVES=1
SIM ?= questa
TOPLEVEL_LANG ?= verilog
 
VERILOG_SOURCES += $(PWD)/../RTL//shared_pkg.sv $(PWD)/../RTL//APB_Wrapper.sv $(PWD)/../RTL//APB_Slave.sv $(PWD)/../RTL//RegisterFile.sv
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = APB_Wrapper
 
# MODULE is the basename of the Python test file
MODULE = APB_test
 
# SCRIPT_FILE := setup.tcl
 
include $(shell cocotb-config --makefiles)/Makefile.sim