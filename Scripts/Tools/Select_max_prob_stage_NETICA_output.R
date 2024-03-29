machine_set_up <- function ()
{
  machine <- System$getHostname()
  switch (machine,
          "CAPSICUM" = 
          {
            # set working directory
            dir_maps <- "C:/Users/miguel.equihua/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo", dir_maps)
            setwd(dir_work)
          },
          "TIGRIDIA" =
          {
            # set working directory
            dir_maps <- "C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo", dir_maps)
            setwd(dir_work)
          },
          "MAQUEO" =
          {
            # set working directory
            dir_maps <- "C:/Users/octavio.maqueo/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo", dir_maps)
            setwd(dir_work)
          },
          "TMAQUEO" =
          {
            # set working directory
            dir_maps <- "D:/Dropbox/Datos Redes Bayesianas/Datos Redes Bayesianas/Datos_para_mapeo/"
            dir_work <- gsub("EI_maps", "Datos_para_mapeo", dir_maps)
            setwd(dir_work)
          }
  )
  return (dir_maps)
}

machine_set_up()

datos <- dir()[grepl("^bn_ie_tabfinal", dir())]

train_data <- read.table(datos,sep=",",header=TRUE, na.strings = "*")
compara_delta_vp <- data.frame(train_data["zz_delt_vp"])



ie_archivos <- dir()[grepl("boosted", dir())]

nombre_corto <- c("full naive", "naiveA", "naiveB", "CV_A", "CV_B", "CV_C")

resultados <- data.frame(var=nombre_corto, cor=rep(0,length(nombre_corto)))
i <- 0
for (r in ie_archivos)
{
  i <- i + 1
  d <- read.table(r, header=TRUE, sep=",")
  c <- cor(compara_delta_vp, d, use = "complete.obs")
  resultados$cor[i] <- c[1] 
  
}

ie_naive_archivos <- dir()[grepl("full_naive1", dir())]
d <- read.table(ie_naive_archivos, header=TRUE, sep=",")
x <- max.col(d)
head (x)
hist(x)
cor(compara_delta_vp, x, use = "complete.obs")
