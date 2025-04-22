module APB_Slave #(
	parameter DATA_WIDTH	= 32,
	parameter ADDR_WIDTH	= 32,
	parameter NBYTES		= DATA_WIDTH/8
	)(
	// Global Signals
	input wire PCLK,
	input wire PRESETn,

	// APB Signals
	input wire						PSELx,
	input wire [ADDR_WIDTH-1:0]		PADDR,
	input wire						PWRITE,
	input wire [NBYTES-1:0]			PSTRB,
	input wire [DATA_WIDTH-1:0]		PWDATA,
	output reg [DATA_WIDTH-1:0]		PRDATA,
	input wire						PENABLE,
	output reg						PREADY,

	// Register File Signals
	output reg [ADDR_WIDTH-1:0]	addr,
	output reg					write_en,
	output reg					read_en,
	output reg [NBYTES-1:0]		byte_strobe,
	output reg [DATA_WIDTH-1:0]	wdata,
	);

	always @(posedge PCLK or negedge PRESETn) begin
		if(~PRESETn) begin
			PREADY <= 1'b0;
			PRDATA <= {DATA_WIDTH{1'b0}};
		end else begin
			if(PENABLE) begin
				addr 		<= PADDR;
				write_en	<= (PWRITE == 1'b1)? 1'b1 : 1'b0;
				read_en		<= ~write_en;
				byte_strobe	<= PSTRB;
				wdata		<= PWDATA;
				PREADY		<= 1'b1;
			end
		end
	end

endmodule