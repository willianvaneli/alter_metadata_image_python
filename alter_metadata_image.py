#!/usr/bin/env python
# -*- coding: utf-8 -*-

import progressbar
import os
import pyexiv2

from PIL import Image
VALOR_PITCH_PADRAO = '0'
VALOR_ROLL_PADRAO = '0'

print("Starting ...")
bar = progressbar.ProgressBar()

if not os.path.isdir('./processados'):
    os.mkdir('./processados')
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
            
            img = pyexiv2.Image(caminho)
            # Metadados originais
            data = img.read_xmp()
            alterado = False
            dic = {}
            
            if(float(data['Xmp.GPano.PosePitchDegrees']) > 1 or float(data['Xmp.GPano.PosePitchDegrees']) < -1)  :
                alterado = True
                dic['Xmp.GPano.PosePitchDegrees'] = VALOR_PITCH_PADRAO
                
            if(float(data['Xmp.GPano.PoseRollDegrees']) > 1 or float(data['Xmp.GPano.PoseRollDegrees']) < -1)  :
                alterado = True
                dic['Xmp.GPano.PoseRollDegrees'] = VALOR_ROLL_PADRAO
            
            # Caso tenha necessidade de alterar passa a imagem para processados e a corrige
            if alterado:
                image = Image.open(caminho)
                image.save(nome_diretorio + '\\processados\\' + arquivo)
                image.save(nome_diretorio + '\\originais\\' + arquivo)
                nova_img = pyexiv2.Image(nome_diretorio + '\\processados\\' + arquivo)
                nova_img.modify_xmp(dic)
                nova_img.close()
            
            img.close()
            i+=1
            bar.update(i)
