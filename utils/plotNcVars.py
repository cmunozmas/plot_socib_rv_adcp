# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:25:42 2016

@author: cmunoz
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import calendar
import os
import numpy as np
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        
def plotVarsRvAdcp(time, timeConverted, depth, depth_units, title, manufacture_name, 
                   instrument_model, instrument_serial, varToPlot, varToPlot_title, varToPlot_units, QCtrigger, newPath):
    #get indices fo the real data intervals
    timeTrigger = []
    timeTrigger.append(0)
    
    for i in range(1,len(time)-1):
        timeDiffPrev = time[i] - time[i-1]
        timeDiffNext = time[i+1] - time[i]
        timeDiffAbs = abs(timeDiffNext - timeDiffPrev)
    
        if timeDiffAbs > 2000:
            timeTrigger.append(i)
            
    timeTrigger.append(len(time)-1)
    
    j = 0
    while j < len(timeTrigger)-1:
        timeInit = timeTrigger[j]
        timeEnd = timeTrigger[j+1]
        j += 2


        fig = plt.figure()
    
        if QCtrigger == 0 or QCtrigger == 2:
            #automate max and min values for the variable
            VMIN_dum = abs(np.nanmin(varToPlot))
            VMAX_dum = np.nanmax(varToPlot)
            VLIM = [VMIN_dum,VMAX_dum]
            minIndex = VLIM.index(min(VLIM))
            VMIN = VLIM[minIndex]
            #set different colorbars depending on the data type
            if varToPlot_title in ('northward sea water velocity', 'eastward sea water velocity', 'error_sea_water_velocity - Error sea water velocity'):
                varType = 'integerNumbers'
                cmap = plt.cm.get_cmap('bwr', 10)
                VMAX = VMIN
                VMIN = -VMIN 

            else:
                varType = 'wholeNumbers'
                cmap = plt.cm.get_cmap('Greens', 100)
                VMAX = VMAX_dum
                VMIN = VMIN

            
        if QCtrigger == 1:
            cmap = plt.cm.get_cmap('hot_r', 10)
            VMIN = -0.5
            VMAX = 9.5
            
        if QCtrigger == 0 or QCtrigger == 1:
            logging.info('Generating Figures: ' + varToPlot_title ) 
        else:
            logging.info('Generating Figures: qcPass ' + varToPlot_title )
        try:    
        #plot variable      
            plt.pcolor(timeConverted[timeInit:timeEnd], depth, varToPlot[timeInit:timeEnd, :].T,  cmap=cmap, vmin=VMIN, vmax = VMAX)
            
        except ValueError:
            pass

    
        if QCtrigger == 0 or QCtrigger == 2:
            if varType == 'integerNumbers':
                cbar = plt.colorbar(extend='both') #extends colorbar beyond limits of range
            if varType == 'wholeNumbers':
                cbar = plt.colorbar()
            cbar.set_label(varToPlot_units, rotation=90, ha='left')
            
        if QCtrigger == 1:
            cbar = plt.colorbar(ticks=np.arange(0, 10.))
            cbar.ax.set_yticklabels(['0  No QC performed','1  Good data','2  Probably good data','3  Probably bad data','4  Bad data',
                         '5','6  Spike','7','8  Interpolated data','9  Missing data'],fontsize=12)

    
    
        timePlot = timeConverted[timeInit]
        plt.xlabel(str(timePlot.day) + ' - ' + str(calendar.month_name[timePlot.month]) + ' - ' + str(timePlot.year))
        
        plt.ylabel('Depth' + ' (' + depth_units + ')')
       
        plt.title(varToPlot_title.split('-')[-1], fontsize=20, fontweight='bold')
        
        #Add extra space under the figure
        plt.gcf().subplots_adjust(bottom=0.15)
    
        comment = (title +  8*' ' + manufacture_name + ' ' + instrument_model + ' s/n' + instrument_serial)
        fig.text(0.03,-0.05,comment,fontsize=14)
        plt.tight_layout()
        

        
        plt.gca().invert_yaxis()
        fig.autofmt_xdate()
        
        #save figures
        #newPath = r'./figures/' 
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        dateStamp = ('_' + str(timePlot.year) + str(calendar.month_name[timePlot.month]) +  str(timePlot.day))
        
        if QCtrigger == 0 or QCtrigger == 1:
            plt.savefig(newPath + varToPlot_title + dateStamp, bbox_inches='tight')
        else:
            plt.savefig(newPath + 'qcPass_' + varToPlot_title + dateStamp, bbox_inches='tight')
        
        plt.close()
  

def plotDataStatistics(QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage, 
                       title, manufacture_name, instrument_model, instrument_serial, 
                       varMean, varStd, varMin, varMax, varToPlot_title, varToPlot_units, figPath, 
                       velErrParamValue, pergVelParamValue, cmagParamValue, echoParamValue):  
        
        varStdFromMeanPos = []
        varStdFromMeanNeg = []
        for i in range(0,len(varMean)):
            dum = varMean[i] + np.abs(varStd[i])
            varStdFromMeanPos.append(dum)
            dum = varMean[i] - np.abs(varStd[i])
            varStdFromMeanNeg.append(dum)
            
        # The slices will be ordered and plotted counter-clockwise.
        labels = 'Good', 'Probably Good', 'Probably Bad', 'Bad', 'Spike'
        sizes = [QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage]
        colors = ['green', 'yellowgreen', 'gold', 'lightcoral', 'lightskyblue']
        explode = (0.03, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        
#        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
#                autopct='%1.1f%%', shadow=True, startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        
        fig = plt.figure()
        ax = fig.gca()
        
#        if QcProbablyGoodPercentage < 1 or QcProbablyBadPercentage < 1:
#            sizes = [QcGoodPercentage, QcBadPercentage, QcSpikePercentage]
#            colors = ['green', 'lightcoral', 'lightskyblue']
#            labels = 'Good', 'Bad', 'Spike'
#            explode = (0.03, 0, 0)
#            if  QcSpikePercentage < 1 :
#                sizes = [QcGoodPercentage, QcBadPercentage]
#                colors = ['green', 'lightcoral']
#                labels = 'Good', 'Bad'
#                explode = (0.03, 0)
#        ax.pie(sizes, explode=explode, colors=colors,
#        autopct='%1.2f%%', pctdistance=0.6, labeldistance=1.2, shadow=False, startangle=90,
#        radius=0.35, center=(0.5, 0.5), frame=True)
        width = 0.01
        dum = len(sizes)
        x = 0
        plt.bar(x, QcGoodPercentage, width, color='g')
        plt.bar(x+0.01, QcBadPercentage, width, color='r')
        plt.bar(x+0.02, QcProbablyGoodPercentage, width, color='yellowgreen')
        plt.bar(x+0.03, QcProbablyBadPercentage, width, color='gold')
        plt.bar(x+0.04, QcSpikePercentage, width, color='lightskyblue')
        ax.grid(True)
        ax.set_xticklabels([])
        plt.title(varToPlot_title.split('-')[-1], fontsize=20, fontweight='bold')
        plt.legend(labels, loc=4, shadow=True)
#        plt.axis('off')

#        ax.set_xlim((0, 1))
#        ax.set_ylim((0, 1))
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        #ax.set_aspect('equal')



        #Add extra space under the figure
        #plt.gcf().subplots_adjust(bottom=0.15)

        comment = []
        #add metadata in text format under the figure
        if velErrParamValue != []:           
            comment.append('error velocity parameter: ' + str(velErrParamValue) + '\n')
        elif pergVelParamValue != []: 
            comment.append('percentage good parameter: ' + str(pergVelParamValue) + '\n')
        elif  cmagParamValue != []:
            comment.append('correleation magnitude parameter: ' + str(cmagParamValue) + '\n')
        elif echoParamValue != []:
            comment.append('echo amplitude threshold parameter: ' + str(echoParamValue) + '\n') 
            
        #comment = (title +  8*' ' + manufacture_name + ' ' + instrument_model + ' s/n' + instrument_serial)
        fig.text(0.5,0.9,comment[0],fontsize=14)
        plt.tight_layout()
        

        statsPath = figPath + 'stats_Figs/'
        if not os.path.exists(statsPath):
            os.makedirs(statsPath)
        plt.savefig(statsPath + varToPlot_title, bbox_inches='tight')
        
        plt.close()        


def plotVarsRvAdcpInstantProfiles(time, timeConverted, depth, depth_units, title, manufacture_name, 
                                  instrument_model, instrument_serial, echoAmp1, echoAmp2, echoAmp3, echoAmp4, echoAmpMean,
                                  varToPlot_title, varToPlot_units, figPath, timeShot, varMean, varStd, varMin, varMax):                 
                
        fig = plt.figure()               
        plt.plot(echoAmp1[timeShot], depth, 'b--', echoAmp2[timeShot], depth,'b--', echoAmp3[timeShot], depth,'b--', echoAmp4[timeShot], depth, 'b--', echoAmpMean[timeShot], depth, 'r-') 
        
        varStdFromMeanPos = []
        varStdFromMeanNeg = []
        var3StdFromMeanPos = []

        for i in range(0,len(varMean)):
            dum = varMean[i] + np.abs(varStd[i])
            varStdFromMeanPos.append(dum)
            dum = varMean[i] - np.abs(varStd[i])
            varStdFromMeanNeg.append(dum)
            dum = varMean[i] + np.abs(3*varStd[i])
            var3StdFromMeanPos.append(dum)

        plt.plot(varMean, depth, 'k--')
        plt.plot(varStdFromMeanPos, depth, 'g--', varStdFromMeanNeg, depth, 'g--')
        plt.plot(var3StdFromMeanPos, depth, 'r--')
        
        #add legend
        blue_patch = mpatches.Patch(color='blue', label = 'Beam Amplitude')
        black_patch = mpatches.Patch(color='black', label = 'Mean')
        green_patch = mpatches.Patch(color='green', label = 'Standard Deviation')
        red_patch = mpatches.Patch(color='red', label = '3 * Standard Deviation')
        
        plt.legend(handles=[blue_patch, black_patch, green_patch, red_patch], loc=0,fontsize=12)
        
        #Add extra space under the figure
        plt.gcf().subplots_adjust(bottom=0.15)
        #add metadata in text format under the figure
        comment = (title +  8*' ' + manufacture_name + ' ' + instrument_model + ' s/n' + instrument_serial)
        fig.text(0.03,-0.05,comment,fontsize=14)
        plt.tight_layout()
        plt.gca().invert_yaxis()
        plt.ylabel('Depth' + ' (' + depth_units + ')')  
        plt.xlabel('counts')
        plt.title('Profile Intensity', fontsize=20, fontweight='bold')
        
        profilePath = figPath + 'echoAmp_ProfileFigs/'
        if not os.path.exists(profilePath):
            os.makedirs(profilePath)
        plt.savefig(profilePath + 'EchoAmp_Profile_instant_' + str(timeConverted[timeShot]) , bbox_inches='tight')
        plt.close()     
        