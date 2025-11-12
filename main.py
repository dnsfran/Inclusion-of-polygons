#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from geo.point import Point
from tycat import read_instance


def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """

    n = len(polygones)
    l_poly_tuples = []

    #Construit une liste contenant les tuples de la forme (aire, numéro du polygone, quadrant) de chaque polygone.
    for i in range(n):
        p = polygones[i]
        l_poly_tuples.append((abs(p.area()),i,p.bounding_quadrant()))
    
    l_poly_tuples.sort()

    res = [-1 for _ in range (n)]

    for i,poly_tuple in enumerate(l_poly_tuples):
        poly_act=polygones[poly_tuple[1]]
        for j in range(i+1,n):
            if poly_tuple[2].inclusion_quadrant(l_poly_tuples[j][2]):
                if point_interieur_poly(poly_act.points[0],polygones[l_poly_tuples[j][1]]):
                    res[poly_tuple[1]]=l_poly_tuples[j][1]
                    break


    return res

def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)





def point_interieur_poly(pt,poly):
    """
    Renvoie True si le point est à l'intérieur du poly
    Le fonctionnement est de voir si le nombre de segments
    traversés lorsqu'on avance dans une direction indéfiniment
    est pair ou impair. Si il est impair alors le point est 
    à l'intérieur du polygone.
    """
    compteur = 0
    segments_a_considerer=selection_segments(pt,poly)

    for segment in segments_a_considerer:
        if segment_croise(pt,segment):
            compteur +=1
    
    if (compteur%2) == 1:
        return True
    
    return False

def segment_croise(pt,segment):
    """"
    Renvoie True si le segment formé par un point à l'infini
    et pt croise segment
    """
    if segment.is_vertical():
        return False

    if min([segment.endpoints[0].coordinates[1],segment.endpoints[1].coordinates[1]]) > pt.coordinates[1]:
        if segment.endpoints[1].coordinates[0] < pt.coordinates[0] or segment.endpoints[0].coordinates[0] < pt.coordinates[0]:
                return True
        else : return False
    
    
    #On cherche le coefficient directeur et l'abscisse à l'origine de la droite (appelée d) dirigée par le segment passant par celui-ci. (éq de droite : y = ax+b)
    a = (segment.endpoints[0].coordinates[1]-segment.endpoints[1].coordinates[1])/(segment.endpoints[0].coordinates[0]-segment.endpoints[1].coordinates[0])
    b = segment.endpoints[0].coordinates[1] - a * segment.endpoints[0].coordinates[0]

    #On calcule l'ordonnée de l'intersection de la droite d et du segment formé par le point et un point beaucoup plus haut avec la même abscisse.
    y_d = a * pt.coordinates[0] + b
    
    if y_d <= max([segment.endpoints[0].coordinates[1],segment.endpoints[1].coordinates[1]]) and y_d >= min([segment.endpoints[0].coordinates[1],segment.endpoints[1].coordinates[1]]) and y_d > pt.coordinates[1]:
        point_intersection = Point((pt.coordinates[0],y_d))
        if point_intersection == segment.endpoints[0]:
            if segment.endpoints[1].coordinates[0] < point_intersection.coordinates[0]:
                return True
            else : return False
        
        elif point_intersection == segment.endpoints[1]:
            if segment.endpoints[0].coordinates[0] < point_intersection.coordinates[0]:
                return True
            else : return False
        
        else:
            return True
    return False

def selection_segments(pt,poly):
    """
    Renvoie la liste des segments à considérer
    pour  savoir si le point est à l'intérieur 
    du polygone  poly
    """

    selec_segments=[]
    for segment in poly.segments():
        if max([segment.endpoints[0].coordinates[1],segment.endpoints[1].coordinates[1]]) >= pt.coordinates[1]:
            if ((min((segment.endpoints[0].coordinates[0],segment.endpoints[1].coordinates[0])) <= pt.coordinates[0]) and (max((segment.endpoints[0].coordinates[0],segment.endpoints[1].coordinates[0])) >= pt.coordinates[0])):
                selec_segments.append(segment)
    return(selec_segments)

if __name__ == "__main__":
    main()
