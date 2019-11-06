data.dir <- "C:/Users/equih/Documents/1 Nubes/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/"
data.file <- list.files(data.dir, pattern = "bn_ie_tabfinal_20150830")[1]
data.red <- list.files(data.dir, pattern = "prueba_RB_3_capas_5")[1]
datos <- read.csv(paste(data.dir, data.file, sep="/"), na.strings = "*", stringsAsFactors = FALSE)

# Estrategia TAN a partir de estructura completa
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"
cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

# Estrategia hacia adelante a partir de estructura mínima
data.red <- list.files(data.dir, pattern = "Mínima_RB_3_capas_37")[1]
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"
cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

# He venido agregando nodos utilizando los valores de sensibilidad en la completa como
# una indicación de la importancia potencial de la variable. Noto que a veces al introducir un
# nodo, la capacidad predictiva de la red disminuye, pero mejora al incorporar vínculos
# con otros nodos en la red.
# Mi mejor modelo es el 37 que es el que está en el directorio Gamma: 0.7516247


# Estrategia hacia adelante a partir de estructura mínima con TAN automático sobre delta_vp como arranque
data.red <- list.files(data.dir, pattern = "TAN_RB_6")[1]
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"
cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

# TAN inicial (1)  no precondiciones y no contexto: 0.6325401
# TAN (2) con precondiciones y no contexto: 0.7371454
# TAN (3) con precondiciones y no contexto sólo zvh31: 0.7354305
# TAN (4) con precondiciones y contexto sólo DEM30 media: 0.7461769
# TAN (5) con precondiciones y contexto sólo DEM30 media y SD: 0.7508099
# TAN (6) con precondiciones y contexto todo: zvh, DEM30 media y SD: 0.7480481


# Estrategia hacia adelante a partir de estructura mínima con TAN automático sobre zvh como arranque
data.red <- list.files(data.dir, pattern = "TAN_ZVH_RB_6")[1]
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"
cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

# TAN_ZVH inicial (1)  no precondiciones: 0.6530151
# TAN_ZVH (2) con precondiciones no DEM30 media ni SD: 0.7362328
# TAN_ZVH (3) con precondiciones y DEM30 media no SD: 0.7376833
# TAN_ZVH (4) con precondiciones y DEM30 SD no media: 0.743796
# TAN_ZVH (5) con precondiciones y DEM30 media, SD: 0.7475894

# Estrategia hacia adelante a partir de todos los nodos con TAN automático sobre zvh como arranque
data.red <- list.files(data.dir, pattern = "TAN_all_nodes_RB_6")[1]
esperados <- read.csv(paste(data.dir, data.red, sep="/"), na.strings = "*", stringsAsFactors = FALSE)
names(esperados) <- "E.delta_vp"
cor(datos$zz_delt_vp, round(esperados$E.delta_vp, 0), use = "complete")

# TAN_all inicial (1)  no precondiciones: 0.6905657
# TAN_all (2) con precondiciones no DEM30 media ni SD: 0.7373216
# TAN_all (3) con precondiciones y DEM30 media no SD: 0.7457737
# TAN_all (4) con precondiciones y DEM30 SD no media: 0.7460076 
# TAN_all (5) con precondiciones y DEM30 media, SD: 0.7571537
# TAN_all (6) con precondiciones y DEM30 media, SD sin Gpp_dry_sd: 0.7557835







