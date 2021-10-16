* Github repository: https://github.com/kuangdai/AxiSEM-3D
* Wiki (documentation): https://github.com/kuangdai/AxiSEM-3D/wiki

Building on ARC
---------------
Documentation for building lives at https://github.com/kuangdai/AxiSEM-3D/wiki/installation - below is a version for ARC

Login to arc-login.arc.ox.ac.uk then start an interactive session on one of the nodes (don't compile on the front end
as it's a virtual machine with a different archetecture and no useful capacity):

    srun -p interactive --pty /bin/bash
    
Do step 1 for the prereqs:

    #!/bin/bash
    # download_Eigen_Boost_AxiSEM3D.sh
    
    # create and cd into a top-level working directory
    export AxiSEM3D_WORK_DIR=$HOME/axisem3d
    mkdir -p $AxiSEM3D_WORK_DIR && cd $_

    # create a dependency directory
    mkdir -p dependencies
    # download Eigen if not exists
    [ ! -d ./dependencies/eigen-master ] && \
    wget -c https://gitlab.com/libeigen/eigen/-/archive/master/eigen-master.tar.bz2 -O - | tar -jx -C ./dependencies
    # download Boost if not exists
    [ ! -d ./dependencies/boost_1_73_0 ] && \
    wget -c https://dl.bintray.com/boostorg/release/1.73.0/source/boost_1_73_0.tar.bz2 -O - | tar -jx -C ./dependencies
    
    # download AxiSEM3D if not exists
    [ ! -d ./AxiSEM3D ] && \
    git clone https://github.com/kuangdai/AxiSEM-3D.git AxiSEM3D
    # synchronize to github
    git -C AxiSEM3D pull
    
Grrr - the boost libary sources seem to have moved. And to be behind some kind of graphic thing. Download from https://boostorg.jfrog.io/ui/native/main/release/1.73.0/source/
and copy to ARC. Must be a better way.

make a build dir, cd and do:

    cmake -Dcxx=mpicxx -Dflags="-O3 -DNDEBUG" -Deigen=$AxiSEM3D_WORK_DIR/dependencies/eigen-master -Dboost=$AxiSEM3D_WORK_DIR/dependencies/boost_1_73_0  -Dfftw=/apps/system/easybuild/software/FFTW/3.3.9-intel-2021a ../AxiSEM3D/SOLVER/
    
    make
    
buidl fails with:

    /home/eart0526/code/AxiSEM3D/AxiSEM3D/SOLVER/src/core/output/station-wise/station/Station.hpp:59:22: error: ‘all’ is not a member of ‘Eigen’
    59 |              (Eigen::all, mNonZeroIndices) *
    
    
Modules:

   module load FFTW
   module load METIS
   module load netCDF
   module load CMake
   module load imkl/2021.2.0-iimpi-2021a
