import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from time import time
import re

''' 
    Este algoritmo permite crear reglas de asociacion, a partir de un csv de la forma:
        {Order_ID, Product_Name, Quantity} = [{OrderA, ProductX, 1}, {OrderA, ProductY,1}, {OrderA, ProductF, 1}, ... , {OrderK, ProductJ,1},...]
        
'''

tiempos = []
tt = time()

t = ('Start', time())
tiempos.append(t)


t = ('Read_CSV_Start', time())
tiempos.append(t)

'''
    Levantar el CSV
'''

#Leer CSV
data = pd.read_csv('../../Data/KaggleData_TrainSet_Cluster.csv', encoding='utf-8-sig',  engine='python')


t = ('Read_CSV_End', time())
tiempos.append(t)
print("Ya levante el CSV. Duracion %0.10f segundos" %  (tiempos[-1][1]-tiempos[-2][1]))

#Ver las primeras 10 filas
#print(data.head(10))

#==================================================================================================================================
'''
    Limpieza de datos
'''

t = ('Data_Cleaning_Start', time())
tiempos.append(t)

#Borrar los espacios en blanco del comienzo de una columna:
#data['Product_Name']=data['Product_Name'].str.strip('')

#Castear una columna
#data['Order_ID'] = data['Order_ID'].astype('int64')

#Excluir registros (where order_id <> '2000645')
#data = data[~data['Order_ID'].str.contains('2000645')]

#Excluir registros en los que las compras se hayan realizafdo a las 11am
#data = data[data['Hour_Of_Day'] != 11]

#Solo contemplar registros cuyas compras hayan sido 10am
#data = data[data['Order_Hour_of_Day'] < 14]
#data = data[~data['Order_ID'].str.endswith('9')]
#data = data[~data['Order_ID'].str.endswith('2')]
#data = data[~data['Order_ID'].str.endswith('7')]
#data = data[~data['Order_ID'].str.endswith('5')]
#data = data[~data['Order_ID'].str.endswith('3')]

#Supuesto I
data = data[data['Order_Hour_of_Day'] >= 7]
data = data[data['Order_Hour_of_Day'] <= 20]

#Filtros sobre Clusters
#data = data[data['Cluster_ID'] == 4]

#print(data)

t = ('Data_Cleaning_End', time())
tiempos.append(t)
print("Ya realice la limpieza de Datos. Duracion %0.10f segundos" %  (tiempos[-1][1]-tiempos[-2][1]))


#==================================================================================================================================
'''
    Transformar los datos a una matriz de la forma:
        [{Order_ID, Product_ID},{Quantity}] tq Quantity=1 si el producto fue comprado, 0 si no 
'''

t = ('Transform_Data_Start', time())
tiempos.append(t)

'''
    Modificar 'Product_Name' por 'Aisle' o 'Department' en el caso qeu se quiera generar las reglas sobre los pasillos o categorias. En ese caso, habilitar la funcion encode_data 
'''
market_basket = data.groupby(['Order_ID', 'Product_name'])['Quantity']
market_basket = market_basket.sum().unstack().reset_index().fillna(0).set_index('Order_ID')

#print(market_basket.head(10))

'''
    Mi origen de datos ya tiene la variable Quantity binaria.
    Si originalmente no fuese asi, se deberia transformar, de forma tal que si quantity>=1 => 1, si no 0
    Esto se puede hacer con el siguiente codigo:
        def encode_data(datapoint):
        if datapoint <= 0:
            return 0
        if datapoint >= 1:
            return 1
        
        market_basket = market_basket.applymap(encode_data)
        
    Ademas, tambien se debe ejecutar si agruparamos por aisle o department, ya que una cesta puede tener quantity>1 en estos casos 
        (esto no se da si se agrupa por producto, pues, una regla de negocio dice que no hay dos product_name en una misma cesta)
'''
def encode_data(datapoint):
    if datapoint <= 0:
        return 0
    if datapoint >= 1:
        return 1

market_basket = market_basket.applymap(encode_data)

t = ('Transform_Data_End', time())
tiempos.append(t)

print("Ya transforme los datos. Duracion %0.10f segundos" %  (tiempos[-1][1]-tiempos[-2][1]))

#==================================================================================================================================
'''
    Primer paso de las Reglas de Asociacion: 
        obtener los productos que superen cierto nivel de SOPORTE.
    
    Soporte = 0.03 => Soporte = 3% => <def de Soporte> => Voy a contemplar los productos que aparezcan en, al menos, el 3% de las cestas.
    Si soporte muy grande => muy pocos productos
    Si soporte muy chico => tiempo computacional gigante
    
'''
t = ('Get_Items_Start', time())
tiempos.append(t)
items = apriori(market_basket, min_support=0.020, use_colnames=True)

'''
    Con Soporte=3% obtuve 21 productos:
        Banana -> Soporte = 15%
        Bag of Organic Bananas -> Soporte = 12%
        ...
        Organic Whole String Cheese -> Soporte = 3%
'''
#print(items)
t = ('Get_Items_End', time())
tiempos.append(t)

print("Ya defini los items que cumplen con el soporte. Duracion %0.10f segundos" %  (tiempos[-1][1]-tiempos[-2][1]))

#==================================================================================================================================
'''
    Generar las reglas de asociacion:
        metric -> nombre de la metrica que se quiere utilizar para generar las reglas. 
        min_threshold -> el umbral minimo que tiene que alcanzar esa metrica.
        
        Ver la definicion de la funcion para ver todos los parametros y rangos de umbrales
        Por defecto metrin='confidence', min_threshold=0.8
         
'''

t = ('Get_Rules_Start', time())
tiempos.append(t)

rules = association_rules(items, metric="lift", min_threshold=1.6)

#Imprimir reglas: DataFrame
'''
for i in range(len(rules)):
    print('Regla ',i,":")
    print("     Antecedente: ", rules.values[i, 0])
    print("     Concecuente: ", rules.values[i, 1])
    print("     Soporte Antecedente: ", rules.values[i, 2])
    print("     Soporte Concecuente: ", rules.values[i, 3])
    print("     Soporte (regla): ", rules.values[i, 4])
    print("     Confianza: ", rules.values[i, 5])
    print("     Lift: ", rules.values[i, 6])
    print("     Leverage: ", rules.values[i, 7])
    print("     Conviction: ", rules.values[i, 8])
'''

t = ('Get_Rules_End', time())
tiempos.append(t)

print("Ya genere las reglas, duracion %0.10f segundos" %  (tiempos[-1][1]-tiempos[-2][1]))

#==================================================================================================================================
'''
    Convert rules de tipo [pd DataFrame] ->
        a tipo compras [list]
'''

t = ('Convert_Rules_Start', time())
tiempos.append(t)

compras = []
for i in range(len(rules)):
        compras.append([str(rules.values[i, j]) for j in range(0, 9)])

#Imprimir compras:List

for c in compras:
    print('Regla')
    print("     Antecedente: ", c[0].strip("frozenset({'").strip("'})"))
    print("     Concecuente: ", c[1].strip("frozenset({'").strip("'})"))
    print("     Soporte Antecedente: ", c[2])
    print("     Soporte Concecuente: ", c[3])
    print("     Soporte (regla): ", c[4])
    print("     Confianza: ", c[5])
    print("     Lift: ", c[6])
    print("     Leverage: ", c[7])
    print("     Conviction: ", c[8])


t = ('Convert_Rules_End', time())
tiempos.append(t)

#==================================================================================================================================
'''
    FIN
'''

t = ('End', time())
tiempos.append(t)
print()
print()
print("Tiempo de ejecucion: %0.10f segundos"  % (tiempos[-1][1]-tiempos[0][1]) )
print()
print("Cantidad de Reglas: ", len(compras))
