# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 21:00:06 2015

@author: Miguel
"""

import os
import re
import json

os.listdir(".")

dropbox_dir = "C:/Users/Miguel/Documents/1 Nube/Dropbox/"
datos_dir = "Datos Redes Bayesianas/"

my_dir = "C:/Users/Miguel/Documents/0 Versiones/2 Proyectos/"
results_dir = "BayesianNetworks/redes_ajuste_MyO/"
results_files = os.listdir(my_dir + results_dir)
results_files = [my_dir + results_dir + r for r in results_files if "txt"
                 in r and "EI" in r]
networks = {}
for net_name in results_files:
    net = re.sub(".txt", "", os.path.basename(net_name))
    networks[net] = {}
    f = open(net_name, "r")
    text = f.readlines()
    f.close()

    # Get relevant data
    num_nodes = int([re.findall("[0-9]+", t)[0]
                     for t in text if "Nodes" in t][0])
    rms = [re.findall("rms = [.0-9]+", t)[0] for t in text if "rms = " in t][0]
    networks[net]["Absolute error (rms)"] = re.sub("rms = ", "", rms)
    networks[net]["Error rate (%)"] = [re.findall("[.0-9]+", t)[0]
                                       for t in text if "Error rate" in t][0]
    networks[net]["Logarithmic loss"] = [re.findall("[.0-9]+", t)[0]
                                         for t in text if "thmic loss" in t][0]
    networks[net]["Quadratic loss"] = [re.findall("[.0-9]+", t)[0]
                                       for t in text if "Quadratic" in t][0]
    networks[net]["Spherical payoff"] = [re.findall("[.0-9]+", t)[0]
                                         for t in text if "Spherical" in t][0]

    # Get sensitivity values of variance reduction due to information in a node
    pos_sens = [i for i, v in enumerate(text) if "at another node" in v][0] + 4
    sensibility = {}
    for i in xrange(pos_sens, pos_sens + num_nodes):
        node = [n for n in text[i].split(" ") if n is not ""][0].strip(" ")
        value = [n for n in text[i].split(" ") if n is not ""][1].strip(" ")
        sensibility[node] = value
    networks[net]["Variables (variance reduction)"] = sensibility

js_txt = u""
sec_1 = [u"Absolute error (rms)", u"Error rate (%)",
         u"Logarithmic loss", u"Quadratic loss", u"Spherical payoff"]
for d in networks:
    js_txt = js_txt + u"\n\n"
    js_txt = js_txt + u"##### " + d + "\n"
    js_txt = js_txt + u"\n"
    js_txt = js_txt + u"```javascript \n"
    js_txt = js_txt + u"{\"" + d + "\":{\n"
    js_txt = js_txt + (u"\"Description\": \"Poner aquí la descripción" +
                       u" del modelo en cuestión\",\n")
    js_txt = js_txt + (u"\"Training_data_set\": \"" +
                       u"bn_train_20150830_sin_NA_Boosted.csv\",\n")
    js_txt = js_txt + u"\"Results\": [\n"
    for v in sec_1:
        if v != sec_1[-1]:
            js_txt = js_txt + (u"    {\"" + v + u"\": " + u"\"" +
                               networks[d][v] + "\"},\n")
    js_txt = js_txt + u"    {\"" + v + "\": " + "\"" + networks[d][v] + "\"}\n"
    js_txt = js_txt + u"      ],\n"
    js_txt = js_txt + u"\"Variables (variance reduction)\": [\n"
    for v in networks[d]["Variables (variance reduction)"]:
        if v != networks[d]["Variables (variance reduction)"].keys()[-1]:
            js_txt = (js_txt + u"    {\"" + v + "\": " + "\"" +
                      networks[d]["Variables (variance reduction)"][v] +
                      u"\"},\n")
    js_txt = js_txt +  (u"    {\"" + v + "\": " + "\"" +
           networks[d]["Variables (variance reduction)"][v] + "\"}\n")
    js_txt = js_txt +  u"      ]\n"
    js_txt = js_txt +  u" }\n"
    js_txt = js_txt +  u"}\n"
    js_txt = js_txt +  u"```\n"

import pyperclip
pyperclip.copy(js_txt)
