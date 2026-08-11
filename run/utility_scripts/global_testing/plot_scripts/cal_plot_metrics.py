#!/usr/bin/env python3
import argparse
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import netCDF4 as nc
from datetime import datetime
from dateutil.relativedelta import relativedelta

#####
#  calculate_metrics
#
#    - set up models and input file names
#    - set up masks and mask file
#    - for each model/reference and each month, calculate metric

def calculate_metrics(input_file_name, metrics, mask, average_option, model):

# separate each model and the corresponding input file names

  input_file_names = input_file_name.split(",")
  models  = model.split(",")
  if not len(models) == len(input_file_names):
    sys.exit("Error: number of input files and model names do not match!")

# BFI: baseflow index (monthly mean climatology 2015-2024)

  if metrics.upper() == 'BFI':
    input_file_names += []
    models += []

# ALBEDO:  (monthly mean climatology 2015-2024)

  elif metrics.upper() == 'ALBEDO':
    input_file_names += []
    models += []

# ETOVERP: Total ET / Precipitation (monthly mean climatology 2015-2024)

  elif metrics.upper() == 'ETOVERP':
    input_file_names += []
    models += []

# ROVERP: Total Runoff / Precipitation (monthly mean climatology 2015-2024)

  elif metrics.upper() == 'ROVERP':
    input_file_names += []
    models += []

# TOVERET: Transpiration / Total ET (monthly mean climatology 2015-2024)

  elif metrics.upper() == 'TOVERET':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GLEAM/C192.mx025/GLEAM.v4.2a.climatology.2015-2024.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GLEAM/C192.mx025/GLEAM.v4.2b.climatology.2015-2024.C192.mx025.nc"]
    models += ["GLEAM4.2a"]
    models += ["GLEAM4.2b"]

# soil_temperature_level1_gfsref: Level 1 Soil Temperature Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_temperature_level1_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.TSOIL.level1.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.TSOIL.level1.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_temperature_level2_gfsref: Level 2 Soil Temperature Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_temperature_level2_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.TSOIL.level2.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.TSOIL.level2.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_temperature_level3_gfsref: Level 3 Soil Temperature Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_temperature_level3_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.TSOIL.level3.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.TSOIL.level3.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_temperature_level4_gfsref: Level 4 Soil Temperature Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_temperature_level4_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.TSOIL.level4.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.TSOIL.level4.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_moisture_level1_gfsref: Level 1 Soil Moisture Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_moisture_level1_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.SOILW.level1.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.SOILW.level1.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_moisture_level2_gfsref: Level 2 Soil Moisture Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_moisture_level2_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.SOILW.level2.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.SOILW.level2.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_moisture_level3_gfsref: Level 3 Soil Moisture Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_moisture_level3_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.SOILW.level3.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.SOILW.level3.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# soil_moisture_level4_gfsref: Level 4 Soil Moisture Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'soil_moisture_level4_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.SOILW.level4.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.SOILW.level4.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# latent_heat_flux_gfsref: Latent Heat Flux Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'latent_heat_flux_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.LHTFL.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.LHTFL.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# sensible_heat_flux_gfsref: Sensible Heat Flux Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'sensible_heat_flux_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.SHTFL.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.SHTFL.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

# ground_heat_flux_gfsref: Ground Heat Flux Compared to GFS Reference (monthly mean 2024-04 to 2026-02)

  elif metrics == 'ground_heat_flux_gfsref':
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv17.GFLUX.day01.monthly_mean.C192.mx025.nc"]
    input_file_names += ["/scratch4/NCEPDEV/land/data/evaluation/GFS_reference/C192.mx025/GFSv16.GFLUX.day01.monthly_mean.C192.mx025.nc"]
    models += ["v17retro_day1"]
    models += ["v16ref_day1"]

  else:
    print("Metric: ",metrics)
    sys.exit("Error: not implemented metric")

# separate the mask names and the file for the masks
# if the file is not given, the mask will read from the data file

  words    = mask.split("@")
  masks    = words[0].split(",")
  if len(words) > 1:
    mask_file_name = words[1]
  else:
    mask_file_name = "/scratch4/NCEPDEV/land/data/evaluation/masks/global_testing/U1D_C192.mx025_VegSoil_masks.nc"

# read in the data and calculate the evaluation metrics

  for file_id in range(len(input_file_names)):

    input_file_name = input_file_names[file_id]
    model_name  = models[file_id]
    if file_id == 0:    # get the length of the time variable

      src = nc.Dataset(input_file_name, "r")
      src_time = src.variables['time'][:]
      src.close()
      number_times = len(src_time)
      
      # create metric variable with size (number models + references, number masks, number times)
      # create time variable with size  (number times)

      metric_mask = np.full((len(input_file_names),len(masks),number_times,), np.nan)
      time  = np.empty((len(input_file_names),number_times,), dtype=object)
      
      if number_times == 12:   # assume this is monthly mean annual cycle
        time_initial = datetime.strptime("2020-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
      elif number_times == 23:   # assume this is monthly retro period
        time_initial = datetime.strptime("2024-04-01 00:00:00", '%Y-%m-%d %H:%M:%S')
      else:
        print("Times: ",number_times)
        sys.exit("Error: number of times not supported")

    for process_time in range(number_times):
      metric_mask[file_id,:,process_time] = read_cal_metrics(
                   model_name, input_file_name, mask_file_name, masks, metrics, average_option, process_time)

      time[:,process_time] = time_initial + relativedelta(months=process_time)
    
  return time, metric_mask, masks, models

#####
#  read_cal_metrics
#
#    - read dataset, read all variables in file
#    - calculation numerator and denominator of metric
#    - average according to average method, then apply mask

def read_cal_metrics(model_name, data_file_name, mask_file_name, masks, metrics, average_option, process_time):

  # open the data file and the mask file
  src_data = nc.Dataset(data_file_name, "r")
  if mask_file_name == None:
    src_mask = src_data
  else:
    src_mask = nc.Dataset(mask_file_name, "r")
  metric_mask = np.full((len(masks),), np.nan)

  # read in data and calculate the evaluation metrics
  #   var_numerator  : has length of the full location vector
  #   var_denominator: has length of the full location vector

  if metrics.upper() == 'BFI':
    var_denominator = src_data.variables['runoff_baseflow'][process_time] + src_data.variables['runoff_surface'][process_time]
    var_numerator   = src_data.variables['runoff_baseflow'][process_time]
  elif metrics.upper() == 'ALBEDO':
    var_numerator   = src_data.variables['sw_reflected_total'][process_time]
    var_denominator = src_data.variables['downward_shortwave_forcing'][process_time]
  elif metrics.upper() == 'ETOVERP':
    var_numerator   = src_data.variables['transpiration'][process_time] + src_data.variables['evaporation_canopy'][process_time]
    var_numerator  += src_data.variables['evaporation_soil'][process_time]
    var_denominator = src_data.variables['precipitation_forcing'][process_time]
  elif metrics.upper() == 'ROVERP':
    var_numerator   = src_data.variables['runoff_surface'][process_time] + src_data.variables['runoff_baseflow'][process_time]
    var_denominator = src_data.variables['precipitation_forcing'][process_time]
  elif metrics.upper() == 'TOVERET':
    if 'GLEAM' in model_name.upper():
      var_numerator    = src_data.variables['Et'][process_time]
      var_denominator  = src_data.variables['Et'][process_time] + src_data.variables['Eb'][process_time]
      var_denominator += src_data.variables['Es'][process_time] + src_data.variables['Ei'][process_time]
    else:
      var_numerator   = src_data.variables['transpiration'][process_time]
      var_denominator = src_data.variables['transpiration'][process_time] + src_data.variables['evaporation_canopy'][process_time]
      var_denominator += src_data.variables['evaporation_soil'][process_time]
  elif metrics == 'soil_temperature_level1_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_temperature_level1'][process_time]
    else:
      var_numerator   = src_data.variables['temperature_soil'][process_time][0]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_temperature_level2_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_temperature_level2'][process_time]
    else:
      var_numerator   = src_data.variables['temperature_soil'][process_time][1]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_temperature_level3_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_temperature_level3'][process_time]
    else:
      var_numerator   = src_data.variables['temperature_soil'][process_time][2]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_temperature_level4_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_temperature_level4'][process_time]
    else:
      var_numerator   = src_data.variables['temperature_soil'][process_time][3]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_moisture_level1_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_water_level1'][process_time]
    else:
      var_numerator    = src_data.variables['soil_moisture_vol'][process_time][0]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_moisture_level2_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_water_level2'][process_time]
    else:
      var_numerator    = src_data.variables['soil_moisture_vol'][process_time][1]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_moisture_level3_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_water_level3'][process_time]
    else:
      var_numerator    = src_data.variables['soil_moisture_vol'][process_time][2]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'soil_moisture_level4_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['soil_water_level4'][process_time]
    else:
      var_numerator    = src_data.variables['soil_moisture_vol'][process_time][3]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'latent_heat_flux_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['latent_heat_flux'][process_time]
    else:
      var_numerator    = src_data.variables['latent_heat_total'][process_time]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'sensible_heat_flux_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['sensible_heat_flux'][process_time]
    else:
      var_numerator    = src_data.variables['sensible_heat_total'][process_time]
    var_denominator  = np.full(len(var_numerator), 1.0)
  elif metrics == 'ground_heat_flux_gfsref':
    if 'v17retro' in model_name or 'v16ref' in model_name:
      var_numerator    = src_data.variables['ground_heat_flux'][process_time]
    else:
      var_numerator    = src_data.variables['ground_heat_total'][process_time]
    var_denominator  = np.full(len(var_numerator), 1.0)
  else:
    print("Metrics: ",metrics.upper())
    sys.exit("Error: not implemented metrics")

  # create mask-averaged metrics
  #   AM : calculate the metrics, then average the metrics over a domain
  #   MA : average the data over a domain, then calculate the metrics

  if average_option.upper() == 'AM':
    metric_no_mask = var_numerator[:]/var_denominator[:]
    for mask_id in range(len(masks)):
      current_mask = src_mask.variables[masks[mask_id]][:]
      metric_mask[mask_id] = np.nansum(metric_no_mask[:]*current_mask)/np.nansum(current_mask)
  elif average_option.upper() == 'MA':
    for mask_id in range(len(masks)):
      current_mask = src_mask.variables[masks[mask_id]][:]
      sum_numerator   = np.nansum(var_numerator[:]*current_mask)
      sum_denominator = np.nansum(var_denominator[:]*current_mask)
      metric_mask[mask_id] = sum_numerator/sum_denominator if sum_denominator != 0 else np.nan
  else:
    sys.exit("Error: not implemented average_option")

  return metric_mask

def plot_timeseries(time, metric_mask, masks, models, metrics, output_file_name, figure_title):

 # set default for all plots, individual set in if block

  ymin = 0
  ymax = 100
  defaultColors = np.array(['black' ,'red' ,'blue'  ,'green' ,'cyan' ,'magneta',
                           'yellow','gray','orange','purple','brown'])
  defaultStyles = np.array(['-',':','--','-.'])

  if metrics.upper() == 'BFI':
    defaultColors = np.array(['black' ,'red' ,'blue'  ,'green' ,'cyan' ,'magneta',
                              'yellow','gray','orange','purple','brown'])
    defaultStyles = np.array(['-' ,'-' ,'-'  ,':'])
  elif metrics.upper() == 'ALBEDO':
    defaultColors = np.array(['black' ,'red' ,'blue'  ,'green' ,'cyan' ,'magneta',
                              'yellow','gray','orange','purple','brown'])
    defaultStyles = np.array(['-' ,'-' ,'-'  ,':'])
  elif metrics.upper() == 'ETOVERP':
    defaultColors = np.array(['black' ,'red' ,'blue'  ,'green' ,'cyan' ,'magneta',
                              'yellow','gray','orange','purple','brown'])
    defaultStyles = np.array(['-' ,'-' ,'-'  ,':'])
  elif metrics.upper() == 'ROVERP':
    defaultColors = np.array(['black' ,'red' ,'blue'  ,'green' ,'cyan' ,'magneta',
                              'yellow','gray','orange','purple','brown'])
    defaultStyles = np.array(['-' ,'-' ,'-'  ,':'])
  elif metrics.upper() == 'TOVERET':
    defaultColors = np.array(['black','red','blue','blue'])
    defaultStyles = np.array(['-'    ,'-'  ,'-'   ,':'   ])
    metric_mask = metric_mask * 100.0
    plot_units = "%"
  elif (metrics == 'soil_moisture_level1_gfsref' or 
        metrics == 'soil_moisture_level2_gfsref' or 
        metrics == 'soil_moisture_level3_gfsref' or 
        metrics == 'soil_moisture_level4_gfsref'):
    defaultColors = np.array(['black','red','blue','green','blue','green'])
    defaultStyles = np.array(['-'    ,'-'  ,'-'   ,'-'    ,':'   ,':'  ])
    ymin = 0.0
    ymax = 0.5
    plot_units = "volumetric"
  elif (metrics == 'soil_temperature_level1_gfsref' or 
        metrics == 'soil_temperature_level2_gfsref' or 
        metrics == 'soil_temperature_level3_gfsref' or 
        metrics == 'soil_temperature_level4_gfsref'):
    defaultColors = np.array(['black','red','blue','green','blue','green'])
    defaultStyles = np.array(['-'    ,'-'  ,'-'   ,'-'    ,':'   ,':'  ])
    ymin = 250.0
    ymax = 320.0
    plot_units = "K"
  elif (metrics == 'latent_heat_flux_gfsref' or
        metrics == 'sensible_heat_flux_gfsref'):
    defaultColors = np.array(['black','red','blue','green','blue','green'])
    defaultStyles = np.array(['-'    ,'-'  ,'-'   ,'-'    ,':'   ,':'  ])
    ymin = 0.0
    ymax = 200.0
    plot_units = "W/m2"
  elif metrics == 'ground_heat_flux_gfsref':
    defaultColors = np.array(['black','red','blue','green','blue','green'])
    defaultStyles = np.array(['-'    ,'-'  ,'-'   ,'-'    ,':'   ,':'  ])
    ymin = -50.0
    ymax = 50.0
    plot_units = "W/m2"
  else:
    print("Metric: ",metrics.upper())
    sys.exit("Error: metric not implemented")

  # Create 3x3 subplots
  fig, axes = plt.subplots(3, 3, figsize=(9, 7))

  # Flatten axes array for easy iteration
  axes = axes.flatten()

  # Plot different lines in each subplot
  #   imask will be each region

  for imask, ax in enumerate(axes):
    for model_id in range(len(models)):
      model = models[model_id]
      x = time[model_id]
      y = metric_mask[model_id,imask]
      color = defaultColors[model_id%11]
      style = defaultStyles[model_id%11]
      ax.plot(x, y, color=color, linestyle=style, label=model)
      ax.set_ylim([ymin,ymax])
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
      if imask < 6:
        ax.tick_params(axis='x', labelbottom=False, direction='in', pad=0.01)
      else:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")
      ax.text(0.03, 0.9, masks[imask], fontsize=10, transform=ax.transAxes, verticalalignment='bottom')

  fig.supylabel(metrics + "["+plot_units+"]", x = 0.06)
  plt.subplots_adjust(wspace=0.20, hspace=0.08)
  axes[0].legend(bbox_to_anchor=(0., 1.03, 3.4, .1), loc='lower left',
                      ncols=4, mode="expand", borderaxespad=0.)

  if not figure_title == '':
    plt.suptitle(figure_title, y=0.98, fontsize=13)

  plt.savefig(output_file_name)
  print("output_file_name: "+output_file_name)

if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument('-if', '--input_file_name',    help="input file path and name",                  required=True)
  ap.add_argument('-mx', '--metrics',            help="evaluation metrics",                        required=True)
  ap.add_argument('-mk', '--mask',               help="masks",                                     required=True)
  ap.add_argument('-md', '--model',              help="model names",                               required=True)
  ap.add_argument('-of', '--output_file_name',   help="output file path and name",                 default="")
  ap.add_argument('-op', '--average_option',     help="AM(avg of metrics) or MA(metrics from avg", default="MA")
  ap.add_argument('-ft', '--figure_title',       help="figure title",                              default="")
  MyArgs = ap.parse_args()

  # read in data and calculate the evaluation metrics
  # time: the x-axis time object
  # metric_mask: evaluation metrics with dimensions: models,regions,time
  # masks: names for each mask
  # models: names for each model, test, or reference
  # output_file_name ends with ".png"

  time, metric_mask, masks, models = calculate_metrics(MyArgs.input_file_name,
                                                           MyArgs.metrics,
                                                           MyArgs.mask,
                                                           MyArgs.average_option, 
                                                           MyArgs.model)

  # plot the timeseries of the evaluation metrics

  plot_timeseries(time, metric_mask, masks, models, MyArgs.metrics, MyArgs.output_file_name, 
                  MyArgs.figure_title)

  print("The script ended normally!")
