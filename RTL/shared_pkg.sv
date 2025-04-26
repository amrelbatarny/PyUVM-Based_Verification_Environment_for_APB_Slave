package shared_pkg;
	parameter DATA_WIDTH	= 32;
    parameter ADDR_WIDTH	= 32;
    parameter NBYTES		= DATA_WIDTH/8;
	
	// States type using onehot encoding
	typedef enum logic [1:0] {
	IDLE   = 2'b01,
	ACCESS  = 2'b10} state_e;

endpackage : shared_pkg