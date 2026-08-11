#!/bin/sh -l
#
# -- Request partition
#SBATCH --partition=u1-service
#
# -- Request n cores
#SBATCH --ntasks=1
#
# -- Specify queue
#SBATCH -q batch
#
# -- Specify a maximum wallclock
#SBATCH --time=0:10:00
#
# -- Specify under which account a job should run
#SBATCH --account=fv3-cpu
#
# -- Set the name of the job, or Slurm will default to the name of the script
#SBATCH --job-name=UFS-Land
#SBATCH -o plot_testing.out
#SBATCH --open-mode=truncate
#
# -- Tell the batch system to set the working directory to the current working directory
#SBATCH --chdir=.

testname="gfsv17"
compare_to="gfsv17"
archive_path="/scratch4/NCEPDEV/land/data/global_testing/"
archive_directory=$archive_path/tests/$testname

rm -rf plot_test
mkdir plot_test
cd plot_test

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

testname_file="${archive_directory}/retro/ufs_land_monthly_mean.retro.nc"
compare_file="$archive_path/tests/${compare_to}/retro/ufs_land_monthly_mean.retro.nc"

metric2plot="soil_moisture_level1_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "0-10cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "0-10cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "0-10cm Soil Moisture in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_moisture_level2_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "10-40cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "10-40cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "10-40cm Soil Moisture in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_moisture_level3_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "40-100cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "40-100cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "40-100cm Soil Moisture in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_moisture_level4_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "100-200cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "100-200cm Soil Moisture in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "100-200cm Soil Moisture in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_temperature_level1_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "0-10cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "0-10cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "0-10cm Soil Temperature in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_temperature_level2_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "10-40cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "10-40cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "10-40cm Soil Temperature in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_temperature_level3_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "40-100cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "40-100cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "40-100cm Soil Temperature in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="soil_temperature_level4_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "100-200cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "100-200cm Soil Temperature in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "100-200cm Soil Temperature in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="latent_heat_flux_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Latent Heat Flux in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Latent Heat Flux in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Latent Heat Flux in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="sensible_heat_flux_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Sensible Heat Flux in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Sensible Heat Flux in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Sensible Heat Flux in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png

metric2plot="ground_heat_flux_gfsref"

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask PacificNW,PacificSW,Southwest,NRockies,SRockies,GreatBasin,NPlains,CPlains,SPlains \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Ground Heat Flux in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky1.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Prairie,GreatLakes,Appalachia,DeepSouth,Southeast,MidAtlantic,NorthAtlantic,SAK,NAK \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Ground Heat Flux in US regions" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.bukovsky2.png

python ../plot_scripts/cal_plot_metrics.py \
 --input_file_name $testname_file,$compare_file \
 --mask Amazon,Yangtze,Congo,Mississippi,Danube,Nile,Murray,Lena,Yukon \
 --metrics $metric2plot \
 --average_option "AM" \
 --model $testname,$compare_to \
 --figure_title "Ground Heat Flux in Major River Basins" \
 --output_file_name ${metric2plot}.${testname}-vs-${compare_to}.basins.png



