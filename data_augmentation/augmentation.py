from PIL import Image
import os

#Class for augmenting dataset
class Augmentation:
    #Runs these scripts on desired directory
    
    def augment_images_in_directory(self, path, degree):
        image_counter = 0
        for image in os.listdir(os.getcwd()):
            img = Image.open(image).convert("RGB")
            self.rotate(img, degree, image_counter)
            self.mirror_image(img, image_counter)

    # Rotate each image in the directory 270 degrees
    def rotate(self, img, degree, image_counter):
        img=img.rotate(degree, expand=True)
        img.save(f"rotated-{image_counter}.jpg")
        
    # Mirror each image in the directory
    def mirror_image(self,img, image_counter):
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(f"mirrored-{image_counter}.jpg")

