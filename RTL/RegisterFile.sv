module RegisterFile #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 32,
    parameter NO_SLAVES  = 1					
) (

// Global Sinals
	input wire  						PCLK,
    input wire							PRESETn,  

    input wire [ADDR_WIDTH-1 : 0]   	RegADDR,
    input wire [DATA_WIDTH-1 : 0]   	RegWDATA,
    input wire                      	RegWRITE,
    input wire 							RegENABLE,

    output reg [DATA_WIDTH-1 : 0]   	RegRDATA,
    output 	                      		RegSLVERR,
    output reg                      	RegREADY      
);

	// RegSLVERR is pripherable 
	assign RegSLVERR = 0;
		
	// Registers
	reg [DATA_WIDTH-1:0] SYS_STATUS_REG;
	reg [DATA_WIDTH-1:0] INT_CTRL_REG;
	reg [DATA_WIDTH-1:0] DEV_ID_REG;
	reg [DATA_WIDTH-1:0] MEM_CTRL_REG;
	reg [DATA_WIDTH-1:0] TEMP_SENSOR_REG;
	reg [DATA_WIDTH-1:0] ADC_CTRL_REG;
	reg [DATA_WIDTH-1:0] DBG_CTRL_REG;
	reg [DATA_WIDTH-1:0] GPIO_DATA_REG;
	reg [DATA_WIDTH-1:0] DAC_OUTPUT_REG;
	reg [DATA_WIDTH-1:0] VOLTAGE_CTRL_REG;
	reg [DATA_WIDTH-1:0] CLK_CONFIG_REG;
	reg [DATA_WIDTH-1:0] TIMER_COUNT_REG;
	reg [DATA_WIDTH-1:0] INPUT_DATA_REG;
	reg [DATA_WIDTH-1:0] OUTPUT_DATA_REG;
	reg [DATA_WIDTH-1:0] DMA_CTRL_REG;
	reg [DATA_WIDTH-1:0] SYS_CTRL_REG;

    always @(posedge PCLK) begin
    	if(~PRESETn) begin
    		RegREADY <= 0;
    		RegRDATA <= 0;
    	end
        else if(RegENABLE) begin

        	if(RegWRITE) begin
            	case (RegADDR)
            		32'h0000_0000: SYS_STATUS_REG	<= RegWDATA;
					32'h0000_0004: INT_CTRL_REG		<= RegWDATA;
					32'h0000_0008: DEV_ID_REG		<= RegWDATA;
					32'h0000_000c: MEM_CTRL_REG		<= RegWDATA;
					32'h0000_0010: TEMP_SENSOR_REG	<= RegWDATA;
					32'h0000_0014: ADC_CTRL_REG		<= RegWDATA;
					32'h0000_0018: DBG_CTRL_REG		<= RegWDATA;
					32'h0000_001c: GPIO_DATA_REG	<= RegWDATA;
					32'h0000_0020: DAC_OUTPUT_REG	<= RegWDATA;
					32'h0000_0024: VOLTAGE_CTRL_REG	<= RegWDATA;
					32'h0000_0028: CLK_CONFIG_REG	<= RegWDATA;
					32'h0000_002c: TIMER_COUNT_REG	<= RegWDATA;
					32'h0000_0030: INPUT_DATA_REG	<= RegWDATA;
					32'h0000_0034: OUTPUT_DATA_REG	<= RegWDATA;
					32'h0000_0038: DMA_CTRL_REG		<= RegWDATA;
					32'h0000_003c: SYS_CTRL_REG		<= RegWDATA;
            	endcase

            end else begin
        		case (RegADDR)
            		32'h0000_0000: RegRDATA <= SYS_STATUS_REG;
					32'h0000_0004: RegRDATA <= INT_CTRL_REG;
					32'h0000_0008: RegRDATA <= DEV_ID_REG;
					32'h0000_000c: RegRDATA <= MEM_CTRL_REG;
					32'h0000_0010: RegRDATA <= TEMP_SENSOR_REG;
					32'h0000_0014: RegRDATA <= ADC_CTRL_REG;
					32'h0000_0018: RegRDATA <= DBG_CTRL_REG;
					32'h0000_001c: RegRDATA <= GPIO_DATA_REG;
					32'h0000_0020: RegRDATA <= DAC_OUTPUT_REG;
					32'h0000_0024: RegRDATA <= VOLTAGE_CTRL_REG;
					32'h0000_0028: RegRDATA <= CLK_CONFIG_REG;
					32'h0000_002c: RegRDATA <= TIMER_COUNT_REG;
					32'h0000_0030: RegRDATA <= INPUT_DATA_REG;
					32'h0000_0034: RegRDATA <= OUTPUT_DATA_REG;
					32'h0000_0038: RegRDATA <= DMA_CTRL_REG;
					32'h0000_003c: RegRDATA <= SYS_CTRL_REG;
            	endcase
            end

            RegREADY <= 1;
        end
		else begin
            RegREADY <= 0;
		end
        
    end

endmodule