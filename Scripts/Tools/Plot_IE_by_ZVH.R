# Graficación de variables vs. IE por ZVH ---------------------------------
library(ggplot2)
#library(R.utils)
library(raster)

machine_set_up <- function ()
{
  machine <- System$getHostname()
  switch (machine,+
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
            dir_maps <- "C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/Mapas_agricultura"
            dir_work <- gsub("Mapas_agricultura", "EI_maps", dir_maps)
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


dirs <- machine_set_up()
dirs <- dir_maps
dirs <- paste(dirs, "2004", sep="/")
setwd("./Stage_3")

dir.figs <- "figs/"
resp_files <- dir(dirs)[grepl("fak.tif$", dir(dirs), perl = T)]
files_plot <- resp_files[grepl("pr_", resp_files, perl = T)]

# Recover names from clipboard
# zvh <- read.table("clipboard", header = F, sep="\t", col.names = "zvh", stringsAsFactors = F)
zvh.r <- raster("C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/TIFs/zvh_31.tif")
zvh.r[zvh.r <= -999] <- NA
head(zvh.r)
plot(zvh.r)
datos <- dir()[grepl("^Final", dir())][1]
data.ie <- raster(datos)
plot(data.ie)

zvh_r <- extend(crop(zvh.r, data.ie), data.ie)
plot(zvh_r)

sb <- brick(data.ie)
sb <- addLayer(sb, zvh_r)
for (f in files_plot)
{
  d <- raster(paste(dirs, f, sep="/"))

  if (extent(d) != extent(data.ie))
  {
    d <- extend(crop(d, data.ie), data.ie)
  }
  sb <- addLayer(sb, d)
}

data.table <- rasterToPoints(sb, spatial = F)
data.table <- data.table[complete.cases(data.table),]
data.table <- data.frame(data.table)
names(data.table)
head(data.table)

data.table$zvh.fact <- factor(data.table$zvh_31, labels = zvh[sort(unique(data.table$zvh_31)),])
templado <- sapply(zvh, function (x) ifelse(grepl("Templado", x), "Templado", "Cálido"))
tc <- data.table$zvh_31
data.table$tc <- templado [tc]


nombres <- names(data.table)
nombres[3] <- "EI"
names(data.table) <- nombres

# graficación a destajo
gr <- ggplot(data = data.table)
var.ie <- nombres[3] # Integridad Ecosistémica o delta_VP
for (i in 5:26)
{
  var.y <- nombres[i]
  gr.vars <- gr + aes_string(x=var.ie, y=var.y) + 
    geom_point(alpha=1/60, col="blue") + 
    stat_smooth(col="red", method = "auto") + 
    facet_grid(facets = . ~ zvh.fact)
  
  nombre.archivo <- file.path(dir.figs, 
                      paste(var.ie, "_", nombres[i],".png", sep=""))
  ggsave(nombre.archivo, gr.vars, width = 22, height = 8, units = "in")
}

nm <- names(data.table[c(3,5:26)])
cr <- by(data.table[c(3,5:26)], data.table$zvh.fact, 
                FUN = function(X) cor(X[,1],X[,2:23], 
                use = "pairwise.complete.obs"))
asoc <- data.frame (t(sapply(cr, cbind)))
names(asoc) <- nm[2:23]
write.table(asoc, "correlations.csv", sep = ",", row.names = T, col.names = T)

regr <- data.frame()
for (i in 2:23)
{
  cr <-  by(data.table[c(3,5:26)], data.table$zvh.fact, 
             FUN = function(X) lm(EI ~ X[,i], data=X))
  if (i == 2)
    regr <- data.frame(t(sapply(cr, coef))[,2])
  else
    regr <- cbind(regr, t(sapply(cr, coef))[,2])
}
names(regr) <- nm[2:23]

write.table(regr, "regr.csv", sep = ",", row.names = T, col.names = T)

