from rembg import remove
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import numpy as np
import cv2
from skimage.transform import resize

url_proyect = os.getcwd()


def verify_create_folder(dir_folder, verbose=True):
    try:
        os.makedirs(dir_folder)
        if verbose: print('\tLa carpeta \'' + dir_folder + '\' ha sido creada EXITOSAMENTE')
    except FileExistsError:
        if verbose: print('\tLa carpeta \'' + dir_folder + '\' ya ha sido creada')


def no_background(input_img_path,
                  BGR_Color,
                  lowest_threshold_value = 5,
                  to_explore = False,
                  show_pictures=False
                  ):
    
    output_img_path = url_proyect + "/outputs"
    verify_create_folder(output_img_path, verbose=False)

    # Reading the input image
    name_field = input_img_path.split("/")[-1].split(".")[0]
    image_input = cv2.imread(input_img_path)

    # Creating the no background image
    original_mask = remove(image_input, only_mask=True)

    if to_explore:
        for min_value in range(1, 11):
            _, mask = cv2.threshold(original_mask, min_value, 255, cv2.THRESH_BINARY)  # Umbralización
            mask = mask.astype(np.uint8)  # Pasamos de float a int para evitar errores
            img_nobg = cv2.bitwise_and(image_input, image_input, mask=mask)
            img_nobg = resize(img_nobg, (img_nobg.shape[0] * 0.25,  # eje y
                                         img_nobg.shape[1] * 0.25,  # eje x
                                         img_nobg.shape[2]))
            cv2.imshow("No Background "+str(min_value), img_nobg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        _, mask = cv2.threshold(original_mask, lowest_threshold_value, 255, cv2.THRESH_BINARY)  # Umbralización
        mask = mask.astype(np.uint8)  # Pasamos de float a int para evitar errores
        img_nobg = cv2.bitwise_and(image_input, image_input, mask=mask)

        # Mascara Invertida - util para construir el background
        inverted_mask = cv2.bitwise_not(mask)

        # Background
        bg = np.ones(image_input.shape, dtype=np.uint8)
        bg[:] = BGR_Color  # Asigno color
        bg_image = cv2.bitwise_and(bg, bg, mask=inverted_mask)  # Recorto

        # Imagen con fondo modificado
        output_img = cv2.add(bg_image, img_nobg)

        # Saving the no-background image
        output_nobg_path = output_img_path + "/" + name_field + "_nobg.png"
        cv2.imwrite(output_nobg_path, img_nobg)  # Saving
        output_wbg_path = output_img_path + "/" + name_field + "_whitebg.png"
        cv2.imwrite(output_wbg_path, output_img)  # Saving

    if show_pictures and not to_explore:
        percent_to_show = 0.2

        image_input = resize(image_input, (image_input.shape[0] * percent_to_show,  # eje y
                                           image_input.shape[1] * percent_to_show,  # eje x
                                           image_input.shape[2]))
        cv2.imshow("Original", image_input)
        mask = resize(mask, (mask.shape[0] * percent_to_show,  # eje y
                             mask.shape[1] * percent_to_show,  # eje x
                             ))
        cv2.imshow("Mask", mask)
        original_mask = resize(original_mask, (original_mask.shape[0] * percent_to_show,  # eje y
                                               original_mask.shape[1] * percent_to_show,  # eje x
                                               ))
        cv2.imshow("Original mask", original_mask)
        img_nobg = resize(img_nobg, (img_nobg.shape[0] * percent_to_show,  # eje y
                                     img_nobg.shape[1] * percent_to_show,  # eje x
                                     img_nobg.shape[2]))
        cv2.imshow("No Background", img_nobg)
        bg_image = resize(bg_image, (bg_image.shape[0] * percent_to_show,  # eje y
                                     bg_image.shape[1] * percent_to_show,  # eje x
                                     bg_image.shape[2]))
        cv2.imshow("New Background", bg_image)
        output_img = resize(output_img, (output_img.shape[0] * percent_to_show,  # eje y
                                         output_img.shape[1] * percent_to_show,  # eje x
                                         output_img.shape[2]))
        cv2.imshow("New Background", output_img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()




if __name__ == '__main__':
    BGR_Color = (255, 255, 255) # Background Color 

    root = Tk()
    root.withdraw()
    input_img_path = askopenfilename()
    root.destroy()
    print("Image ->", input_img_path)

    #no_background(input_img_path, BGR_Color, show_pictures=True, to_explore=True)
    no_background(input_img_path, BGR_Color, lowest_threshold_value=10, show_pictures=True)

