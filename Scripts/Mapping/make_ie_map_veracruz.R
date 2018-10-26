# packages
library("raster")
library("rgdal")
library("R.utils")
library("data.table")

# Utiliza el comando "net" de DOS para mapear una url a un disco local virtual.
url <- "https://inecol.sharepoint.com/sites/ie-2016/Base_de_datos_IE/3_vars_explicativas/Formato_tabular"
if (!dir.exists("Z:/")) system(paste("net use Z:", url, sep = " "))

dir_datos_bn <- "Z:/"
list.files(dir_datos_bn)
datos_bn <- paste(dir_datos_bn, "2_set_cobertura_completa/ie_time_series.csv", sep="")

# load data
data <- fread(datos_bn, stringsAsFactors = FALSE, showProgress = TRUE)
data_veracruz <- subset(data, subset = state_name == "VERACRUZ DE IGNACIO DE LA LLAVE") 
data_veracruz <- data_veracruz[complete.cases(data_veracruz),]

# head of train data
head(data_veracruz)

# load base raster
base <- raster(paste(dir_datos_bn, "/bov_cbz_km2.tif", sep=""))
plot (base)



mapas <- names(data_veracruz)[c(3,6:16)]
for (mapa in mapas)
{
  if (mapa == "zvh_31")
    ie <- data_veracruz[,..mapa]
  else
    dato <- data_veracruz[,..mapa] * 100
  
  # ie map
  map_df <- data.frame(x=data_veracruz$x, y=data_veracruz$y, dato)
  coordinates(map_df) <- ~ x + y
  gridded(ie_map_df) <- TRUE
  raster_map <- raster(map_df)
  
  # set projection
  projection(raster_map) <- projection(base)
  plot (raster_map, axes=FALSE, box=FALSE, main = mapa)
  
  # write to disk
  tif_file <- paste(dir_datos_bn, "veracruz/ver_",  mapa, ".tif", sep="")
  ie <- writeRaster(raster_map, filename=tif_file, format="GTiff", overwrite=TRUE)
}

#

