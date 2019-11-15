"""
Created on Sat Nov 14 16:13:13 2015

Generates new data sets where NA are replaced by "*" as expected for Netica.

@author: Miguel
"""

import os
import time
import socket

def on_toy():
    # Machine dependant basic path data
    machine = socket.gethostname()
    if machine == "Gamma-Lap":  # Laptop Miguel
        dirs = {"dir_usr": u"C:\\Users\\equih\\",
                "dir_git": u"Documents\\0 Versiones\\2 Proyectos\\",
                "dir_RB": u"BN_GitHub\\redes_ajuste_MyO\\Gamma\\",
                "dir_wrk": u"Documents\\1 Nubes\\Dropbox\\",
                "dir_dat": u"Datos Redes Bayesianas\\Datos_para_mapeo\\",
                "dir_ShP": u"z:\\2_set_cobertura_completa\\",
                "dir_NETICA": u"C:\\Program Files\\Netica\\Netica 605\\"}
    elif machine == "Capsicum":
        # Descktop Inecol - Miguel
        dirs = {"dir_usr": u"C:\\Users\\equih\\",
                "dir_git": u"Documents\\0 Versiones\\2 Proyectos\\",
                "dir_RB": u"BN_GitHub\\redes_ajuste_MyO\\Gamma\\",
                "dir_wrk": u"Documents\\1 Nubes\\Dropbox\\",
                "dir_dat": u"Datos Redes Bayesianas\\Datos_para_mapeo\\",
                "dir_ShP": u"z:\\2_set_cobertura_completa\\",
                "dir_NETICA": u"C:\\Program Files\\Netica\\Netica 605\\"}
    elif machine == "Equihua":
        # Descktop casa - Julián
        dirs = {"dir_usr": u"E:\\",
                "dir_git": u"repositories\\",
                "dir_RB": u"BayesianNetworks\\redes_ajuste_MyO\\Final\\",
                "dir_wrk": u"work\\20150720_infys_modis\\",
                "dir_dat": u"training_tables_20151006\\products\\",
                "dir_NETICA": u"E:\\software\\Netica\\Netica 605\\"}
    else:
        dirs = {}
        print("Don't know where am I!!!!")

    return dirs

directorios = on_toy()
dir_usr = directorios["dir_usr"]
dir_wrk = directorios["dir_wrk"]
dir_dat = directorios["dir_dat"]
dir_ShP = directorios["dir_ShP"]

archivos_datos_en_z = [fl for fl in sorted(os.listdir(dir_ShP))
                       if fl.startswith("ie_mex_full_dataset")]
print("\n".join(archivos_datos_en_z))

start = time.time()
for file in archivos_datos_en_z:
    with open(dir_ShP + file, "r") as infile,\
         open(dir_usr + dir_wrk + dir_dat + "NA_replaced_" + file, "w") as outfile:
        data_tabla = infile.read()
        print("\nLectura terminada (s): ", time.time() - start)
        start = time.time()
        data_tabla = data_tabla.replace("NA", "*")
        print("Conversión terminada (s): ", time.time() - start)
        start = time.time()
        outfile.write(data_tabla)
        print("Escritura terminada (s): ", time.time() - start)
        start = time.time()

print("Fin")
print (time.time()- start)
