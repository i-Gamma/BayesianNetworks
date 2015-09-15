# Graficación de variables vs. IE por ZVH ---------------------------------
library(ggplot2)
library(R.utils)

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
dir.figs <- "figs/"

# Recover names from clipboard
zvh <- read.table("clipboard", header = F, sep="\t")

datos <- dir()[grepl("^bn_ie_tabfinal", dir())]
data_set_all <- read.table(datos, sep=",",header=TRUE, na.strings = "*")
files_IE <- dir()[grepl("(?:boosted_2_CV_[A-C].csv)", dir(), perl = T)]

nombre_corto <- c("full_naive", "naiveA", "naiveB", "CV_A", "CV_B", "CV_C")


for (f in files_IE)
{
  d <- read.table(f, header=TRUE, sep=",")
  if (f == files_IE[1]) IE <- data.frame(d) else IE <- cbind(IE, d)
}
names(IE) <- nombre_corto
data_set_all <- cbind (data_set_all, IE)

data_set_all$zvh.fact <- factor(x = data_set_all$zvh_31)
nombres <- names(data_set_all)
vars.interes <- c(4,5,8,9,14,15,18,19,21:26,28:45,47,54)

# graficación a destajo
gr <- ggplot(data = data_set_all[complete.cases(data_set_all),])
var.ie <- nombres[48] # Integridad Ecosistémica expresada en porcentaje (100 = deteriorado)
for (i in vars.interes)
{
  var.y <- nombres[i]
  gr.vars <- gr + aes_string(x=var.ie, y=var.y) + 
    geom_point(alpha=1/60, col="blue") + 
    stat_smooth(col="red", method = lm) + 
    facet_grid(facets = . ~ zvh.fact)
  
  nombre.archivo <- file.path(dir.figs,paste("ie_lm_var_",nombres[i],".png", sep=""))
  ggsave(nombre.archivo, gr.vars, width = 11, height = 8)
}
