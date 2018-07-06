#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import re
from win32com.client import Dispatch
import socket


"""
  Funciones locales para el cálculo de la IE
"""


def lista_nodos_diccionario(BNet):
    # Get the pointer to the set of nodes
    nodesList_p = BNet.Nodes
    # get number of nodes
    nnodes = nodesList_p.Count
    # Collect all node names in network
    node_names = {}
    for i in range(nnodes):
        node_p = nodesList_p[i]   # node_p
        name = node_p.name        # name
        node_names[name] = node_p
    return node_names


def process_on_data_table(net, data_table):
    # Read the beleif values under specified conditions
    net.compile()
    # BELIEF_UPDATE =  0x100 or greater to set AutoUpdate on, 0 is off
    integrity_val = []
    for j in range(data_table.shape[0]):
        net.AutoUpdate = 0
        net.RetractFindings()

        # Use list comprehension to improve performance
        [node_lst[nd].EnterValue(data_table[nd][j]) for nd in data_table.columns if pd.notnull(data_table[nd][j])]
        net.AutoUpdate = 1
        expected_val = node_lst["zz_delt_vp_1"].GetExpectedValue()
        integrity_val.append(100 * (1 - expected_val[0] / 18))
    return integrity_val


def on_toy():
    # Machine dependant basic path data
    machine = socket.gethostname()
    if machine == "ideaus":
        dbx = "C:/Users/equih/Documents/1 Nubes/Dropbox/"
        netica = u"C:/Program Files/Netica/Netica 605/"
        datos = u"Datos Redes Bayesianas/Datos_para_mapeo/"
        red = "C:/Users/equih/Documents/0 Versiones/2 Proyectos/BN_GitHub/redes_ajuste_MyO/Final"

    elif machine == "Capsicum":
        dbx = "C:/Users/equih/Documents/1 Nubes/Dropbox/"
        netica = u"C:/Program Files/Netica/Netica 605/"
        datos = u"Datos Redes Bayesianas/Datos_para_mapeo/"
        red = "C:/Users/equih/Documents/0 Versiones/2 Proyectos/BN_GitHub/redes_ajuste_MyO/Final"
    else:
        dbx, datos, red = "", "", ""
        netica = u"C:/Program Files/Netica/Netica 605/"
        print("Don't know where am I!!!!")

    # Data subdirectory
    return dbx, netica, red, datos

# ----------------------------------------------------

# Find out if a known file configuration is available and set paths accordingly
dir_dbx, dir_netica, red_file, dir_datos = on_toy()
os.listdir(dir_netica)


# Link NETICA COM interface and starts the application
nt = Dispatch("Netica.Application")
print("Welcome to Netica API for COM with Python!")

# Read license to use full NETICA
lic_arch = dir_dbx + dir_datos + "inecol_netica.txt"
licencia = open(lic_arch, "rb").read()
nt.SetPassword(licencia)

# Window status could be: Regular, Minimized, Maximized, Hidden
nt.SetWindowPosition(status="Hidden")

# Display NETICA version
print("Using Netica version " + nt.VersionString)

net_file_name = red_file + u"/Final_net_Scores_codep.neta"

# Prepare the stream to read requested BN
streamer = nt.NewStream(net_file_name)

# ReadBNet 'options' can be one of "NoVisualInfo", "NoWindow",
# or the empty string (means create a regular window)
net = nt.ReadBNet(streamer, "NoVisualInfo")
node_lst = lista_nodos_diccionario(net)

# read table using pandas: all data
os.chdir(dir_dbx + dir_datos)
data_files = os.listdir(dir_dbx + dir_datos)
data_files = [f for f in data_files if "bn" in f]
data = pd.read_csv(data_files[0], na_values="*")
data_table = data[[node for node in node_lst.keys() if "zz_delt" not in node]]
data_table.columns

## Read EI
#os.chdir(dir_dbx + dir_datos)
#data_files = os.listdir(".")
#data_files = [f for f in data_files if "Final" in f]
#data = pd.read_csv(data_files[0], na_values="*")
#data_table["IE"] = (1 - data / 18) * 100

# insert process to predict using data_table
ie_map = process_on_data_table(net, data_table)
f = open(dir_dbx + dir_datos + "IE_test.csv", "w")
f.writelines("\n".join(["IE"] + map(str, ie_map)))
f.close()
print("Resultado guardado en IE_test.csv")

# Se libera el espacio de momoria usado por la red
net.Delete()
