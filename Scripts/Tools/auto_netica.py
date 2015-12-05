# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:13:13 2015

@author: Miguel
"""
import time
from pywinauto.application import Application
import socket
import os
import locale

def on_toy():
    # Machine dependant basic path data
    machine = socket.gethostname()
    if machine == "Tigridia":
        # Laptop Miguel
        dirs = {"dir_usr": u"C:\\Users\\Miguel\\",
                "dir_git": u"Documents\\0 Versiones\\2 Proyectos\\",
                "dir_RB": u"BayesianNetworks\\redes_ajuste_MyO\\Final\\",
                "dir_wrk": u"Documents\\1 Nube\\Dropbox\\",
                "dir_dat": u"Datos Redes Bayesianas\\Datos_para_mapeo\\",
                "dir_NETICA": u"C:\\Program Files\\Netica\\Netica 519\\"}
    elif machine == "Capsicum":
        # Descktop Inecol - Miguel
        dirs = {"dir_usr": u"C:\\Users\\miguel.equihua\\",
                "dir_git": u"Documents\\0-GIT\\Publicaciones y proyectos\\",
                "dir_RB": u"BayesianNetworks\\redes_ajuste_MyO\\Final\\",
                "dir_wrk": u"Documents\\1 Nube\\Dropbox\\",
                "dir_dat": u"Datos Redes Bayesianas\\Datos_para_mapeo\\",
                "dir_NETICA": u"C:\\Program Files\\Netica\\Netica 519\\"}
    elif machine == "Equihua":
        # Descktop casa - Julián
        dirs = {"dir_usr": u"E:\\",
                "dir_git": u"repositories\\",
                "dir_RB": u"BayesianNetworks\\redes_ajuste_MyO\\Final\\",
                "dir_wrk": u"work\\20150720_infys_modis\\",
                "dir_dat": u"training_tables_20151006\\products\\",
                "dir_NETICA": u"E:\\software\\Netica\\Netica 519\\"}
    else:
        print "Don't know where am I!!!!"

    return dirs

"""
Main body

Operates Netica to Process Cases

"""

# Ubicaciónes usadas
directorios = on_toy()
dir_NETICA = directorios["dir_NETICA"]
dir_usr = directorios["dir_usr"]
dir_git = directorios["dir_git"]
dir_RB = directorios["dir_RB"]
dir_wrk = directorios["dir_wrk"]
dir_dat = directorios["dir_dat"]
file_RB = dir_usr + dir_git + dir_RB + u"Final_net_Scores_codep.neta"
file_NETICA = dir_NETICA + u"Netica.exe"
dir_trabajo = dir_usr + dir_wrk + dir_dat

# Tiempo máximo de espera para procesamiento de un archivos de casos completo
wait_time_case = 360

# Ajuste los dialgos al idioma de la maquina que se usa
if locale.getdefaultlocale()[0] == "en_US":
    win_open = "Open"
    win_names = "Name"
    win_save = "Yes"
    win_ok = "Ok"
    win_confirm_save = u"Confirm Save As"
else:
    win_open = "Abrir"
    win_names = "Nombre"
    win_save = u"S\xed"
    win_confirm_save = u"Confirmar Guardar como"


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
comboboxex.TypeKeys(file_RB, with_spaces=True)
button = window[win_open]
button.Click()
time.sleep(3)
netica.Wait("ready", timeout=wait_time_case)

# Localiza y prepara el procesamiento de archivos de datos disponibles
if socket.gethostname() == "Equihua":
    datos = [fl for fl in os.listdir(dir_trabajo) if "bn_ie_tabfinal" in fl
                                                      and not "out" in fl]
    dat_names = ["_".join(["map_rb"] + nm.strip(".csv").split("_")[3:])
                 for nm in datos ]
else:
    datos = ["bn_ie_tabfinal_20150823.csv"]
    dat_names = ["prueba_1", "prueba_2"]


for i in xrange(1, len(datos) + 1, 1):
    # Inicia procesamiento de casos para producir salida para mapear
    menu_item = netica.MenuItem(u"Cases->Process Cases")
    menu_item.Click()

    # Selección del archivo de control
    window = app[u"Control File (Cancel to Skip)"]
    comboboxex = window["Nombre:ComboBoxEx"]
    comboboxex.TypeKeys(dir_trabajo + u"control.txt", with_spaces=True)
    button = window[win_open]
    button.Click()

    # Selección del archivo de datos
    time.sleep(2)
    window = app[u"Case file to process:"]
    comboboxex = window[u"Nombre:ComboBoxEx"]
    comboboxex.TypeKeys(datos[i])
    button = window[win_open]
    button.Click()

    # Selección del archivo de salida
    time.sleep(2)
    window = app.window_(title_re="Output cases to:", class_name="#32770")
    combobox = window["Edit"]
    combobox.TypeKeys(dat_names[i] + u".csv")
    window.Wait("ready")
    if window["&Save"].Exists():
      button = window["&Save"]
    else:
      button = window["Save"]
    button.Click()

    # Si el archivo de salida ya existe confirma sobrescribirlo
    time.sleep(10)
    if app.Dialog.Exists():
        window = app[win_confirm_save]
        window.Wait("ready")
        button = window[win_save]
        button.Click()

    # Dialogo para expandir los intervalos de las variables
    time.sleep(20)
    if app.window_(title_re = "Netica", class_name = "#32770").Exists():
        window = app.window_(title_re = "Netica", class_name = "#32770")
        window.Wait("ready")
        button_dialog_netica = window[u"Expand All"]
        button_dialog_netica.Click()

    # Espera hasta que procese todo el archivo antes de pasar al siguiente
    time.sleep(15)
    netica.Wait("ready", timeout=wait_time_case)

# Termina NETICA
app.Kill_()
