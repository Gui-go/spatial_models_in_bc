library(dplyr)

bc <- readr::read_csv("data/bc_imoveis_filtered_clean.csv")


lm1 <- lm(price ~ area, data = bc)
lm2 <- lm(price ~ area + garages, data = bc)

summary(lm1)
summary(lm2)
