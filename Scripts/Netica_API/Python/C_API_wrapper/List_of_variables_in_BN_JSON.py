# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 16:42:54 2015

@author: Miguel
"""

import os
import re
import logging

# import ctypes for wrapping netica.dll
from ctypes.util import find_library
from ctypes import windll, c_char, c_char_p, c_void_p, c_int, c_double
from ctypes import create_string_buffer

# constants
MESGLEN = 600
REGULAR_WINDOW = 0x70
logger = logging.getLogger(__name__)

# TODO finish making the wrapping to all used NETICa API functions


# Wrapping of Netica C API functions to use in python through ctypes module
def NewFileStream(name, env_p):
    """
    create stream
    """
    # (const char* filename, environ_ns* env, const char* access)
    libN.NewFileStream_ns.argtypes = [c_char_p, c_void_p, c_char_p]
    libN.NewFileStream_ns.restype = c_void_p
    name = create_string_buffer(name)
    return libN.NewFileStream_ns(name, env_p, None)  # file_p


def NewNeticaEnviron(licencia):
    """
    Set-up environment condition to run Netica
    """
    libN.NewNeticaEnviron_ns.argtypes = [c_char_p, c_void_p, c_void_p]
    libN.NewNeticaEnviron_ns.restype = c_void_p
    if not licencia:
        env = libN.NewNeticaEnviron_ns(None, None, None)
    else:
        env = libN.NewNeticaEnviron_ns(licencia, None, None)
    return env


def InitNetica(env_p):
    """
    Initilize Netica with environment conditions already defined
    """
    mesg = create_string_buffer(MESGLEN)
    # (environ_ns* env, char* mesg)
    libN.InitNetica2_bn.argtypes = [c_void_p, c_char_p]
    libN.InitNetica2_bn.restype = c_int
    res = libN.InitNetica2_bn(env_p, mesg)
    logger.info(mesg.value)
    return res


def CloseNetica(env_p):
    """
    close environment
    """
    # (environ_ns* env, char* mesg)
    libN.CloseNetica_bn.argtypes = [c_void_p, c_char_p]
    libN.CloseNetica_bn.restype = c_int
    mesg = create_string_buffer(MESGLEN)
    res = libN.CloseNetica_bn(env_p, mesg)
    logger.info(mesg.value)
    return res, mesg


def SaveNet(name, env_p, net_p):
        """
        Creates new stream and writes net
        """
        file_p = NewFileStream(name, env_p)
        libN.WriteNet_bn.argtypes = [c_void_p, c_void_p]
        libN.WriteNet_bn.restype = None
        libN.WriteNet_bn(net_p, file_p)


def ReadNet(name, env_p):
    """
    Reads a net from file
    """
    # (stream_ns* file, int options)
    file_p = NewFileStream(name, env_p)
    libN.ReadNet_bn.argtypes = [c_void_p, c_int]
    libN.ReadNet_bn.restype = c_void_p
    return libN.ReadNet_bn(file_p, REGULAR_WINDOW)  # net_p


def GetNetNodes(net_p):
    """
    get net nodes
    """
    zerochar_type = c_char*0
    # (const net_bn* net, const char options[])
    libN.GetNetNodes2_bn.argtypes = [c_void_p, zerochar_type]
    libN.GetNetNodes2_bn.restype = c_void_p
    return libN.GetNetNodes2_bn(net_p, zerochar_type())  # nl_p


# find and load the library, assuming in a relative path closeby
my_dir = "C:/Users/equih/Documents/0 Versiones/2 Proyectos/"
proy_dir = "BN_GitHub/Scripts/Netica_API/Python/C_API_wrapper"

# Prepare some data paths by replaceing where appropriated
netica_dir = my_dir + "BN_GitHub/Scripts/Netica_API/Python/"
datos_dir = re.sub("Scripts/Netica_API/Python/C_API_wrapper", "redes_ajuste_MyO/", proy_dir)
net_dsk = os.listdir(my_dir + datos_dir)
net_dsk = [my_dir + datos_dir + net for net in net_dsk
           if "neta" in net and "test" not in net]

# load the library, assuming in a relative path closeby
libN = windll.LoadLibrary(netica_dir + "netica/Netica.dll")
licensefile = netica_dir + "netica/inecol_netica.txt"
licencia = open(licensefile, 'r').readlines()[0].strip().split()[0]

# Initialize a PyNetica instance/env using password in a text file
env_p = NewNeticaEnviron(licencia)

# Initialize NETICA environment
mesg = create_string_buffer(MESGLEN)
res = InitNetica(env_p)
logger.info(mesg.value)
print('\n'*2 + '#' * 40 + '\nOpening Netica:')
print(mesg.value)

for net in net_dsk:
    net_p = ReadNet(net, env_p)  # net_p

    # TODO API function to wrap!!!
    file_name = c_char_p(libN.GetNetFileName_bn(net_p))
    net_name = c_char_p(libN.GetNetName_bn(net_p))

    """
    get net nodes
    """
    # (const net_bn* net, const char options[])
    zerochar_type = c_char*0
    nl_p = GetNetNodes(net_p)  # nl_p

    """
    get number of nodes
    """
    # (const nodelist_bn* nodes)
    nnodes = c_int(libN.LengthNodeList_bn(nl_p))  # nnodes

    # Collect all node names in network
    node_names = {"gral": {}, "infys": {}, "pp": {}, "pt": {},
                  "tm": {}, "tr": {}, "tx": {}}
    for i in range(nnodes.value):
        node_p = c_void_p(libN.NthNode_bn(nl_p, i))  # node_p
        name = c_char_p(libN.GetNodeName_bn(node_p))  # name
        if re.search(r"^[xyZzdC]", name.value):
            if name.value is "y": name.value = "latitude"
            node_names["gral"][name.value] = node_p
        elif re.search(r"(^ntre|^Diam|^Alt|^Ins|^Sin|^prob|^Psn|^Gpp)",
                       name.value):
            node_names["infys"][name.value] = node_p
        elif re.search(r"^ppt[0-1]{1}", name.value):
            node_names["pp"][name.value] = node_p
        elif re.search(r"^pptm", name.value):
            node_names["pt"][name.value] = node_p
        elif re.search(r"^tma", name.value):
            node_names["tx"][name.value] = node_p
        elif re.search(r"^tmi", name.value):
            node_names["tm"][name.value] = node_p
        else:
            node_names["tr"][name.value] = node_p

        a1 = sorted(node_names["gral"].keys() + node_names["infys"].keys())
        a1 = ["    {\"" + nodo + "\": \"0.0\"}" for nodo in a1]

    print("\n\n")
    print("##### " + re.sub(".neta", "",os.path.basename(file_name.value)))
    print("\n")
    print("```javascript")
    print("{\"" + re.sub(".neta", "",os.path.basename(file_name.value)) + "\":{")
    print("\"Description\": \"Poner aquí la descripción del modelo en cuestión\",")
    print("\"Training_data_set\": \"data\",")
    print("\"Results\": [")
    print("    {\"Absolute error (rms)\": \"0.0\"},")
    print("    {\"Error rate (%)\": \"0.0\"},")
    print("    {\"Logarithmic loss\": \"0.0\"},")
    print("    {\"Quadratic loss\": \"0.0\"},")
    print("    {\"Spherical payoff\": \"0.0\"}")
    print("      ],")
    print("\"Variables (variance reduction)\": [")
    print(",\n".join(a1))
    print("      ]")
    print(" }")
    print("}")
    print("```")
net_dsk_ref = [re.sub("/", r"\\", f) for f in net_dsk]
