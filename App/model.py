﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import datetime as dt
import time
import math 
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos
def museoArrayList():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    

    museo= {'artistas': None,
            'obras': None,
            'medio': None,
            "nacionalidad":None,
            'ObrasM': None,
            'ArtistasM': None,
            'constituentID': None,
            'department': None,
            'fechaCompra': None,
            'fechaNacimiento': None}

    museo['artistas'] = lt.newList('ARRAY_LIST')
    museo['obras'] = lt.newList('ARRAY_LIST')    
    museo['ObrasM']=mp.newMap(10000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareObrasByID)
    museo['ArtistasM']=mp.newMap(10000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareArtistaByNombre)
  
    museo['medio'] = mp.newMap(10000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareObrasByMedium )      
    museo['nacionalidad'] = mp.newMap(118, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=cmpNacionalidad )   
    museo['constituentID']=mp.newMap(10000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareObrasByID ) 
    museo['department']=mp.newMap(30000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareObrasByDepartment )

    museo['fechaNacimiento']=mp.newMap(30000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=cmpArtistByDateBirth2 )
    museo['objectID']=mp.newMap(10000, 
                                maptype='CHAINING',
                                loadfactor=4.0,
                                comparefunction=compareObrasByObjectID ) 

    return museo


# Funciones para agregar informacion al catalogo
def crearArtista(nombre, nacionalidad, genero, ano_nacimiento):
    artista = {'nombre': "",
               'nacionalidad': "",
               'genero': "",
               'ano_nacimiento': 0}
    artista['nombre']=nombre
    artista['nacionalidad'] = lt.newList('ARRAY_LIST')
    artista['nacionalidad']=nacionalidad
    artista['genero']=genero 
    artista['ano_nacimiento']=ano_nacimiento

    
    return artista

def crearObra(titulo, artistas, fecha_creacion, medio, fecha_adquisicion, dimensiones):

    obra= {'titulo': " ",
            'artistas': " ",
            'fecha_creacion': " ",
            'medio': " ",
            'fecha_adquisicion': " ",
            'dimensiones': " "}
    obra['titulo']=titulo
    obra['artistas'] = lt.newList('ARRAY_LIST')
    obra['artistas']=artistas
    obra['fecha_creacion']= fecha_creacion
    obra['medio']=medio
    obra['fecha_adquisicion']= fecha_adquisicion
    obra['dimensiones']= dimensiones
    return obra
#Funciones para adicionar al mapa#

def addArtista(museo, artista):
    # Se adiciona el libro a la lista de libros
    lt.addLast(museo['artistas'], artista)
    


def addObra(museo, obra):
    
    lt.addLast(museo['obras'], obra)
   

def addMedio(museo, medio, obra):

    medios = museo['medio']
    existe = mp.contains(medios, medio)
    if existe:
        dupla = mp.get(medios, medio)
        medio_actual = me.getValue(dupla)
    else:
        medio_actual = lt.newList("ARRAY_LIST")
        mp.put(medios, medio, medio_actual)
    lt.addLast(medio_actual, obra)

def addNacionalidad(museo,nacionalidad,obra):
    nacion = museo["nacionalidad"]
    contains = mp.contains(nacion, nacionalidad)
    if contains :
        pareja = mp.get(nacion,nacionalidad)
        actual = me.getValue(pareja)
    else:
        actual = lt.newList("ARRAY_LIST")
        mp.put(nacion, nacionalidad, actual)
    lt.addLast(actual, obra)

def compararID(obra,artista,museo):##TODO
    ID_obra = obra["ConstituentID"][1:-1].split(",")
    lista = lt.newList("ARRAY_LIST")
    for constituent in ID_obra:
        for artista in lt.iterator(museo["artista"]):
            ID_artista = museo["artista"]["ConstituentID"]
            if ID_artista == ID_obra:
                lt.addLast(lista,artista["Nationality"])

def addNombre(museo, nombre, artista):
    medios = museo['ArtistasM']
    existe = mp.contains(medios, nombre)
    if existe:
        dupla = mp.get(medios, nombre)
        medio_actual = me.getValue(dupla)
    else:
        medio_actual = lt.newList("ARRAY_LIST")
        mp.put(medios, nombre, medio_actual)
    lt.addLast(medio_actual, artista)

def addObraById(museo, obra):
    obrasPorID = museo['ObrasM']
    b=str(obra['ConstituentID'])     
    b = b.replace("[", "")
    b = b.replace("]", "")
    c=b.split(",")
    for constituentID in c:
        existe = mp.contains(obrasPorID,constituentID)
        if existe:
            dupla = mp.get(obrasPorID, constituentID)
            ID_actual = me.getValue(dupla)
        else:
            ID_actual = lt.newList("ARRAY_LIST")
            mp.put(obrasPorID, constituentID, ID_actual)
        lt.addLast(ID_actual, obra)
        
def addObraByDepartment(museo,obra,departamento):
    medios = museo['department']
    existe = mp.contains(medios, departamento)
    if existe:
        dupla = mp.get(medios, departamento)
        medio_actual = me.getValue(dupla)
    else:
        medio_actual = lt.newList("ARRAY_LIST")
        mp.put(medios, departamento, medio_actual)
    lt.addLast(medio_actual, obra)

def addObraByObjectID(museo, obra, ObjectID):
    id = museo['objectID']
    existe = mp.contains(id, ObjectID)
    if existe:
        dupla = mp.get(id, ObjectID)
        medio_actual = me.getValue(dupla)
    else:
        medio_actual = lt.newList("ARRAY_LIST")
        mp.put(id, ObjectID, medio_actual)
    lt.addLast(medio_actual, obra)

def addArtistaByDate(museo, obra, fecha):
    medios = museo['fechaNacimiento']
    existe = mp.contains(medios, fecha)
    if existe:
        dupla = mp.get(medios, str(fecha))
        medio_actual = me.getValue(dupla)
    else:
        medio_actual = lt.newList("ARRAY_LIST")
        mp.put(medios, fecha, medio_actual)
    lt.addLast(medio_actual, obra)

# Funciones para creacion de datos

# Funciones de consulta
def darUltimosArtistas(museo):
    b= lt.size(museo)
    listaUltimos= lt.subList(museo, (b-2),3)
    return listaUltimos

def darUltimasObras(museo):
    b= lt.size(museo)
    listaUltimos= lt.subList(museo, (b-2),3)
    return listaUltimos

def darPrimerosArtistas(museo):
    listaUltimos= lt.subList(museo, 1,3)
    return listaUltimos

def darPrimerasObras(museo):
    listaUltimos= lt.subList(museo, 1,3)
    return listaUltimos


def numeroArtistas(museo):
    size= lt.size(museo['artistas'])
    return size

def numeroObras(museo):
    size= lt.size(museo['obras'])
    return size

def obrasPurchase(obras):
    numero=0
    for i in range(1, lt.size(obras)):
        a=lt.getElement(obras, i)
        if 'chase' in a['CreditLine']:
             numero +=1
    return numero


#Requisito 6
def fechasRangoObras(lista, fechai, fechaf):
    size=lt.size(lista)
    listaf=lt.newList('ARRAY_LIST')
    a= int(fechai)
    b= int(fechaf)
    for i in range(1, size+1):
        try:
            obra = lt.getElement(lista,i)
            c= int(obra['Date'])
            if c<=b and c>=a:
                lt.addLast(listaf, obra)
            
        except ValueError:
             pass
        
    return listaf

def metrosObras(area, listaf):
    size=lt.size(listaf)
    metrosOcupados=0
    obras= lt.newList('ARRAY_LIST')
    retorno=lt.newList('ARRAY_LIST')
    
    for i in range(1, size+1):
        a=lt.getElement(listaf, i)
        d=a['Diameter (cm)']
        h=a['Height (cm)']
        w=a['Length (cm)']
        depth= a['Depth (cm)']
        l=a['Width (cm)']
        areaO=0
        if (w==''or w=='0') and (depth=='' or depth=='0') and (d=='' or d=='0') and (h!='' and h!='0') and (l!='' and l!='0') :
            areaO= float(h)*float(l)
            areaO=areaO/100
        if d!='' and d!='0':
            areaO= 3.1416592*((float(d)/2)**2)
            areaO= areaO/100
        if metrosOcupados< area and metrosOcupados+areaO< area:
            metrosOcupados+=areaO
            lt.addLast(obras, a)

    lt.addLast(retorno, obras)
    lt.addLast(retorno, metrosOcupados)
    return retorno


def darPrimerasObras5(museo):

    listaUltimos= lt.subList(museo, 1,5)
    return listaUltimos
            

#Requisito3
def getArtworkByMedio(museo, medio):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    author = mp.get(museo['medio'], medio)
    if author:
        return me.getValue(author)
    return None

def getObrasByArtista(museo, nombre):
    artista= mp.get(museo['Artistas'], nombre)
    if artista:
        return me.getValue(artista)
    return None

def getObrasById(museo, ID):
    constituentId= mp.get(museo['constituentID'], ID)
    if constituentId:
        return me.getValue(constituentId)
    return None

def getArtistaNombre(museo, nombre):
    nombres= mp.get(museo['ArtistasM'], nombre)
    if nombres:
        x=me.getValue(nombres)
        return (lt.getElement(x,1))['ConstituentID']
    return None

def obrasID(museo, id):
    mapa=museo['ObrasM']
    obras=mp.get(mapa, id)                
    lista=me.getValue(obras)
    return lista
        
def clasificarObrasPorTecnica(listaf, tecnica):
    i=1
    size=lt.size(listaf)
    obrasTecnica= lt.newList('ARRAY_LIST')
    while i<=size:
        if lt.getElement(listaf,i)['Medium']==tecnica:
            lt.addLast(obrasTecnica, lt.getElement(listaf,i))
        i+=1
    return obrasTecnica

def listarTecnicas(listaf):
    tecnicas=lt.newList('ARRAY_LIST')
    size=lt.size(listaf)
    for i in range(1, size+1):
        try:
            a=lt.getElement(listaf, i)
            b= a['Medium']
            lt.addLast(tecnicas, b)
            
        except ValueError:
            pass
    return tecnicas

def contarTecnicas(tecnicas):
    duplas = {}
    for i in range(1, lt.size(tecnicas) + 1):
        tecnica = lt.getElement(tecnicas, i)
        if not tecnica in duplas.keys():
            duplas[tecnica] = 1
        else:
            num = duplas[tecnica]
            duplas[tecnica] = num + 1
    return duplas

def tecnicaMasFrecuente(listaT):
    mayor = 0
    tecnica = ""
    for llave in listaT.keys():
        if listaT[llave] > mayor:
            mayor = listaT[llave]
            tecnica = llave
    retorno = lt.newList('ARRAY_LIST')
    lt.addLast(retorno, tecnica)
    lt.addLast(retorno, mayor) 
    return retorno

def darUltimasN(lista, numero):
    
    listaUltimos= lt.subList(lista, 1,numero)
    return listaUltimos


# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArtworkByDateAcquired(artwork1, artwork2):
    """Devuelve True si la DateAquired de artwork1 es menor que la de artwork2
    artwork: Información de la primera obra que incluye su"""
    a= artwork1['DateAcquired']
    b= artwork2['DateAcquired']
    try:
        if a == '':
            artwork1['DateAcquired'] = '2050-12-12'
        if b == '':
            artwork2['DateAcquired'] = '2050-12-12'
        elif a !='' and b!='':
            x= dt.datetime.strptime(a, '%Y-%m-%d')
            y= dt.datetime.strptime(b, '%Y-%m-%d')
            if x<y:
                return True
        else: 
            return False
    except ValueError:
        return False

def cmpArtworkByDate(artwork1, artwork2):
    """Devuelve True si la DateAquired de artwork1 es menor que la de artwork2
    artwork: Información de la primera obra que incluye su"""
    a= artwork1['Date']
    b= artwork2['Date']
    try:
        if a !='' and b!='':
            x= int(a)
            y= int(b)
            if x<y:
                return True
        else: 
            return False
    except ValueError:
        return False

def cmpArtistByDateBirth(artista1, artista2):
    """Devuelve True si la DateAquired de artwork1 es menor que la de artwork2
    artwork: Información de la primera obra que incluye su"""
    a= artista1['BeginDate']
    b= artista2['BeginDate']
    x= int(a)
    y= int(b)
    if x<y:
        return True
    else: 
        return False
def compareObrasByMedium(keyname, medio):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    medioEntry = me.getKey(medio)
    if (keyname == medioEntry):
        return 0
    elif (keyname > medioEntry):
        return 1
    else:
        return -1
def compareArtistaByNombre(keyname, nombre):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    medioEntry = me.getKey(nombre)
    if (keyname == medioEntry):
        return 0
    elif (keyname > medioEntry):
        return 1
    else:
        return -1

def compareObrasByID(keyname, objectID ):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    medioEntry = me.getKey(objectID)
    if (keyname == medioEntry):
        return 0
    elif (keyname > medioEntry):
        return 1
    else:
        return -1
def compareObrasByObjectID(keyname, objectID ):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    medioEntry = me.getKey(objectID)
    if (keyname == medioEntry):
        return 0
    elif (keyname > medioEntry):
        return 1
    else:
        return -1
def cmpArtistByDateBirth2(keyname, fecha):
    medioEntry = me.getKey(fecha)
    if (keyname == medioEntry):
        return 0
    elif (keyname > medioEntry):
        return 1
    else:
        return -1

def compareObrasByDepartment(keyname, departamento ):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    medioEntry = me.getKey(departamento)
    if (keyname == medioEntry):
        return 0
    elif (keyname > medioEntry):
        return 1
    else:
        return -1

def cmpNacionalidad(keyname, nacionalidad):

    nacionEntry = me.getKey(nacionalidad)
    if (keyname == nacionEntry):
        return 0
    elif (keyname > nacionEntry):
        return 1
    else:
        return -1
# Funciones de ordenamiento obras



def sortArrayListMerge(lista):
    merge.sort(lista, cmpfunction=cmpArtworkByDateAcquired)
    merge.sort(lista, cmpfunction=cmpArtworkByDateAcquired)
    return lista

def fechasRango( lista, fechai, fechaf):
    
    listaf=lt.newList('ARRAY_LIST')
    a= dt.datetime.strptime(fechai, '%Y-%m-%d')
    b= dt.datetime.strptime(fechaf, '%Y-%m-%d')
    for i in range(1, lt.size(lista)+1):
        try:
            obra = lt.getElement(lista,i)
            c= dt.datetime.strptime(obra['DateAcquired'], '%Y-%m-%d')
            
            if a<=c<=b:
                lt.addLast(listaf, obra)
            
        except ValueError:
            pass
        
    return listaf


 # Funciones de ordenamiento artistas   

def sortArrayListArtistMerge(lista):
    size = lt.size(lista)
    if size > 1:
        mid = (size // 2)
        """se divide la lista original, en dos partes, izquierda y derecha,
        desde el punto mid."""
        leftlist = lt.subList(lista, 1, mid)
        rightlist = lt.subList(lista, mid+1, size - mid)

        """se hace el llamado recursivo con la lista izquierda y derecha"""
        sortArrayListArtistMerge(leftlist)
        sortArrayListArtistMerge(rightlist)

        """i recorre la lista izquierda, j la derecha y k la lista original"""
        i = j = k = 1

        leftelements = lt.size(leftlist)
        rightelements = lt.size(rightlist)

        while (i <= leftelements) and (j <= rightelements):
            elemi = lt.getElement(leftlist, i)
            elemj = lt.getElement(rightlist, j)
            """compara y ordena los elementos"""
            if cmpArtistByDateBirth(elemj, elemi):  
                lt.changeInfo(lista, k, elemj)
                j += 1
            else:                           
                lt.changeInfo(lista, k, elemi)
                i += 1
            k += 1

        """Agrega los elementos que no se comprararon y estan ordenados"""
        while i <= leftelements:
            lt.changeInfo(lista, k, lt.getElement(leftlist, i))
            i += 1
            k += 1

        while j <= rightelements:
            lt.changeInfo(lista, k, lt.getElement(rightlist, j))
            j += 1
            k += 1
    return lista

def fechasRangoArtista(museo, fechai, fechaf):
    lista=museo['fechaNacimiento']
    anio=fechai
    listaf=lt.newList('ARRAY_LIST')
    inicial=int(fechai)
    final= int(fechaf)
    anio=inicial
    while anio<=final:
        a=str(anio)
        artistas=mp.get(lista, a)
        c=me.getValue(artistas)
        for i in range(1, lt.size(c)+1):
            artista=lt.getElement(c, i)
            lt.addLast(listaf, artista)
            
        b=int(anio)
        anio=b+1
    return listaf


#Requerimiento 5
def obraDepartamento(museo, departamento):
    mapa=museo['department']
    obras=mp.get(mapa,departamento)
    lista=me.getValue(obras)
    return lista



def precioObra (obras):
    llaves = lt.newList("ARRAY_LIST")
    lt.addLast(llaves, "Circumference (cm)")
    lt.addLast(llaves, "Depth (cm)")
    lt.addLast(llaves, "Diameter (cm)")
    lt.addLast(llaves, "Height (cm)")
    lt.addLast(llaves, "Length (cm)")
    lt.addLast(llaves, "Width (cm)")
    for j in range(1,lt.size(obras)+1):
        obra = lt.getElement(obras, j)
        valores = lt.newList("ARRAY_LIST")
        for i in range(1, lt.size(llaves)+1):
            llave = lt.getElement(llaves, i)
            try: 
                atributo = float(obra[llave])/100
            except ValueError:
                atributo = 0.0
            lt.addLast(valores, atributo)
        
        costo = lt.getElement(valores, 1)*math.pi*18

        area_plan = lt.getElement(valores, 4)*lt.getElement(valores, 6)*72
        profundidad = lt.getElement(valores, 2)
        ancho = lt.getElement(valores, 5)
    
        if  ancho != 0 and profundidad == 0:
            area_plan = ancho
        if  profundidad  != 0:
            area_plan *=profundidad
        if area_plan > costo:
            costo = area_plan
        peso = obra["Weight (kg)"]
        if peso != '':
            peso2 = float(peso)*72
            if  peso2 > costo:
                costo = peso2

        if costo == 0:
            costo = 48
        obra["Costo"] = costo



            
def cmpArtworkByDate(artwork1, artwork2):
    """Devuelve True si la DateAquired de artwork1 es menor que la de artwork2
    artwork: Información de la primera obra que incluye su"""
    a= artwork1['Date']
    b= artwork2['Date']
    try:
        if a !='' and b!='':
            x= int(a)
            y= int(b)
            if x<y:
                return True
        else: 
            return False
    except ValueError:
        return False
def sortArrayListMergeDate(lista):
    size = lt.size(lista)
    if size > 1:
        mid = (size // 2)
        """se divide la lista original, en dos partes, izquierda y derecha,
        desde el punto mid."""
        leftlist = lt.subList(lista, 1, mid)
        rightlist = lt.subList(lista, mid+1, size - mid)

        """se hace el llamado recursivo con la lista izquierda y derecha"""
        sortArrayListMergeDate(leftlist)
        sortArrayListMergeDate(rightlist)

        """i recorre la lista izquierda, j la derecha y k la lista original"""
        i = j = k = 1

        leftelements = lt.size(leftlist)
        rightelements = lt.size(rightlist)

        while (i <= leftelements) and (j <= rightelements):
            elemi = lt.getElement(leftlist, i)
            elemj = lt.getElement(rightlist, j)
            """compara y ordena los elementos"""
            if cmpArtworkByDate(elemj, elemi):  
                lt.changeInfo(lista, k, elemj)
                j += 1
            else:                           
                lt.changeInfo(lista, k, elemi)
                i += 1
            k += 1

        """Agrega los elementos que no se comprararon y estan ordenados"""
        while i <= leftelements:
            lt.changeInfo(lista, k, lt.getElement(leftlist, i))
            i += 1
            k += 1

        while j <= rightelements:
            lt.changeInfo(lista, k, lt.getElement(rightlist, j))
            j += 1
            k += 1
    
    return lista
def darUltimasObras5(museo):
    b= lt.size(museo)
    listaUltimos= lt.subList(museo, (b-4),5)
    return listaUltimos


def cmpArtworkByCost(artwork1, artwork2):
    """Devuelve True si la DateAquired de artwork1 es menor que la de artwork2
    artwork: Información de la primera obra que incluye su"""
    a= artwork1['Costo']
    b= artwork2['Costo']
    try:
        if a !='' and b!='':
            x= float(a)
            y= float(b)
            if x<y:
                return True
        else: 
            return False
    except ValueError:
        return False
def sortArrayListMergeCost(lista):
    size = lt.size(lista)
    if size > 1:
        mid = (size // 2)
        """se divide la lista original, en dos partes, izquierda y derecha,
        desde el punto mid."""
        leftlist = lt.subList(lista, 1, mid)
        rightlist = lt.subList(lista, mid+1, size - mid)

        """se hace el llamado recursivo con la lista izquierda y derecha"""
        sortArrayListMergeCost(leftlist)
        sortArrayListMergeCost(rightlist)

        """i recorre la lista izquierda, j la derecha y k la lista original"""
        i = j = k = 1

        leftelements = lt.size(leftlist)
        rightelements = lt.size(rightlist)

        while (i <= leftelements) and (j <= rightelements):
            elemi = lt.getElement(leftlist, i)
            elemj = lt.getElement(rightlist, j)
            """compara y ordena los elementos"""
            if cmpArtworkByCost(elemj, elemi):  
                lt.changeInfo(lista, k, elemj)
                j += 1
            else:                           
                lt.changeInfo(lista, k, elemi)
                i += 1
            k += 1

        """Agrega los elementos que no se comprararon y estan ordenados"""
        while i <= leftelements:
            lt.changeInfo(lista, k, lt.getElement(leftlist, i))
            i += 1
            k += 1

        while j <= rightelements:
            lt.changeInfo(lista, k, lt.getElement(rightlist, j))
            j += 1
            k += 1
    
    return lista



def pesoObra(obras):
    cuenta = 0
    for i in range(1, lt.size(obras)+1):
        obra=lt.getElement(obras, i)
        peso=obra["Weight (kg)"]
        if peso!='':
            peso= float(peso)
            cuenta += peso
    return cuenta

def sumaPrecios(obras):
    cuenta = 0
    for i in range(1, lt.size(obras)+1):
        obra=lt.getElement(obras, i)
        cuenta += obra["Costo"]
    return cuenta




# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

#requisito2
def crearListaObras(museo):
    a = museo['medio']
    lista = mp.valueSet(a)
    listaf = lt.newList("ARRAY_LIST", cmpfunction=cmpArtworkByID)
    for i in range(1,lt.size(lista)+1):
        actual = lt.getElement(lista,i)
        for j in range(1, lt.size(actual)+1):
            obra = lt.getElement(actual,j)
            if lt.isPresent(listaf,obra) == 0:
                lt.addLast(listaf,obra)
    return listaf


def cmpArtworkByID(artwork1, artwork2):
    """Devuelve True si la DateAquired de artwork1 es menor que la de artwork2
    artwork: Información de la primera obra que incluye su"""
    a= artwork1['ObjectID']
    b= artwork2['ObjectID']
    try:
        if a !='' and b!='':
            if a<b:
                return True
        else: 
            return False
    except ValueError:
        return False