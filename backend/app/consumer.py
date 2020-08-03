from channels.generic.websocket import AsyncWebsocketConsumer
import json


from app.models import User,JoinCode






class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        print(self.scope['url_route']['kwargs']['usercode'])

        
        

        
        self.groupname='dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self,close_code):

        print("disconnect")

        disconnected_user=self.scope['url_route']['kwargs']['usercode']


        first_user=JoinCode.objects.filter(creater__name=disconnected_user)

        print(first_user)
        another_user=first_user[0].joiner
        print(another_user)

        first_user_object=User.objects.get(name=disconnected_user)
        print(first_user_object)
        first_user.update(joiner=first_user_object)
        print("jnjjjn")

        another_user_table=JoinCode.objects.filter(creater__name=another_user)

        another_user_object=User.objects.get(name=another_user)

        another_user_table.update(joiner=another_user_object)

        d={
            'value':'disconnect',
            'sender':disconnected_user,
            'joiner':str(another_user)
        }
        print(d)

        await self.fake(json.dumps(d))

        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
    

    async def fake(self, text_data):
        print("here")
        datapoint = json.loads(text_data)
        val =datapoint['value']
        sender=datapoint['sender']
        reciever=datapoint['joiner']
        print("hat")


        await self.channel_layer.group_send(
            self.groupname,
            {
                'type':'deprocessing',
                'value':val,
                'sender':sender,
                'reciever':reciever
            }
        )

    

    async def receive(self, text_data):
        print ('>>>>',text_data)
        datapoint = json.loads(text_data)
        val =datapoint['value']
        sender=datapoint['sender']


        join=JoinCode.objects.get(creater__name=sender)
        print(join.joiner)

        reciever=str(join.joiner)
        if(sender==reciever):
            return 

        await self.channel_layer.group_send(
            self.groupname,
            {
                'type':'deprocessing',
                'value':val,
                'sender':sender,
                'reciever':reciever
            }
        )


        # pass

    async def deprocessing(self,event):
        value=event['value']
        sender=event['sender']
        reciever=event['reciever']

        print(sender,reciever)
    
        print("fake")
        await self.send(text_data=json.dumps({
            'value':value,
            'sender':sender,
            'reciever':reciever

            }))







class JoinConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.groupname='joingroup'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self,close_code):

        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
    

    

    async def receive(self, text_data):
        print ('>>>>',text_data)
        datapoint = json.loads(text_data)
        joining_code =datapoint['joincode']
        joiner =datapoint['joiner']
        print("joincode",joining_code,sep=" ")
        print("joiner",joiner,sep=" ")

        
        

        joining_code_check=User.objects.filter(joining_code=joining_code)
        print(joining_code_check)

        if(joining_code_check.exists()):


            


            anotheruser=joining_code_check[0].name
            print(anotheruser)
            join_table=JoinCode.objects.filter(creater__name=anotheruser)
            

            # if user and joiner are same
            print(join_table)

            

            
            if(str(join_table[0].joiner)==str(anotheruser)):
                print("empty")

                

                new_user=User.objects.get(name=joiner)
                print(join_table)

                join_table.update(joiner=new_user)


                print("joiner.........",joiner,sep=" ")

                joiner_table=JoinCode.objects.filter(creater__name=joiner)
                print("joining table................",joiner_table[0].creater,sep=" ")

                me=User.objects.get(name=anotheruser)
                print(me)
                joiner_table.update(joiner=me)


                val='✓ joined'
            else:
                anotheruser=''
                if(str(join_table[0].joiner)==str(joiner)):
                    val='✓ already joined'

                else:
                    val='✕ room is Full'
        

        else:
            anotheruser=''
            val='✕ given code doesn\'t exist'


        await self.channel_layer.group_send(
            self.groupname,
            {
                'type':'deprocessing',
                'value':val,
                'joiner':joiner,
                'user':anotheruser
            }
        )


        # pass

    async def deprocessing(self,event):
        valOther=event['value']
        joinerOther=event['joiner']
        userother=event['user']
        print(valOther)
        print("ori")

        await self.send(text_data=json.dumps({
            'value':valOther,
            'joiner':joinerOther,
            'user':userother
            }))
