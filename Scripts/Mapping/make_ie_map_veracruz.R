# packages
library("raster")
library("rgdal")
library ("ggplot2")
library("data.table")
library("scales")

# Utiliza el comando "net" de DOS para mapear una url a un disco local virtual.
url <- "https://inecol.sharepoint.com/sites/ie-2016/Base_de_datos_IE/3_vars_explicativas/Formato_tabular"
if (!dir.exists("Z:/")) system(paste("net use Z:", url, sep = " "))

dir_datos_bn <- "Z:/"
list.files(dir_datos_bn)
datos_bn <- paste(dir_datos_bn, "2_set_cobertura_completa/ie_time_series.csv", sep="")

# Functions to get and process Mexican state data.
get_state_data <- function(state)
{
  print(state)
  data <- subset(data, subset = state_name == state) 
  data <- data[complete.cases(data),]
  return(data)
}

zvh_area <- function(state_data)
{
  state_data[ , count := .N, by = list(zvh_31)]
  zvh_area <- unique(state_data[, c("zvh_31", "count")])
  zvh_area$zvh <- paste("zvh", zvh_area$zvh_31, sep = "_")
  names(zvh_area) <- c("zvh_31", "area", "zvh")
  return(zvh_area)
}


ie_trend_plot <- function(state_data)
{
  promedios_generales <- apply(state_data[, 6:16, with = FALSE], 2, mean)
  p <- qplot(2004:2014, promedios_generales, geom = "line", main = state_data$state_name[1])
}


ie_mean_zvh <- function (state_data)
{
  # Average per life zone
  promedios_zvh <- as.data.table(t(aggregate(state_data[,c(6:16)], FUN=mean, 
                                             by=list(zvh_31=state_data$zvh_31))))
  
  # First line of average data has the label of zvh
  zvh_state <- sapply(as.character(as.integer(promedios_zvh[1,])), 
                      function (x) paste("zvh", x, sep = "_"))
  promedios_zvh <-promedios_zvh[2:dim(promedios_zvh)[1],] * 100
  promedios_zvh <- cbind(c(2004:2014), toupper(substr(state_data$state_name[1], 1,3)), 
                         state_data$state_name[1], promedios_zvh)
  names(promedios_zvh) <- c("year", "state", "state_name", zvh_state)
  
  return(promedios_zvh)  
}


#------------------------------------------------------------

# load data
data <- fread(datos_bn, stringsAsFactors = FALSE, showProgress = TRUE)
data_veracruz <- get_state_data("VERACRUZ DE IGNACIO DE LA LLAVE")
data_aguascalientes <- get_state_data("AGUASCALIENTES")
data_durango <- get_state_data("DURANGO")
data_jalisco <- get_state_data("JALISCO")

# Calculate the area of each zvh in Veracruz by countink pixels by zvh label
zvh_area_veracruz <- zvh_area(data_veracruz)
zvh_area_aguascalientes <- zvh_area(data_aguascalientes)
zvh_area_durango <- zvh_area(data_durango)
zvh_area_jalisco <- zvh_area(data_jalisco)

all_zvh_areas <-list(AGU=zvh_area_aguascalientes, DUR=zvh_area_durango,
                     JAL=zvh_area_jalisco, VER=zvh_area_veracruz) 

# head of data
head(data_veracruz)
head(data_aguascalientes)
head(data_durango)
head(data_jalisco)

# load base raster
base <- raster(paste(dir_datos_bn, "/bov_cbz_km2.tif", sep=""))
plot (base)

# Generate selected State maps based on geometry of raster available: "base"
mapas <- list(data.frame(x=data_veracruz$x, y=data_veracruz$y, data_veracruz$zvh_31), 
              data.frame(x=data_veracruz$x, y=data_veracruz$y, data_veracruz$ie_2014), 
              data.frame(x=data_aguascalientes$x, y=data_aguascalientes$y, data_aguascalientes$zvh_31), 
              data.frame(x=data_aguascalientes$x, y=data_aguascalientes$y, data_aguascalientes$ie_2014), 
              data.frame(x=data_durango$x, y=data_durango$y, data_durango$zvh_31),
              data.frame(x=data_durango$x, y=data_durango$y, data_durango$ie_2014),
              data.frame(x=data_jalisco$x, y=data_jalisco$y, data_jalisco$zvh_31),
              data.frame(x=data_jalisco$x, y=data_jalisco$y, data_jalisco$ie_2014))


for (mapa in mapas)
{
  if (length(grep("zvh_31", names(mapa)))==0)
     mapa[,3] <- mapa[,3] * 100
  
  # Identify State name
  state <- sub(".zvh_31", " ZVH", sub(".ie_2014", " IE_2014", sub("data_", "", names(mapa)[3])))
  state <- paste(toupper(substring(state, 1,1)), substring(state, 2), sep="", collapse=" ")
  
  # ie map
  coordinates(mapa) <- ~ x + y
  gridded(mapa) <- TRUE
  raster_map <- raster(mapa)
  
  # set projection
  projection(raster_map) <- projection(base)
  plot (raster_map, axes=FALSE, box=FALSE, main = state)
  
  # write to disk
  tif_file <- paste(dir_datos_bn, "Estados/", state, ".tif", sep="")
  ie <- writeRaster(raster_map, filename=tif_file, format="GTiff", overwrite=TRUE)
}

# IE trends
# Overall average of State IE
names(all_data)
all_data <- list(data_aguascalientes, data_durango, data_jalisco, data_veracruz)
for (data in all_data)
{
  plot(ie_trend_plot(data))  
}

# Average per life zone
all_promedios_zvh <- vector("list", 0)
all_promedios_zvh_long <- vector("list", 0)
for (data in all_data)
{
  state <- substring(data$state_name[1],1,3)
  all_promedios_zvh[[state]] <- ie_mean_zvh(data)
  zvh_area <- all_zvh_areas[[substring(data$state_name[1],1,3)]]

  promedios_zvh_long <- melt(all_promedios_zvh[[state]], id.vars = c("year", "state", "state_name"), 
                             variable.factor = FALSE, value.name = "ie", variable.name = "zvh")
  all_promedios_zvh_long[[state]] <- merge(promedios_zvh_long, zvh_area, by.x="zvh", by.y="zvh")
  
}

# Plots
# Zvh trend lines
for (prom_state in all_promedios_zvh_long)
{
  state_name_label <- paste(substring(prom_state$state_name[1],1,1), 
                            tolower(substring(prom_state$state_name[1], 2)), sep = "" )
  
  p <- ggplot(prom_state, aes(x = year, y = ie, group = zvh)) + 
    geom_line(aes(color=zvh)) + labs(title = paste("Evolución de la IE en ", 
                                                   state_name_label, sep = ""))
  
  ggsave(paste(dir_datos_bn, "Estados/", prom_state$state[1], "_evolución_ie.jpg", sep=""), p)
  
}


# Zvh trend coefficients
all_trends <- vector("list", 0)
for (promedios in all_promedios_zvh)
{
  zvh_area <- all_zvh_areas[[promedios$state[1]]]
  trend <- data.table(zvh = names(promedios[,4:length(promedios)]),
                      state_name = promedios$state_name[1],
                       trend = sapply(promedios[,4:length(promedios)], function (x) line(x)[[2]][2]),
                       stringsAsFactors = FALSE)
  trend <- merge(trend, zvh_area, by.x="zvh", by.y="zvh")
  all_trends[[promedios$state[1]]] <- trend
}


# Rectangle plot with width proportional to zvh area in Veracruz
# preparation
for (trend in all_trends)
{
  trend$w <- cumsum(trend$area)
  trend$wm <- trend$w - trend$area
  trend$wt <- trend$wm + (trend$w - trend$wm)/2
  
  state_name_label <- paste(substring(trend$state_name[1],1,1), 
                            tolower(substring(trend$state_name[1], 2)), sep = "" )
  
  p <- ggplot(trend, aes(ymin = 0)) + 
    labs(title = "Tendencia de cambio entre 2004 y 2014\nen el Índice porcentual de integridad ecosistemica", 
         subtitle = state_name_label, x = "Zona de vida", y = "Tendencia (D(ie%)/año)") +
    geom_rect(aes(xmin = wm, xmax = w, ymax =trend, fill=zvh)) +
    theme(legend.position="none", plot.title = element_text(hjust = 0.5),
          plot.subtitle = element_text(hjust = 0.5), 
          axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0, size = 0))
  
  ggsave(paste(dir_datos_bn, "Estados/",trend$state_name[1], "_trends_rect", ".jpg", sep=""), p)
}


# Simple column plot
for (trend in all_trends)
{
  trend$w <- cumsum(trend$area)
  trend$wm <- trend$w - trend$area
  trend$wt <- trend$wm + (trend$w - trend$wm)/2
  
  state_name_label <- paste(substring(trend$state_name[1],1,1), 
                            tolower(substring(trend$state_name[1], 2)), sep = "" )

  p <- ggplot(trend, aes(x = zvh, y = trend)) + 
    labs(title = "Tendencia de cambio entre 2004 y 2014\nen el Índice porcentual de integridad ecosistemica", 
         subtitle = state_name_label, x = "Zona de vida", y = "Tendencia (D(ie%)/año)") +
    geom_col(aes(fill=zvh)) +
    theme(legend.position="none", plot.title = element_text(hjust = 0.5),
          plot.subtitle = element_text(hjust = 0.5), 
          axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0))
  
  ggsave(paste(dir_datos_bn, "Estados/",trend$state_name[1], "_trends", ".jpg", sep=""), p)
}


# Ecosystem integrity in 2014
for (prom_state in all_promedios_zvh_long)
{
  state_name_label <- paste(substring(prom_state$state_name[1],1,1),
                            tolower(substring(prom_state$state_name[1], 2)), sep = "" )
  
  p <- ggplot(subset(prom_state, year == 2014), aes(x = zvh, y = ie)) + 
    labs(title = "Integridad ecosistémica porcentual en 2014", 
         subtitle = state_name_label, x = "Zona de vida", y = "integridad ecosistémica (%)") +
    geom_col(aes(fill=zvh)) +
    theme(legend.position="none", plot.title = element_text(hjust = 0.5),
          plot.subtitle = element_text(hjust = 0.5), 
          axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0))
  
  stat3 <- tolower(substring(prom_state$state_name[1],1,3)) 
  ggsave(paste(dir_datos_bn, "Estados/", stat3, "_ie_promedio_2014", ".jpg", sep=""), p)
}


# ZVH area in Veracruz
for (prom_state in all_promedios_zvh_long)
{
  state_name_label <- paste(substring(prom_state$state_name[1],1,1), 
                            tolower(substring(prom_state$state_name[1], 2)), sep = "" )
  p <- ggplot(prom_state, aes(x = zvh, y = area, fill = zvh)) + 
    geom_col() + scale_y_continuous(labels = comma)  +
    labs(title = "Cobertura de las zonas de vida", 
         subtitle = state_name_label, x = "Zona de vida", 
         y = expression(paste("área (", km^{2}, ")"))) +  
    theme(legend.position="none", plot.title = element_text(hjust = 0.5),
          plot.subtitle = element_text(hjust = 0.5),
          axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0))
  
  stat3 <- tolower(substring(prom_state$state_name[1],1,3)) 
  ggsave(paste(dir_datos_bn, "Estados/", stat3, "_zvh_area", ".jpg", sep=""), p)
}
