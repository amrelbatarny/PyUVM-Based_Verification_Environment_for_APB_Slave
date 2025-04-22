module dummy_dpi_initializer;

    import APB_seq_item_pkg::*;
    
    initial begin
        string dummy_get;
        string dummy_put;
        dummy_put = "0000000100000002000000030000000400000005";
        
        // Make dummy calls to force elaboration of DPI export to trigger the DPI binding.
        $display("========================== dummy_dpi_initializer: ==========================");

        dummy_get = sv_get();
        $display("Called sv_get and returned data: %s", dummy_get);

        sv_put("dummy_put");
        $display("Called sv_put with sample data: %s", dummy_put);

        $display("============================================================================");
    end
endmodule