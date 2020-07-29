
import hashlib 

import random 
  
# printing the equivalent hexadecimal value. 


class Hash:
    def __init__(self,username):
        self.username=username
    
    def get_hash(self):

        new_user_identity=self.username+str(random.randint(1,10000))



        result = hashlib.md5(new_user_identity.encode()) 
        return result.hexdigest()
