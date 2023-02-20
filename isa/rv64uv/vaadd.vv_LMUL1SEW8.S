
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    vsetvli t1, t0, e8,mf8,ta,ma
    vredand.vs v1, v1, v5

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN

    RVTEST_DATA_END
    
