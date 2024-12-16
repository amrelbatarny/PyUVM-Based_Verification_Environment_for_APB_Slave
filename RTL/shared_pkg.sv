package shared_pkg;
	parameter DATA_WIDTH = 32;
    parameter ADDR_WIDTH = 32;
    parameter NO_SLAVES  = 1;	
    int clk_cycle = 4;
	
	// States type using onehot encoding
	typedef enum logic [2:0] {
	IDLE   = 3'b001,
	SETUP  = 3'b010,
	ACCESS = 3'b100} state_e;

	parameter ACTIVE_RESET = 2;	
	parameter READ_OP = 30;	
	parameter WRITE_OP = 70;	
	parameter MAX_DATA = 32'hFFFF_FFFF;	
	parameter MIN_DATA = 32'h0000_0000;	

	parameter READ_ACTIVE_PENABLE_LOOP 	  = 12;	
	parameter READ_INACTIVE_PENABLE_LOOP  = 2;	
	parameter WRITE_ACTIVE_PENABLE_LOOP   = 12;	
	parameter WRITE_INACTIVE_PENABLE_LOOP = 2;	
	parameter TOGGLE_LOOP   = 5;
	parameter RANDOM_LOOP   = 10;
endpackage : shared_pkg