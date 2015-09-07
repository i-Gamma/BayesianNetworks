# packages
library("raster")
library("rgdal")

machine_set_up <- function ()
{
  users <- dir("c:/users")
  if (("Miguel" %in% users) & !("equihu" %in% users))
  {
    # set working directory
    dir_maps <- "C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/mapas/"
    dir_work <- gsub("mapas", "Datos_para_mapeo", dir_maps)
    setwd(dir_work)
  }
  if ("miguel.equihua" %in% users)
  {
    # set working directory
    dir_maps <- "C:/Users/miguel.equihua/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/mapas/"
    dir_work <- gsub("mapas", "Datos_para_mapeo", dir_maps)
    setwd(dir_work)
  }
  if ("escritorio.octavio" %in% users)
  {
    # set working directory
    dir_maps <- "C:/Users/octavio.maqueo/Dropbox/Datos Redes Bayesianas/mapas/"
    dir_work <- gsub("mapas", "Datos_para_mapeo", dir_maps)
    setwd(dir_work)
  }
  if ("lap.octavio" %in% users)
  {
    # set working directory
    dir_maps <- "D:/Dropbox/Datos Redes Bayesianas/Datos Redes Bayesianas/mapas/"
    dir_work <- gsub("mapas", "Datos_para_mapeo", dir_maps)
    setwd(dir_work)
  }
  
  return (dir_maps)
}

dir_maps <- machine_set_up()

# load train data
train_data <- read.table("bn_ie_tabfinal_20150830.csv",sep=",",header=TRUE)

# head of train data
head(train_data)

maps <- dir()[grepl("^EI", dir())]

for (IE_data in maps)
{
  # load BN prediction
  bn_output <- read.table(IE_data, sep=",",header=TRUE)
  length(bn_output[,1])
  
  # ie
  ie <- (max(bn_output[,1])-bn_output[,1])/(max(bn_output[,1]))
  head(ie)
  
  
  # ie map
  ie_map_df = data.frame(x=train_data$x, y=train_data$y, ie=ie)
  coordinates(ie_map_df) <- ~ie_map_df$x + ie_map_df$y
  gridded(ie_map_df) <- TRUE
  ie_raster <- raster(ie_map_df)
  
  # load base raster
  base <- raster("bov_cbz_km2.tif")
  
  # set projection
  projection(ie_raster) <- projection(base)
  plot (ie_raster)
  
  # write to disk
  
  tif_file <- paste(dir_maps, gsub("txt", "tif", IE_data), sep="")
  ie <- writeRaster(ie_raster, filename=tif_file, format="GTiff", overwrite=TRUE)
}

