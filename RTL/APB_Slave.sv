module APB_Slave #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 32,
    parameter NO_SLAVES  = 1
) (
`ifdef AMBA4
      input [DATA_WIDTH/8 -1 : 0]  PSTRB       , 
      input [2:0]                  PPROT       , 
      output reg [DATA_WIDTH/8 -1 : 0] RegSTRB ,
      output reg [2:0]                 RegPROT ,
`endif 
// PSI => Previous System IN
// PSO => Previous System OUT
// Global Sinals
    input PCLK                                 ,
    input PRESETn                              ,  

// input SLAVE FROM MASTER  
    input [ADDR_WIDTH-1 : 0]     PADDR         ,
    input                        PWRITE        ,
    input [DATA_WIDTH-1 : 0]     PWDATA        ,
    input                        PENABLE       ,

// input SLAVE FROM REG_FILE  
    input [DATA_WIDTH-1 : 0]     RegRDATA      ,
    input                        RegSLVERR     ,
    input                        RegREADY      ,
    input [NO_SLAVES-1 : 0]      PSELx         ,
  
// output SLAVE TO MASTER  
    output reg                       PREADY    ,
    output reg [DATA_WIDTH-1 : 0]    PRDATA    ,
    output reg                       PSLVERR   ,

// output SLAVE TO REG_FILE  
    output reg [ADDR_WIDTH-1 : 0]    RegADDR   ,
    output reg [DATA_WIDTH-1 : 0]    RegWDATA  ,
    output reg                       RegENABLE,
    output reg                       RegWRITE
);
    
    import shared_pkg::*;
    state_e NextState, CurrentState;
    
// Next State Logic
    always @(*) begin
        case (CurrentState)
            IDLE: begin
                if (PENABLE) begin
                    NextState <= SETUP;
                end
                else begin
                    NextState <= IDLE;
                end
            end
            SETUP: begin
                NextState <= ACCESS;
            end
            ACCESS: begin
                if (PSLVERR) begin
                    NextState <= IDLE;
                end 
                else begin
                    if (RegREADY & PENABLE) begin
                        NextState <= SETUP;
                    end 
                    else if (RegREADY & !PENABLE) begin
                        NextState <= IDLE;
                    end
                    else begin
                        NextState <= ACCESS;
                    end
                end
            end
        endcase
    end

// State Memory
    always @(posedge PCLK or negedge PRESETn) begin
        if (!PRESETn) begin
            CurrentState = IDLE;
        end else begin
            CurrentState = NextState;
        end
    end

    
// output Logic
    always @(posedge PCLK or negedge PRESETn) begin
        if (!PRESETn) begin
            RegENABLE    <= 0;
            RegADDR      <= 0; 
            RegWRITE     <= 0;
            PREADY       <= 0;
            PRDATA       <= 0;
            PSLVERR      <= 0;
            RegWDATA     <= 0;
            `ifdef AMBA4
            RegSTRB      <= 0;
            RegPROT      <= 0;
            `endif
        end
        else if (CurrentState == SETUP) begin
            RegENABLE   <= PENABLE  ;
            PREADY      <= 0        ;
            RegADDR     <= PADDR    ; 
            RegWRITE    <= PWRITE   ;
            if (PWRITE == 1) begin // WRITE
                RegWDATA <= PWDATA;
                `ifdef AMBA4
                RegSTRB <= PSTRB;
                `endif
            end else if (PWRITE == 0) begin // READ 
                `ifdef AMBA4
                RegSTRB <= 'b0;
                `endif
            end
        end
        else if (CurrentState == ACCESS) begin
            RegENABLE = 1;
            `ifdef AMBA4
            RegPROT <= PPROT;
            `endif
            if (RegREADY == 1) begin
                if (PWRITE == 0) begin
                    PRDATA <= RegRDATA;
                end
                PSLVERR <= PSLVERR;
            end
                PREADY <= RegREADY;
        end
        else begin
            RegENABLE = 0;
            PREADY    = 0;
        end
    end

// // ADDRESS Decoding
//     always @(posedge PCLK or negedge PRESETn) begin
//         if (!PRESETn) begin
//             PSELx <= 'b0;
//         end
//         else if (NextState == IDLE) begin
//             PSELx <= 'b0;
//         end
//         else begin
//             case (PADDR[31:30])
//                 'b00: PSELx <= 4'b0001;
//                 'b01: PSELx <= 4'b0010;
//                 'b10: PSELx <= 4'b0100;
//                 'b11: PSELx <= 4'b1000;
//                 default: begin
//                    PSELx <= 'b0;
//                 end
//             endcase
//         end
//     end
endmodule