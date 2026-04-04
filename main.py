import hashlib
import random
import cv2 as cv

class Block:

    def __init__(self,index,data,previous_hash,difficulty):

        self.index=index
        self.data=data
        self.previous_hash=previous_hash
        self.hash=None
        self.nounce=0
        self.difficulty=difficulty

    def calculate_hash(self):

        hash=hashlib.sha256((str(self.index)+self.data+self.previous_hash+str(self.nounce)).encode()).hexdigest()
        return hash

    def mine(self):
        
        if self.hash==self.calculate_hash():
            return
        self.hash=self.calculate_hash()
        print(f"The block index {self.index} is minning.....")
        while self.hash[:self.difficulty]!="0"*self.difficulty :
            self.nounce+=1
            self.hash=self.calculate_hash()
        print(f"The block index {self.index} is mined")

class BlockChain:

    def __init__(self,difficulty):
        self.list=[]
        self.difficulty=difficulty
    
    def is_valid(self):
        
        previous_hash=""
        for block in self.list:
            computed_hash=block.calculate_hash()

            #checking for block validation
            if computed_hash!=block.hash:
                print("The Blockchain is not valid")
                print(f"The computed hash doesnt match stored one in block index {block.index}!")
                return False
            
            #checking for block hash continuation
            if previous_hash!=block.previous_hash:
                print("The Blockchain is not valid")
                print(f"The previous hash stored hash in block index {block.index} doesnt match")
                return False
            previous_hash=block.hash
        print("The Blockchain is valid")
        return True

    def create_genesis_block(self):
        if len(self.list)!=0:
            print("There is already a block")
            return
        
        block=Block(index=0,data="Genesis Block",previous_hash="",difficulty=self.difficulty)
        block.mine()
        self.list.append(block)
        print("The Genisis Block is added")
        return block
    
    def add_block(self,data):
        if len(self.list)==0:
            print("There is no genesis block")

        previous_block=self.list[-1]
        block=Block(previous_block.index+1,data,previous_block.hash,self.difficulty)
        block.mine()
        self.list.append(block)
        print(f"The Block of index {block.index} is added")
        return block
    
    def print_chain(self):

        for block in self.list:
            print(f"Block index {block.index}")
            print(f"    Data : {block.data}")
            print(f"    previous hash : {block.previous_hash}")
            print(f"    hash : {block.hash}")
            print("\n")

if __name__=="__main__":

    bc=BlockChain(5) 
    bc.create_genesis_block()
    names = ["Alice","Bob","John","Claire","Leon","Ada","Jane"]
    transactions = []
    count=10
    while(count>0):
        sender=random.choice(names)
        reciver=random.choice(names)
        if sender==reciver:
            continue
        transactions.append(f"{sender} sends {random.randint(1,10000)} to {reciver}")
        count-=1
    for d in transactions:
        bc.add_block(d)
    bc.print_chain()
    bc.is_valid()
    bc.list[3].data="Jane sends 100000 to Ada"
    bc.list[3].mine()
    for i in range(4,7):
        bc.list[i].previous_hash=bc.list[i-1].calculate_hash()
        bc.list[i].mine()
    bc.is_valid()