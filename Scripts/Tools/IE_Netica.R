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


# variantes de estimación  de relación IE vs. agric ------------------

estima_dando_datos_promedio <- function ()
{
  val.med <- data.frame(t(rep(NA, 31)))
  names(val.med) <- paste("zvh", 1:31, sep="")
  val.med <- cbind (val.med, p.agr=0:10 / 10)
  for (zi in zonas)
  { 
    RetractNetFindings(ie.net)
    SetNetworkAutoUpdate(ie.net, newautoupdate = F)
    NodeValue(nodos[["zvh_31"]]) <- as.numeric(zi)
    for (nf in nodos.nombres)
    {
      NodeValue(node = nodos[[nf]]) <- resumen[1, nf]
    }
    
    SetNetworkAutoUpdate(ie.net, newautoupdate = T)
    pasos.x <- length(val.med$zvh1) - 1
    for (xi in val.med$p.agr)
    {
      NodeValue(node = nodos[["proporcion_agricultura"]]) <- xi
      delt_vp.esperado <- NodeExpectedValue(nodos[["zz_delt_vp"]])
      val.med[(xi * pasos.x ) + 1, zi] <- (1 - delt_vp.esperado[[1]] / 18) * 100
    }
  }
  return(val.med)  
}

estima_dando_solo_contexto <- function ()
{
  val.med <- data.frame(t(rep(NA, 31)))
  names(val.med) <- paste("zvh", 1:31, sep="")
  val.med <- cbind (val.med, p.agr=0:10 / 10)
  for (zi in zonas)
  { zi <-2
    RetractNetFindings(ie.net)
    SetNetworkAutoUpdate(ie.net, newautoupdate = F)
    NodeValue(nodos[["zvh_31"]]) <- as.numeric(zi)
    SetNetworkAutoUpdate(ie.net, newautoupdate = T)
    pasos.x <- length(val.med$zvh1) - 1
    for (xi in val.med$p.agr)
    {
      NodeValue(node = nodos[["proporcion_agricultura"]]) <- xi
      delt_vp.esperado <- NodeExpectedValue(nodos[["zz_delt_vp"]])
      val.med[(xi * pasos.x ) + 1, zi] <- (1 - delt_vp.esperado[[1]] / 18) * 100
    }
  }
  return(val.med)  
}

estima_dando_esperados <- function ()
{
  CompileNetwork(ie.net)
  val.med <- data.frame(t(rep(NA, 31)))
  names(val.med) <- paste("zvh", 1:31, sep="")
  val.med <- cbind (val.med, p.agr=0:10 / 10)
  pasos.x <- length(val.med$zvh1) - 1
  for (zi in zonas)
  {
    for (xi in val.med$p.agr)
    { 
      SetNetworkAutoUpdate(ie.net, newautoupdate = F)
      RetractNetFindings(ie.net)
      NodeValue(nodos[["zvh_31"]]) <- as.numeric(zi)
      NodeValue(node = nodos[["proporcion_agricultura"]]) <- xi
      SetNetworkAutoUpdate(ie.net, newautoupdate = T)
      for (nf in nodos.nombres)
      {
        if (!grepl("proporcion_agri", nf))
        {
          val.esp <- NodeExpectedValue(nodos[[nf]])
          NodeValue(nodos[[nf]]) <- val.esp
        }
      }
      delt_vp.esperado <- NodeExpectedValue(nodos[["zz_delt_vp"]])
      val.med[(xi * pasos.x ) + 1, zi] <- (1 - delt_vp.esperado[[1]] / 18) * 100
    }
  }
  return(val.med)  
}


# Lectura de datos para dar evidencia ----------
data.file <- "~/1 Nube/Dropbox/Datos Redes Bayesianas/Datos_para_mapeo/bn_ie_tabfinal_20150830.csv"
datos <- read.table(data.file, header = T, sep = ",", na.strings = "*")
resumen <- aggregate(datos[,3:44], by=list(datos$zvh_31), 
                     function (x) mean(x, na.rm=T))
zonas <- sort(unique(datos$zvh_31))


#  Uso de netica ---------------
# Prepara el acceso a la licencia de Netica y entonces 
# la carga para uso sin restricciones
dir_vers <- "~/0 Versiones/2 Proyectos/BayesianNetworks"
dir_api <- "/Scripts/Netica_API/"
lic_file <- paste(dir_vers, dir_api, "Inecol_netica.txt", sep="")
NeticaLicenseKey <- scan(lic_file, "character")
library(RNetica)

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
# Valor esperado y desviaci?n estandar de delta_vp
delt_vp.esperado <- NodeExpectedValue(nodos[["zz_delt_vp"]])
c(media=delt_vp.esperado[[1]], sd=attributes(delt_vp.esperado)[[1]])

# Asignar evidencia en nodos específicos para obtener el valor esperado 
# de la condicón del ecosistema. 

# La inspecciono (es continua, por lo tanto no tiene estados sino niveles)
# y cada nivel tiene su valor de probabilidad o "2"belief"
# NodeLevels(nodos[["zz_delt_vp"]])
# NodeBeliefs(nodos[["zz_delt_vp"]])
# NodeLevels(nodos[["zz_delt_vp"]])[which.max(prob)]
#  NodeValue(nodos[["proporcion_agricultura"]]) <- 0.38
#  NodeValue(nodos[["zvh_31"]]) <- 4
#  NodeBeliefs(nodos[["zvh_31"]])
#  NodeBeliefs(nodos[["zz_delt_vp"]])
#  NodeExpectedValue(nodos[["zz_delt_vp"]])

# Limpio la red de cualquier evidencia que pudiera haber sido dada
RetractNetFindings(ie.net)

# Le asigno datos a los nodos excepto a zz_delt_vp para recuperar
# el valor esperado de delt_vp y lo convierto en IE = 1-delt_vp/18
# c(media=delt_vp.esperado[[1]], sd=attributes(delt_vp.esperado)[[1]]))
#
# Usa las funciones de estimación desarrolladas para las distintas modalidades
valores.medios.prom.gral <- estima_dando_datos_promedio()
valores.medios.cont <- estima_dando_solo_contexto()
valores.medios.esp.cond <- estima_dando_esperados()

zon.names <- names(valores.medios.esp.cond)
graficas <- lapply (zonas, function (x)
  {
     ggplot(valores.medios.esp.cond, aes_string(x="p.agr", y=zon.names[x])) +
         ggtitle("Degradation curve") +
         geom_smooth() +
         labs(x = "agriculture (%)", y = "EI (%)", title = zon.names[x]) +
         scale_y_continuous(limits=c(0, 100)) +
         theme(plot.title = element_text(size = rel(0.9)),
               axis.title.x = element_text(size = rel(0.7)),
               axis.title.y = element_text(size = rel(0.7)))
  }
)

multiplot(plotlist = graficas, cols = 6)

# Libera el espacio de memoria usado por la red bayesiana
DeleteNetwork(ie.net)

ie.values.file <- "../../Datos_para_mapeo/Stage_3/Final_net_Scores.csv"
IE.datos <- (1 - as.numeric(read.table(ie.values.file, 
                            header = T, sep = ",")[,1]) / 18) * 100
datos$IE <- IE.datos

graficas <- lapply (zonas, function (x)
  {
    ggplot(datos[datos$zvh_31==x, c(32, 48)], 
           aes_string(x="proporcion_agricultura", y="IE")) +
      ggtitle("Degradation curve") +
      geom_smooth() +
      labs(x = "agriculture (%)", y = "EI (%)", title = zon.names[x]) +
      scale_y_continuous(limits=c(0, 100)) +
      theme(plot.title = element_text(size = rel(0.9)),
            axis.title.x = element_text(size = rel(0.7)),
            axis.title.y = element_text(size = rel(0.7)))
  }
)

multiplot(plotlist = graficas, cols = 6)
