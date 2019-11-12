# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:13:13 2015

Generates new data sets of "expected" EI values.
Uses the already trained BN: "Final_net_Scores_codep.neta" for ROBIN projec
                             "red_todo_TAN_ZVH_auto.neta" for Gamma project
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
        print("Don't know where am I!!!!")

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
dir_ShP = directorios["dir_ShP"]
file_RB = dir_usr + dir_git + dir_RB + u"red_todo_TAN_ZVH_auto.neta" #ROBIN u"Final_net_Scores_codep.neta"
file_NETICA = dir_NETICA + u"Netica.exe"
dir_trabajo = dir_usr + dir_wrk + dir_dat

# Tiempo máximo de espera para procesamiento de un archivos de casos completo
wait_time_case = 360

# Ajuste los dialgos al idioma de la maquina que se usa
if locale.getdefaultlocale()[0] == "en_US":
    win_open = "Open"
    win_names = "Name"
    win_yes = "Yes"
    win_ok = "Ok"
    win_confirm_save = u"Confirm Save As"
else:
    win_open = "Abrir"
    win_names = "Nombre"
    win_yes = u"S\xed"
    win_confirm_save = u"Confirmar Guardar como"
    win_save = u"Guardar"


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
if socket.gethostname() == "Capsicum": # ROBIN "Equihua"
    datos = [fl for fl in sorted(os.listdir(dir_ShP)) if fl.startswith("ie_mex_full_dataset")]  # ROBIN "bn_ie_tabfinal" in fl and not "out" in fl]
    dat_names = ["_".join(["map_rb"] + nm.strip(".csv").split("_")[3:]) for nm in datos ]
else:
    datos = ["bn_ie_tabfinal_20150830.csv"]
    dat_names = ["prueba_1a", "prueba_2b"]

# Verifica el nombre de la variable "latente"
# Localiza el nodo "latente": zz_delt_vp...
time.sleep(10)
netica.Wait("ready", timeout=wait_time_case)
menu_item = netica.MenuItem(u"&Edit->&Find...\tCtrl+F")
netica.Wait('ready', timeout=wait_time_case)
menu_item.Click()

# Localiza la ventana de dialogo para buscar el nodo que inicia con "zz"
window = app.Dialog
edit = window.Edit
edit.SetEditText("")
edit.SetEditText("zz")
edit.TypeKeys("{ENTER}")
time.sleep(2)

# Abre la ventana de propiedades del nodo seleccionado
netica.Wait("ready", timeout=wait_time_case)
net_window = netica.red_todo_TAN_ZVH_auto   # ROBIN Final_net_Scores_codep)
net_window.TypeKeys("{ENTER}")

# Localiza la ventana de propiedade del nodo
window = app.Dialog
window.Wait('ready', timeout=wait_time_case)

# Si el nodo latente se llama igual que la columna de datos cambia el nombre del nodo
node_props = window.Edit
node = node_props.Texts()[0]
if node == "zz_delt_vp":
    node_props.SetEditText("zz_delt_vp_1")
button = window.OK
button.Click()

menu_item = netica.MenuItem(u'&Window->&1 Netica Messages')
menu_item.Click()
menu_item = netica.MenuItem(u'&Window->&3 netica.red_todo_TAN_ZVH_auto') # ROBIN Final_net_Scores_codep)
menu_item.Click()
netica.Wait("ready", timeout=wait_time_case)


for i in range(0, len(datos)):

    # Read data file, if missing data found in the dataset are replaced by "*"
    working_data = dir_trabajo + "NA_replaced_" + archivos_datos_en_z[i]
    with open(dir_ShP + archivos_datos_en_z[0], "r") as infile, \
            open(working_data, "w") as outfile:
        data_tabla = infile.read()
        print("\nLectura terminada")
        print(time.time() - start)
        data_tabla = data_tabla.replace("NA", "*")
        print("Conversión terminada")
        print(time.time() - start)
        outfile.write(data_tabla)
        print("Escritura terminada")
        print(time.time() - start)

    # Inicia procesamiento de casos para producir salida para mapear
    # Selección del archivo de control
    menu_item = netica.MenuItem(u"Cases->Process Cases")
    menu_item.Click()
    window = app[u"Control File (Cancel to Skip)"]
    comboboxex = window["Nombre:ComboBoxEx"]
    comboboxex.TypeKeys(dir_trabajo + u"control.txt", with_spaces=True)
    button = window[win_open]
    button.Click()

    # Selección del archivo de datos
    time.sleep(2)
    window = app[u"Case file to process:"]
    comboboxex = window[u"Nombre:ComboBoxEx"]
    comboboxex.TypeKeys(working_data, with_spaces=True)
    button = window[win_open]
    button.Click()

    # Selección del archivo de salida
    time.sleep(2)
    window = app.window_(title_re="Output cases to:", class_name="#32770")
    combobox = window["Edit"]
    combobox.TypeKeys(dir_trabajo + dat_names[i] + u".csv")
    window.Wait("ready")
    if window["&"+ win_save].Exists():
      button = window["&"+ win_save]
    else:
      button = window[win_save]
    button.Click()

    # Si el archivo de salida ya existe confirma sobrescribirlo
    time.sleep(10)
    if app.Dialog.Exists():
        window = app[win_confirm_save]
        window.Wait("ready")
        button = window[win_yes]
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

    print("Datos del archivo {} procesados".format(datos[i]))

# Termina NETICA
app.Kill_()
