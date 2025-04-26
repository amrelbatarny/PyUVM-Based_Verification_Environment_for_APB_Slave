module APB_Wrapper #(
	parameter DATA_WIDTH	= 32,
	parameter ADDR_WIDTH	= 32,
	parameter NBYTES		= DATA_WIDTH/8
	)(
	// Global Signals
	input wire						PCLK,
	input wire						PRESETn,

	// APB Signals
	input wire						PSELx,
	input wire [ADDR_WIDTH-1:0]		PADDR,
	input wire						PWRITE,
	input wire [NBYTES-1:0]			PSTRB,
	input wire [DATA_WIDTH-1:0]		PWDATA,
	input wire						PENABLE,
	output wire [DATA_WIDTH-1:0]	PRDATA,
	output wire						PREADY
	);
	
	// Register File Signals
	wire [ADDR_WIDTH-1:0]	addr;
	wire					write_en;
	wire					read_en;
	wire [NBYTES-1:0]		byte_strobe;
	wire [DATA_WIDTH-1:0]	wdata;
	wire [DATA_WIDTH-1:0]	rdata;

	assign PRDATA = rdata;

	RegisterFile #(
		.DATA_WIDTH(DATA_WIDTH),
		.ADDR_WIDTH(ADDR_WIDTH),
		.NBYTES(NBYTES)
		)RegisterFile_inst(
		.clk(PCLK),
		.rst_n(PRESETn),
		.addr(addr),
		.read_en(read_en),
		.write_en(write_en),
		.byte_strobe(byte_strobe),
		.wdata(wdata),
		.rdata(rdata)
		);
	
	APB_Slave #(
		.DATA_WIDTH(DATA_WIDTH),
		.ADDR_WIDTH(ADDR_WIDTH),
		.NBYTES(NBYTES)
		)APB_Slave_inst(
		.PCLK(PCLK),
		.PRESETn(PRESETn),
		.PSELx(PSELx),
		.PADDR(PADDR),
		.PWRITE(PWRITE),
		.PSTRB(PSTRB),
		.PWDATA(PWDATA),
		.PENABLE(PENABLE),
		.PREADY(PREADY),
		.addr(addr),
		.write_en(write_en),
		.read_en(read_en),
		.byte_strobe(byte_strobe),
		.wdata(wdata)
		);
	
	dummy_dpi_initializer dummy_dpi_initializer_inst();
endmodule