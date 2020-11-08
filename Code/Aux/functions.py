def cuanto_items(d):
    cant = 0
    for x in range(20):
        if (d.values[1,x]!=''):
            cant+=1
    return cant

def inspect(results):
    rh = [tuple(result[2][0][0]) for result in results]
    lh = [tuple(result[2][0][1]) for result in results]
    supports = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts = [result[2][0][3] for result in results]
    return list(zip(rh, lh, supports, confidences, lifts))