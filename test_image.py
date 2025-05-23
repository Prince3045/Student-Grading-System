from PIL import Image

try:
    img = Image.open("C:/Users/HP/OneDrive/Desktop/RMS/images/logo_p.png")
    img.show()
except Exception as e:
    print("Error:", e)
