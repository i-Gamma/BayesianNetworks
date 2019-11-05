# packages
library("raster")
library("rgdal")
library("R.utils")
library("data.table")
library ("ggplot2")
library("reshape")
library("scales")

# Utiliza el comando "net" de DOS para mapear una url a un disco local virtual.
url <- "https://inecol.sharepoint.com/sites/ie-2016/Base_de_datos_IE/3_vars_explicativas/Formato_tabular"
if (!dir.exists("Z:/")) system(paste("net use Z:", url, sep = " "))

dir_datos_bn <- "Z:/"
list.files(dir_datos_bn)
datos_bn <- paste(dir_datos_bn, "2_set_cobertura_completa/ie_time_series.csv", sep="")

# load data
data <- fread(datos_bn, stringsAsFactors = FALSE, showProgress = TRUE)
data_veracruz <- subset(data, subset = state_name == "VERACRUZ DE IGNACIO DE LA LLAVE") 
data_veracruz <- data_veracruz[complete.cases(data_veracruz),]
data_guanajuato <- subset(data, subset = state_name == "GUANAJUATO") 
data_guanajuato <- data_guanajuato[complete.cases(data_guanajuato),]
data_jalisco <- subset(data, subset = state_name == "JALISCO") 
data_jalisco <- data_jalisco[complete.cases(data_jalisco),]
data_aguascalientes <- subset(data, subset = state_name == "AGUASCALIENTES") 
data_aguascalientes <- data_aguascalientes[complete.cases(data_aguascalientes),]


# Calculate the area of each zvh in Veracruz by countink pixels by zvh label
data_veracruz[ , count := .N, by = list(zvh_31)]
zvh_area <- unique (data_veracruz[, c("zvh_31", "count")])
zvh_area$zvh <- paste("zvh", zvh_area$zvh_31, sep = "_")
names(zvh_area) <- c("zvh_31", "area", "zvh")
# Verificación área conocida de Veracruz 71,820 km²
sum(zvh_area$area)
cat("71820  - sum(zvh_area$area) = ", 71820  - sum(zvh_area$area), "\n") 

# head of train data
head(data_veracruz)

# load base raster
base <- raster(paste(dir_datos_bn, "/bov_cbz_km2.tif", sep=""))
plot (base)

# Generate Veracruz maps based on geometry of raster available: "base"
mapas <- names(data_veracruz)[c(3,6:16)]
for (mapa in mapas)
{
  if (mapa == "zvh_31")
    ie <- data_veracruz[,..mapa]
  else
    dato <- data_veracruz[,..mapa] * 100
  
  # ie map
  map_df <- data.frame(x=data_veracruz$x, y=data_veracruz$y, dato)
  coordinates(map_df) <- ~ x + y
  gridded(ie_map_df) <- TRUE
  raster_map <- raster(map_df)
  
  # set projection
  projection(raster_map) <- projection(base)
  plot (raster_map, axes=FALSE, box=FALSE, main = mapa)
  
  # write to disk
  tif_file <- paste(dir_datos_bn, "veracruz/ver_",  mapa, ".tif", sep="")
  ie <- writeRaster(raster_map, filename=tif_file, format="GTiff", overwrite=TRUE)
}

# IE trends
# Overall average of State IE 
promedios_generales <- apply(data_veracruz[, mapas[2:12], with = FALSE], 2, mean)
qplot(2004:2014, promedios_generales, ylim = c(0.4, 0.5), geom = "line")

# Average per life zone
promedios_zvh <- as.data.table(t(aggregate(data_veracruz[,c(6:16)], FUN=mean, 
                              by=list(zvh_31=data_veracruz$zvh_31))))
# First line of average data has the label of zvh
zvh_veracruz <- sapply(as.character(as.integer(promedios_zvh[1,])), 
                      function (x) paste("zvh", x, sep = "_"))
promedios_zvh <-promedios_zvh[2:dim(promedios_zvh)[1],] * 100
promedios_zvh <- cbind(c(2004:2014), promedios_zvh)
names(promedios_zvh) <- c("year", zvh_veracruz)

# Plots
# Zvh trend lines
promedios_zvh_long <- melt(promedios_zvh, id.vars = "year", variable.factor = FALSE,
                           value.name = "ie", variable.name = "zvh")
promedios_zvh_long <- merge(promedios_zvh_long, zvh_area, by.x="zvh", by.y="zvh")

p <- ggplot(promedios_zvh_long, aes(x = year, y = ie, group = zvh)) + 
     geom_line(aes(color=zvh)) + labs(title = "Evolución de la IE en Veracruz")

ggsave(paste(dir_datos_bn, "veracruz/ver_evolución_ie",  mapa, ".jpg", sep=""), p)


# Zvh trend coefficients
trend <- data.table(zvh = names(promedios_zvh[,2:length(promedios_zvh)]), 
                    trend = sapply(promedios_zvh[,2:length(promedios_zvh)], 
                                   function (x) line(x)[[2]][2]), 
                    stringsAsFactors = FALSE)

# Rectangle plot with width proportional to zvh area in Veracruz
# preparation
trend$w <- cumsum(trend$area)
trend$wm <- trend$w - trend$area
trend$wt <- trend$wm + (trend$w - trend$wm)/2

p <- ggplot(trend, aes(ymin = 0)) + 
  labs(title = "Tendencia de cambio entre 2004 y 2014\nen el Índice porcentual de integridad ecosistemica", 
       subtitle = "Veracruz", x = "Zona de vida", y = "Tendencia (D(ie%)/año)") +
  geom_rect(aes(xmin = wm, xmax = w, ymax =trend, fill=zvh)) +
  theme(legend.position="none", plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5), 
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0, size = 0))

ggsave(paste(dir_datos_bn, "veracruz/ver_trends_rect", ".jpg", sep=""), p)

# Simple column plot
p <- ggplot(trend, aes(x = zvh, y = trend)) + 
  labs(title = "Tendencia de cambio entre 2004 y 2014\nen el Índice porcentual de integridad ecosistemica", 
       subtitle = "Veracruz", x = "Zona de vida", y = "Tendencia (D(ie%)/año)") +
  geom_col(aes(fill=zvh)) +
  theme(legend.position="none", plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5), 
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0))

ggsave(paste(dir_datos_bn, "veracruz/ver_trends", ".jpg", sep=""), p)

# Ecosystem integrity in 2014
p <- ggplot(subset(promedios_zvh_long, year == 2014), aes(x = zvh, y = ie)) + 
  labs(title = "Integridad ecosistémica porcentual en 2014", 
       subtitle = "Veracruz", x = "Zona de vida", y = "integridad ecosistémica (%)") +
  geom_col(aes(fill=zvh)) +
  theme(legend.position="none", plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5), 
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0))

ggsave(paste(dir_datos_bn, "veracruz/ver_ie_promedio_2014", ".jpg", sep=""), p)

# ZVH area in Veracruz
p <- ggplot(promedios_zvh_long, aes(x = zvh, y = count, fill = zvh)) + 
  geom_col() + scale_y_continuous(labels = comma)  +
  labs(title = "Cobertura de las zonas de vida", 
       subtitle = "Veracruz", x = "Zona de vida", 
       y = expression(paste("área (", km^{2}, ")"))) +  
  theme(legend.position="none", plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0))
  
ggsave(paste(dir_datos_bn, "veracruz/ver_zvh_area", ".jpg", sep=""), p)
