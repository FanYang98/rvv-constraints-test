import os
import time

sew = ['e8', 'e16', 'e32', 'e64']
lmul = ['mf8', 'mf4', 'mf2', 'm1', 'm2', 'm4', 'm8']


vreg = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']

insns_vvv = ['vadd', 'vrgather', 'vwaddu']

insns_wv = ['vwaddu', 'vnclip']

insns_vs = ['vredand']
insns_vs_suffixs = ['.vs']

# spike --isa=rv64gcv --varch=vlen:256,elen:64 /your/pk/path /your/bin/path > spikenoerrorlog 2>spikeerrorlog
spike_cmd = ""
# /your/gem5.opt/path /your/gem5/se.py --cmd=/your/bin/path  > gem5noerrorlog 2>gem5errorlog
gem5_cmd = ""

def gencodevredand(e,m,v1,v2,v3):
    return '''
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    vsetvli t1, t0, %s,%s,ta,ma
    vredand.vs %s, %s, %s

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN

    RVTEST_DATA_END
    '''%(e,m,v1,v2,v3)

def gencodewv(e,m,insn,v1,v2,v3):
    return '''
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    vsetvli t1, t0, %s,%s,ta,ma
    %s.wv %s, %s, %s

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN

    RVTEST_DATA_END
    '''%(e,m,insn,v1,v2,v3)

def gencodevv(e,m,insn,v1,v2,v3):
    return '''
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    vsetvli t1, t0, %s,%s,ta,ma
    %s.vv %s, %s, %s

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN

    RVTEST_DATA_END
    '''%(e,m,insn,v1,v2,v3)
    
def gencodevmv1r(e,m,v1,v2):
    return '''
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    vsetvli t1, t0, %s,%s,ta,ma
    vmv1r.v %s, %s

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN

    RVTEST_DATA_END
    '''%(e,m,v1,v2)
    
def gencodevslideup(e,m,v1,v2):
    return '''
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    li a5, 1
    vsetvli t1, t0, %s,%s,ta,ma
    vslideup.vx %s, %s, a5

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN

    RVTEST_DATA_END
    '''%(e,m,v1,v2)

def gencodevlu(e,m,v1,v2):
    return '''
    
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    la a5, tdat
    vsetvli t1, t0, %s,%s,ta,ma
    vluxei8.v  %s, (a5), %s

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN
    tdat:
        .quad 0x103f8ffefefff
    RVTEST_DATA_END
    '''%(e,m,v1,v2)
    
def gencodevlre(e,m,v1):
    return '''
    
    #include "riscv_test.h"
    #include "test_macros.h"

    RVTEST_RV64UV

    RVTEST_CODE_BEGIN
    
    li t0, 16
    la a5, tdat
    vsetvli t1, t0, %s,%s,ta,ma
    vl1re16.v  %s, (a5)

    TEST_PASSFAIL

    RVTEST_CODE_END

    .data
    RVTEST_DATA_BEGIN
    tdat:
        .quad 0x103f8ffefefff
    RVTEST_DATA_END
    '''%(e,m,v1)
    
def checkspikeerror(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line[:10]=="An illegal":
                #print("spike error occur")
                return True
    return False

def checkgem5error(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line[:7]=="Aborted":
                #print("gem5 error occur")
                return True
    return False

for insn in insns_vvv:
    for e_set in sew:
        for lmul_set in lmul:
            for v1 in vreg:
                for v2 in vreg:
                    for v3 in vreg:
                        print("run %s %s %s %s %s %s test" %(insn, e_set, lmul_set, v1, v2, v3))
                        os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodevv(e_set, lmul_set, insn, v1, v2, v3)))
                        os.system("make")
                        os.system(spike_cmd)
                        os.system(gem5_cmd)
                        if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                            print("%s %s %s %s %s %s spike gem5 match error occur" %(insn, e_set, lmul_set, v1, v2, v3))
                        if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                            print("%s %s %s %s %s %s spike gem5 match error occur" %(insn, e_set, lmul_set, v1, v2, v3))
                            
for insn in insns_wv:
    for e_set in sew:
        for lmul_set in lmul:
            for v1 in vreg:
                for v2 in vreg:
                    for v3 in vreg:
                        print("run %s %s %s %s %s %s test" %(insn, e_set, lmul_set, v1, v2, v3))
                        os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodewv(e_set, lmul_set, insn, v1, v2, v3)))
                        os.system("make")
                        os.system(spike_cmd)
                        os.system(gem5_cmd)
                        if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                            print("%s %s %s %s %s %s spike gem5 match error occur" %(insn, e_set, lmul_set, v1, v2, v3))
                        if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                            print("%s %s %s %s %s %s spike gem5 match error occur" %(insn, e_set, lmul_set, v1, v2, v3))
                            
for e_set in sew:
    for lmul_set in lmul:
        for v1 in vreg:
            for v2 in vreg:
                for v3 in vreg:
                    print("run vredand.vs %s %s %s %s %s test" %(e_set, lmul_set, v1, v2, v3))
                    os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodevredand(e_set, lmul_set, v1, v2, v3)))
                    os.system("make")
                    os.system(spike_cmd)
                    os.system(gem5_cmd)
                    if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                        print("vredand %s %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2, v3))
                    if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                        print("vredand %s %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2, v3))
for e_set in sew:
    for lmul_set in lmul:
        for v1 in vreg:
            for v2 in vreg:
                print("run vmv1r %s %s %s %s test" %(e_set, lmul_set, v1, v2))
                os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodevredand(e_set, lmul_set, v1, v2)))
                os.system("make")
                os.system(spike_cmd)
                os.system(gem5_cmd)
                if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                    print("vredand %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2))
                if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                    print("vredand %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2))
                    
for e_set in sew:
    for lmul_set in lmul:
        for v1 in vreg:
            for v2 in vreg:
                print("run vslideup %s %s %s %s test" %(e_set, lmul_set, v1, v2))
                os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodevslideup(e_set, lmul_set, v1, v2)))
                os.system("make")
                os.system(spike_cmd)
                os.system(gem5_cmd)
                if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                    print("vredand %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2))
                if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                    print("vredand %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2))
for e_set in sew:
    for lmul_set in lmul:
        for v1 in vreg:
            for v2 in vreg:
                print("run vluxei %s %s %s %s test" %(e_set, lmul_set, v1, v2))
                os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodevlu(e_set, lmul_set, v1, v2)))
                os.system("make")
                os.system(spike_cmd)
                os.system(gem5_cmd)
                if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                    print("vredand %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2))
                if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                    print("vredand %s %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1, v2))

for e_set in sew:
    for lmul_set in lmul:
        for v1 in vreg:
            print("run vlre %s %s %s test" %(e_set, lmul_set, v1))
            os.system("echo '%s' > ./rv64uv/vaadd.vv_LMUL1SEW8.S" %(gencodevlre(e_set, lmul_set, v1)))
            os.system("make")
            os.system(spike_cmd)
            os.system(gem5_cmd)
            if checkspikeerror("spikenoerrorlog") == False and checkgem5error("gem5errorlog") == True:
                print("vredand %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1))
            if checkspikeerror("spikenoerrorlog") == True and checkgem5error("gem5errorlog") == False:
                print("vredand %s %s %s spike gem5 match error occur" %(e_set, lmul_set, v1))


                

  



            
            


                
        
