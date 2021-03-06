import streamlit as st
import numpy as np
import cv2
from math import sqrt, atan
from math import atan, degrees
from PIL import Image
import numpy as np 
import streamlit as st 
import os
import base64

kernel_blur = np.array([0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11]).reshape(3,3)
kernel_conv_Y = np.array([1,0,-1,1,0,-1,1,0,-1]).reshape(3,3)
kernel_conv_X = kernel_conv_Y.transpose()

height = 0 
width = 0

def apply_convolution(img, kernel, height, width):
  height = img.shape[0]
  width = img.shape[1]
  pixels = []
  #pixels are extracted from the image converted to grayscale
  for i in range(height):
    for j in range(width):
      pixels.append(img[i,j])

  #The pixels array is resized in accordance with the size of the image
  pixels = np.array(pixels).reshape(height,width)

  #To handle the edge cases, sentinel values are used
  #The pixels array is bound by zeros on all edges

            # 00000000
            # 0PIXELS0
            # 00000000
  #This is done to ensure that the kernel is applied to all the pixels
  #Sentinel values to ensure the edges arent missed out

  #Along the rows and columns
  pixels = np.insert(pixels , [0,height] , np.zeros(len(pixels[0])) , axis = 0)
  pixels = np.insert(pixels , [0, width] , np.zeros((len(pixels[:, 0]) ,1)) , axis = 1)

  #Convolution is applied here
  convolute = []
  for i in range(1,height):
    for j in range(1,width):
      temp = pixels[i:i+3 , j:j+3]
      product = np.multiply(temp,kernel)
      convolute.append(sum(sum(product)))

  convolute = np.array(convolute).reshape(height-1,width-1)
  return(convolute)

def blur_image(img):
  height = img.shape[0]
  width = img.shape[1]
  pixels = []
  kernel = np.array([0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11]).reshape(3,3)
  #pixels are extracted from the image converted to grayscale
  for i in range(height):
    for j in range(width):
      pixels.append(img[i,j])

  #The pixels array is resized in accordance with the size of the image
  pixels = np.array(pixels).reshape(height,width)

  #To handle the edge cases, sentinel values are used
  #The pixels array is bound by zeros on all edges

            # 00000000
            # 0PIXELS0
            # 00000000
  #This is done to ensure that the kernel is applied to all the pixels
  #Sentinel values to ensure the edges arent missed out

  #Along the rows and columns
  pixels = np.insert(pixels , [0,height] , np.zeros(len(pixels[0])) , axis = 0)
  pixels = np.insert(pixels , [0, width] , np.zeros((len(pixels[:, 0]) ,1)) , axis = 1)

  #Convolution is applied here
  blur = []
  for i in range(1,height):
    for j in range(1,width):
      temp = pixels[i:i+3 , j:j+3]
      product = np.multiply(temp,kernel)
      blur.append(sum(sum(product)))

  blur = np.array(blur).reshape(height-1,width-1)
  return(blur)

def convolute_x(img):
  pixels = []
  kernel = np.array([-1,-2,-1,0,0,0,1,2,1]).reshape(3,3)
  kernel = kernel.transpose()
  #pixels are extracted from the image converted to grayscale
  for i in range(height-1):
    for j in range(width-1):
      pixels.append(img[i,j])

  #The pixels array is resized in accordance with the size of the image
  pixels = np.array(pixels).reshape(height-1,width-1)

  #To handle the edge cases, sentinel values are used
  #The pixels array is bound by zeros on all edges

            # 00000000
            # 0PIXELS0
            # 00000000
  #This is done to ensure that the kernel is applied to all the pixels
  #Sentinel values to ensure the edges arent missed out

  #Along the rows and columns
  pixels = np.insert(pixels , [0,height-1] , np.zeros(len(pixels[0])) , axis = 0)
  pixels = np.insert(pixels , [0, width-1] , np.zeros((len(pixels[:, 0]) ,1)) , axis = 1)

  #Convolution is applied here
  convoluted_X = []
  for i in range(1,height-1):
    for j in range(1,width-1):
      temp = pixels[i:i+3 , j:j+3]
      product = np.multiply(temp,kernel)
      convoluted_X.append(sum(sum(product)))

  convoluted_X = np.array(convoluted_X).reshape(height-2,width-2)
  return(convoluted_X)

def sobel_filter(convoluted_X, convoluted_Y, height, width):
  sobel = []
  arc = []
  for i in range(height-2):
    for j in range(width-2):
      in_x = pow(convoluted_X[i,j] ,2)
      in_y = pow(convoluted_Y[i,j] , 2)
      gr_X = convoluted_X[i,j]
      gr_Y = convoluted_Y[i,j]
      grad = sqrt(in_x + in_y)
      sobel.append(grad)
  sobel = np.array(sobel).reshape(height-2, width-2)
  return(sobel)

def change_dimensions(convoluted_X, convoluted_Y, sobel):
  height_con = convoluted_X.shape[0]
  width_con = convoluted_X.shape[1]
  convoluted_X = np.insert(convoluted_X , [0,height_con-1] , np.zeros(len(convoluted_X[0])) , axis = 0)
  convoluted_X = np.insert(convoluted_X , [0, width_con-1] , np.zeros((len(convoluted_X[:, 0]) ,1)) , axis = 1)    
  convoluted_Y = np.insert(convoluted_Y , [0,height_con-1] , np.zeros(len(convoluted_Y[0])) , axis = 0)
  convoluted_Y = np.insert(convoluted_Y , [0, width_con-1] , np.zeros((len(convoluted_Y[:, 0]) ,1)) , axis = 1)
  sobel = np.insert(sobel , [0,sobel.shape[0]-1] , np.zeros(len(sobel[0])) , axis = 0)
  sobel = np.insert(sobel , [0, sobel.shape[1]-1] , np.zeros((len(sobel[:, 0]) ,1)) , axis = 1)
  return(convoluted_X , convoluted_Y, sobel)

def non_linearity(convoluted_X, convoluted_Y, sobel1):
  value = 0
  non_li = []
  height_con = convoluted_X.shape[0] - 1
  width_con = convoluted_X.shape[1] - 1
  for i in range(1 , height_con-1):
    for j in range(1, width_con-1):
      grx = convoluted_X[i, j]
      gry = convoluted_Y[i, j]
      sob = sobel1[i, j]
      if gry == 0:
        if sob >= sobel1[i, j+1] and sob >= sobel1[i, j-1]:
          value = sob
        else:
          value = 0
      elif grx == 0:
        if sob >= sobel1[i+1, j] and sob >= sobel1[i-1, j]:
          value = sob
        else:
          value = 0
      else:
        angle = degrees(atan(gry/grx))
        if grx > 0 and gry > 0:
          gr = angle
        elif grx < 0 and gry < 0:
          gr = 180 + angle
        elif grx > 0 and gry < 0:
          gr = 360 + angle
        else:
          gr = 180 + angle
        p1 = [*range(0,22)]
        p2 = [*range(22,67)]
        p3 = [*range(67,112)]
        p4 = [*range(112,157)]
        p5 = [*range(157,202)]
        p6 = [*range(202,247)] 
        p7 = [*range(247,290)]
        p8 = [*range(290,337)]          
        p9 = [*range(337,360)]
        gr = int(gr)
        if gr in p1 or gr in p5 or gr in p9:
          if sob >= sobel1[i, j+1] and sob >= sobel1[i, j-1]:
            value = sob
          else:
              value = 0
        elif gr in p2 or gr in p6:
          if sob >= sobel1[i-1, j+1] and sob >= sobel1[i+1, j-1]:
            value = sob
          else:
              value = 0
        elif gr in p3 or gr in p7:
          if sob >= sobel1[i-1, j] and sob >= sobel1[i+1, j]:
            value = sob
          else:
              value = 0
        elif gr in p4 or gr in p8:
          if sob >= sobel1[i-1, j-1] and sob >= sobel1[i+1, j + 1]:
            value = sob
          else:
              value = 0
      non_li.append(value)

  non_li = np.array(non_li).reshape(height_con-2, width_con-2)
  return(non_li)
    

def convolute_y(blur):
  pixels = []
  kernel = np.array([-1,-2,-1,0,0,0,1,2,1]).reshape(3,3)
  #pixels are extracted from the image converted to grayscale
  for i in range(height-1):
    for j in range(width-1):
      pixels.append(blur[i,j])

  #The pixels array is resized in accordance with the size of the image
  pixels = np.array(pixels).reshape(height-1,width-1)

  #To handle the edge cases, sentinel values are used
  #The pixels array is bound by zeros on all edges

            # 00000000
            # 0PIXELS0
            # 00000000
  #This is done to ensure that the kernel is applied to all the pixels
  #Sentinel values to ensure the edges arent missed out

  #Along the rows and columns
  pixels = np.insert(pixels , [0,height-1] , np.zeros(len(pixels[0])) , axis = 0)
  pixels = np.insert(pixels , [0, width-1] , np.zeros((len(pixels[:, 0]) ,1)) , axis = 1)

  #Convolution is applied here
  convoluted_Y = []
  for i in range(1,height-1):
    for j in range(1,width-1):
      temp = pixels[i:i+3 , j:j+3]
      product = np.multiply(temp,kernel)
      convoluted_Y.append(sum(sum(product)))

  convoluted_Y = np.array(convoluted_Y).reshape(height-2,width-2)
  return(convoluted_Y)


def double_threshold(non_li):
  ha, wi = non_li.shape
  high = np.amax(non_li)*0.8
  low = np.amax(non_li)*0
  final = []
  for i in range(ha):
    for j in range(wi):
      if non_li[i,j] > high:
        final.append(255)
      elif low <= non_li[i,j] <= high:
        final.append(non_li[i,j])
        #final.append(190)
      else:
        final.append(0)
  final = np.array(final).reshape(ha, wi)
  return(final)

def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image



def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    st.markdown(href, unsafe_allow_html=True)
    return

def main_image():
    st.title("Try out the canny edge detector on a picture !")
    uploadFile = st.file_uploader(label="Upload image", type=['jpg', 'png'])
    if uploadFile is not None:
        st.write("Image Uploaded Successfully")
        our_image = Image.open(uploadFile)
        new_img = np.array(our_image.convert('RGB'))
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = gray
        height = img.shape[0]
        width = img.shape[1]
        #img = load_image(uploadFile)
        st.image(img)
        #st.write("dimensios are ")
        #st.write(height)
        #st.write(width)
        #img = cv2.imread('/content/kolkata.jpg',0)

        height = img.shape[0]
        width = img.shape[1]
        blurred_img = apply_convolution(img, kernel_blur, height, width)
        st.write("\n\nBlurred Image\n\n")
        cv2.imwrite('tempImage.jpg', blurred_img)
        st.image('tempImage.jpg')
        
        #cv2.imshow("Blurred image" , blurred_img)  
        #st.image(blurred_img)

        height = height - 1
        width = width - 1
        conv_Y = apply_convolution(blurred_img, kernel_conv_Y, height, width)
        st.write("\n\nConvolute_Y Image\n\n")
        #cv2.imshow("Conv Y", conv_Y)
        cv2.imwrite('tempImage.jpg', conv_Y)
        st.image('tempImage.jpg')
        #st.image(conv_Y)


        conv_X = apply_convolution(blurred_img, kernel_conv_X, height, width )
        st.write("\n\nConvolute_X Image\n\n")
        #cv2_imshow(conv_X)
        #st.image(conv_X)
        cv2.imwrite('tempImage.jpg', conv_X)
        st.image('tempImage.jpg')

        sobel = sobel_filter(conv_X, conv_Y, height, width)
        st.write("\n\nAfter Sobel\n\n")
        cv2.imwrite('tempImage.jpg', sobel)
        st.image('tempImage.jpg')


        conv_X, conv_Y, sobel = change_dimensions(conv_X, conv_Y, sobel)

        non_linear_filter = non_linearity(conv_X, conv_Y, sobel)
        st.write("\n\nAfter non-linearity\n\n")
        #cv2_imshow(non_linear_filter)
        cv2.imwrite('tempImage.jpg', non_linear_filter)
        st.image('tempImage.jpg')

        #st.write(non_linear_filter)

        canny_filtered_image = double_threshold(non_linear_filter)
        st.write("\n\nAfter Canny\n\n")
        cv2.imwrite('tempImage.jpg', canny_filtered_image)
        st.image('tempImage.jpg')

        get_binary_file_downloader_html('tempImage.jpg', 'After Canny Filter')
    else:
        st.write("Make sure you image is in JPG/PNG Format.")

main_image()
