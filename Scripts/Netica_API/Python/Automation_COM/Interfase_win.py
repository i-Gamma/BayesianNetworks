# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 13:31:05 2015
@author: Miguel

"""

import wx
import os
from funciones import xl_out, learn_method, pyNetica, Netica_RB_EcoInt


def entrena_red(self, analisis, zvh, base, equipo):
    # Index for excel writting
    xl_row, xl_col = 1, 1

    # Recupera informacion y establece los parametros de ejecución
    zvh_seleccionado = zvh - 1
    net_dsk = base
    pruebas = set(analisis)
    equipo = equipo

    if equipo == "lap_m":
        netica_dir = u"".join([
            u"C:/Users/Miguel/Documents/0 Versiones/2 Proyectos/",
            u"BN_Mapping/Netica/"])
        dir_robin =\
            u"C:/Users/Miguel/Documents/1 Nube/GoogleDrive/2 Proyectos/RoBiN"
    else:
        netica_dir = u"".join([u"C:/Users/miguel.equihua/Documents/0-GIT/",
                              u"Publicaciones y proyectos/BN_Mapping/Netica/"])
        dir_robin = u"C:/Users/miguel.equihua/Documents/1 Nube/" +\
                    u"Google Drive/2 Proyectos/RoBiN"

    dir_datos = u"". join([u"/Datos RoBiN/México/0_Vigente/GIS/",
                          "Mapas_base/2004/train_data_pack/"])

    nodos_zvh_dic = {u"Zvh_8ph": u"B01_test.neta", u"zvh": u"B02_test.neta",
                     u"zvh_31": u"B03_test.neta"}

    nodo_zvh = nodos_zvh_dic.keys()[zvh_seleccionado]
    nodo_objetivo = u"zz_delt_vp"
    nueva_red_nombre = u"-".join([nodo_objetivo, nodo_zvh])
    primerPlano = 1

    # Initialize NETICA environment and Excel
    netica_app = pyNetica(netica_dir, primerPlano).netica_app
    xl_app = xl_out("Resultados_EI", True)
    xlwrite = xl_app.xlw

    # Open selected Network file
    if net_dsk.rfind(".neta") < 0:
        net_dsk = dir_robin + dir_datos + "variables_2.neta"
    else:
        net_dsk = dir_robin + dir_datos + net_dsk
    name = netica_app.NewStream(net_dsk)
    net_p = netica_app.ReadBNet(name, "")
    coment_red_origen = net_p.Comment
    net_p.Comment = u"Colección de variables con discretización a 2 niveles"
    mez = Netica_RB_EcoInt(netica_app, net_p, learn_method.counting,
                           nodo_zvh, nodo_objetivo, nueva_red_nombre)

    # netica_app.visible = primerPlano
    # netica_app.UserControl = controlUsuario ----- no se puede cambiar
#    opciones_str = u"".join([str(zvh), " ", pruebas, " ", base])
    xlwrite(2, 1, u"".join(["#" * 10, " Abriendo Netica ", "#" * 10]))
    xlwrite(3, 1, u"Parametros: ")
#    xlwrite(3, 2, opciones_str)
    xlwrite(4, 1, u"Netica iniciada: ")
    xlwrite(4, 2, netica_app.VersionString)
    xlwrite(5, 1, u"Licencia buscada en: ")
    xlwrite(5, 2, netica_dir)
    xlwrite(6, 1, u"Red abierta: ")
    xlwrite(6, 2, net_p.Name)
    xlwrite(7, 1, u"Archivo seleccionado: ")
    xlwrite(7, 2, net_p.FileName.split("/")[-1])
    xlwrite(8, 1, u"Descripcion de la red: ")
    xlwrite(8, 2, coment_red_origen)
    xlwrite(9, 1, u"Nodo <ZVH> seleccionado: ")
    xlwrite(9, 2, nodo_zvh)
    xlwrite(10, 1, u"Probabilidad de error al elegir al azar: ")
    xlwrite(10, 2, u"=1-1/18")
    xl_row = 11

    # Anota en un diccionario los datos de los nodos contenidos
    # en "variables.neta"
    # nodos_dic =
    mez.lista_nodos_diccionario()

    # Selecciona nodos de interes y los copia en una nueva red.
    mez.copia_variables_interes(nodos_zvh_dic)
    xlwrite(xl_row, 1, u"".join(["Nodo objetivo: ", nodo_objetivo]))
    xlwrite(xl_row + 1, 2, u"Error RB")
    xl_row = xlwrite(xl_row + 1, 3, u"Mejora")

    # Cierra la red de todas las variables.
    net_p.Delete()

    # Prepara casos para entrenamiento y pruebas
    # casos_st =
    casos_dsk = u"".join([dir_robin, dir_datos,
                          "bn_train_20150713_sin_NA.csv"])
    mez.prepara_casos(casos_dsk)

    # Lista usada para organizar el proceso iterativo de prueba
    variables_set = set(mez.nuevos_nodos["infys"].keys())

    if set([0]).issubset(pruebas):
        # Prueba la red con todos los enlaces tipo "naive"
        for nn in nodos_zvh_dic:
            err = mez.prueba_RB_naive(xl_row, variables_set,
                                      nn, netica_dir, xlwrite)
            xl_row = xl_row
            xlwrite(xl_row, 1, u"Error modelo \"Naive\" completo <" +
                    nn + "> : ")
            xlwrite(xl_row, 2, err)
            xl_row = xlwrite(xl_row, 3, "=($B$10 / B{:0d}".format(xl_row) +
                                        ") - 1")

    if set([1]).issubset(pruebas):
        mez.pruebas_de_1(xl_row, variables_set, xlwrite)

    if set([2]).issubset(pruebas):
        error = mez.pruebas_de_2(xl_row, variables_set, xlwrite)

    if set([3]).issubset(pruebas):
        xl_row, error, var_set = mez.pruebas_3(xl_row, variables_set, xlwrite)

    # Anota resultados en la hoja de descripcion
    # descripcion_nueva_red(nt_nueva, err_naive, errores, errores2)

    # Guarda la nueva
    nueva_dsk = dir_robin + dir_datos + nueva_red_nombre + ".neta"
    nueva_st = mez.netApp.NewStream(nueva_dsk)
    mez.nt_nueva.Write(nueva_st)
    xl_row = xl_row + 1
    xlwrite(xl_row, 1, "".join(["Nueva red guardada en: ", nueva_red_nombre]))

    xl_row = xl_row + 1
    xlwrite(xl_row, 1, "procesamiento terminado ***************")
    xl_row = xl_row + 1
    xlwrite(xl_row, 1, "Cerrando NETICA!")

    nueva_st.Delete()
    mez.nt_nueva.Delete()
    mez.netApp.Quit()
    del mez

    # Close Excel and get rid of object refering to it
    os.chdir(u"".join([dir_robin, dir_datos]))
    xl_wd = os.getcwdu()
    node_niveles = os.path.basename(net_dsk).split("_")[1].split(".")[0]
    xl_dsk = xl_wd + u"\\Step_Naive_EI_" + nodo_zvh + "_" + \
        node_niveles + ".xlsx"

    try:
        xl_app.workbook.SaveAs(xl_dsk)
    except IOError as e:
        print "Archivo no guardado: <" + e + ">"
    xl_app.excelapp.Quit()
    del xl_app.excelapp
    del xl_app


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Stepwise RB-IE datos INFyS",
                          size=(450, 300))

        # Datos generales
        self.panel = wx.Panel(self, -1)
        zvh_lst = ["Zvh_8ph", "zvh", "zvh_31"]
        rb_base_lst = ["variables_2n.neta", "variables_3n.neta",
                       "variables_4n.neta", "variables_5n.neta",
                       "variables_10n.neta"]

        self.picture = wx.StaticBitmap(self.panel, size=(100, 150), pos=(1, 1))
        self.picture.SetBitmap(wx.Bitmap('ROBIN_1.jpg'))

        # arreglo generals de los componentes del panel
        wx.StaticText(self.panel, -1, "Modalidad ZVH:", (320, 15))
        self.cb_zvh = wx.ComboBox(self.panel, -1, "Elige", (320, 35),
                                  wx.DefaultSize, zvh_lst, wx.CB_DROPDOWN)
        wx.StaticText(self.panel, -1, "Variables Base:", (180, 15))
        self.cb_rb_base = wx.ComboBox(self.panel, -1, "Elige variables:",
                                      (180, 35), (115, 24),
                                      rb_base_lst, wx.CB_DROPDOWN)
        self.st = wx.StaticText(self.panel, label="Hola", pos=(180, 220))
        wx.StaticText(self.panel, -1, u"Tipo de análisis:", (180, 100))
        self.cxb_naive = wx.CheckBox(self.panel, -1,
                                     "Entrena Naive completa",
                                     (180, 120), wx.DefaultSize)
        self.cxb_uno = wx.CheckBox(self.panel, -1,
                                   "Uno por uno", (180, 140), wx.DefaultSize)
        self.cxb_step = wx.CheckBox(self.panel, -1,
                                    "Por pasos", (180, 160), wx.DefaultSize)
        self.boton = wx.Button(self.panel, wx.ID_OK, pos=(315, 210))
        self.CreateStatusBar()

        # Bindings
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.cb_zvh.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.boton.Bind(wx.EVT_BUTTON, self.OnClick)

    def OnSelect(self, e):
        i = e.GetString()
        self.st.SetLabel = i

    def OnCheck(self, e):
        analisis = e.GetEventObject()
        if analisis == self.cxb_naive:
            self.st.Label = u"Naive completa"
            msg = "Naive: %s" % self.cxb_naive.GetValue()
            self.PushStatusText(msg)
        elif analisis == self.cxb_uno:
            self.st.Label = u"Prueba uno por uno"
            msg = "Uno por uno: %s" % self.cxb_uno.GetValue()
            self.PushStatusText(msg)
        elif analisis == self.cxb_step:
            self.st.SetLabel = u"Agrega por pasos"
            msg = "Por pasos: %s" % self.cxb_step.GetValue()
            self.PushStatusText(msg)
        else:
            e.Skip()

    def OnClick(self, event):
        analisis = []
        if self.cxb_naive.IsChecked():
            analisis = [0]
        if self.cxb_uno.IsChecked():
            analisis = analisis + [1]
        if self.cxb_step.IsChecked():
            analisis = analisis + [2]

        if self.cb_zvh.GetSelection() != wx.NOT_FOUND:
            zvh = self.cb_zvh.StringSelection
            zvh_i = self.cb_zvh.Selection
        else:
            zvh = "Zvh_8ph"
            zvh_i = 0

        if self.cb_rb_base.GetSelection() != wx.NOT_FOUND:
            base = self.cb_rb_base.StringSelection
        else:
            base = "variables_2n.neta"

        msg = "Boton -> Analisis: [%s]" % ", ".join(map(str, analisis)) +\
              " -- %s --" % zvh + " <%s>" % base
        self.PushStatusText(msg)
        analisis = set(analisis)

        entrena_red(self, analisis, zvh_i, base, "lap_m")


class App(wx.App):
    """ Clase Aplicación """

    def OnInit(self):
        self.frame = Frame
        self.frame().Show()
        return True


def main():
    app = App(redirect=True)
    app.MainLoop()


if __name__ == "__main__":
    main()
