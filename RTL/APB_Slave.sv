/***********************************************************************
 * Author : Amr El Batarny
 * File   : APB_Slave.sv
 * Brief  : Implements the APB slave module with register interface and
 *          control logic.
 **********************************************************************/

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
	input wire						PENABLE,
	output reg						PREADY,

	// Register File Signals
	output reg [ADDR_WIDTH-1:0]	addr,
	output reg					write_en,
	output reg					read_en,
	output reg [NBYTES-1:0]		byte_strobe,
	output reg [DATA_WIDTH-1:0]	wdata
	);

	import shared_pkg::*;
	state_e current_state, next_state;

	// State Memory
	always @(posedge PCLK or negedge PRESETn) begin
        if (~PRESETn) begin
            current_state <= IDLE;
        end else begin
            current_state <= next_state;
        end
    end

    // Next State Logic
    always_comb begin
    	case(current_state)
    		IDLE:
    			if(PENABLE && PSELx)
    				next_state = ACCESS;
    			else
    				next_state = IDLE;
    		
    		ACCESS:
				next_state = IDLE;

			default:
				next_state = IDLE;
    	endcase
    end

    // Output Logic
	always @* begin
		if(~PRESETn) begin
			PREADY = 1'b0;
		end else begin
			if(current_state == IDLE)
				PREADY = 1'b0;
			else if(current_state == ACCESS) begin
				addr 		= PADDR;
				write_en	= (PWRITE == 1'b1)? 1'b1 : 1'b0;
				read_en		= ~write_en;
				byte_strobe	= PSTRB;
				wdata		= PWDATA;
				PREADY		= 1'b1;
			end
		end
	end

endmodule