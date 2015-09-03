#******************************************************************************
#  Name: concentrates GeoTIFF input and output capabilities
#  Purpose:  open, close, read and write GeoTIFF rasters
#
#
#  Author: Julian Equihua

import sys
import os
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32, GDT_Int16

def readtif(imagepath):
    gdal.AllRegister()
    inDataset = gdal.Open(imagepath,GA_ReadOnly)
    cols = inDataset.RasterXSize
    rows = inDataset.RasterYSize
    bands = inDataset.RasterCount
    return(inDataset,rows,cols,bands)

def createtif(driver,rows,cols,bands,outpath,data_type=32):
    if data_type==32:
        outDataset = driver.Create(outpath,cols,rows,bands,GDT_Float32)
    elif data_type==16:
        outDataset = driver.Create(outpath,cols,rows,bands,GDT_Int16)
    return(outDataset)

def writetif(outDataset,data,projection,geotransform,order='r'):
    # order controls if the columns or the rows should be considered the observations
    cols = outDataset.RasterXSize
    rows = outDataset.RasterYSize

    if geotransform is not None:
        gt = list(geotransform)
        gt[0] = gt[0] + 0*gt[1]
        gt[3] = gt[3] + 0*gt[5]
        outDataset.SetGeoTransform(tuple(gt))
    if projection is not None:
        outDataset.SetProjection(projection)

    if data.ndim==1:
        outBand = outDataset.GetRasterBand(1)
        outBand.WriteArray(np.resize(data,(rows,cols)),0,0)
        outBand.FlushCache()
    else:
        if order=='r':
            n=np.shape(data)[0]
            for k in range(n):
                outBand = outDataset.GetRasterBand(k+1)
                outBand.WriteArray(np.resize(data[k,:],(rows,cols)),0,0)
                outBand.FlushCache()
        elif order=='c':
            n=np.shape(data)[1]
            for k in range(n):
                outBand = outDataset.GetRasterBand(k+1)
                outBand.WriteArray(np.reshape(data[:,k],(rows,cols)))
                outBand.FlushCache()

    #close the dataset properly
    outDataset = None