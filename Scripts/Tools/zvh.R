zvh.lbl <- "NA
Desierto alvar [Templado - Lluvioso]
Desierto alvar [Templado - Muy Lluvioso]
Desierto alvar [Cálido - Muy Lluvioso]
Desierto Templado Cálido [Templado - Seco]
Desierto Subtropical [Cálido - Seco]
Tundra Húmeda subalpina [Templado - Lluvioso]
Tundra Húmeda alpina [Templado - Subhúmedo]
Estepa Espinosa prermontana [Templado - Seco]
Estepa montana [Templado - Seco]
Matorral Desértico [Cálido - Seco]
Matorral Desértico premontano [Cálido - Seco]
Matorral Desértico montano bajo [Templado - Seco]
Bosque Espinoso [Cálido - Seco]
Bosque Muy Seco [Cálido - Subhúmedo]
Bosque Seco premontano [Cálido - Subhúmedo]
Bosque Seco montano bajo [Templado - Subhúmedo]
Bosque Subhúmedo [Cálido - Lluvioso]
Bosque Subhúmedo premontano [Cálido - Lluvioso]
Bosque Subhúmedo montano [Templado - Subhúmedo]
Bosque Subhúmedo subalpino [Templado - Seco]
Bosque Subhúmedo subalpino [Templado - Subhúmedo]
Bosque Húmedo premontano [Cálido - Lluvioso]
Bosque Húmedo montano bajo [Templado - Lluvioso]
Bosque Húmedo montano [Templado - Lluvioso]
Bosque Húmedo subalpino [Templado - Lluvioso]
Bosque Lluvioso [Cálido - Muy Lluvioso]
Bosque Lluvioso premontano [Cálido - Muy Lluvioso]
Bosque Lluvioso montano bajo [Cálido - Muy Lluvioso]
Bosque Lluvioso montano bajo [Templado - Muy Lluvioso]
Bosque Lluvioso montano [Cálido - Muy Lluvioso]
Bosque Lluvioso montano [Templado - Muy Lluvioso]"

# Read zvh legend for QGis
zvh.dir <- "C:/Users/Miguel/Documents/1 Nube/Dropbox/Datos Redes Bayesianas/TIFs/zvh.txt"
zvh.txt <- read.table(zvh.dir, sep=",", skip = 2, 
                      col.names = c("val", "r", "g", "b", "a", "label"))

# zvh labels
zvh.lbl <- unlist(strsplit(zvh.lbl, "\\n"))

zvh.txt$label <- zvh.lbl 
encabezado <- "# Archivo de exportación de mapa de colores generado por QGIS
INTERPOLATION:DISCRETE"
write(encabezado, zvh.dir)
write.table(zvh.txt, zvh.dir, sep=",", col.names = F, row.names = F,
            quote = F, append = T)
