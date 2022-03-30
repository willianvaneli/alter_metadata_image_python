#!/usr/bin/env python
# -*- coding: utf-8 -*-

import progressbar
import os
import pyexiv2
import copy
import shutil

VALOR_PITCH_PADRAO = '0'
VALOR_ROLL_PADRAO = '0'

print("Starting ...")
bar = progressbar.ProgressBar()

if not os.path.isdir('./originais'):
    os.mkdir('./originais')

pasta = './'
for diretorio, subpastas, arquivos in os.walk(pasta):
    bar.start(len(arquivos))
    i=0
    for arquivo in arquivos:
        if 'jpg' in arquivo:
            caminho = os.path.join(os.path.realpath(arquivo))
            
            nome_diretorio = os.path.dirname(caminho)
            
            try:
                img = pyexiv2.Image(caminho)            
                # Metadados originais
                data = img.read_xmp()
                alterado = False
                dic = copy.deepcopy(data)
                
                if ('Xmp.GPano.PosePitchDegrees' in data) and (float(data['Xmp.GPano.PosePitchDegrees']) > 1 or float(data['Xmp.GPano.PosePitchDegrees']) < -1)  :
                    alterado = True
                    dic['Xmp.GPano.PosePitchDegrees'] = VALOR_PITCH_PADRAO
                    
                if ('Xmp.GPano.PoseRollDegrees' in data) and (float(data['Xmp.GPano.PoseRollDegrees']) > 1 or float(data['Xmp.GPano.PoseRollDegrees']) < -1)  :
                    alterado = True
                    dic['Xmp.GPano.PoseRollDegrees'] = VALOR_ROLL_PADRAO
                
                # Caso tenha necessidade de alterar passa a imagem para processados e a corrige
                if alterado:
                    #shutil.copy2(caminho, nome_diretorio + '\\originais\\' + arquivo)
                    shutil.copy2(caminho, nome_diretorio + '\\originais\\' + arquivo)
                    nova_img = pyexiv2.Image(caminho)
                    nova_img.modify_xmp(dic)
                    nova_img.close()
                img.close()
            except:
                print("Imagem " + caminho + " não pode ser aberta")

            
            i+=1
            bar.update(i)
