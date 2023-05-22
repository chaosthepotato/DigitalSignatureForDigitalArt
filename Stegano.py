import numpy as np
from PIL import Image

def ConvertMsgToBinary(msg):
    res = ''.join([format(ord(i), "08b") for i in msg])
    return res

def IntToBinary(num):
    bin_num = '{0:08b}'.format(num)
    return bin_num

def Encode(src, msg, dest):
    #load image
    img = Image.open(src, 'r')
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    width, height = img.size
    img_arr = np.array(list(img.getdata()))
    total_pixels = img_arr.size//n

    #set end of line for hidden message
    #convert hidden message to binary
    msg += "3OfFf"
    b_message = ConvertMsgToBinary(msg)
    req_pixels = len(b_message)

    #check if total length of hidden message exceeds total pixel of image file given
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    #insert hidden message binary into image file per pixel -> per channel(R/G/B/A)
    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    print('----------------')
                    print(b_message[index])
                    print(str(IntToBinary(img_arr[p][q])))
                    temp = list(str(IntToBinary(img_arr[p][q])))
                    temp[7] = b_message[index]
                    res = ''.join(temp)
                    img_arr[p][q] = int(res, 2)
                    print(str(IntToBinary(img_arr[p][q])))
                    print('----------------')
                    index += 1

        img_arr=img_arr.reshape(height, width, n)
        enc_img = Image.fromarray(img_arr.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")

def Decode(src):

    #get hidden binary from least significant bit (LSB) from each channel from each pixel until end of line reached
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4    
        
    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    #get hidden message until before end of line
    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "3OfFf":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "3OfFf" in message:
        print("Hidden Message:")
        print(message[:-5])
    else:
        print("No Hidden Message Found")
        
    return message[:-5]