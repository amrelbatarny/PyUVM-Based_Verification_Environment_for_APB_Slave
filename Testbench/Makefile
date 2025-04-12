# Makefile

# Force GUI mode and export variables
GUI = 1
WAVES = 1
SIM ?= questa
TOPLEVEL_LANG ?= verilog

# RTL Files 
VERILOG_SOURCES += ../RTL/shared_pkg.sv ../RTL/APB_Wrapper.sv ../RTL/APB_Slave.sv ../RTL/RegisterFile.sv
VERILOG_SOURCES += APB_SVA.sv SVA_bind.sv
VERILOG_SOURCES += APB_seq_item_pkg.sv APB_seq_item.svh

# Ensure Questa finds all files
VLOG_ARGS += +incdir+$(PWD)

# Top-level and module
TOPLEVEL = APB_Wrapper

# MODULE is the basename of the Python test file
MODULE = APB_test

# Compilation arguments
VLOG_ARGS += -mfcu -cuname -timescale=1ns/1ps

# Tell Questa to look in this dir for libsv_conduit.so
VSIM_ARGS += -sv_lib /home/amrelbatarny/myenv/lib/python3.9/site-packages/pyquesta/makefiles/sv_conduit

# Use setup.tcl for waveform configuration
VSIM_ARGS += -do setup.tcl

# Include Cocotb's Makefile AFTER variable exports
include $(shell cocotb-config --makefiles)/Makefile.sim

# Clean target
.PHONY: clean
clean::
	rm -rf __pycache__ modelsim.ini transcript vsim.wlf

# PyUCIS-Viewer target
.PHONY: pyucis
pyucis::
	pyucis-viewer ../Coverage_Reports/Exported_by_PyVSC/apb_coverage.xml