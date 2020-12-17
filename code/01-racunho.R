# R-script 00-rascunho.R

# Setup -------------------------------------------------------------------
rm(list = ls())
gc()
options(stringsAsFactors = F)
theme_set(ggplot2::theme_minimal())
options(scipen = 666)

# Packages ----------------------------------------------------------------

if(!require(readr)){install.packages("readr")}
if(!require(plyr)){install.packages("plyr")}
if(!require(dplyr)){install.packages("dplyr")}
if(!require(ggplot2)){install.packages("ggplot2")}
if(!require(janitor)){install.packages("janitor")}
if(!require(sf)){install.packages("sf")}
if(!require(sp)){install.packages("sp")}
if(!require(st)){install.packages("st")}
if(!require(leaflet)){install.packages("leaflet")}
if(!require(mongolite)){install.packages("mongolite")}
if(!require(readxl)){install.packages("readxl")}
if(!require(janitor)){install.packages("janitor")}
if(!require(spdep)){install.packages("spdep")}
if(!require(vroom)){install.packages("vroom")}



# Functions ---------------------------------------------------------------

shpToHexagon <- function(shp, cellsize = 0.8, square = F, crs = 4326){
  hex <- sf::st_make_grid(
    shp, 
    cellsize = cellsize, 
    square = square
  ) %>% 
    base::data.frame(., hexagon = paste0("H", stringr::str_pad(1:length(.), 3, pad = "0"))) %>% 
    sf::st_as_sf() %>% 
    sf::st_set_crs(crs)
  return(hex)
}


# Data --------------------------------------------------------------------


shp_bc <- sf::st_read("data/SC_Setores_2019/SC_Setores_2019.shp") %>%
  janitor::clean_names() %>% 
  dplyr::filter(cd_mun == '4202008') %>% 
  dplyr::group_by(cd_mun) %>% 
  dplyr::summarise() %>% 
  shpToHexagon(shp = ., cellsize = .006)
  
# plot(shp_bc["cd_setor"])
# plot(shp_bc["cd_mun"])
plot(shp_bc["hexagon"])
