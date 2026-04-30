#!/usr/bin/env python3
import argparse
import sys
import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import netCDF4 as nc

def calculate_metrics(rootd, ifname, ofname, metrics, mask, option, model):

# seperate each model and the corresponding input file names
  ifnames = ifname.split(",")
  models  = model.split(",")
  if not len(models) == len(ifnames):
    sys.exit("Error: number of input files and model names do not match!")

  if metrics.upper() == 'BFI':
    ifnames += []
    models += []
  elif metrics.upper() == 'ALBEDO':
    ifnames += []
    models += []
  elif metrics.upper() == 'ETOVERP':
    ifnames += []
    models += []
  elif metrics.upper() == 'ROVERP':
    ifnames += []
    models += []
  elif metrics.upper() == 'TOVERET':
    ifnames += ["/scratch4/NCEPDEV/land/data/evaluation/GLEAM/C192.mx025/GLEAM.v4.2a.climatology.2015-2024.C192.mx025.nc"]
    ifnames += ["/scratch4/NCEPDEV/land/data/evaluation/GLEAM/C192.mx025/GLEAM.v4.2b.climatology.2015-2024.C192.mx025.nc"]
    models += ["GLEAM4.2a"]
    models += ["GLEAM4.2b"]
  else:
    print("Metrics: ",metrics.upper())
    sys.exit("Error: not implemented metrics")

# seperate the mask names and the file for the masks
# if the file is not given, the mask will read from the data file
  words    = mask.split("@")
  masks    = words[0].split(",")
  if len(words) > 1:
    mfname = words[1]
  else:
    mfname = "/scratch4/NCEPDEV/land/data/evaluation/masks/global_testing/U1D_C192.mx025_mask.nc"

# read in monthly data and calculate the evaluation metrics
  months = 12
  var_idx = np.full((len(ifnames),len(masks),months,), np.nan)
  for fid in range(len(ifnames)):
    ifname = ifnames[fid]
    model  = models[fid]
    if not rootd == "":
      ifname = rootd + "/" + ifname
    for month in range(months):
      fname_in  = ifname.replace("%MM",str(month+1).zfill(2))
      tmp_numerator, tmp_denominator, var_idx[fid,:,month] = read_cal_metrics(
                   model, fname_in, mfname, masks, metrics, option, month)
      if not ofname == "" and ofname.endswith('.nc'):
        if month == 0:
          var_numerator        = np.zeros((months,)+tmp_numerator.shape, dtype=tmp_numerator.dtype)
          var_denominator      = np.zeros((months,)+tmp_numerator.shape, dtype=tmp_numerator.dtype)
          var_idx2d            = np.zeros((months,)+tmp_numerator.shape, dtype=tmp_numerator.dtype)
          avg_numerator        = np.zeros(tmp_numerator.shape, dtype=tmp_numerator.dtype)
          avg_denominator      = np.zeros(tmp_numerator.shape, dtype=tmp_numerator.dtype)
          avg_idx2d            = np.zeros(tmp_numerator.shape, dtype=tmp_numerator.dtype)
          if fid == 0:
            dst = nc.Dataset(ofname, "w")
            if len(tmp_numerator.shape) == 1:
              dst.createDimension('location', len(tmp_numerator))
              dim = ('location',)
            else:
              dst.createDimension('lat', len(tmp_numerator))
              dst.createDimension('lon', len(tmp_numerator[0]))
              dim = ('lat','lon',)
            dim_wt = ('time',) + dim
            dst.createDimension('time', months)
          dst.createVariable(metrics+'_'+model, tmp_numerator.dtype, dim_wt)
          dst.createVariable(metrics+'_numerator_'+model,   tmp_numerator.dtype, dim_wt)
          dst.createVariable(metrics+'_denominator_'+model, tmp_numerator.dtype, dim_wt)
          dst.createVariable(metrics+'_avg_'+model, tmp_numerator.dtype, dim)
          dst.createVariable(metrics+'_numerator_avg_'+model,   tmp_numerator.dtype, dim)
          dst.createVariable(metrics+'_denominator_avg_'+model, tmp_numerator.dtype, dim)
        var_numerator[month]   = tmp_numerator
        var_denominator[month] = tmp_denominator
        var_idx2d[month]       = tmp_numerator/tmp_denominator
      if not ofname == "" and ofname.endswith('.nc'):
        avg_numerator   = np.nanmean(var_numerator, axis=0)
        avg_denominator = np.nanmean(var_denominator, axis=0)
        avg_idx2d       = avg_numerator/avg_denominator
        dst[metrics+'_'+model][:]                 = var_idx2d[:]
        dst[metrics+'_numerator_'+model][:]       = var_numerator[:]
        dst[metrics+'_denominator_'+model][:]     = var_denominator[:]
        dst[metrics+'_avg_'+model][:]             = avg_idx2d[:]
        dst[metrics+'_numerator_avg_'+model][:]   = avg_numerator[:]
        dst[metrics+'_denominator_avg_'+model][:] = avg_denominator[:]
  if not ofname == "" and ofname.endswith('.nc'):
    dst.close()
# for rid in range(len(masks)):
#   print(rid, var_idx[rid,0])
  time = [datetime.date(2020, month+1, 15) for month in range(12)]
  return time, var_idx, masks, models

def read_cal_metrics(model, dfname, mfname, masks, metrics, option, month):
  # open the data file and the mask file
  src_data = nc.Dataset(dfname, "r")
  if mfname == None:
    src_mask = src_data
  else:
    src_mask = nc.Dataset(mfname, "r")
  var_idx = np.full((len(masks),), np.nan)

  # read in data and calculate the evaluation metrics
  if metrics.upper() == 'BFI':
    var_base = src_data.variables['runoff_baseflow'][0]
    var_sfc  = src_data.variables['runoff_surface'][0]
    var_denominator = var_base + var_sfc
    var_numerator   = var_base
  elif metrics.upper() == 'ALBEDO':
    var_numerator   = src_data.variables['sw_reflected_total'][0]
    var_denominator = src_data.variables['downward_shortwave_forcing'][0]
  elif metrics.upper() == 'ETOVERP':
    var_numerator   = src_data.variables['transpiration'][0] + src_data.variables['evaporation_canopy'][0]
    var_numerator  += src_data.variables['evaporation_soil'][0]
    var_denominator = src_data.variables['precipitation_forcing'][0]
  elif metrics.upper() == 'ROVERP':
    var_numerator   = src_data.variables['runoff_surface'][0] + src_data.variables['runoff_baseflow'][0]
    var_denominator = src_data.variables['precipitation_forcing'][0]
  elif metrics.upper() == 'TOVERET':
    if 'GLEAM' in model.upper():
      var_numerator    = src_data.variables['Et'][month]
#     var_denominator  = src_data.variables['E'][month]
      var_denominator  = src_data.variables['Et'][month] + src_data.variables['Eb'][month]
      var_denominator += src_data.variables['Es'][month] + src_data.variables['Ei'][month]
    else:
      var_numerator   = src_data.variables['transpiration'][0]
      var_denominator = src_data.variables['transpiration'][0] + src_data.variables['evaporation_canopy'][0]
      var_denominator += src_data.variables['evaporation_soil'][0]
  else:
    print("Metrics: ",metrics.upper())
    sys.exit("Error: not implemented metrics")
# print("shape: ",var_numerator.shape)

  if option.upper() == 'AM':
    # calculate the metrics, then average the metrics over a domain defined by the mask
    idx = var_numerator[:]/var_denominator[:]
    for rid in range(len(masks)):
      vmask = src_mask.variables[masks[rid]][:]
      var_idx[rid] = np.nansum(idx[:]*vmask)/np.nansum(vmask)*100.
#     print(rid, var_idx[rid])
  elif option.upper() == 'MA':
    # average the data over a domain, then calculate the metrics from the averages
    for rid in range(len(masks)):
      vmask = src_mask.variables[masks[rid]][:]
      sum_numerator   = np.nansum(var_numerator[:]*vmask)
      sum_denominator = np.nansum(var_denominator[:]*vmask)
      var_idx[rid] = sum_numerator/sum_denominator*100. if sum_denominator != 0 else np.nan
#     print(rid, var_idx[rid])
  else:
    sys.exit("Error: not implemented option")
  src_data.close()
  if not mfname == None:
    src_mask.close()
  return var_numerator, var_denominator, var_idx

def plot_timeseries(time, avg, masks, models, vname, ofname):
  defaultColors = np.array(['k', 'r', 'b', 'g', 'c', 'm', 'y', 'gray', 'orange', 'purple', 'brown'])
  if ofname == "" or not ofname.endswith('.png'):
    matplotlib.use("TkAgg")

  # Create 3x3 subplots
  fig, axes = plt.subplots(3, 3, figsize=(9, 7))

  # Flatten axes array for easy iteration
  axes = axes.flatten()

  # Plot different lines in each subplot
  for i, ax in enumerate(axes):
    for mid in range(len(models)):
      model = models[mid]
      y = avg[mid,i]
      color = defaultColors[mid%11]
      ax.plot(time, y, color=color, label=model)
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
      if i < 6:
        ax.tick_params(axis='x', labelbottom=False, direction='in', pad=0.01)
      else:
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right",rotation_mode="anchor")
      ax.text(0.5, 0.05, masks[i], fontsize=6, transform=ax.transAxes, verticalalignment='bottom')
  fig.supylabel(vname + "(%)", x = 0.06)
  plt.subplots_adjust(wspace=0.30, hspace=0.04)
  plt.legend()
  if not ofname == "" and ofname.endswith('.png') :
    plt.savefig(ofname)
    print("Ofname: "+ofname)
#   os.system("display "+ofname)
  else:
    plt.show()

if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument('-if', '--ifname',  help="input file path and name",                  required=True)
  ap.add_argument('-mx', '--metrics', help="evaluation metrics",                        required=True)
  ap.add_argument('-mk', '--mask',    help="masks",                                     required=True)
  ap.add_argument('-md', '--model',   help="model names",                               required=True)
  ap.add_argument('-rd', '--rootd',   help="root directory",                            default="")
  ap.add_argument('-of', '--ofname',  help="output file path and name",                 default="")
  ap.add_argument('-op', '--option',  help="AM(avg of metrics) or MA(metrics from avg", default="MA")
  MyArgs = ap.parse_args()

  #read in data and calculate the evaluation metrics
  #time: the x-axis time object
  #var_idx: evaluation metrics with dimensions: models,regions,time
  #masks: names for each mask
  #models: names for each model, test, or reference
  #if ofname ends with ".png", output the figure to the file
  #                    ".nc", output the metrics and its components to a netcdf file
  #if no ofname is given, display the figure to the screen
  time, var_idx, masks, models = calculate_metrics(MyArgs.rootd, MyArgs.ifname, MyArgs.ofname, 
                                   MyArgs.metrics, MyArgs.mask,  MyArgs.option, MyArgs.model)

  #plot the timeseries of the evaluation metrics
  plot_timeseries(time, var_idx, masks, models, MyArgs.metrics, MyArgs.ofname)
  print("The script ended normally!")
