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
    
**Grrr -** the boost libary sources seem to have moved. And to be behind some kind of graphic thing. Download from https://boostorg.jfrog.io/ui/native/main/release/1.73.0/source/
and copy to ARC. Must be a better way.

**Double Grrr -** When building with this version of eigen I get an error about `all` not being a present (see below). Instead 
clone from the gitlab repository and check out an older version (see https://github.com/UMich-BipedLab/LiDARTag/issues/6). This seems to work:

    git clone https://gitlab.com/libeigen/eigen.git
    cd eigen
    git checkout 6f0f6f792e441c32727ed945686fefe02e6bdbc6
    cd ..
    
Then make a build dir, cd and do:

    module load FFTW
    module load METIS
    module load netCDF
    module load CMake
    module load imkl/2021.2.0-iimpi-2021a    
    cmake -Dcxx=mpicxx -Dflags="-std=c++17 -O3 -DNDEBUG" -Deigen=$AxiSEM3D_WORK_DIR/dependencies/eigen -Dboost=$AxiSEM3D_WORK_DIR/dependencies/boost_1_73_0  -Dfftw=/apps/system/easybuild/software/FFTW/3.3.9-intel-2021a ../AxiSEM3D/SOLVER/
    make -j8
    
NB this uses eigen and not eigen-master. Those modle loads keep swapping between gcc versions (which seems a bit
fragile) but we end up with 3.10 and this does not, by default, support C++17, so we specify that. Anyway, this
produces an MPI executable. 

With master tarball from eigen, the build fails with:

    /home/eart0526/code/AxiSEM3D/AxiSEM3D/SOLVER/src/core/output/station-wise/station/Station.hpp:59:22: error: ‘all’ is not a member of ‘Eigen’
    59 |              (Eigen::all, mNonZeroIndices) *
    
    
Running a test
--------------

Right now, rather than worrying about the mesher etc. I just ran a test that seems to come with the source. Get the data in a directory in your home space root by doing:

    cd 
    cp -r $AxiSEM3D_WORK_DIR/AxiSEM3D/examples/01_spherical_Earth_PREM_50s .
    cd 01_spherical_Earth_PREM_50s
    
Your input files all now live in `input` which seems to have to be located next to the executable. So copy the executable:

    cp $AxiSEM3D_WORK_DIR/build/axisem3d .
    
You also need a job submission script. Mine is:

    #!/bin/bash 
    #SBATCH --nodes=1 
    #SBATCH --ntasks-per-node=48
    #SBATCH --mem-per-cpu=2G
    #SBATCH --time=00:10:00 
    #SBATCH --job-name=myjob 
    #SBATCH --partition=short

    module load FFTW
    module load METIS
    module load netCDF
    module load CMake
    module load imkl/2021.2.0-iimpi-2021a

    mpirun axisem3d
    
Then just `sbatch axisem3d.sub` (i.e. my submission script) to run. For this case 48 cores and 10 mins is overkill... Output shows up in an `output` directory. 
