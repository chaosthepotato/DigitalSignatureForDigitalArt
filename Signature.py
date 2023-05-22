from RSA import *
from SHA256 import *

class Signature:
    def __init__(self, text, key=None, mode=None):
        #cases are if user want to import text file, or input the text itself
        if(mode == None):
            f = open(text, "r")
            self.text = f.read()
        elif(mode == "string"):
            self.text = text

        #if user import the a public key file
        if(key != None):
            f = open(key, "r")
            key = f.read()
            pubN,pubE = key.replace(" ","").split(",")
            self.n, self.e = int(pubN), int(pubE)
            f.close()

    def signFile(self):
        #apply hashing method (SHA256) to plaintext
        #encrypt hashed message using RSA to make digital signature
        signature = int(sha256(self.text), 16)
        rsa = RSA(str(signature))
        signature = rsa.encryptNumber()
        signedText = self.text + "\n\n**Digital Signature**" + signature + "**Digital Signature**"
    
        f_signed = open('signedText.txt', 'w')
        f_signed.write(signedText)
        f_signed.close()

        return signedText

    def validateSign(self):
        #check if decrypted signature is equal with hashed message
        
        splittedText = self.text.split("**Digital Signature**")
        textFile = splittedText[0][:-2]
        while(textFile[-1] == '\n' or textFile[-1] == '\r'):
            textFile = textFile[:-1]
        signature = splittedText[1]

        hashedText = int(sha256(textFile), 16) % self.n
        processedSignature = (int(signature, 16) ** self.e) % self.n

        if(hashedText == processedSignature):
            return True
        else:
            return False

# # signing
# # text = "punya ray"
# text = "sign.txt"
# sign1 = Signature(text)
# print(text)
# signedText = sign1.signFile()
# print(signedText)

# # validating
# print("======VALIDATING======")
# signedText = "signedText.txt"
# pubkey = "publicKey.pub"
# sign2 = Signature(signedText, pubkey)
# valid = sign2.validateSign()

# if(valid):
#     print("Valid!")
# else:
#     print("Invalid!")