# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:13:13 2015

@author: Miguel
"""
import time
from pywinauto.application import Application

# Ubicaciónes usadas
file_RB = u"Final_net_Scores_codep.neta"
file_NETICA = u"C://Program Files//Netica//Netica 515//Netica.exe"
dir_eq = u"C:\\Users\\Miguel\\Documents\\0 Versiones\\2 Proyectos\\"
dir_RB = u"BayesianNetworks\\redes_ajuste_MyO\\Final\\"
dir_wrk = u"C:\\Users\\Miguel\\Documents\\1 Nube\\Dropbox\\"
dir_dat = u"Datos Redes Bayesianas\\Datos_para_mapeo\\"

# Tiempo máximo de espera para procesamiento de un archivos de casos completo
wait_time_case = 360

# Abre NETICA
app = Application().Start(cmd_line=file_NETICA)
netica = app.Netica
netica.Wait('ready')

# Abre la rRB de interés
menu_item = netica.MenuItem(u'&File->&Open...\tCtrl+O')
menu_item.Click()
window = app.Dialog
comboboxex = window.ComboBoxEx
comboboxex.Click()
comboboxex.TypeKeys(dir_eq + dir_RB + file_RB, with_spaces=True)
button = window[u'&Abrir']
button.Click()
time.sleep(15)
# netica.Wait('ready', timeout=wait_time_case)

for i in range(1, 3):
    # Inicia procesamiento de casos para producir salida para mapear
    menu_item = netica.MenuItem(u'&Cases->&Process Cases')
    menu_item.Click()
    window = app.Dialog
    window.Wait('ready')

    # Selección del archivo de control
    comboboxex = window.ComboBoxEx
    comboboxex.Click()
    comboboxex.TypeKeys(dir_wrk + dir_dat + u"control.txt", with_spaces=True)
    button = window[u'&Abrir']
    button.Click()

    # Selección del archivo de datos
    comboboxex = window.ComboBoxEx
    comboboxex.Click()
    comboboxex.TypeKeys("bn_ie_tabfinal_20150830.csv")
    button = window[u'&Abrir']
    button.Click()

    # Selección del archivo de salida
    combobox = window[u'ComboBox']
    combobox.Click()
    combobox.TypeKeys(u"prueba" + str(i) + u".csv")
    button = window.Button
    button.Click()

    # Si el archivo de salida ya existe confirma sobreescribirlo
    if app[u"Confirmar Guardar como"].Exists():
        window = app[u"Confirmar Guardar como"]
        button = window[u"&S\xed"]
        button.Click()

    # Espera hasta que procese todo el archivo antes de pasar al siguiente
    time.sleep(wait_time_case)
    #netica.Wait("enabled", timeout=wait_time_case)

# Termina NETICA
app.Kill_()
