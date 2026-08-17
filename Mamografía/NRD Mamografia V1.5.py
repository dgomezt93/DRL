import pandas as pd
import pydicom
import os
import numpy as np
from datetime import datetime
import PySimpleGUI as sg
sg.theme('LightGrey')

ruta_carpeta = sg.popup_get_folder("Seleccionar carpeta")
print(ruta_carpeta)

contador = 0

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()
fecha_actual = str(fecha_hora_actual.date()) + "_" + str(fecha_hora_actual.hour) + str(fecha_hora_actual.minute)
print("Fecha actual:", fecha_actual)

# Especificar la ruta del archivo Excel

ruta_archivo = "C:/Users/Daniela G/Desktop/PruebaDicom/Mamografia" + str(fecha_actual) + ".xlsx"#asigno una ruta para archivo 


# Define the tags
tagEdad = (0x0010, 0x1010)
tagkVp = (0x0018, 0x0060)
tagExpTime = (0x0018, 0x1150)
tagmAs = (0x0018, 0x1152)
tagOrganDose = (0x0040, 0x0316)
tagEntranceDose = (0x0040, 0x8302)
tagStudyDescrip = (0x0008, 0x1030)
tagImageLaterality = (0x0020, 0x0060)  # Corregido el tag de '002,0016' a '0020,0060'
tagViewPosition = (0x0018, 0x5101)
tagThickness = (0x0018, 0x11A0)
tagAnode = (0x0018, 0x1191)
tagFilterMaterial = (0x0018, 0x7050)
tagManufacture = (0x0008, 0x0070)
tagModel= (0x0008, 0x1090)
tagInstitutionName = (0x0008,0x0080)
tagUID = (0x0020,0x000D)
tagserial = (0x0018,0x1000)
tagLaterality = (0x0020,0x0062)

# Definir funciones
def listar_archivos_en_carpeta(ruta_carpeta):
    nombres_archivos = []
    if os.path.isdir(ruta_carpeta):
        archivos_en_carpeta = os.listdir(ruta_carpeta)
        for archivo in archivos_en_carpeta:
            ruta_absoluta = os.path.join(ruta_carpeta, archivo)
            if os.path.isfile(ruta_absoluta):
                nombres_archivos.append(archivo)
    else:
        print("La ruta proporcionada no es una carpeta.")
    return nombres_archivos


import pydicom
import os

# Función para extraer metadatos DICOM con filtrado por espesor de mama
def extract_dicom_metadata(dicom_file):
    try:
        ds = pydicom.dcmread(dicom_file)  # Leer archivo DICOM
    except Exception as e:
        print(f"Error al leer {dicom_file}: {e}")
        return None  # Si el archivo no se puede leer, devolver None

    # Obtener nombre del archivo
    nombre_archivo = os.path.basename(dicom_file)

    # Verificar si `tagThickness` existe y tiene un valor válido
    if tagThickness in ds and ds[tagThickness].value is not None:
        try:
            espesor = float(ds[tagThickness].value) / 10  # Convertir a mm
        except ValueError:
            print(f"Error en el espesor de {dicom_file}")
            return None  # Si el espesor no es un número válido, descartar el archivo

        # Si el espesor NO está en el rango, descartar la imagen
        if not (4.2 < espesor < 4.8):
            return None  

    else:
        return None  # Si no tiene `tagThickness`, descartar el archivo

    # Extraer metadatos de manera segura
    metadata = [
        nombre_archivo,
        ds.get(tagStudyDescrip, "N/A"),
        ds.get(tagkVp, "N/A"),
        ds.get(tagExpTime, "N/A"),
        ds.get(tagmAs, "N/A"),
        ds.get(tagEntranceDose, "N/A"),
        ds.get(tagViewPosition, "N/A"),
        espesor,  # Guardar espesor dentro del rango
        ds.get(tagManufacture, "N/A"),
        ds.get(tagModel, "N/A"),
        ds.get(tagInstitutionName, "N/A"),
        ds.get(tagUID, "N/A"),
        ds.get(tagserial, "N/A"),
        ds.get(tagLaterality, "N/A")
    ]

    return metadata  # Retornar la lista con metadatos



# Ruta de la carpeta con imágenes DICOM
nombres_archivos = listar_archivos_en_carpeta(ruta_carpeta)

# Definir las columnas del DataFrame
columnas = ['Archivo', 'Estudio', 'kV', 'Tiempo de Exposición mSec', 'mAs', 'Dosis de Entrada [mGy]', 'Proyección', 'Espesor', 'Fabricante','Modelo','Institución', 'UID','Serial','Laterality']
#se crea el dataframe con las columnas definidas
df = pd.DataFrame(columns=columnas)

index = 0
for nombre_archivo in nombres_archivos:
    print(nombre_archivo)  # Imprimir nombre del archivo procesado
    index += 1
    sg.one_line_progress_meter("Current Progress", index, len(nombres_archivos))

    dicom_file = os.path.join(ruta_carpeta, nombre_archivo)  # Obtener la ruta completa
    metadata = extract_dicom_metadata(dicom_file)  # Extraer información DICOM

    if metadata is None:
        print(f"Imagen descartada: {nombre_archivo}")
        continue  # ❌ Saltar esta imagen si no cumple los criterios

    print(metadata)  # ✅ Solo imprimir si metadata es válido
    #print(len(metadata))  # ✅ Evita TypeError

    # Agregar al DataFrame si metadata es válido
    if len(metadata) == len(columnas):  # Verificar que metadata tenga el tamaño correcto
        df.loc[len(df)] = metadata  # Agregar fila al DataFrame
        print("Imagen procesada correctamente")
    else:
        print(f"Error en metadata de {nombre_archivo}, tamaño incorrecto")

    # 
    if len(metadata) != 0:
        df.loc[len(df)] = metadata# agrego al dataframe una fila con los valores de la informacion de la imagen dicom
   
        print("****************************")# caracteres para separar un archivo de otro y repito el for hasta lea todos los archivos existentes en la carpeta
    else:
        print("paciente pediatrico")
print(df)#muestro el dataframe





# Guardar el DataFrame en un archivo Excel
df.to_excel(ruta_archivo, index=False)#creo un archivo excel apartir del df, con nombre DatosFechahora.xlsx

print("Datos guardados en el archivo Excel:", ruta_archivo)

sg.popup_ok("Tarea realizada")
#print("# de Archivos con EntranceDoseInmGy = ", contador)


while True:
    try:
        T1 = df['Serial'].unique()
        layout = [
        [sg.Text('Seleccione una opción:')],
        [sg.Combo(T1, default_value=T1[0], key='-COMBO-', size=(30,1))],
        [sg.Button('Seleccionar')]
        ]
         # Create the window
        window = sg.Window('Seleccionar equipo de interés', layout)
        
        event, values = window.read()
        # If the user clicks the Submit button
        if event == 'Seleccionar':
            selected_option = values['-COMBO-']
            Serial=selected_option
            window.close()
        if event == sg.WIN_CLOSED:
            exit()
        df1 = None  # ✅ Inicializa df1 como None antes del bucle
        if Serial in T1:
            df1 = df[df['Serial']==Serial]#en DF1 dataframe filtrado por modelo del equipo
            print("\n",df1,"\n")
            unique_strings = df1['Proyección'].unique()

            
            

            print(unique_strings)
            unique_strings_2 = [s.strip() for s in unique_strings]  # Eliminar espacios extra
            print(unique_strings_2)

        
            for est in unique_strings_2:
                print("Nivel de Referencia proyección " + est)
                df2=df1[df1['Proyección']==est]#dentro del Dataframe para un modelo de equipo filtro por descripcion de la serie ej: "Torax simple"
                dfresultado=df2
                # Agrupar por 'NOMBRE' y sumar los valores de 'DLP'
                #dfresultado = df2.groupby('Nombre Imagen', as_index=False).agg({'DLP': 'sum','CTDIvol_name': 'sum'})

                # Mostrar el resultado
                #print(dfresultado)

                Entrance_Dose_np = dfresultado['Dosis de Entrada [mGy]'].to_numpy()  # Convert to NumPy array if needed
                    
                # Calculate percentiles and statistics
                fq_ed = np.percentile(Entrance_Dose_np, 25)
                sq_ed = np.percentile(Entrance_Dose_np, 50)
                tq_ed = np.percentile(Entrance_Dose_np, 75)
                max_ed = np.max(Entrance_Dose_np)
                min_ed = np.min(Entrance_Dose_np)

                print("fq_ed:", fq_ed)
                print("sq_ed:", sq_ed)
                print("tq_ed:", tq_ed)
                print("max_ed:", max_ed)
                print("min_ed:", min_ed)

                    

                columnas2 = ['Estadística','Dosis de entrada [mGy]']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
                #'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
                dataFrame = pd.DataFrame(columns=columnas2)# creo un dataframe y nombro las columnas del como sea requerido

                # Append statistics to DataFrame
                dataFrame.loc[len(dataFrame)] = ['1st Quartile', "{:.1f}".format(fq_ed)]
                dataFrame.loc[len(dataFrame)] = ['2nd Quartile', "{:.1f}".format(sq_ed)]
                dataFrame.loc[len(dataFrame)] = ['3rd Quartile', "{:.1f}".format(tq_ed)]
                dataFrame.loc[len(dataFrame)] = ['Min', "{:.1f}".format(min_ed)]
                dataFrame.loc[len(dataFrame)] = ['Max', "{:.1f}".format(max_ed)]

                print(dataFrame)  # Display DataFrame

                # Convert the DataFrame to a list of lists
                data_list = dataFrame.values.tolist()
                header_list = dataFrame.columns.tolist()

                # Define the layout for PySimpleGUI
                layout = [
                    [sg.Table(values=data_list, headings=header_list,
                            auto_size_columns=True, display_row_numbers=False,
                            justification='center', num_rows=min(25, len(data_list)))],
                    [sg.Button('Exit')]
                ]

                # Create the window
                window = sg.Window("Nivel de Referencia "+est, layout)


                # Event loop to process events and get values from the inputs
                while True:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'Exit':
                        break

                # Close the window
                window.close()


    except Exception as e:
        # Handle any other unexpected errors
        print("Error try: ")
        print(e)

    break
print('df1:::::::::::::::::')
print(df1)
df_dosis_proyeccion = df.groupby(['UID', 'Laterality', 'Proyección'], as_index=False)['Dosis de Entrada [mGy]'].sum()
df_dosis_mama = df_dosis_proyeccion.groupby(['UID', 'Laterality'], as_index=False)['Dosis de Entrada [mGy]'].sum()
df_dosis_total = df_dosis_mama.groupby('UID', as_index=False)['Dosis de Entrada [mGy]'].sum()
df_dosis_total['Dosis Total'] = df_dosis_total['Dosis de Entrada [mGy]'] / 2  # Promedio de ambas mamas
print('Dosis total')
print(df_dosis_total)

Dosis_total_np = df_dosis_total['Dosis de Entrada [mGy]'].to_numpy()  # Convert to NumPy array if needed
                    
# Calculate percentiles and statistics
fq_ed = np.percentile(Entrance_Dose_np, 25)
sq_ed = np.percentile(Entrance_Dose_np, 50)
tq_ed = np.percentile(Entrance_Dose_np, 75)
max_ed = np.max(Entrance_Dose_np)
min_ed = np.min(Entrance_Dose_np)

print("fq_ed:", fq_ed)
print("sq_ed:", sq_ed)
print("tq_ed:", tq_ed)
print("max_ed:", max_ed)
print("min_ed:", min_ed)

    

columnas3 = ['Estadística','Dosis total [mGy]']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
#'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
dataFrame = pd.DataFrame(columns=columnas2)# creo un dataframe y nombro las columnas del como sea requerido

# Append statistics to DataFrame
dataFrame.loc[len(dataFrame)] = ['1st Quartile', "{:.1f}".format(fq_ed)]
dataFrame.loc[len(dataFrame)] = ['2nd Quartile', "{:.1f}".format(sq_ed)]
dataFrame.loc[len(dataFrame)] = ['3rd Quartile', "{:.1f}".format(tq_ed)]
dataFrame.loc[len(dataFrame)] = ['Min', "{:.1f}".format(min_ed)]
dataFrame.loc[len(dataFrame)] = ['Max', "{:.1f}".format(max_ed)]

print(dataFrame)  # Display DataFrame

# Convert the DataFrame to a list of lists
data_list = dataFrame.values.tolist()
header_list = dataFrame.columns.tolist()

# Define the layout for PySimpleGUI
layout = [
    [sg.Table(values=data_list, headings=header_list,
            auto_size_columns=True, display_row_numbers=False,
            justification='center', num_rows=min(25, len(data_list)))],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Nivel de Referencia Dosis Total', layout)


# Event loop to process events and get values from the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

# Close the window
window.close()
