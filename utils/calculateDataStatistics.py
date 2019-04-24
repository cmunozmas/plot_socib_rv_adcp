# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:18:57 2016

@author: cmunoz
"""
import numpy as np
import logging



def calculatePercent(QCvarToPlot, QCvarToPlot_title):

    logging.info('Applying statistics: ' + QCvarToPlot_title)           

    y = np.array(QCvarToPlot)
    QcGoodMeasures = float((y == 1 ).sum())
    QcProbablyGoodMeasures = float((y == 2 ).sum())
    QcProbablyBadMeasures = float((y == 3 ).sum())
    QcBadMeasures = float((y == 4 ).sum())
    QcSpikeMeasures = float((y == 6 ).sum())
    
    QcTotalMeasures = float((y != 9 ).sum())
    
    QcGoodPercentage = float(QcGoodMeasures/QcTotalMeasures)*100
    QcProbablyGoodPercentage = float(QcProbablyGoodMeasures/QcTotalMeasures)*100
    QcProbablyBadPercentage = float(QcProbablyBadMeasures/QcTotalMeasures)*100
    QcBadPercentage = float(QcBadMeasures/QcTotalMeasures)*100
    QcSpikePercentage = float(QcSpikeMeasures/QcTotalMeasures)*100
                       
    return QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage;
    
def calculatePercentFailsInCells(QCvarToPlot, QCvarToPlot_title):
    QcBadPercentage = []
    variablePercentFail = []
    for i in range(0, QCvarToPlot.shape[0]):
        for j in range(0, QCvarToPlot.shape[1]):
            y = np.array(QCvarToPlot)

            QcTotalMeasures = float((y[:,:] == 4 ).sum())
            QcBadMeasures = float((y[:,j] == 4 ).sum())
            QcBadPercentage = float(QcBadMeasures/QcTotalMeasures)*100
            variablePercentFail.append(QcBadPercentage)
        
        return variablePercentFail;
            
    
    
def calculateMeanStdMinMax(var_mask,depth_vector):

    varMean = []
    varStd = []
    varMin = []
    varMax = []
    for i in range(0,len(depth_vector)):   
        
        varMean.append(np.mean(var_mask[i][:]))
        varStd.append(np.std(var_mask[i][:]))
        varMin.append(np.min(var_mask[i][:]))
        varMax.append(np.max(var_mask[i][:]))
   
    return varMean, varStd, varMin, varMax;
    
def calculateMeanStdMinMaxSingleProfile(var, depth_vector):

    varMean = []
    varStd = []
    varMin = []
    varMax = []
    
    for i in range(0,len(depth_vector)):   
        
        varMean.append(np.mean(var))
        varStd.append(np.std(var))
        varMin.append(np.min(var))
        varMax.append(np.max(var))
   
    return varMean, varStd, varMin, varMax;
    
    
def generateStatsFile(statsFile, varToPlot_title, QcGoodPercentage, QcProbablyGoodPercentage, QcProbablyBadPercentage, QcBadPercentage, QcSpikePercentage):
   
    statsFile.write(varToPlot_title + '\n')
    statsFile.write('Good Data: ' + ("%.2f" % QcGoodPercentage) + '%' + '\n')
    statsFile.write('Probably Good Data: ' + ("%.2f" % QcProbablyGoodPercentage) + '%' + '\n')
    statsFile.write('Probably Bad Data: ' + ("%.2f" % QcProbablyBadPercentage) + '%' + '\n')
    statsFile.write('Bad Data: ' + ("%.2f" % QcBadPercentage) + '%' + '\n')
    statsFile.write('Spike Data: ' + ("%.2f" % QcSpikePercentage) + '%' + 2*'\n')
        
    return;
    
