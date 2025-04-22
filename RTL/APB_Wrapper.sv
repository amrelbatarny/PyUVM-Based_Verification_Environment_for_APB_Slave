module APB_Wrapper #(
    parameter DATA_WIDTH = 32				 ,
    parameter ADDR_WIDTH = 32				 ,
    parameter NO_SLAVES  = 1					
) (
`ifdef AMBA4
	input [DATA_WIDTH/8 -1 : 0] 	PSTRB  	 , 
	input [2:0]                 	PPROT  	 , 
`endif 

// Global Sinals
    input 						 	PCLK     ,  
    input 						 	PRESETn  ,  

// Slave FROM Master
    input [ADDR_WIDTH-1 : 0]     	PADDR    ,
    input                        	PWRITE   ,
    input [DATA_WIDTH-1 : 0]     	PWDATA   ,
    input                        	PENABLE  ,
    input                           PSELx    ,

// Slave TO Master
    output                          PREADY   ,
    output [DATA_WIDTH-1 : 0]    	PRDATA   ,
    output                       	PSLVERR 	
);

// input Slave FROM RegisterFile
    wire [DATA_WIDTH-1 : 0]     RegRDATA    ;
    wire                        RegSLVERR   ;
    wire                        RegREADY    ;

// output Slave TO RegisterFile
    wire [ADDR_WIDTH-1 : 0]    RegADDR      ;
    wire [DATA_WIDTH-1 : 0]    RegWDATA     ;
    wire                       RegWRITE     ;
    wire                       RegENABLE    ;

RegisterFile #(
    .DATA_WIDTH(DATA_WIDTH) ,
    .ADDR_WIDTH(ADDR_WIDTH) ,
    .NO_SLAVES(NO_SLAVES)
)reg_file(
`ifdef AMBA4
    .RegSTRB(RegSTRB)       ,
    .RegPROT(RegPROT)       ,
`endif 

    .PCLK(PCLK)             ,
    .PRESETn(PRESETn)       ,

    .RegADDR(RegADDR)       ,
    .RegWDATA(RegWDATA)     ,
    .RegWRITE(RegWRITE)     ,
    .RegENABLE(RegENABLE)   ,

    .RegRDATA(RegRDATA)     ,
    .RegSLVERR(RegSLVERR)   , 
    .RegREADY(RegREADY)   
);

APB_Slave #(
    .DATA_WIDTH(DATA_WIDTH) ,
    .ADDR_WIDTH(ADDR_WIDTH) ,
    .NO_SLAVES(NO_SLAVES)
)apb_slave(
    `ifdef AMBA4
    .PSI_STRB(PSI_STRB)     ,
    .PSI_PROT(PSI_PROT)     ,
    .PSTRB(PSTRB)           ,
    .PPROT(PPROT)           ,
    `endif 
// PSI => Previous System IN
// PSO => Previous System OUT
// Global Sinals
    .PCLK(PCLK)             ,
    .PRESETn(PRESETn)       ,

// input Slave FROM Master
    .PSELx(PSELx)           ,
    .PADDR(PADDR)           ,
    .PWRITE(PWRITE)         ,
    .PWDATA(PWDATA)         ,
    .PENABLE(PENABLE)       ,
// input Slave FROM RegisterFile
    .RegRDATA(RegRDATA)     ,
    .RegSLVERR(RegSLVERR)   ,
    .RegENABLE(RegENABLE),
    .RegREADY(RegREADY)     ,

// output Slave TO Master
    .PREADY(PREADY)         ,
    .PRDATA(PRDATA)         ,
    .PSLVERR(PSLVERR)       ,

// output Slave TO RegisterFile
    .RegADDR(RegADDR)       ,
    .RegWDATA(RegWDATA)     ,
    .RegWRITE(RegWRITE)
);
dummy_dpi_initializer dummy_dpi_initializer_inst();    
endmodule