# packages
library("raster")
library("rgdal")

machine_set_up <- function ()
{ users <- dir("c:/users")
  if grepl("miguel.equihua", users)
  {
    equipo <- "escritorio_miguel"
  }
  return equipo
}


# set working directory
setwd("C:/Users/miguel.equihua/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo")

# load train data
train_data = read.table("bn_ie_tabfinal_20150830.csv",sep=",",header=TRUE)

# head of train data
head(train_data)

# load BN prediction
bn_output = read.table("IE_Naive_Step_n5_zvh31_peinada_sin_medias_oct2_EMBB - copia.txt",sep=",",header=TRUE)
length(bn_output[,1])

# ie
ie = (max(bn_output[,1])-bn_output[,1])/(max(bn_output[,1]))
head(ie)


# ie map
ie_map_df = data.frame(x=train_data$x, y=train_data$y, ie=ie)
coordinates(ie_map_df)=~x+y
gridded(ie_map_df)=TRUE
ie_raster = raster(ie_map_df)

# load base raster
base = raster("bov_cbz_km2.tif")

# set projection
projection(ie_raster)=projection(base)
plot (ie_raster)

# write to disk
dir_maps <- "C:/Users/miguel.equihua/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/mapas/"
tif_file <- paste(dir_maps, "IE_Naive_Step_n5_zvh31_peinada_sin_medias_oct2_EMBB - copia.txt.tif", sep="")
ie <- writeRaster(ie_raster, filename=tif_file, format="GTiff", overwrite=TRUE)

