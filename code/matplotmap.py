import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/bc_imoveis.csv')

BBox = ((df.lng.min(),   df.lng.max(), df.lat.min(), df.lat.max()))

ruh_m = plt.imread('img/map.osm')
