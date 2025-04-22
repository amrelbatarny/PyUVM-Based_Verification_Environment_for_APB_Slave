package APB_seq_item_pkg;
export "DPI-C" function sv_get;
export "DPI-C" function sv_put;
export "DPI-C" function sv_transport;


// *** APB_seq_item ***
    typedef byte unsigned APB_seq_item_buf_t[20];
    typedef bit[0:159] APB_seq_item_packed_t;

    class APB_seq_item;
       rand  int unsigned  PRESETn;
       rand  int unsigned  PWDATA;
       rand  int unsigned  PENABLE;
       rand  int unsigned  PWRITE;
       rand  int unsigned  PADDR;

        function new(APB_seq_item_buf_t buffer={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0});
            APB_seq_item_packed_t packed_buf;
            packed_buf = 160'(buffer);
            PRESETn = packed_buf[0:31];
            PWDATA = packed_buf[32:63];
            PENABLE = packed_buf[64:95];
            PWRITE = packed_buf[96:127];
            PADDR = packed_buf[128:159];
        endfunction

        function string serialize();
            string buffer;
            buffer = $sformatf("%08h%08h%08h%08h%08h",PRESETn,PWDATA,PENABLE,PWRITE,PADDR);
            return buffer;
        endfunction

        // User Defined
        function void deserialize(string str);
            // Extract fields from the packed string format:
            // Format: PRESETn (1 char) + PWDATA (8-char hex) + PENABLE (1 char) + PWRITE (1 char) + PADDR (8-char hex)
            
            // PRESETn (1 character)
            PRESETn = str.substr(0, 0).atoi();
            
            // PWDATA (characters 1-8, 8-digit hex)
            PWDATA = str.substr(1, 8).atohex();
            
            // PENABLE (character 9)
            PENABLE = str.substr(9, 9).atoi();
            
            // PWRITE (character 10)
            PWRITE = str.substr(10, 10).atoi();
            
            // PADDR (characters 11-18, 8-digit hex)
            PADDR = str.substr(11, 18).atohex();
        endfunction

    endclass

    `include "APB_seq_item.svh"
endpackage
