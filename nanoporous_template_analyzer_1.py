# Copyright: Leonardo Tomiatti
# Last update: 26-09-2024
# Release date: 26-09-2024

#  Copyright 2024 Leonardo Tomiatti
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from jes4py import * # Pacote para ler caminho da imagem.
from PIL import Image,ImageEnhance # Pacote para substituir cores em escala preto em branco para cores RGB padrão.
import math # Pacote para obter o valor de pi.

# Verifica se a imagem de entrada está em escala preto e branco.
def check_grayscale(picture):
    #rgb_picture=picture.convert('RGB')
    width,height=picture.size
    for y in range(height):
        for x in range(width):
            r,g,b=picture.getpixel((x, y))
            if r!=g or r!=b or g!=b:
                print("\nYour image is not in grayscale! This program cannot analyze this.")
                passive_user_response3=input("\nPress any key to close the program.")
                print()
                exit()
    return print("\nYour image is in grayscale. This program can analyze this!")

# Trata e converte uma imagem em escala preto e branco para cores RGB padrão.
def grayscale_to_RGB_standard(picture):
    r_limit=int(input("Define the first cut (0-255): "))
    g_limit=int(input("Define the second cut (0-255): "))
    b_limit=255
    #rgb_standard_picture=picture.convert('RGB')
    rgb_standard_picture=picture.copy()
    width,height=rgb_standard_picture.size
    pixel=rgb_standard_picture.load()
    for y in range(height):
        for x in range(width):
            r,g,b=rgb_standard_picture.getpixel((x, y))
            if r<=r_limit:
                pixel[x,y]=(255,0,0)
            elif r<=g_limit:
                pixel[x,y]=(0,255,0)
            elif r<=b_limit:
                pixel[x,y]=(0,0,255)
    return rgb_standard_picture
    
# Trata uma imagem em escala preto e branco.
def improve_picture(picture):
    color_improvement=float(input("\nColor improvement (%): "))
    contrast_improvement=float(input("Contrast improvement (%): "))
    brightness_improvement=float(input("Brightness improvement (%): "))
    sharpness_improvement=float(input("Sharpness improvement (%): "))
    picture_improved=picture
    improved_bol=False
    if color_improvement!=0:
        improved_bol=True
        color_improvement_factor=1+color_improvement/100
        picture_improved=ImageEnhance.Color(picture_improved)
        picture_improved=picture_improved.enhance(color_improvement_factor)
    if contrast_improvement!=0:
        improved_bol=True
        contrast_improvement_factor=1+contrast_improvement/100
        picture_improved=ImageEnhance.Contrast(picture_improved)
        picture_improved=picture_improved.enhance(contrast_improvement_factor)
    if brightness_improvement!=0:
        improved_bol=True
        brightness_improvement_factor=1+brightness_improvement/100
        picture_improved=ImageEnhance.Brightness(picture_improved)
        picture_improved=picture_improved.enhance(brightness_improvement_factor)
    if sharpness_improvement!=0:
        improved_bol=True
        sharpness_improvement_factor=1+sharpness_improvement/100
        picture_improved=ImageEnhance.Sharpness(picture_improved)
        picture_improved=picture_improved.enhance(sharpness_improvement_factor)
    #rgb_standard_picture=picture_improved.convert('RGB')
    return picture_improved,improved_bol

# Contabiliza o número de pixels RGB padrão em rgb_standard_picture e retorna a tupla (NpxR,NpxG,NpxB).
def count_standard_RGB_pixels(rgb_standard_picture):
    NpxR=NpxG=NpxB=0
    width,height=rgb_standard_picture.size
    pixel=rgb_standard_picture.load()
    for y in range(height):
        for x in range(width):
            if pixel[x,y]==(255,0,0):
                NpxR+=1
            elif pixel[x,y]==(0,255,0):
                NpxG+=1
            elif pixel[x,y]==(0,0,255):
                NpxB+=1
            else:
                print("\nYour image is not in RGB standard colors scale! This function cannot work properly.\n")
                exit()
    return (NpxR,NpxG,NpxB)

def check_blank_line(picture,y_candidate):
    #rgb_picture=picture.convert('RGB')
    width,height=picture.size
    for x in range(width):
        r,g,b=picture.getpixel((x, y_candidate))
        if r!=255 or g!=255 or b!=255:
            return False
    return True
    
def find_y_crop(picture):
    #rgb_picture=picture.convert('RGB')
    width,height=picture.size
    for y in range(height):
        if check_blank_line(picture,y):
            return y
    return height

print("""
                                ▓███████████░░▓▓░                               
                          ▓▒▒▒▓█████████████░░░▒▒▒▒▒▒▓░                         
                      ░░▒▒▒▒▒▒█████████████▓ ░░▒▒▒▒▒▒▒▒▒▒▒░                     
                  ▓███▒░░▒▒▒▒▒████████████▓░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓                  
                ██████▓░░▒▒▒▒▒▒██████████▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                
              ████████▒░▒▒▒▒▒▒▒▒▓██████▓▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▓██              
            █████████▓░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒████████▓▒▒▒▒▒▒▒▓████            
          █████████▓▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████████▓░▒▒▒▒▒▓█████          
        ▓▒▓▓█████▓▓▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓████████████▒░▒▒▒▒▒▒▓▓▓██▓        
       ▓▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▓███████▓▒░░▒▒▒▒▒▒▒▒█████████████▒░░▒▒▒▒▒▒▒▒▒▒▒▓       
      ▒▒▒▒▒▒▒ ▒▒▒ ▒▒▒▒▒▒████████████▓░░░▒▒▒▒▒▓███████████▓▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒      
     ▒▒▒▒▒▒▒▒  ▓▒ ▓▒▒▒▒▓██████████████░░░▒▒▒▒▒▓█████████▓▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒     
    ▒▒▒▒▓▓▓▒▒ ▒ ▒ ▓▒   ██ ░  █░   ██ ░  ░    ▒▓ ░ ▒█    ▒ ▓▒ ▓▒   ▓▒▒▒▒▒▒▒▒▒    
   ▓▒▓███████ ░ ░ ▓▓▓▒ ██ ██ █ ░█ ██ █▒ ▒ ▒▒ ▓▓ ▒  ▓ ▓▒ ▒ ▓▒ ▓▒ ▓▓▓██▓▒▒▒▒▒▒▓   
  ▓▒▓████████ ░█  ▓ ░▓ █▓ █▓ █ ░█ ██ ▓▒ ▒ ▒▒ ▓▓ ▒▒▒▒ ▒░ ▒ ▓▒ ███░ ░█████▒▒▒▒▒█  
  ▒▒█████████ ░██ ▒    ▓▒ █▓ █    █▓    ▒    ▓▓ ▒▒▒▓    ▒    █▓    ██████▒▒▒▒▒  
 ▓▒▓████████████▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒ ▒▒▒▒▒▒▓██▓▓▓▒▒▒▒▒▒▒▒▒▒▓█████████████▓▒▒▒▒▓ 
 ▒▒▓████████████▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████▓▒▒▒▒▒▒▒▒▒▓████████████▓░▒▒▒▒ 
 ▒▒▒███████████▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████░░▒▒▒▒▒▒▓███████████▒▒▒▒▒▒ 
▓░░▒▒▓███████▓▒▒▒▒▒     ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓███ ▓███████▓░▒▒▒▒▒▒▒▓▓███████▓▒▒▒▒▒▒▒▓
▒░░▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒ ▓██████▓▒▒▒▒▒▒▒▒▒▒▓███ ▒██████▓ ▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▒▒▒▒▓▒▒▒▓
▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒█ ▓██    █       ▓▒    █ ▒█    █   ▒    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓██
▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▓██ ▓██ ██ █  ▓ ░▒ ▓▓ ▓▒ █ ▒███▓ █▓ ▒▒ ▓▒ ▓▒▒▒▒▒▒▒▒▒▒▒▓▓▒▓▓███
▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██ ▓██ ████  █ ░▒ ▓▓ ▓▒ ▓ ▒▓ ▓▓ ▓▓ ▒▒ ▓▒▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓███
▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓██ ▓██    █  ▓ ░▒ ▓▓   ░▒ ▒▒    ▓▓  ▓    ██████▒▒▒▒▒▒▒▒▒▓▓██▓
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓████████████▒▒▒▒▒▒▓ ▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▓████████████▒▒▒▒▒▒▒▓▓█ 
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓████████▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▓█████████████▒░▒▒▒▒▒▒▓ 
 ▓██▓░░░░▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓███▓▒▒▒▒▒▒▒▒▒▒▒▓█████████████▓▒▒▒▒▒▒▒▓ 
  ███▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒  ▓▒▒▒▒▒▒▒▒▒▒▒▓█ ████████▓▒▒▒▒▒▒▒▒▓▓███████████▓▒▒▒▒▒▒▒▒  
  ▓██▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ░░▒▒▒▒▒▒▒▒▒▒▓██ ██████████▒▒▒▒▒▒▒▒▓▓▓███████▓▓▒▒▒▒▒▒▒▒▓  
   ██▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▓ ▒▒    ▓ ░░ ██ █ ▒█ █    ▓ ░░ ▒    ▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▓   
    ▓░░▒▒▒▒▒▒▓███████ ░░ ▓▒ ▒▒ ▒░   █▓ █▓ █ ██  █▒    ▒  ▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█    
     ░▒▒▒▒▒▒█████████ ▓▓ ░░ ▒▒ ▒ ▓▒ ▓▓ ██  ██░ █▓▒ ▓▒ ▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██     
      ▒▒▒▒▒▓████████▓ ██▓ █ ▒▒ ▒░ ▓ ▓▓ ▓▓▒ ▓▓    ▒   ░▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██      
       ▓▒▒▒███████████████▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓█▓▒▒▒▒▒▒▒▒▒▒▓▓▓       
        ▒▒▓▓██████████████▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█████████▒▒▒▒▒▒▒▒         
          ▓▓▓▓▓████████▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓███████████▓▒▒▒▒▒          
            ▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▓▒▓▓▓▓▓▓████████████▒▒▒            
              ▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█████████▓▒▒▒▒▒▒▒▓████████████▒              
                ▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████████▒▒▒▒▒▒▒▓▓████████▓                
                  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█████████████▓░▒▒▒▒▒▒▓▓▓▓▓█▓▒                  
                      ▒▒▒▒▒▒▒▒▒▒▓█████████████▓▒▒▒▒▒▒▒▒▒▒▓                      
                          ▓░▒▒▒▒▒▓▓██████████▓▒░▒▒▒▒▒▓                          
                                ▓▓▓▓▓██████▓▓▒▓▓                                
                                                    Copyright: Leonardo Tomiatti
""")

print("Welcome to Nanoporous Template Analyzer 1!")
passive_user_response1=input("\nPress any key to select your Scanning Electron Microscopy (SEM) image. It cannot have 'jpg' extension and your filename cannot contain special characters!")

path_to_picture=pickAFile() # Fornece o caminho da imagem que iremos trabalhar.
picture=Image.open(path_to_picture) # Armazena a imagem na variável de trabalho.
picture=picture.convert('RGB') # Converte para RGB.
        
check_grayscale(picture)

print()
path_to_save=input(r"Where you want to save the resulting images: ")+"\\"
rgb_standard_picture_name=input("What is the new images name: ")
rgb_standard_picture_ext="png"
path=path_to_save+rgb_standard_picture_name+"_rgb-standard."+rgb_standard_picture_ext

width,height=picture.size
cropped_picture=picture.crop((0,0,width,find_y_crop(picture)))

path_cropped=path_to_save+rgb_standard_picture_name+"_cropped."+rgb_standard_picture_ext
print("\nThe path to your cropped image is: "+path_cropped)
cropped_picture.save(path_cropped)

print("\nThe challenge now is find two optimal cut parameters to divide grayscale in three RGB standard colors. Consider that this scale limits are 0 (black) and 255 (white).")
passive_user_response2=input("Your final image will have only three RGB standard colors. Each one have different meaning: red is empty pore, green is interstitial region and blue is filled pore.")

cropped_picture.show()

satisfied="N"
while satisfied!="Y" and satisfied!="y":
    if satisfied=="N" or satisfied=="n":
        picture_improved,improved_bol=improve_picture(cropped_picture)
        rgb_standard_picture=grayscale_to_RGB_standard(picture_improved)
        rgb_standard_picture.show()
        satisfied=input("These are your optimal parameters (Y/N): ")
    else:
        print("The program cannot understand what you typed.")
        satisfied_cut="N"

print("\nThe path to your RGB standard colors image is: "+path)

if improved_bol==True:
    path_improved=path_to_save+rgb_standard_picture_name+"_improved."+rgb_standard_picture_ext
    print("The path to your improved image is: "+path_improved)
    picture_improved.save(path_improved)

rgb_standard_picture.save(path) # Escreve a nova imagem no diretório especificado.

print("\nProvide information about your SEM image to complete the analysis: ")
scale_unit=input("Scale unit: ")
scale_factor=float(input("Scale factor in px/"+scale_unit+" units: "))
pore_diameter=float(input("Mean diameter of your pore in "+scale_unit+" units: "))

(NpxR,NpxG,NpxB)=count_standard_RGB_pixels(rgb_standard_picture)

A_pores_px=NpxR+NpxB
A_filled_pores_px=NpxB
A_total_px=NpxR+NpxG+NpxB

A_pores=A_pores_px/pow(scale_factor,2)
A_filled_pores=A_filled_pores_px/pow(scale_factor,2)
A_total=A_total_px/pow(scale_factor,2)

filling_rate_percentage=100*A_filled_pores_px/A_pores_px
porosity_percentage=100*A_pores_px/A_total_px

A_one_pore=(math.pi*pow(pore_diameter,2))/4

N_pores=A_pores/A_one_pore
N_filled_pores=A_filled_pores/A_one_pore

d_pores=N_pores/A_total
d_filled_pores=N_filled_pores/A_total

print("\n---------- ANALYSIS RESULTS ----------")

print("\nPIXELS COUNTING:")
print("RGB standard colors image:",A_total_px,"px")
print("Empty pores:",NpxR,"px")
print("Interstitial region:",NpxG,"px")
print("Filled pores:",A_filled_pores_px,"px")
print("Pores:",A_pores_px,"px")

print("\nPHYSICAL QUANTITIES:")
print("One pore's area:",A_one_pore,scale_unit+"\N{SUPERSCRIPT TWO}")
print("Pore density:",d_pores,scale_unit+"\u207B"+"\N{SUPERSCRIPT TWO}")
print("Pore filled density:",d_filled_pores,scale_unit+"\u207B"+"\N{SUPERSCRIPT TWO}")

print("\nQUALIFYING CALCULATIONS:")
print("Pores counted:",N_pores)
print("Porosity (%):",porosity_percentage)
print("Filled pores counted:",N_filled_pores)
print("Filling rate (%):",filling_rate_percentage)

passive_user_response3=input("\nPress any key to close the program.")
print()