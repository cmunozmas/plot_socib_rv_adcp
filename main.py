#!/opt/anaconda2/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:19:50 2016

@author: cmunoz
"""

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma
import logging
import io

import sys
sys.path.append("/home/cmunoz/Documents/programming/PythonScripts/plot_socib_rv_adcp/lib/")
import utils.plotNcVars as plotNcVars
import calculateDataStatistics
import dbConnect




plt.style.use('RV_ADCP')
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

commonVarsRvAdcp = ['time','depth']
varsRvAdcp = ['VEL_EAS', 'VEL_NOR', 'VEL_UPW','CUR_SPE', 'VEL_ERR', 'CORR_BEAM1', 'CORR_BEAM2', 'CORR_BEAM3', 'CORR_BEAM4', 'PERG_VEL', 'AMP_BEAM1', 'AMP_BEAM2', 'AMP_BEAM3', 'AMP_BEAM4' ]
QCvarsRvAdcp = ['QC_VEL_EAS','QC_VEL_NOR', 'QC_VEL_UPW','QC_CUR_SPE', 'QC_VEL_ERR', 'QC_CORR_BEAM1', 'QC_CORR_BEAM2', 'QC_CORR_BEAM3', 'QC_CORR_BEAM4', 'QC_PERG_VEL', 'QC_AMP_BEAM1', 'QC_AMP_BEAM2', 'QC_AMP_BEAM3', 'QC_AMP_BEAM4' ]

#varsRvAdcp = ['VEL_EAS', 'VEL_NOR']
#QCvarsRvAdcp = ['QC_VEL_EAS','QC_VEL_NOR']

#dataFile = ("http://thredds.socib.es/thredds/dodsC/research_vessel/current_profiler/socib_rv-scb_rdi001/L1/2019/dep0024_socib-rv_scb-rdi001_L1_2019-03.nc")
dataFile = ("/opt/localProcessing/opendap/observational/research_vessel/current_profiler/socib_rv-scb_rdi001/L1/2019/dep0024_socib-rv_scb-rdi001_L1_2019-03.nc")
with netCDF4.Dataset(dataFile) as nc:
    
    #import metadata from NetCDF file
    title = nc.getncattr('title')
    abstract = nc.getncattr('abstract')
    featureType = nc.getncattr('featureType')
    instrument_serial = nc.getncattr('instrument_serial')
    instrument_model = nc.getncattr('instrument_model')
    manufacture_name = nc.getncattr('manufacture_name')
    
    #import dimension variables from NetCDF file
    time = nc.variables['time'][:]
    time_units = nc.variables['time'].units
    timeConverted = netCDF4.num2date(time, time_units)
    depth = nc.variables['DEPTH_ADCP4'][:]
    depth_units = nc.variables['DEPTH_ADCP4'].units
    
    #create path to save figures and statsFile
    newPath = r'./figures/' 
    #create statsFile to keeep data statistics
    statsFile = io.FileIO(newPath + "stats.txt", "w") 
    statsFile.write('---------------------------' + '\n' +
                    '---- Statistics report ----' + '\n' +
                    '---------------------------'+ 3*'\n')
    
    for i in range(0,len(varsRvAdcp)):
        #load variables and QCvariables
        a = varsRvAdcp[i]
        varToPlot = nc.variables[a][:]
        varToPlot_title = nc.variables[a].long_name
        varToPlot_units = nc.variables[a].units
        a = QCvarsRvAdcp[i]
        QCvarToPlot_name = QCvarsRvAdcp[i]                
        QCvarToPlot = nc.variables[a][:]
        QCvarToPlot_title = nc.variables[a].long_name
        QCvarToPlot_units = []

        #mask variables to show only values flagged as 1 (QC Good Flag)
#        varToPlot_mask_dum = numpy.ma.masked_where(QCvarToPlot == 4, varToPlot)
#        varToPlot_mask_dum1 = numpy.ma.masked_where(QCvarToPlot == 6, varToPlot_mask_dum)
#        varToPlot_mask_dum2 = numpy.ma.masked_where(QCvarToPlot == 9, varToPlot_mask_dum1)
#        varToPlot_mask_dum3 = numpy.ma.masked_where(QCvarToPlot == 3, varToPlot_mask_dum2)
#        varToPlot_mask = numpy.ma.masked_where(np.isnan(varToPlot_mask_dum3), varToPlot_mask_dum3)

        #connect to database to retrieve information relevant to the statistics report
        velErrParamValue, pergVelParamValue, cmagParamValue, echoParamValue = dbConnect.getAttsFromDB(QCvarToPlot_name)
        #save DB info in stats.txt file. Makes it only once
        if i == 0:
            if velErrParamValue != []:
                statsFile.write('RDI_ADCP_ErrorVelocity Test. err_vel parameter: ' + velErrParamValue + '\n')
            elif pergVelParamValue != []:
                statsFile.write('RDI_ADCP_PercentGoodVelocity Test. pgood parameter: ' + pergVelParamValue + '\n')
            elif echoParamValue != []:
                statsFile.write('RDI_ADCP_EchoIntensityVelocity Test. echo_amplitude_threshold parameter: ' + echoParamValue + '\n')
            elif cmagParamValue != []:
                statsFile.write('RDI_ADCP_CorrelationMagnitude Test. cmag parameter: ' + cmagParamValue + '\n') 
            statsFile.write('\n')
       
        
        #obtain variable statistics                          
        QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage = calculateDataStatistics.calculatePercent(QCvarToPlot, QCvarToPlot_title)
        varMean, varStd, varMin, varMax = calculateDataStatistics.calculateMeanStdMinMax(varToPlot_mask, depth)
        
        #add satatistics results to stats.txt file    
        calculateDataStatistics.generateStatsFile(statsFile, varToPlot_title, QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage)
        
        #plot variables
        varToPlot_mask_nan = numpy.ma.masked_where(np.isnan(varToPlot), varToPlot)      
        QCtrigger = 0
        plotNcVars.plotVarsRvAdcp(time, timeConverted, depth, depth_units, 
                                  title, manufacture_name, instrument_model, 
                                  instrument_serial, varToPlot_mask_nan, varToPlot_title, varToPlot_units, QCtrigger, newPath)
        
        #plot QC variables
        QCtrigger = 1                         
        plotNcVars.plotVarsRvAdcp(time, timeConverted, depth, depth_units, 
                                  title, manufacture_name, instrument_model, 
                                  instrument_serial, QCvarToPlot, QCvarToPlot_title, QCvarToPlot_units, QCtrigger, newPath)
                            
##        QCtrigger = 2
#        plotNcVars.plotVarsRvAdcp(time, timeConverted, depth, depth_units, 
#                                  title, manufacture_name, instrument_model, 
#                                  instrument_serial, varToPlot_mask, varToPlot_title, varToPlot_units, QCtrigger, newPath)

#        if varToPlot_title in ('northward sea water velocity', 
#                               'eastward sea water velocity', 
#                               'error_sea_water_velocity - error sea water velocity', 
#                               'sea_water_percent_good_velocity - sea water percent good velocity', 
#                               'sea_water_particle_distribution_correlation_magnitude_from_acoustic_beams - correlation magnitude from beam 1', 'sea_water_particle_distribution_correlation_magnitude_from_acoustic_beams - correlation magnitude from beam 2', 'sea_water_particle_distribution_correlation_magnitude_from_acoustic_beams - correlation magnitude from beam 3', 'sea_water_particle_distribution_correlation_magnitude_from_acoustic_beams - correlation magnitude from beam 4',
#                               'sea_water_noise_amplitude_beam - sea water noise amplitude beam 1','sea_water_noise_amplitude_beam - sea water noise amplitude beam 2', 'sea_water_noise_amplitude_beam - sea water noise amplitude beam 3', 'sea_water_noise_amplitude_beam - sea water noise amplitude beam 4'):                    
#            
#            plotNcVars.plotDataStatistics(QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage, title, manufacture_name, instrument_model, instrument_serial, 
#                                          varMean, varStd, varMin, varMax, varToPlot_title, varToPlot_units, newPath)
#
#
#        
#        if varToPlot_title in ('eastward sea water velocity'):
##            calculateDataStatistics.calculatePercentFailsInCells(QCvarToPlot, QCvarToPlot_title)
#            
#            plotNcVars.plotDataStatistics(QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage, 
#                                          title, manufacture_name, instrument_model, instrument_serial, 
#                                          varMean, varStd, varMin, varMax, varToPlot_title, varToPlot_units, newPath, 
#                                          velErrParamValue, pergVelParamValue, cmagParamValue, echoParamValue)
    
    
## Plot echo amplitude profiles    
#    timeShot = 83      
#    
#    for i, j in enumerate(varsRvAdcp):
#        if j == 'AMP_BEAM1':
#            echoAmp1 = nc.variables[varsRvAdcp[i]][:]
#        elif j == 'AMP_BEAM2':
#            echoAmp2 = nc.variables[varsRvAdcp[i]][:]
#        elif j == 'AMP_BEAM3':
#            echoAmp3 = nc.variables[varsRvAdcp[i]][:]
#        elif j == 'AMP_BEAM4':
#            echoAmp4 = nc.variables[varsRvAdcp[i]][:]
#            
#    echoAmpMean = (echoAmp1 + echoAmp2 + echoAmp3 + echoAmp4) / 4
#    
#    varMean, varStd, varMin, varMax = calculateDataStatistics.calculateMeanStdMinMaxSingleProfile(echoAmp1, depth)
#    
#    plotNcVars.plotVarsRvAdcpInstantProfiles(time, timeConverted, depth, depth_units, title, manufacture_name, 
#                                             instrument_model, instrument_serial, echoAmp1, echoAmp2, echoAmp3, echoAmp4, echoAmpMean,
#                                             varToPlot_title, varToPlot_units, newPath, timeShot, varMean, varStd, varMin, varMax)
           

    



                