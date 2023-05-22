import math
import random

class RSA:
    def __init__(self, text, n=None, e=None):
        self.text = text.lower().replace(" ", "").rstrip("\n")
        if(n != None):
            self.n = n
        if(e != None):
            self.e = e

    def gcd(self, a, b):
        #find Greatest Common Divisor
        if (b == 0):
            return a
        else:
            return self.gcd(b, a % b)

    def findD(self, toitent, e):
        #for decryption key
        found = False
        k = 1
        while (found == False):
            findD = (1 + (k*toitent))/e
            if(findD % 1 != 0):
                k+=1
            else:
                found = True
                d = int(findD)
        return d

    def generate_keys(self):
        #Generate public and private keys
        foundEven = False

        while(foundEven == False):
            rand1 = random.randint(100, 300)
            rand2 = random.randint(100, 300)

            fo = open('primes.txt', 'r')
            lines = fo.read().splitlines()
            fo.close()
            
            #choose p and q
            # p = int(lines[rand1])
            # q = int(lines[rand2])
            p = 47
            q = 71
            if (len(str(p*q)) % 2 == 0):
                foundEven = True

        n = p * q
        toitent = (p-1)*(q-1)
        
        #search for e
        searching = True
        while (searching):
            # e = random.randrange(2, toitent)
            e = 79
            if(self.gcd(e, toitent) == 1):
                searching = False
        
        d = self.findD(toitent, e)

        f_public = open('publicKey.pub', 'w')
        f_public.write(str(n) + ', ' + str(e))
        f_public.close()

        f_private = open('privateKey.pri', 'w')
        f_private.write(str(n) + ', ' + str(d))
        f_private.close()
        return n,e,d

    def findPrimeFactors(self, n):
        if(n % 2 == 0):
            res1 = 2

        while(n % 2 == 0):
            n = n/2

        for i in range(3,int(math.sqrt(n))+1,2):
            if(n % i == 0 ):
                while (n % i == 0):
                    res1 = i      
                    n = n / i
        
        if n > 2:
            res2 = n
        else:
            res2 = 2
        
        return int(res1), int(res2)

    def msgBlocking(self, processedMsg, n):
        msgBlock = []
        blockingProcessing = True
        blockSize = len(str(n))

        while(blockingProcessing):
            if(len(processedMsg) == 0):
                blockingProcessing = False
            else:
                temp = ""
                if(len(processedMsg) < blockSize):
                    for i in range(blockSize - (len(processedMsg) % blockSize)):
                        processedMsg = "0" + processedMsg
                
                for i in range(blockSize):
                        temp += processedMsg[0]
                        processedMsg = processedMsg[1:]

                if((int(temp) > n-1)):
                    processedMsg = temp[-1:] + processedMsg
                    temp = "0" + temp[:-1]
                
                msgBlock.append(temp)
        return msgBlock
    
    def encrypt(self):
        self.n, self.e, self.d = self.generate_keys()

        processedMsg = ""
        for letter in self.text:
            alphOrder = str(ord(letter) - 96)
            if(len(alphOrder) < 2):
                alphOrder = "0" + alphOrder
            processedMsg += alphOrder

        msgBlock = self.msgBlocking(processedMsg, self.n)

        encryptedMsg = ""
        for blocks in msgBlock:
            blockReady = False
            while (blockReady == False):
                if(blocks[0] == 0):
                    blocks = blocks[1:]
                else:
                    blockReady = True
            
            blocksInt = int(blocks)
            res = str((blocksInt ** self.e) % self.n)
            
            if(len(res) != len(str(self.n))):
                for i in range (len(str(self.n)) - (len(res))):
                    res = "0" + res
            
            res += " "
            encryptedMsg += res

        encryptedMsg = encryptedMsg[:-1]

        f_output = open('output.txt', 'w')
        f_output.write(encryptedMsg)
        f_output.close()

        return encryptedMsg

    def encryptNumber(self):
        self.n, self.e, self.d = self.generate_keys()

        text = int(self.text)
        res = text ** self.d
        res = res % self.n
        res = hex(res)

        return res

    def decrypt(self):
        pDecrypt, qDecrypt = self.findPrimeFactors(self.n)
        toitentDecrypt = (pDecrypt-1)*(qDecrypt-1)
        dDecrypt = self.findD(toitentDecrypt, self.e)
        nDecrypt = pDecrypt*qDecrypt

        encryptedMsg = self.text.replace(" ", "")

        blockDecryptedMsg = self.msgBlocking(encryptedMsg, nDecrypt)
        decryptedText = []
        for blocks in blockDecryptedMsg:
            res = str((int(blocks) ** dDecrypt) % self.n)

            if(len(res) < len(str(self.n))):
                for i in range(int(len(str(self.n)) - (len(res)))):
                    res = "0" + res
            decryptedText.append(res)

        processedDecryptedText = ""
        
        for blocks in decryptedText:
            processedDecryptedText += blocks
        
        decryptResult = ""
        for i in range(int(len(processedDecryptedText) / 2)):
            temp = ""
            if(processedDecryptedText[0] == "0" and processedDecryptedText[1] == "0"):
                for j in range(2):
                    processedDecryptedText = processedDecryptedText[1:]
            else:
                if(processedDecryptedText[0] != "0"):
                    for j in range(2):
                        temp += processedDecryptedText[0]
                        processedDecryptedText = processedDecryptedText[1:]
                else:
                    temp += processedDecryptedText[1]
                    processedDecryptedText = processedDecryptedText[2:]
                temp = chr(int(temp) + 96)
                decryptResult += temp

        return decryptResult

def RSAMain():
    print("==============")
    print("|    RSA     |")
    print("==============")

    print("Choose Message Source:")
    print("1. File")
    print("2. Input")
    print("--------------")
    msgSource = int(input("Input Message Source Number: "))
    if(msgSource == 1):
        msgPath = str(input("Input Filename: "))
        f = open(msgPath, "r")
        message = f.read()
        message = str(message)
        f.close()
    else:
        message = str(input("Input Message: "))

    print("--------------")
    print("Choose Action:")
    print("1. Encrypt")
    print("2. Decrypt")
    print("--------------")
    action = int(input("Input Action Number: "))
    print("--------------")

    if(action == 1):
        print("Encrypting...")
        rsa = RSA(message)
        print(rsa.encrypt())
    else:
        print("Choose Key Source:")
        print("1. From Generated Key")
        print("2. Input")
        print("--------------")
        keySource = int(input("Input Key Source Number: "))
        print("--------------")

        if(keySource == 1):
            f = open("publicKey.pub", "r")
            key = f.read()
            n,e = key.replace(" ","").split(",")
            n,e = int(n), int(e)
            f.close()
        else:
            n = int(input("Input n Value: "))
            e = int(input("Input e Value: "))
            print("--------------")
        print("Decrypting...")
        rsa = RSA(message, n, e)
        print(rsa.decrypt())