import os

dir_trabajo = "Z:\\2_set_cobertura_completa\\"
archivos_datos_en_z = [fl for fl in os.listdir(dir_trabajo)
                       if fl.startswith("ie_mex_full_dataset")]
print(archivos_datos_en_z)

with open(dir_trabajo + archivos_datos_en_z[0], "r") as infile,\
     open(dir_trabajo + "corregido.csv", "w") as outfile:
    data_tabla = infile.read()
    data_tabla.replace("NA", "*")
    outfile.write(data_tabla)

print("Fin")