# packages
library("raster")
library("rgdal")
library("R.utils")
library("data.table")

# Utiliza el comnado de DOS para mapear una url a un disco local virtual.
url <- "https://inecol.sharepoint.com/sites/ie-2016/Base_de_datos_IE/3_vars_explicativas/Formato_tabular"
if (!dir.exists("Z:/")) system(paste("net use Z:", url, sep = " "))

dir_datos_bn <- "Z:/"
list.files(dir_datos_bn)
datos_bn <- paste(dir_datos_bn, "2_set_cobertura_completa/ie_time_series.csv", sep="")

# load data
data <- fread(datos_bn)
data_veracruz <- subset(data, subset = state_name == "VERACRUZ DE IGNACIO DE LA LLAVE") 
data_veracruz <- data_veracruz[complete.cases(data_veracruz),]

# head of train data
head(data_veracruz)

# load base raster
base <- raster(paste(dir_datos_bn, "/bov_cbz_km2.tif", sep=""))
plot (base)


year <- 2004
for (ie in data_veracruz[,6:16])
{

  # ie map
  ie_map_df <- data.frame(x=data_veracruz$x, y=data_veracruz$y, ie=ie * 100)
  coordinates(ie_map_df) <- ~ x + y
  gridded(ie_map_df) <- TRUE
  ie_raster <- raster(ie_map_df)
  
  # set projection
  projection(ie_raster) <- projection(base)
  plot (ie_raster, axes=FALSE, box=FALSE, main = year)
  
  # write to disk
  tif_file <- paste(dir_datos_bn, "veracruz/ver_",  year, ".tif", sep="")
  ie <- writeRaster(ie_raster, filename=tif_file, format="GTiff", overwrite=TRUE)
  year <- year + 1
}

