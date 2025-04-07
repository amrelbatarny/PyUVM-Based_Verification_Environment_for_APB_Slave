from cocotb_test.simulator import run

def test_apb_wrapper():
    run(
        gui=1,
        waves=1,
        toplevel_lang="verilog",
        verilog_sources=[
            "../RTL/shared_pkg.sv",
            "../RTL/APB_Wrapper.sv",
            "../RTL/APB_Slave.sv",
            "../RTL/RegisterFile.sv",
            "APB_SVA.sv",
            "SVA_bind.sv"
        ],
        toplevel="APB_Wrapper",
        module="APB_test",
        sim_args=["-do", "../setup.tcl"],
        compile_args=[
            "-mfcu", 
            "-cuname", 
            "-timescale=1ns/1ps",
        ]
    )