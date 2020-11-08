""""
este metodo para leer csv tiene un error,
    y es que contempla a 'NaN' como un producto
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import functions as f
from apyori import apriori

dataset = pd.read_csv("Market_Basket.csv", header=None, keep_default_na=False, na_values=[""])

min_support = 0.003
min_confidence=0.2
min_lift=3
min_lenght=2

compras = []
for i in range(len(dataset)):
    compras.append([str(dataset.values[i,j]) for j in range(0,20)])

#print (f.cuanto_items(dataset[1]))

rules = apriori(compras, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift, min_length=min_lenght)

results=list(rules)

frame = pd.DataFrame(f.inspect(results), columns=['p2', 'p1', 'Soporte', 'Condianza', 'Lift'])

for x in range(len(frame)):
    print(x, " - Regla: " , frame["p1"][x] , " --> " , frame["p2"][x] ,
          ". Soporte: ", frame["Soporte"][x], ". Confianza: ", frame["Condianza"][x],
          ". Lift: ", frame["Lift"][x])