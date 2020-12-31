# Rscript - geoprocessing

# Setup -------------------------------------------------------------------

rm(list = ls())
gc()
options(stringsAsFactors = F)

# Packages ----------------------------------------------------------------

if(!require(dplyr)){install.packages("dplyr")}
if(!require(ggplot2)){install.packages("ggplot2")}
if(!require(readr)){install.packages("readr")}
if(!require(rio)){install.packages("rio")}

# Get the real data
bc_data <- readr::read_csv('data/bc_imoveis_filtered_d20201115.csv')
sapply(bc_data, unique)
dim(bc_data)

bc <- bc_data %>%
    dplyr::mutate(garages=replace(garages, garages=="--", 0)) %>%
    dplyr::mutate(garages=as.numeric(garages)) %>%
    dplyr::filter(
        garages<=6,
        bathrooms<=6,
        bedrooms<=6,
        area>=30 & area<=300
    )

# dplyr::glimpse(bc)
# length(bc$address)

rio::export(bc, 'data/bc_imoveis_filtered_clean.csv')
