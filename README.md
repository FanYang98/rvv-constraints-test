# RISC-V Vector Constraints Tests

RISC-V V-extension 1.0 has been frozen for a while, [PLCT](https://github.com/plctlab) has developed [gem5](https://github.com/plctlab/plct-gem5) supporting RVV for all CPU models. To ensure RVV instructions run correctly, there are many constraints in simulator to avoid illegal vset and vreg overlap.

[The Spike simulator](https://github.com/riscv-software-src/riscv-isa-sim) is known as the RISC-V gold standard simulator, I compare Spike outputs and [gem5](https://github.com/plctlab/plct-gem5) outputs to check if the constraints in [gem5](https://github.com/plctlab/plct-gem5) are correct.

In RVV 1.0, the instructions constraints can be classified according to the number of operation registers and the width of the registers. I have classified all the constraints in RVV 1.0 into the following categories as in Spike, each type of constraints can be tested by **a representative instruction**. In the **progress** column, we can see the progress of gem5 for supporting all constraints.

| Constraints        | representative insn | **progress**      |
| ------------------ | ------------------- | ----------------- |
| VI_CHECK_SSS       | vaddu.vv            | √                 |
| VI_CHECK_DSS       | vwaddu.vv           | √                 |
| VI_CHECK_DDS       | vwaddu.wv           | √                 |
| VI_CHECK_SDS       | vnclip.wv           | √                 |
| VI_CHECK_REDUCTION | vredand.vs          | √                 |
| VI_CHECK_VRGATHER  | vrgather.vv         | √                 |
| VMV_CHECK          | vmv1r.v             | √                 |
| VI_VV_EXT_CHECK    | vzext.vf8           | √                 |
| VI_CHECK_SLIDE     | vslideup.vx         | √                 |
| VI_CHECK_LD_INDEX  | vluxei8.v           | e8 m2 v1 v1 error |
| VI_CHECK_ST_INDEX  | vsuxei8.v           | e8 m2 v1 v1 error |
| VI_CHECK_STORE     | vse8.v              | e8 m2 v1 v1 error |
| VI_CHECK_LOAD      | vle8.v              | e8 m2 v1 v1 error |
| VI_CHECK_LD_WHOLE  | vl1re16.v           | √                 |
| VI_CHECK_ST_WHOLE  | vs1r.v              | √                 |

## Prerequisite

1. `riscv64-unknown-elf-gcc` with RVV 1.0 support
2. The Spike simulator
3. The gem5 simulator

## How to use

```
cd isa
```

Then, you should edit **compare.py** according to your bin path. After editing, you can type in `python compare.py` to test all constraints in gem5.

## License

This project uses third-party projects, and the licenses of these projects are attached to the corresponding directories.

The code for this project is distributed under the MIT license.
