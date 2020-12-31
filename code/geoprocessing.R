# Rscript - geoprocessing

# Setup -------------------------------------------------------------------

rm(list = ls())
gc()
options(stringsAsFactors = F)
credentials <- config::get(file = "conf/globalresources.yml")

# Packages ----------------------------------------------------------------

if(!require(dplyr)){install.packages("dplyr")}
if(!require(config)){install.packages("config")}
if(!require(ggmap)){install.packages("ggmap")}
if(!require(readr)){install.packages("readr")}
if(!require(rio)){install.packages("rio")}


# Credentials -------------------------------------------------------------

# ?ggmap::register_google # Pacote para adiquirir as geolocalizações
ggmap::register_google(key = credentials[['gplacesAPIkey']]) # Registrar usuário

# TESTE
ggmap::geocode(c("UFSC, Florianópolis, Brasil", "UDESC, Florianópolis, Brasil"))

# Get the real data
bc_data <- readr::read_csv('data/bc_imoveis_filtered_clean.csv')
# sapply(bc_data, unique)

uniqueaddresses <- unique(bc_data$address)

location <- ggmap::geocode(uniqueaddresses)
paste0(nrow(location), " novos pontos de imóveis")

ll <- data.frame(
    address = uniqueaddresses,
    lng = location$lon,
    lat = location$lat
)

rio::export(ll, "data/fetched_geolocation.csv")

ll <- readr::read_csv("data/fetched_geolocation.csv")
bc <- readr::read_csv("data/bc_imoveis_filtered_clean.csv")


bcl <- dplyr::left_join(bc, ll)

summary(bcl)

bcl[complete.cases(bcl), ]

rio::export(bcl, "data/bc_imoveis.csv")
