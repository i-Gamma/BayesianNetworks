# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:13:13 2015

@author: Miguel
"""
import time
from pywinauto.application import Application
import socket


def on_toy():
    # Machine dependant basic path data
    machine = socket.gethostname()
    if machine == "Tigridia":
        # Laptop Miguel
        dirs = {"dir_usr": u"C:\\Users\\Miguel\\",
                "dir_git": u"Documents\\0 Versiones\\2 Proyectos\\",
                "dir_RB": u"BayesianNetworks\\redes_ajuste_MyO\\Final\\",
                "dir_wrk": u"Documents\\1 Nube\\Dropbox\\",
                "dir_dat": u"Datos Redes Bayesianas\\Datos_para_mapeo\\"}
    elif machine == "Capsicum":
        # Descktop Inecol - Miguel
        dirs = {"dir_usr": u"C:\\Users\\miguel.equihua\\",
                "dir_git": u"Documents\\0-GIT\\Publicaciones y proyectos\\",
                "dir_RB": u"BayesianNetworks\\redes_ajuste_MyO\\Final\\",
                "dir_wrk": u"Documents\\1 Nube\\Dropbox\\",
                "dir_dat": u"Datos Redes Bayesianas\\Datos_para_mapeo\\"}
    else:
        print "Don't know where am I!!!!"

    return dirs

"""
Main body

Operates Netica to Process Cases

"""

# Ubicaciónes usadas
directorios = on_toy()
file_RB = u"Final_net_Scores_codep.neta"
file_NETICA = u"C:\\Program Files\\Netica\\Netica 519\\Netica.exe"
dir_usr = directorios["dir_usr"]
dir_git = directorios["dir_git"]
dir_RB = directorios["dir_RB"]
dir_wrk = directorios["dir_wrk"]
dir_dat = directorios["dir_dat"]

# Tiempo máximo de espera para procesamiento de un archivos de casos completo
wait_time_case = 360

# Abre NETICA
app = Application().Start(cmd_line=file_NETICA)
netica = app.Netica
time.sleep(2)
netica.Wait("ready")

# Abre la RB de interés
menu_item = netica.MenuItem(u"&File->&Open...\tCtrl+O")
menu_item.Click()
window = app[u"Document to Open:"]
comboboxex = window[u"No&mbre:ComboBoxEx"]
comboboxex.TypeKeys(dir_usr + dir_git + dir_RB + file_RB, with_spaces=True)
button = window[u"&Abrir"]
button.Click()
time.sleep(3)
netica.Wait("ready", timeout=wait_time_case)

for i in range(1, 3):
    # Inicia procesamiento de casos para producir salida para mapear
    menu_item = netica.MenuItem(u"&Cases->&Process Cases")
    menu_item.Click()

    # Selección del archivo de control
    window = app[u"Control File (Cancel to Skip)"]
    window.Wait("ready")
    comboboxex = window[u"No&mbre:ComboBoxEx"]
    dir_trabajo = dir_usr + dir_wrk + dir_dat
    comboboxex.TypeKeys(dir_trabajo + u"control.txt", with_spaces=True)
    button = window[u"&Abrir"]
    button.Click()
    time.sleep(2)

    # Selección del archivo de datos
    window = app[u"Case file to process:"]
    window.Wait("ready")
    comboboxex = window[u"No&mbre:ComboBoxEx"]
    comboboxex.TypeKeys("bn_ie_tabfinal_20150830.csv")
    button = window[u"&Abrir"]
    button.Click()
    time.sleep(2)

    # Selección del archivo de salida
    window = app[u"Output cases to:"]
    window.Wait("ready")
    combobox = window[u"Edit"]
    combobox.TypeKeys(u"prueba" + str(i) + u".csv")
    button = window.Button
    button.Click()
    time.sleep(2)

    # Si el archivo de salida ya existe confirma sobreescribirlo
    if app[u"Confirmar Guardar como"].Exists():
        window = app[u"Confirmar Guardar como"]
        button = window[u"&S\xed"]
        button.Click()

    # Espera hasta que procese todo el archivo antes de pasar al siguiente
    time.sleep(10)
    netica.Wait("ready", timeout=wait_time_case)

# Termina NETICA
app.Kill_()
