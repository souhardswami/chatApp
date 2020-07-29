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

        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
    

    async def receive(self, text_data):
        print ('>>>>',text_data)
        datapoint = json.loads(text_data)
        val =datapoint['value']

        await self.channel_layer.group_send(
            self.groupname,
            {
                'type':'deprocessing',
                'value':val
            }
        )


        # pass

    async def deprocessing(self,event):
        valOther=event['value']
        print("fake")
        await self.send(text_data=json.dumps({'value':valOther}))







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

            
            if(str(join_table[0].joiner)==str(anotheruser)):
                print("empty")

                

                new_user=User.objects.get(name=joiner)
                print(join_table)

                join_table.update(joiner=new_user)

                val='joined'
            else:
                
                val='already joined'
        

        else:
            val='given code doesn\'t exist'


        await self.channel_layer.group_send(
            self.groupname,
            {
                'type':'deprocessing',
                'value':val
            }
        )


        # pass

    async def deprocessing(self,event):
        valOther=event['value']
        print(valOther)
        print("ori")
        await self.send(text_data=json.dumps({'value':valOther}))
