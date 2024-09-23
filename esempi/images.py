import numpy as np
import matplotlib.pyplot as plt
import imgmatrices as mg 
from PIL import Image


cat_matrix = np.array([
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 0, 0, 255, 255, 255, 255, 0, 0, 255],
    [255, 0, 0, 255, 255, 255, 255, 0, 0, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 0, 0, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255, 0, 255, 255, 255, 255, 0, 255, 255],
    [255, 255, 0, 0, 0, 0, 0, 0, 255, 255],
    [255, 255, 255, 190, 0, 0, 190, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
])

random_img = np.random.normal(size=(1000, 1000))


tiny_imagenet = mg.tiny_imagenet[10]['image']
img = tiny_imagenet.convert('RGB')
# Converti l'immagine in un array NumPy
img_array_full = np.array(img)

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(img_array_full, cmap='Grays')
plt.tight_layout()
plt.show()


R = img_array_full.copy()
G = img_array_full.copy()
B = img_array_full.copy()

R[:, :, 1] = 0
R[:, :, 2] = 0
G[:, :, 0] = 0
G[:, :, 2] = 0
B[:, :, 0] = 0
B[:, :, 1] = 0

# def matrix_to_latex(matrix):
#     # Inizia la stringa LaTeX con l'ambiente tabular
#     latex_str = "\\begin{bmatrix}\n"
    
#     # Aggiunge ogni riga della matrice
#     for row in matrix:
#         latex_str += " & ".join(map(str, row)) + " \\\\\n"
    
#     # Chiude l'ambiente tabular
#     latex_str += "\\end{bmatrix}"
    
#     return latex_str

# matrix = np.random.randint(0, 255 + 1, size=(10, 10))

# #print(matrix)

# #print(matrix_to_latex(cat_matrix))

# #print(img_array.shape)

# print(matrix_to_latex(img_array_full[30:41, 30:41, 0]))

fig, ax = plt.subplots(figsize=(10, 3), ncols=4)
ax[0].imshow(img_array_full)
ax[0].set_title('Immagine completa')
ax[0].axis('off')
ax[1].imshow(R)
ax[1].set_title('Canale del rosso')
ax[1].axis('off')
ax[2].imshow(G)
ax[2].set_title('Canale del verde')
ax[2].axis('off')
ax[3].imshow(B)
ax[3].set_title('Canale del blu')
ax[3].axis('off')
plt.tight_layout()
plt.show()

# th = 50
# img_array_full[0, :, 1] = np.array([x if x > th else 200 for x in img_array_full[0, :, 1]])
# img_array_full[-1, :, 1] = np.array([x if x > th else 200 for x in img_array_full[-1, :, 1]])
# img_array_full[:, 0, 1] = np.array([x if x > th else 200 for x in img_array_full[:, 0, 1]])
# img_array_full[:, -1, 1] = np.array([x if x > th else 200 for x in img_array_full[:, -1, 1]])


# fig, ax = plt.subplots()
# ax.imshow(img_array_full)
# ax.axis('off')
# plt.tight_layout()
# plt.show()
