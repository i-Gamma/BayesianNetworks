# packages
library("raster")
library("rgdal")
library(R.utils)

machine_set_up <- function ()
{
  machine <- System$getHostname()
  switch (machine,
     "CAPSICUM" = 
          {
             # set working directory
             dir_maps <- "C:/Users/miguel.equihua/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/EI_maps/"
             dir_work <- gsub("EI_maps", "Datos_para_mapeo/Stage_3", dir_maps)
             setwd(dir_work)
          },
     "TIGRIDIA" =
          {
            # set working directory
            dir_maps <- "C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/EI_maps/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo/Stage_3", dir_maps)
            setwd(dir_work)
          },
    "MAQUEO" =
          {
            # set working directory
            dir_maps <- "C:/Users/octavio.maqueo/Dropbox/Datos Redes Bayesianas/EI_maps/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo/Stage_3", dir_maps)
            setwd(dir_work)
          },
    "TMAQUEO" =
          {
            # set working directory
            dir_maps <- "D:/Dropbox/Datos Redes Bayesianas/Datos Redes Bayesianas/EI_maps/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo/Stage_3", dir_maps)
            setwd(dir_work)
          }
  )
  return (dir_maps)
}

dir_maps <- machine_set_up()
dir_datos_bn <- gsub("EI_maps/", "Datos_para_mapeo", dir_maps)
datos_bn <- paste(dir_datos_bn, "/bn_ie_tabfinal_20150830.csv", sep="")

# load train data
train_data <- read.table(datos_bn, sep=",", header=TRUE)

# head of train data
head(train_data)

# load base raster
base <- raster(paste(dir_datos_bn, "/bov_cbz_km2.tif", sep=""))
plot (base)

maps <- dir()[grepl("Final", dir())]

for (IE_data in maps[1])
{
  # load BN prediction
  bn_output <- read.table(IE_data, sep=",",header=TRUE)
  length(bn_output[,1])
  
  ie <- (19-bn_output[,1])/19
  head(ie)

  # ie map
  ie_map_df = data.frame(x=train_data$x, y=train_data$y, ie=ie)
  coordinates(ie_map_df) <- ~ x + y
  gridded(ie_map_df) <- TRUE
  ie_raster <- raster(ie_map_df)
  
  # set projection
  projection(ie_raster) <- projection(base)
  plot (ie_raster)
  
  # write to disk
  
  tif_file <- paste(dir_maps, gsub("?:.txt|.csv", "_delt_vp.tif", IE_data), sep="")
  ie <- writeRaster(ie_raster, filename=tif_file, format="GTiff", overwrite=TRUE)
}

