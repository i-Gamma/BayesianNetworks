
# packages
library("raster")
library("rgdal")

# set working directory
setwd("E:/data/Miguel/Integridad")

# load train data
train_data = read.table("bn_ie_tabfinal_20150830.csv",sep=",",header=TRUE)

# head of train data
head(train_data)

# load BN prediction
bn_output = read.table("IE_casi_final_oct3Cd_lat15_TAN.txt",sep=",",header=TRUE)
length(bn_output[,1])

# ie
ie = (max(bn_output[,1])-bn_output[,1])/(max(bn_output[,1]))
head(ie)


# ie map
ie_map_df = data.frame(x=train_data$x,y=train_data$y,ie=ie)
coordinates(ie_map_df)=~x+y
gridded(ie_map_df)=TRUE
ie_raster = raster(ie_map_df)

# load base raster
base = raster("E:/data/base/bov_cbz_km2.tif")

# set projection
projection(ie_raster)=projection(base)

# write to disk
ie <- writeRaster(ie_raster, filename="IE_casi_final_oct3Cd_lat15_TAN.tif", format="GTiff", overwrite=TRUE)

