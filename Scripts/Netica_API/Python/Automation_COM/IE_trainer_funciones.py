# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 10:48:19 2015

@author: Miguel
"""

import os
import re

from win32com.client import Dispatch


class xl_out(object):
    # Prepares Excel to receive results from processing
    def __init__(self, file_name, make_visible=False):
        """Open spreadsheet"""
        self.excelapp = Dispatch("Excel.Application")
        if make_visible:
            self.excelapp.Visible = 1  # fun to watch!
        self.excelapp.Workbooks.Add()
        self.workbook = self.excelapp.ActiveWorkbook
        self.file_name = file_name
        self.default_sheet = self.excelapp.ActiveSheet
        self.default_sheet.Name = "BNet_EI"

    def getExcelApp(self):
        """Get Excel App for use"""
        return self.excelapp

    def xlw(self, row, col, value):
        # Write value to the specified (col, row) Excel cell
        self.default_sheet.Cells(row, col).Value = value
        row = row + 1
        return row


class learn_method:
        counting = 1
        EM = 3
        gradient = 4


class pyNetica (object):
    # Vincula la interface COM de NETICA y activa la aplicacion
    # Asume que la licencia esta en el mismo directorio de la aplicacion
    # si no la encuentra arranca en modo limitado
    def __init__(self, lic_dir, desp):
        self.netica_app = Dispatch("Netica.Application")
        self.licenseFile = os.path.join(lic_dir, u"inecol_netica.txt")
        try:
            self.licencia = open(self.licenseFile, 'r').read()
        except IOError as e:
            self.licencia = ""
            print u"License not found (" + e + ")"
        # Initialize Netica instance/env using password from a provided file
        self.netica_app.SetPassword(self.licencia)
        # Regular, Minimized, Maximized, Hidden
        self.netica_app.SetWindowPosition(desp)


class Netica_RB_EcoInt:
    # Use Netica to process database for Ecosystem Integrity
    def __init__(self, netApp, BNet, metodo, nodo_zvh, nodo_objetivo, nueva_red_nombre):
        self.netApp = netApp
        self.BNet = BNet
        self.metodo = metodo
        self.nodo_zvh = nodo_zvh
        self.nodo_obj = nodo_objetivo
        self.nueva_red_nombre = nueva_red_nombre

    def lista_nodos_diccionario(self):
        # Get the pointer to the set of nodes
        self.nodesList_p = self.BNet.Nodes
        # get number of nodes
        self.nnodes = self.nodesList_p.Count
        # Collect all node names in network
        self.node_names = {"gral": {}, "infys": {}, "pp": {}, "pt": {},
                           "tm": {}, "tr": {}, "tx": {}}
        for i in range(self.nnodes):
            node_p = self.nodesList_p[i]   # node_p
            name = node_p.name        # name
            if re.search(r"^[xyZzdC]", name):
                self.node_names["gral"][name] = node_p
            elif re.search(r"(^ntre|^Diam|^Alt|^Ins|^Sin|^prob|^Psn|^Gpp)",
                           name):
                self.node_names["infys"][name] = node_p
            elif re.search(r"^ppt[0-1]{1}", name):
                self.node_names["pp"][name] = node_p
            elif re.search(r"^pptm", name):
                self.node_names["pt"][name] = node_p
            elif re.search(r"^tma", name):
                self.node_names["tx"][name] = node_p
            elif re.search(r"^tmi", name):
                self.node_names["tm"][name] = node_p
            else:
                self.node_names["tr"][name] = node_p

    def copia_variables_interes(self, zvh):
        self.node_names["gral"][self.nodo_obj].IsSelected = True
        for n in zvh:
            self.node_names["gral"][n].IsSelected = True
        self.node_names["gral"]["dem30_mean1000"].IsSelected = True
        self.node_names["gral"]["dem30_sd1000"].IsSelected = True
        for n, v in self.node_names["infys"].iteritems():
            v.IsSelected = True
        nodos_interes = self.BNet.SelectedNodes
        # Crea una nueva red con los nodos de interes y los arregla
        self.nt_nueva = self.netApp.NewBNet("nueva_red")
        self.nt_nueva.CopyNodes(nodos_interes)
        self.nodosNuevosList_p = self.nt_nueva.Nodes
        self.nuevos_nodos = {"gral": {}, "infys": {}}
        self.nuevos_nodos["gral"][self.nodo_obj] = self.nodosNuevosList_p[
                                                self.nodo_obj]
        self.nuevos_nodos["gral"]["dem30_mean1000"] = self.nodosNuevosList_p[
            "dem30_mean1000"]
        self.nuevos_nodos["gral"]["dem30_sd1000"] = self.nodosNuevosList_p[
            "dem30_sd1000"]
        for n in self.node_names["infys"]:
            self.nuevos_nodos["infys"][n] = self.nodosNuevosList_p[n]
        self.ordena_nodos()
#        return self.nt_nueva, self.nodosNuevosList_p

    def ordena_nodos(self):
        # Function to arrange the nodes in NETICA
        y = 0
        for nodo in sorted(self.node_names):
            j, items = 0, "    "
            y = y + 30
            for k in sorted(self.node_names[nodo].keys()):
                if len(items) > 100:
                    y = y + 30
                    j, items = 0, "    "
                x = j * 21 + len(items) * 8 + len(k) * 4
                self.node_names[nodo][k].VisualPosition = (x, y)
                items = items + k
                j = j + 1

    def prepara_casos(self, arch):
        # Prepara el entrenamiento a partir de casos en archivo
        self.casos_dsk = "".join(arch)
        self.casos_st = self.netApp.NewStream(self.casos_dsk)
        self.casos = self.netApp.NewCaseset("entrena")
        self.casos.AddCasesFromFile(self.casos_st)
#        return self.casos_st


    def prueba_BNet(self):
        # Organiza la prueba de la red y calcula la tasa de error
        nodoObjetivo_nl = self.nodosNuevosList_p[self.nodo_obj]
        nodoObjetivo_nl.IsSelected = True
        nodo_prueba = self.nt_nueva.SelectedNodes
        nodoObjetivo_nl.IsSelected = False
        tester = self.nt_nueva.NewNetTester(nodo_prueba, nodo_prueba, -1)
        tester.TestWithCases(self.casos)
        self.valorError = tester.ErrorRate(nodo_prueba[0])
        tester.Delete()
        return self.valorError

    def entrena_BNet(self, nodos, degree):
        # Aplica el aprendizaje elejido.  Las opciones de aprendizaje son:
        entrenamiento = self.netApp.NewLearner(learn_method.EM)
        entrenamiento.LearnCPTs(nodos, self.casos, degree)  # Degree usualy 1
        self.nt_nueva.compile()

    def red_nula(self, var_set):
        # Erase tables of involved nodes in current network
        nodos_hijos = [n.name for n in
                       self.nodosNuevosList_p[self.nodo_zvh].Children]
        self.nodosNuevosList_p[self.nodo_obj].DeleteTables()
        self.nodosNuevosList_p[self.nodo_zvh].DeleteTables()
        self.nodosNuevosList_p["dem30_mean1000"].DeleteTables()
        self.nodosNuevosList_p["dem30_sd1000"].DeleteTables()
        for pp in var_set:
            self.nodosNuevosList_p[pp].DeleteTables()
            if pp in nodos_hijos:
                self.nodosNuevosList_p[pp].DeleteLink(
                    self.nodosNuevosList_p[self.nodo_obj])
                self.nodosNuevosList_p[pp].DeleteLink(
                    self.nodosNuevosList_p[self.nodo_zvh])
                self.nodosNuevosList_p[pp].DeleteLink(
                    self.nodosNuevosList_p["dem30_mean1000"])
                self.nodosNuevosList_p[pp].DeleteLink(
                    self.nodosNuevosList_p["dem30_sd1000"])

    def prueba_RB_naive(self, xl_row, vars_set, zvh, netica_dir, xlw):
        # Crea todos los links tipo "Naive" del "nodo_objetivo" hacia los demas
        for pp in sorted(self.nuevos_nodos["infys"]):
            self.nodosNuevosList_p[pp].AddLink(self.nodosNuevosList_p[zvh])
            self.nodosNuevosList_p[pp].AddLink(
                self.nodosNuevosList_p[self.nodo_obj])
            self.nodosNuevosList_p[pp].AddLink(
                self.nodosNuevosList_p["dem30_mean1000"])
            self.nodosNuevosList_p[pp].AddLink(
                self.nodosNuevosList_p["dem30_sd1000"])
        # Entrena y prueba la nueva red
        zvh_orig = self.nodo_zvh
        self.nodo_zvh = zvh
        self.entrena_BNet(self.nodosNuevosList_p, 1)
        tasaError = self.prueba_BNet()

        # Anota avance del calculo en la seccion de "descripcion" de la red
        self.red_nula(vars_set)
        self.nodo_zvh = zvh_orig
        return tasaError

    def pruebas_de_1(self, xl_row, vars_set, xlw):
        # Prueba la red "un-nodo-a-la-vez" tomado de la lista de variables
        self.nt_nueva.Comment = "".join([self.nt_nueva.Comment,
                                         "\n" * 2, "-" * 80])
        errores = {}
        for nodo in sorted(vars_set):
            self.red_nula(vars_set)
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p[self.nodo_zvh])
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p[self.nodo_obj])
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p["dem30_mean1000"])
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p["dem30_sd1000"])
            self.entrena_BNet(self.nodosNuevosList_p, 1)
            tasaError = self.prueba_BNet()
            errores[nodo] = tasaError
            xl_row = xl_row + 1
            xlw(xl_row, 1, "Tasa de error ")
            xlw(xl_row, 2, u"".join(["<", nodo, ">: "]))
            xlw(xl_row, 3, tasaError)
        self.red_nula(vars_set)

    def pruebas_de_2(self, xl_row, vars_set, xlw):
        # Prueba de la red con pares de variables
        self.nt_nueva.Comment = "".join([
            self.nt_nueva.Comment, "\n\nBloque de pruebas en bloques de 2"])
        self.nt_nueva.Comment = "".join([
            self.nt_nueva.Comment, "\n", "-" * 80])
        errores, nodo_min_err = {}, {"a": 100}
        for nodo in sorted(vars_set):
            self.red_nula(vars_set)
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p[self.nodo_zvh])
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p[self.nodo_obj])
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p["dem30_mean1000"])
            self.nodosNuevosList_p[nodo].AddLink(
                self.nodosNuevosList_p["dem30_sd1000"])
            self.entrena_BNet(self.nodosNuevosList_p, 1)
            tasaError = self.prueba_BNet()
            errores[nodo] = tasaError
            xl_row = xl_row + 1
            xlw(xl_row, 1,   "".join(["Tasa de error <", nodo, "> : "]))
            xlw(xl_row, 2,   tasaError)
            xlw(xl_row, 3, "=($B$10 / B{:0d}".format(xl_row) + " - 1")
            if tasaError < nodo_min_err[nodo_min_err.keys()[0]]:
                nodo_min_err.popitem()
                nodo_min_err[nodo] = tasaError
            nodo_1 = nodo_min_err.keys()[0]
            self.nt_nueva.Comment = "".join([self.nt_nueva.Comment, "\n"])
        errores2 = {}
        for odon in sorted(vars_set - set([nodo_1])):
            self.red_nula(vars_set)
            self.nodosNuevosList_p[odon].AddLink(
                self.nodosNuevosList_p[self.nodo_zvh])
            self.nodosNuevosList_p[odon].AddLink(
                self.nodosNuevosList_p[self.nodo_obj])
            self.nodosNuevosList_p[odon].AddLink(
                self.nodosNuevosList_p["dem30_mean1000"])
            self.nodosNuevosList_p[odon].AddLink(
                self.nodosNuevosList_p["dem30_sd1000"])
            self.nodosNuevosList_p[nodo_1].AddLink(
                self.nodosNuevosList_p[self.nodo_zvh])
            self.nodosNuevosList_p[nodo_1].AddLink(
                self.nodosNuevosList_p[self.nodo_obj])
            self.nodosNuevosList_p[nodo_1].AddLink(
                self.nodosNuevosList_p["dem30_mean1000"])
            self.nodosNuevosList_p[nodo_1].AddLink(
                self.nodosNuevosList_p["dem30_sd1000"])
            self.entrena_BNet(self.nodosNuevosList_p, 1)
            tasaError = self.prueba_BNet()
            errores2[nodo_1 + "_" + odon] = tasaError
            if tasaError < nodo_min_err[nodo_min_err.keys()[0]]:
                nodo_min_err.popitem()
                nodo_min_err[nodo_1 + "_" + odon] = tasaError
            xl_row = xl_row + 1
            xlw(xl_row, 1, u"".join(["Tasa de error <",
                                     nodo_1, "_", odon, "> :"]))
            xlw(xl_row, 2, tasaError)
            xlw(xl_row, 3, "=($B$10 / B{:0d}".format(xl_row) + ") - 1")
            self.nt_nueva.Comment = u"".join([
                self.nt_nueva.Comment, "Tasa de error <", nodo_1, "_",
                odon, "> : ""{:10.4f}\n".format(tasaError)])
            self.nt_nueva.Comment = "".join([
                self.nt_nueva.Comment, "\n", "-" * 80 + "\n"])
        self.red_nula(vars_set)
        return nodo_min_err

    def pruebas_3(self, xl_row, vars_set, xlw):
        # Prueba de la red con crecimiento stepwise
        self.nt_nueva.Comment = "".join([self.nt_nueva.Comment,
                                         "\n\nRecorrido stepwise"])
        self.nt_nueva.Comment = "".join([
            self.nt_nueva.Comment, "\n", "-" * 80])
        nodo_min_err = {"a": 100}
        set_in = {}
        set_test = vars_set
        while set_test != {}:
            for odon in sorted(set_test):
                self.red_nula(vars_set)
                for n_in in set_in:
                    self.nodosNuevosList_p[n_in].AddLink(
                        self.nodosNuevosList_p[self.nodo_zvh])
                    self.nodosNuevosList_p[n_in].AddLink(
                        self.nodosNuevosList_p[self.nodo_obj])
                    self.nodosNuevosList_p[n_in].AddLink(
                        self.nodosNuevosList_p["dem30_mean1000"])
                    self.nodosNuevosList_p[n_in].AddLink(
                        self.nodosNuevosList_p["dem30_sd1000"])
                # New variable to test
                self.nodosNuevosList_p[odon].AddLink(
                    self.nodosNuevosList_p[self.nodo_zvh])
                self.nodosNuevosList_p[odon].AddLink(
                    self.nodosNuevosList_p[self.nodo_obj])
                self.nodosNuevosList_p[odon].AddLink(
                    self.nodosNuevosList_p["dem30_mean1000"])
                self.nodosNuevosList_p[odon].AddLink(
                    self.nodosNuevosList_p["dem30_sd1000"])
                self.entrena_BNet(self.nodosNuevosList_p, 1)
                tasaError = self.prueba_BNet()
                if tasaError < nodo_min_err[nodo_min_err.keys()[0]]:
                    nodo_min_err.popitem()
                    nodo_min_err[odon] = tasaError
                self.nt_nueva.Comment = \
                    u"".join([self.nt_nueva.Comment,
                              "Tasa de error  al agregar: ", odon,
                              "> : ""{:10.4f}\n".format(tasaError)])
            if nodo_min_err.keys()[0] in set_in:
                set_test = {}
            else:
                set_in[nodo_min_err.keys()[0]] =\
                    nodo_min_err[nodo_min_err.keys()[0]]
                set_test = set_test - set([nodo_min_err.keys()[0]])
                err = nodo_min_err[nodo_min_err.keys()[0]]
                nodos = ", ".join(set_in.keys())
                xlw(xl_row, 1, u"Paso incluye <" + nodos + u">:")
                xlw(xl_row, 2, err)
                xl_row = xlw(xl_row, 3,
                             "=($B$10 / B{:0d}".format(xl_row) + ") - 1")
                self.nt_nueva.Comment = u"".join([self.nt_nueva.Comment,
                                                  "\n", "-" * 80 + "\n"])
            self.red_nula(vars_set)
        return xl_row, nodo_min_err, vars_set

    def descripcion_nueva_red(red_nva, err_nv, err1, err2):
        resultados = red_nva.Comment
        resultados.append("\n" + "-" * 80)
        resultados.append("Modelos una variable a la vez")
        for e in sorted(err1):
            resultados.append("".join(["Tasa de error con la variable ", e,
                                       ": {:10.4f}".format(err1[e])]))
        resultados.append("".join(["-" * 80, "\n"*2]))
        resultados.append("".join(["\n", "-" * 80]))
        resultados.append("Modelos con dos variable")
        for e in sorted(err2):
            resultados.append("".join(["Tasa de error con la variable ", e,
                                       ": {:10.4f}".format(err2[e])]))
        resultados.append("".join(["-" * 80, "\n"*2]))
        resultados.append("procesamiento terminado ***************")
        resultados.append("Cerrando NETICA!")
        red_nva.Comment = "\n".join(resultados)

#    def get_expected_values (red):
        """
        Calcula media y varianza de los nodos indicados dada
        la evidencia ingresada.
        """
"""
        void RetractFindings() Member of Netica.IBNode
        # void ReadFindings(ref int case_posn, Netica.Streamer stream,
        # bool add_to_existing, [Netica.BNodes Nodes = null], out int IDnum,
        # out double freq) Member of Netica.IBNet
        enterFinding
        void EnterFinding(object state) Member of Netica.IBNode
        double FindingsProbability() Member of Netica.IBNet
        double GetExpectedValue(out double std_dev)
        Member of Netica.IBNode
"""