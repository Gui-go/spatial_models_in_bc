# R Script to manage data into and out of mongoDB

# Setup -------------------------------------------------------------------
rm(list = ls())
gc()


# Packages ----------------------------------------------------------------
if(!require('dplyr')){install.packages('dplyr')}
if(!require('mongolite')){install.packages('mongolite')}


# Credentials -------------------------------------------------------------
mongo_credentials <- config::get(file = "config/globalresource.yml")

tabela_final_v30 <- mongo("collection_teste", url = mongo_credentials$mongoURL)


# All collections
mongo(url = mongo_credentials$mongoURL)$run('{"listCollections":1}')$cursor$firstBatch %>% as_tibble()

# Metadata on a collection
db = mongo(collection = "collection1", url = mongo_credentials$mongoURL)

# Finding the data
data <- db$find()