# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:42:48 2016

@author: cmunoz
"""

import sys
import re
import logging
#
#reload(sys)  
#sys.setdefaultencoding('utf8')
sys.path.append('/home/cmunoz/Documents/programming/PythonScripts/python_packages/lib/python2.7/site-packages/')
import psycopg2


def getAttsFromDB(QCvarToPlot_name):
    
    #Error Velocity Information
    qc_variable_name = 'QC_VEL_ERR'
    qc_test_catalog_id = str(22)
    velErrParamValue = queryOneQCparamToDB(qc_test_catalog_id, qc_variable_name)
  
    #Percentage Good Velocity Information
    qc_variable_name = 'QC_PERG_VEL'
    qc_test_catalog_id = str(21)
    pergVelParamValue = queryOneQCparamToDB(qc_test_catalog_id, qc_variable_name)
    
    #Correlation Magnitude Information
    qc_variable_name = 'QC_CORR_BEAM1'
    qc_test_catalog_id = str(20)
    cmagParamValue = queryOneQCparamToDB(qc_test_catalog_id, qc_variable_name)
    
    #Echo Amplitude Velocity Information
    qc_variable_name = 'QC_AMP_BEAM1'
    qc_test_catalog_id = str(19)
    echoParamValue = queryOneQCparamToDB(qc_test_catalog_id, qc_variable_name)

    
    
    return velErrParamValue, pergVelParamValue, cmagParamValue, echoParamValue;
    
    
def queryOneQCparamToDB(qc_test_catalog_id, qc_variable_name):
    
    reload(sys)  
    sys.setdefaultencoding('utf8')
    conn = psycopg2.connect(dbname='dbname',host='hostname',port='portnumber', user='username', password='password') #define connection
    logging.info('Connecting to database\n	->%s' % (conn))
    cursor = conn.cursor()  # conn.cursor will return a cursor object, you can use this cursor to perform queries
    logging.info('Connected!\n')
    
    cursor.execute('SELECT qc_variable.qc_variable_id FROM processing.qc_variable WHERE qc_variable.qc_variable_name=' + '\''+ qc_variable_name  + '\';')
    varID = cursor.fetchall()
    
    for i in range(0,len(varID)):
        varID_dum = re.findall(r'\d+', str(varID[i]))
        varID_dum = str(varID_dum[0])
        cursor.execute('SELECT qc_test_instance.qc_test_instance_id FROM processing.qc_test_instance WHERE qc_test_instance.qc_test_instance_qc_test_catalog_id=' + qc_test_catalog_id + ' AND qc_test_instance.qc_test_instance_qc_variable_id=' + varID_dum +' AND qc_test_instance.qc_test_instance_bad_flag=4;')
        varTestInstanceID = cursor.fetchall()
        if varTestInstanceID:
            varTestInstanceID = re.findall(r'\d+', str(varTestInstanceID[0]))
            varTestInstanceID = str(varTestInstanceID[0]) 
            break

    
    if varTestInstanceID != []:
        cursor.execute('SELECT qc_parameter.qc_parameter_value FROM processing.qc_parameter WHERE qc_parameter.qc_parameter_qc_test_instance_id=' + varTestInstanceID + ';')
        varParamValue = cursor.fetchall() 
        varParamValue = re.findall(r'\d+', str(varParamValue[0]))
        varParamValue = str(varParamValue[0])
    
        return varParamValue;
    
    else:
        varParamValue = []
        return varParamValue;
    
