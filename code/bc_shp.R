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



# Data --------------------------------------------------------------------


bc_shp <- sf::st_read("data/SC_Setores_2019/SC_Setores_2019.shp") %>%
  janitor::clean_names() %>% 
  dplyr::filter(cd_mun == '4202008') %>% 
  dplyr::group_by(cd_mun) %>% 
  dplyr::summarise()

plot(bc_shp['cd_mun'])


sf::write_sf(bc_shp, "bc_shp.shp")
bc_shp <- sf::st_read("data/bc_shp/")
plot(bc_shp['cd_mun'])
