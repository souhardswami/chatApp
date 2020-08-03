from channels.generic.websocket import AsyncWebsocketConsumer
import json


from app.models import User,JoinCode






class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):

        
        

        
        self.groupname='chatboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self,close_code):

        disconnected_user=self.scope['url_route']['kwargs']['usercode']


        first_user=JoinCode.objects.filter(creater__name=disconnected_user)
        another_user=first_user[0].joiner

        first_user_object=User.objects.get(name=disconnected_user)
        first_user.update(joiner=first_user_object)

        another_user_table=JoinCode.objects.filter(creater__name=another_user)
        another_user_object=User.objects.get(name=another_user)
        another_user_table.update(joiner=another_user_object)

        d={
            'value':'disconnect',
            'sender':disconnected_user,
            'joiner':str(another_user)
        }


        await self.disconnectinfo(json.dumps(d))

        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
    

    async def disconnectinfo(self, text_data):
        datapoint = json.loads(text_data)
        val =datapoint['value']
        sender=datapoint['sender']
        reciever=datapoint['joiner']



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
        datapoint = json.loads(text_data)
        val =datapoint['value']
        sender=datapoint['sender']


        join=JoinCode.objects.get(creater__name=sender)


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




    async def deprocessing(self,event):
        value=event['value']
        sender=event['sender']
        reciever=event['reciever']
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
        
        datapoint = json.loads(text_data)
        joining_code =datapoint['joincode']
        joiner =datapoint['joiner']
        joining_code_check=User.objects.filter(joining_code=joining_code)
        if(joining_code_check.exists()):
            anotheruser=joining_code_check[0].name
            join_table=JoinCode.objects.filter(creater__name=anotheruser)

            if(str(join_table[0].joiner)==str(anotheruser)):
                new_user=User.objects.get(name=joiner)

                join_table.update(joiner=new_user)
                joiner_table=JoinCode.objects.filter(creater__name=joiner)
                me=User.objects.get(name=anotheruser)
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


        

    async def deprocessing(self,event):
        valOther=event['value']
        joinerOther=event['joiner']
        userother=event['user']

        await self.send(text_data=json.dumps({
            'value':valOther,
            'joiner':joinerOther,
            'user':userother
            }))
