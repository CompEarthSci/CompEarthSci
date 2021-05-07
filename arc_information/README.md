# ARC for Earth Science users

Some (hopefully helpful) information for ARC users in Earth Sciences can be found
below along with some example scripts. New users (to ARC, or to high perfomance
computing in general) may benifit from a discussing plans with Andrew Walker
(andrew.walker@earth.ox.ac.uk).

## Links and quick start

Documentation - links etc.

## Compiling on the new ARC cluster

The login and submission nodes on the new arc cluster (arc-login.arc.ox.ac.uk)
have different processors to the compute nodes. Compile in an interactive
session. Some examples (for future reference) can be found below.

### CASTEP

(This is from memory - needs checking and updating. This was for version 20.11)

1. Obtain source (AMW has licence, and password for download) and place on arc-login
2. Start interactive session (`srun -p interactive --pty /bin/bash`)
3. Load intel module (`module load intel/2020b`) - this includes MKL and sets up the lib paths
4. Now just build (parallel) `make install COMMSARCH=mpi MATHLIBS=mkl FFT=MKL`
5. And serial  `make install COMMSARCH=serial MATHLIBS=mkl FFT=MKL`
6. Run a test job. Note that executing on a head node fails with `Please verify that both the operating system and the processor support Intel(R) AVX512F, AVX512DQ, AVX512CD, AVX512BW and AVX512VL instructions.`

### PETSc

TBC
