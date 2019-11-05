data.dir <- "C:/Users/equih/Documents/1 Nubes/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/"
data.file <- list.files(data.dir, pattern = "bn_ie_tabfinal_20150830")[1]
data.red <- list.files(data.dir, pattern = "prueba_RB_3_capas_4")[1]

# Estrategia TAN a partir de estructura completa
datos <- read.csv(paste(data.dir, data.file, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"

cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

# Estrategia hacia adelante a partir de estructura mínima
data.red <- list.files(data.dir, pattern = "Mínima_RB_3_capas")[1]
datos <- read.csv(paste(data.dir, data.file, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"

cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

