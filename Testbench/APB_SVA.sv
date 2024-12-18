module APB_SVA #(
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

// PSI => Previous System IN
// PSO => Previous System OUT

// Slave FROM Master
    input [ADDR_WIDTH-1 : 0]     	PADDR    ,
    input                        	PWRITE   ,
    input [DATA_WIDTH-1 : 0]     	PWDATA   ,
    input                        	PENABLE  ,
    input                           PSELx    ,

// Slave TO Master
    input                          PREADY   ,
    input [DATA_WIDTH-1 : 0]    	PRDATA   ,
    input                       	PSLVERR 	
);

assert property (@(posedge PCLK) (!PRESETn) |=> (PRDATA == 0));

endmodule : APB_SVA