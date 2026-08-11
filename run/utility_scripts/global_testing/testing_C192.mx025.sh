#!/bin/sh -l
#
# -- Request partition
#SBATCH --partition=u1-service
#
# -- Request n cores
#SBATCH --ntasks=64
#
# -- Specify queue
#SBATCH -q batch
#
# -- Specify a maximum wallclock
#SBATCH --time=3:30:00
#
# -- Specify under which account a job should run
#SBATCH --account=fv3-cpu
#
# -- Set the name of the job, or Slurm will default to the name of the script
#SBATCH --job-name=UFS-Land
#SBATCH -o ufs-land-global_testing.%j.out
#SBATCH --open-mode=truncate
#
# -- Tell the batch system to set the working directory to the current working directory
#SBATCH --chdir=.

module purge
module use /contrib/spack-stack/spack-stack-1.9.2/envs/ue-oneapi-2024.2.1/install/modulefiles/Core
module load stack-oneapi/2024.2.1 
module load stack-intel-oneapi-mpi/2021.13 
module load netcdf-fortran/4.6.1 
module load nco/5.2.4 

testname="gfsv17"
description="gfsv17 configuration"
compare_to="gfsv17"
archive_path="/scratch4/NCEPDEV/land/data/global_testing/"
noahmp_parameter_table="../../../ccpp-physics/physics/SFC_Models/Land/Noahmp/noahmptable.tbl"
ccpp_code_directory="../../../ccpp-physics/physics/SFC_Models/Land/Noahmp"

################################################################
# noahmp options: 

dynamic_vegetation_option=4
canopy_stomatal_resistance_option=2
soil_wetness_option=1
runoff_option=1
surface_exchange_option=1
supercooled_soilwater_option=1
frozen_soil_adjust_option=1
radiative_transfer_option=3
snow_albedo_option=1
precip_partition_option=1
soil_temp_lower_bdy_option=2
soil_temp_time_scheme_option=3
thermal_roughness_scheme_option=2
surface_evap_resistance_option=4
glacier_option=2
tq_diagnostic_option=2

################################################################
# test for run and archive directory 

archive_directory=$archive_path/tests/$testname
if [ -d $archive_directory ]; then 
  echo "ERROR: archive directory $archive_directory already exists"
  echo "ERROR: overwriting is not allowed"
  exit 1
else
  echo "creating directory: "$archive_directory
  mkdir -p $archive_directory
fi

if [ -d $testname ]; then 
  echo "ERROR: run directory $testname already exists"
  echo "ERROR: overwriting is not allowed"
  exit 2
else
  echo "creating directory: "$testname
  mkdir -p $testname
fi


################################################################
# create a configuration file: 

echo "testname = $testname" > configuration
echo "description = $description" >> configuration
echo "compare_to = $compare_to" >> configuration
echo "archive_directory = $archive_directory" >> configuration
echo "noahmp_parameter_table = $noahmp_parameter_table" >> configuration
echo "dynamic_vegetation_option = $dynamic_vegetation_option" >> configuration
echo "canopy_stomatal_resistance_option = $canopy_stomatal_resistance_option" >> configuration
echo "soil_wetness_option = $soil_wetness_option" >> configuration
echo "runoff_option = $runoff_option" >> configuration
echo "surface_exchange_option = $surface_exchange_option" >> configuration
echo "supercooled_soilwater_option = $supercooled_soilwater_option" >> configuration
echo "frozen_soil_adjust_option = $frozen_soil_adjust_option" >> configuration
echo "radiative_transfer_option = $radiative_transfer_option" >> configuration
echo "snow_albedo_option = $snow_albedo_option" >> configuration
echo "precip_partition_option = $precip_partition_option" >> configuration
echo "soil_temp_lower_bdy_option = $soil_temp_lower_bdy_option" >> configuration
echo "soil_temp_time_scheme_option = $soil_temp_time_scheme_option" >> configuration
echo "thermal_roughness_scheme_option = $thermal_roughness_scheme_option" >> configuration
echo "surface_evap_resistance_option = $surface_evap_resistance_option" >> configuration
echo "glacier_option = $glacier_option" >> configuration
echo "tq_diagnostic_option = $tq_diagnostic_option" >> configuration

cp configuration $archive_directory

################################################################
# start namelist generation

cp ufs-land.namelist.template ufs-land.namelist

sed -i "s/<dynamic_vegetation_option>/$dynamic_vegetation_option/g" ufs-land.namelist
sed -i "s/<canopy_stomatal_resistance_option>/$canopy_stomatal_resistance_option/g" ufs-land.namelist
sed -i "s/<soil_wetness_option>/$soil_wetness_option/g" ufs-land.namelist
sed -i "s/<runoff_option>/$runoff_option/g" ufs-land.namelist
sed -i "s/<surface_exchange_option>/$surface_exchange_option/g" ufs-land.namelist
sed -i "s/<supercooled_soilwater_option>/$supercooled_soilwater_option/g" ufs-land.namelist
sed -i "s/<frozen_soil_adjust_option>/$frozen_soil_adjust_option/g" ufs-land.namelist
sed -i "s/<radiative_transfer_option>/$radiative_transfer_option/g" ufs-land.namelist
sed -i "s/<snow_albedo_option>/$snow_albedo_option/g" ufs-land.namelist
sed -i "s/<precip_partition_option>/$precip_partition_option/g" ufs-land.namelist
sed -i "s/<soil_temp_lower_bdy_option>/$soil_temp_lower_bdy_option/g" ufs-land.namelist
sed -i "s/<soil_temp_time_scheme_option>/$soil_temp_time_scheme_option/g" ufs-land.namelist
sed -i "s/<thermal_roughness_scheme_option>/$thermal_roughness_scheme_option/g" ufs-land.namelist
sed -i "s/<surface_evap_resistance_option>/$surface_evap_resistance_option/g" ufs-land.namelist
sed -i "s/<glacier_option>/$glacier_option/g" ufs-land.namelist
sed -i "s/<tq_diagnostic_option>/$tq_diagnostic_option/g" ufs-land.namelist

################################################################
# assemble a working directory and run model

mv ufs-land.namelist $testname
cp $noahmp_parameter_table ${testname}/noahmptable.tbl

cd $testname

echo "Begin model run: $(date)"

time srun -n $SLURM_NTASKS ../../../ufsLand.exe

echo "End model run: $(date)"

echo "Start nco commands: $(date)"

ncra ufs_land_monthly_mean.201[5-9]-01.nc ufs_land_monthly_mean.202[0-4]-01.nc  ufs_land_monthly_mean.2015-2024.01.nc
ncra ufs_land_monthly_mean.201[5-9]-02.nc ufs_land_monthly_mean.202[0-4]-02.nc  ufs_land_monthly_mean.2015-2024.02.nc
ncra ufs_land_monthly_mean.201[5-9]-03.nc ufs_land_monthly_mean.202[0-4]-03.nc  ufs_land_monthly_mean.2015-2024.03.nc
ncra ufs_land_monthly_mean.201[5-9]-04.nc ufs_land_monthly_mean.202[0-4]-04.nc  ufs_land_monthly_mean.2015-2024.04.nc
ncra ufs_land_monthly_mean.201[5-9]-05.nc ufs_land_monthly_mean.202[0-4]-05.nc  ufs_land_monthly_mean.2015-2024.05.nc
ncra ufs_land_monthly_mean.201[5-9]-06.nc ufs_land_monthly_mean.202[0-4]-06.nc  ufs_land_monthly_mean.2015-2024.06.nc
ncra ufs_land_monthly_mean.201[5-9]-07.nc ufs_land_monthly_mean.202[0-4]-07.nc  ufs_land_monthly_mean.2015-2024.07.nc
ncra ufs_land_monthly_mean.201[5-9]-08.nc ufs_land_monthly_mean.202[0-4]-08.nc  ufs_land_monthly_mean.2015-2024.08.nc
ncra ufs_land_monthly_mean.201[5-9]-09.nc ufs_land_monthly_mean.202[0-4]-09.nc  ufs_land_monthly_mean.2015-2024.09.nc
ncra ufs_land_monthly_mean.201[5-9]-10.nc ufs_land_monthly_mean.202[0-4]-10.nc  ufs_land_monthly_mean.2015-2024.10.nc
ncra ufs_land_monthly_mean.201[5-9]-11.nc ufs_land_monthly_mean.202[0-4]-11.nc  ufs_land_monthly_mean.2015-2024.11.nc
ncra ufs_land_monthly_mean.201[5-9]-12.nc ufs_land_monthly_mean.202[0-4]-12.nc  ufs_land_monthly_mean.2015-2024.12.nc

ncrcat -h ufs_land_monthly_mean.2015-2024.??.nc ufs_land_monthly_mean.2015-2024.climo.nc

ncrcat ufs_land_monthly_mean.2024-0[4-9].nc ufs_land_monthly_mean.2024-1[0-2].nc ufs_land_monthly_mean.2025-??.nc ufs_land_monthly_mean.2026-0[1-2].nc ufs_land_monthly_mean.retro.nc

echo "End nco commands: $(date)"

############
# Archive 
############

echo "Start archive commands: $(date)"

mkdir -p $archive_directory/climatology
rsync -av ufs_land_monthly_mean.2015-2024.??.nc $archive_directory/climatology
rsync -av ufs_land_monthly_mean.2015-2024.climo.nc $archive_directory/climatology

mkdir -p $archive_directory/monthly_mean
rsync -av ufs_land_monthly_mean.20??-??.nc $archive_directory/monthly_mean

mkdir -p $archive_directory/retro
rsync -av ufs_land_monthly_mean.retro.nc $archive_directory/retro

mkdir -p $archive_directory/diurnal
rsync -av ufs_land_diurnal.201[5-9]*.nc $archive_directory/diurnal
rsync -av ufs_land_diurnal.202[0-4]*.nc $archive_directory/diurnal

cp ufs-land.namelist $archive_directory

mkdir -p $archive_directory/code_parameters

cp noahmptable.tbl ${archive_directory}/code_parameters
cp ../${ccpp_code_directory}/module_sf_noahmplsm.F90 ${archive_directory}/code_parameters
cp ../${ccpp_code_directory}/module_sf_noahmp_glacier.F90 ${archive_directory}/code_parameters
cp ../${ccpp_code_directory}/noahmpdrv.F90 ${archive_directory}/code_parameters

echo "End archive commands: $(date)"

############
# Create plots 
############

echo "Start plot commands: $(date)"

module purge
module use /contrib/spack-stack/spack-stack-1.9.2/envs/ue-oneapi-2024.2.1/install/modulefiles/Core
module load stack-oneapi/2024.2.1
module load stack-intel-oneapi-mpi/2021.13
module load python/3.11.7
module load py-netcdf4/1.7.1.post2
module load py-matplotlib/3.7.4
module load python/3.11

testname_file="${archive_directory}/climatology/ufs_land_monthly_mean.2015-2024.climo.nc"
compare_file="$archive_path/tests/${compare_to}/climatology/ufs_land_monthly_mean.2015-2024.climo.nc"

metric2plot="ToverET"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --model $testname,$compare_to \
 --figure_title "Transpiration % of ET in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --model $testname,$compare_to \
 --figure_title "Transpiration % of ET in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --model $testname,$compare_to \
 --figure_title "Transpiration % in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

############
# Archive plots 
############

mkdir -p $archive_directory/plots

cp *.png $archive_directory/plots

echo "End plot commands: $(date)"

