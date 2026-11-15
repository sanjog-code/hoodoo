import os
from PIL import Image
import numpy as np

p1_l = Image.open(r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\diagnose_halves\p1_L.jpg").convert('RGB')
p1_r = Image.open(r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\diagnose_halves\p1_R.jpg").convert('RGB')

w, h = p1_l.size
# Check center graphic of p1_L vs p1_R
crop_l = p1_l.crop((int(w*0.2), int(h*0.2), int(w*0.8), int(h*0.6)))
crop_r = p1_r.crop((int(w*0.2), int(h*0.2), int(w*0.8), int(h*0.6)))

crop_l.save(r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\p1_L_graphic.png")
crop_r.save(r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\p1_R_graphic.png")

print("Saved p1_L_graphic and p1_R_graphic.")
