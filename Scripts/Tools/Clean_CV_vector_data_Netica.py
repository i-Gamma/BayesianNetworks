# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:50:39 2015

@author: Miguel
"""

import os

# Basic path data
dropbox_dir = "C:/Users/Miguel/Documents/1 Nube/Dropbox/"
# datos_dir = "Datos Redes Bayesianas/CrossValidation_data/Results_bel_vec/"
datos_dir = "Datos Redes Bayesianas/CrossValidation_data/temp/"

# List of files to clean
f_cv = [f for f in os.listdir(dropbox_dir + datos_dir) if "csv" in f]

for a_f in f_cv:
    f = open(dropbox_dir + datos_dir + a_f, "r")
    text = f.readlines()
    f.close()
    var_name = ",".join(["p_delt_vp_{0}".format(i) for i in range(19)]) + "\n"
    data = [",".join(t.strip("(").strip(")\n").split(" ")) +
            "\n" for t in text[1:]]
    f_out = open(dropbox_dir + datos_dir + "clean/" + a_f, "w")
    f_out.writelines(var_name)
    f_out.writelines(data)
    f_out.close()
