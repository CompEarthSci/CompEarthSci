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

2023 I used:
* CASTEP-22.11
* module load intel/2022b
* make install COMMSARCH=mpi MATHLIBS=mkl FFT=mkl 

### PETSc

What I ended up doing was:

```
srun -p interactive --pty /bin/bash
git clone -b release https://gitlab.com/petsc/petsc.git petsc
cd petsc/
git checkout v3.14
module load intel/2020b # NB: this sets $MKLROOT
module load OpenMPI/4.0.5-iccifort-2020.4.304 # NB: this sets mpicc etc. to point at intel compilers (otherwise you get a gcc build)
./configure --prefix=/home/eart0526/code/petsc-build --with-blaslapack-dir=$MKLROOT --download-hdf5 --download-mumps --download-scalapack --download-parmetis --download-metis --download-cmake --with-debugging=0 --enable-shared --download-pastix --download-ptscotch --with-cxx-dialect=C++11 --download-superlu_dist --download-spooles --download-suitesparse --download-ml --download-hypre --download-hwloc --download-make --FOPTFLAGS='-O2 -xHost' --CXXOPTFLAGS='-O2 -xHost' --COPTFLAGS='-O2 -xHost'
make PETSC_DIR=/home/eart0526/code/petsc PETSC_ARCH=arch-linux-c-opt all
make PETSC_DIR=/home/eart0526/code/petsc PETSC_ARCH=arch-linux-c-opt install
make PETSC_DIR=/home/eart0526/code/petsc-build PETSC_ARCH="" check
```

All tests reported passing. I've not (yet) worked out how to build the python bindings. Need to add `--download-mpi4py --download-petsc4py` but also 
link to a intel python I expect.

The following seemed to build okay, link against the system HDF5 and MKL (which works with gcc) but ended up with a gcc build:
```
srun -p interactive --pty /bin/bash
git clone -b release https://gitlab.com/petsc/petsc.git petsc
cd petsc/
git checkout v3.14
module load intel/2020b # NB: this sets $MKLROOT
module load HDF5/1.10.2-intel-2020b
module load Python/3.6.6-intel-2020b
./configure --prefix=/home/eart0526/code/petsc-build --with-blaslapack-dir=$MKLROOT --with-hdf5 --download-mumps --download-scalapack --download-parmetis --download-metis --download-cmake --with-debugging=0 --enable-shared --download-pastix --download-ptscotch --with-cxx-dialect=C++11 --download-superlu_dist --download-spooles --download-suitesparse --download-ml --download-hypre --download-hwloc --download-make --FOPTFLAGS=-O2 --CXXOPTFLAGS=-O2 --COPTFLAGS=-O2
```


