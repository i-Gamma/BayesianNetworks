library(R.utils)

machine_set_up <- function ()
{
  machine <- System$getHostname()
  switch (machine,
          "CAPSICUM" = 
          {
            # set working directory
            dir_maps <- "C:/Users/miguel.equihua/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/set_de_Entrenamiento/"
            dir_work <- gsub("set_de_Entrenamiento/", "set_de_Entrenamiento/Stage3", dir_maps)
            setwd(dir_work)
          },
          "IDEAUS" =
          {
            # set working directory
            dir_maps <- "C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/set_de_Entrenamiento/"
            dir_work <- gsub("set_de_Entrenamiento", "set_de_Entrenamiento/Stage3", dir_maps)
            setwd(dir_work)
          },
          "MAQUEO" =
          {
            # set working directory
            dir_maps <- "C:/Users/octavio.maqueo/Dropbox/Datos Redes Bayesianas/set_de_Entrenamiento/"
            dir_work <- gsub("set_de_Entrenamiento", "set_de_Entrenamiento/Stage3", dir_maps)
            setwd(dir_work)
          },
          "TMAQUEO" =
          {
            # set working directory
            dir_maps <- "D:/Dropbox/Datos Redes Bayesianas/Datos Redes Bayesianas/set_de_Entrenamiento/"
            dir_work <- gsub("set_de_Entrenamiento", "set_de_Entrenamiento/Stage3", dir_maps)
            setwd(dir_work)
          }
  )
  return (dir_maps)
}

datos_map <- machine_set_up()

datos <- dir(dir_work)[grepl("bn_test30", dir(dir_work))]
#datos <- paste(datos_map, datos, sep="")
cwd <- getwd()
setwd(dir_work)
test_data <- read.table(datos, sep=",",header=TRUE, na.strings = "*")
compara_delta_vp <- data.frame(test_data["zz_delt_vp"])

nombre_corto <- c("CV_B_EM", "CV_B_Scores", "CV_B_with_extra_ZVH", "CV_B_to_C", 
                  "CV_C_Scores", "Final_Codep", "Final", "full_naive_EM", 
                  "full_naive_scores", "New with zvh to delt_vp", "New")
test <- function ()
{
  ie_archivos <- dir()[grepl("(?:Scores.csv|EM.csv)", dir())]
  resultados <- data.frame(var=nombre_corto, cor=rep(0,length(nombre_corto)))
  i <- 0
  for (r in ie_archivos)
  {
    i <- i + 1
    d <- read.table(r, header=TRUE, sep=",")
    c <- cor(compara_delta_vp, d, use = "complete.obs")
    resultados$cor[i] <- c[1] 
    
  }
  print (resultados)
}

print ("Soften 4")
test()

