#----------------------------------------------
#
# Cálculo de las marginales de delta_vp
# condicional a valores de uso agrícola
#
# Author: Miguel Equihua
# email: equihuam@gmail.com
# Institution: Inecol
#
#-----------------------------------------------

library (ggplot2)

# Prepara el acceso a la licencia de Netica y entonces 
# la carga para uso sin restricciones
dir_vers <- "~/0 Versiones/2 Proyectos/BayesianNetworks"
dir_api <- "/Scripts/Netica_API/"
lic_file <- paste(dir_vers, dir_api, "Inecol_netica.txt", sep="")
NeticaLicenseKey <- scan(lic_file, "character")
library(RNetica)

# Lectura de datos para dar evidencia
data.file <- "~/1 Nube/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/bn_ie_tabfinal_20150830.csv"
datos <- read.table(data.file, header = T, sep = ",", na.strings = "*")
resumen <- aggregate(datos[,3:44], by=list(datos$zvh_31), 
                     function (x) mean(x, na.rm=T))

# Lee la red del disco y la compila en preparación para su uso
net_path <- path.expand(paste(dir_vers, "/redes_ajuste_MyO/Stage_3/", sep=""))
ie.file <- paste(net_path, "Final_net_Scores.neta", sep="")
ie.net <- ReadNetworks(ie.file)
CompileNetwork(ie.net)

# Estos son todos los nodos de la red preparados para su uso en R
nodos <- NetworkAllNodes(ie.net)
nodos.nombres <- names(nodos)

# Elige los nodos de evidencia y omite zz_delt_vp y zvh_31 del conjunto
nodos.nombres <- nodos.nombres[!grepl("z", nodos.nombres)]

# Cálculo de la esperanza del nodo zz_delt_vp
# sin contar con ninguna otra evidencia particular.
# Valor esperado y desviación estandar de delta_vp
delt_vp.esperado <- NodeExpectedValue(nodos[["zz_delt_vp"]])
c(media=delt_vp.esperado[[1]], sd=attributes(delt_vp.esperado)[[1]])

# Asignar evidencia en nodos específicos para obtener el valor esperado 
# de la condición del ecosistema. 

# La inspecciono (es continua, por lo tanto no tiene estados sino niveles)
# y cada nivel tiene su valor de probabilidad o "2"belief"
NodeLevels(nodos[["zz_delt_vp"]])
NodeBeliefs(nodos[["zz_delt_vp"]])

# Limpio la red de cualquier evidencia que pudiera haber sido dada
RetractNetFindings(ie.net)

# Le asigno datos a los nodos excepto a zz_delt_vp para recuperar
# el valor esperado de delt_vp y lo convierto en IE = 1-delt_vp/18
# c(media=delt_vp.esperado[[1]], sd=attributes(delt_vp.esperado)[[1]]))

zonas <- sort(unique(datos$zvh_31))
valores.medios <- data.frame(t(rep(NA, 31)))
names(valores.medios) <- paste("zvh", 1:31, sep="")
valores.medios <- cbind (valores.medios, p.agr=0:10 / 10)
for (zi in zonas)
{ 
  RetractNetFindings(ie.net)
  SetNetworkAutoUpdate(ie.net, newautoupdate = F)
  NodeValue(nodos[["zvh_31"]]) <- as.numeric(zi)
  for (nf in nodos.nombres)
  {
    if (nf != "proporcion_agricultura")
        NodeValue(node = nodos[[nf]]) <- resumen[1, nf]
  }
  
  SetNetworkAutoUpdate(ie.net, newautoupdate = T)
  for (xi in valores.medios$p.agr)
  {
    NodeValue(node = nodos[["proporcion_agricultura"]]) <- xi
    delt_vp.esperado <- NodeExpectedValue(nodos[["zz_delt_vp"]])
    valores.medios[xi + 1, zi] <- 1 - delt_vp.esperado[[1]] / 18
  }
}

zon.names <- names(valores.medios)
graficas <- lapply (zonas, function (x)
  {
     ggplot(valores.medios, aes_string(x="p.agr", y=zon.names[x])) +
         geom_point(shape=1) +    # Use hollow circles
         geom_smooth()
  }
)

multiplot(plotlist = graficas, cols = 6)

p <- ggplot(valores.medios, aes(x=p.agr, y=zvh1)) +
  geom_point(shape=1) +    # Use hollow circles
  geom_smooth() +
p

# Libera el espacio de memoria usado por la red bayesiana
DeleteNetwork(ie.net)
