import json

import eda
from tqdm import tqdm

# Cargar parámetros
with open("eda_params.json", "r", encoding="utf8") as file_params:
    params = json.load(file_params)

# Cargar conjunto de entrenamiento (conll)
train_chv = open(params['input_conll'], 'r', encoding='utf8')

# Generar nuevo conjunto de entrenamiento
new_train_chv = open(params['output_conll'], 'w', encoding='utf8')

# Separar conll por ficheros
file = ''
file_name = '?'
for line in tqdm(train_chv):

    # Omitir líneas vacías
    if line != '\n':

        # Si es el inicio de un fichero (tag == '-')
        if line.split(' ')[2] == '-\n':

            # Si el ya había un fichero antes, aplicar EDA al fichero
            if file != '':

                # Apply EDA
                new_files_list = eda.eda(file, alpha_sr=params['alpha_sr'], alpha_ri=params['alpha_ri'],
                                         alpha_rs=params['alpha_rs'], alpha_rd=params['alpha_rd'],
                                         num_aug=params['num_augmented_sentences'])

                new_train_chv.write('\n' + file)

                index = 1
                for f in new_files_list:
                    new_train_chv.write('\n' + f)
                    index += 1

            # Inicializar nuevo fichero
            file = ''

        # Añadir lineas
        file += line

# Apply EDA (for the last file)
new_files_list = eda.eda(file, alpha_sr=params['alpha_sr'], alpha_ri=params['alpha_ri'],
                         alpha_rs=params['alpha_rs'], alpha_rd=params['alpha_rd'],
                         num_aug=params['num_augmented_sentences'])

new_train_chv.write(f'\n{file}\n')

for f in new_files_list:
    new_train_chv.write('\n' + f)

train_chv.close()
new_train_chv.close()
