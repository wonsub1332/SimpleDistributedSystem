from flask import Flask
from flask import request,json
import requests
from datetime import datetime as dt

app=Flask(__name__)

with open('config2.json','r') as f:
    config = json.load(f)

print("config = "+str(config))

serviceport=config['serviceport']
PriUri="http://"+config['replicas'][0]

if serviceport==5000:
    print('==================================')
    print('primary')
    print('==================================')
    n1={'id':1,'title':"dsfsdf",'body':'sdfjsdfdsfd'}
    n2={'id':2,'title':"dsfsdsdf",'body':'sdfsdfdsfjsdfdsfd'}
    n3={'id':3,'title':"dsfsdsdf",'body':'sdfsdfdsfjsdfdsfd'}
    note_list=[n1,n2,n3]
    index=4
    print(note_list)
else:
    print('==================================')
    print('replica')
    print('==================================')
    note_list=[]
    tmp=PriUri+'/note'
    r=requests.get(url=tmp)
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    for i in data:
        note_list.append(i)
        print(i)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/note',methods=['GET','POST'])
def noteGet():
    if request.method=='GET':
        data=[]
        for i in note_list:
            data.append(i)
        return json.dumps(data)

    if request.method=='POST':
        tmp=PriUri+'/primary'
        print("[{}] REPLICA [REQUEST] Forward request to pri".format(dt.now().time()))
        r=requests.post(url=tmp,data=request.data)
        print("r= "+str(r))#all backup com 을 받아야 함
        data=note_list[len(note_list)-1]
        print("[{}] REPLICA [REPLY] Forward request to pri".format(dt.now().time()))
        return json.dumps(data)

@app.route('/note/<id>',methods=['GET','PUT','PATCH','DELETE'])
def noteIndex(id):
    if request.method=='GET':
        for i in note_list:
                print(str(i))
                if i.get('id')==int(id):
                    print(i)
                    data=i
                    break
        return json.dumps(data)

    if request.method=='PUT':
        tmp=PriUri+'/primary/'+id
        print("[{}] REPLICA [REQUEST] Forward request to pri".format(dt.now().time()))
        r=requests.put(url=tmp,data=request.data)
        print("r= "+str(r))#all backup com 을 받아야 함

        for i in note_list:
                print(str(i))
                if i.get('id')==int(id):
                    print(i)
                    data=i
                    break
        print("[{}] REPLICA [REPLY] Forward request to pri".format(dt.now().time()))
        return json.dumps(data)
    
    if request.method=='PATCH':
        tmp=PriUri+'/primary/'+id
        print("[{}] REPLICA [REQUEST] Forward request to pri".format(dt.now().time()))
        r=requests.patch(url=tmp,data=request.data)
        print("r= "+str(r))#all backup com 을 받아야 함

        for i in note_list:
                print(str(i))
                if i.get('id')==int(id):
                    print(i)
                    data=i
                    break
        print("[{}] REPLICA [REPLY] Forward request to pri".format(dt.now().time()))
        return json.dumps(data)
    
    if request.method=='DELETE':
        tmp=PriUri+'/primary/'+id
        print("[{}] REPLICA [REQUEST] Forward request to pri".format(dt.now().time()))
        r=requests.delete(url=tmp)
        print("[{}] REPLICA [REPLY] Forward request to pri".format(dt.now().time()))
        return json.dumps({'msg':'delete complete'})

@app.route('/primary',methods=['POST'])
def primary():
    if request.method=="POST":
        print("[{}] REPLICA [REQUEST] Forward request to pri".format(dt.now().time()))

        global index
        data={'id':index}
        nt=json.loads(request.data)
        if(nt.get('title')!=None):
            data['title']=nt.get('title')
        if(nt.get('body')!=None):
            data['body']=nt.get('body')
        note_list.append(data)
        index=index+1

        backupURL("POST",data)
        
        return json.dumps({"msg":"all backup com"})

def backupURL(method,data,id=0):
    for i in config['replicas']:
        try:
            tmp="http://{}".format(i)+'/backup'
            print("[{}] REPLICA [REQUEST] Tell backups to update".format(dt.now().time()))
            if method=="POST":
                r=requests.post(url=tmp,data=json.dumps(data)) #backup com 을 받아야함

            tmp="http://{}".format(i)+'/backup/'+str(id)
            if method=="PUT":
                r=requests.put(url=tmp,data=json.dumps(data)) #backup com 을 받아야함

            if method=="DELETE":
                r=requests.delete(url=tmp,data=json.dumps(data)) #backup com 을 받아야함
            
            if method=="PATCH":
                r=requests.patch(url=tmp,data=json.dumps(data)) #backup com 을 받아야함
            print("[{}] REPLICA [REPLY] Acknowledge update".format(dt.now().time()))
        except:
            print("{} connection fail".format(i))
    #============
    print("[{}] REPLICA [REPLY] All Complete".format(dt.now().time()))

@app.route('/primary/<id>',methods=['DELETE','PUT','PATCH'])
def primaryid(id):
    for i in note_list:
            print(str(i))
            if i.get('id')==int(id):
                print(i)
                data=i
                break

    if request.method=='PUT':
        nt=json.loads(request.data)
        if(nt.get('title')!=None):
            print(nt.get('title'))
            data['title']=nt.get('title')
            print(data.get('title'))
        else:
            data.pop('title')
        if(nt.get('body')!=None):
            data['body']=nt.get('body')
        else:
            data.pop('body')
        
        backupURL("PUT",data,id)
        
        return json.dumps({"msg":"all backup com"})
    
    if request.method=='DELETE':
        note_list.remove(data)
        backupURL("DELETE",data,id)
        return json.dumps({"msg":"all backup com"})
    
    if request.method=='PATCH':
        nt=json.loads(request.data)
        if(nt.get('title')!=None):
            data['title']=nt.get('title')
        if(nt.get('body')!=None):
            data['body']=nt.get('body')
        
        backupURL("PATCH",data,id)
        
        return json.dumps({"msg":"all backup com"})

@app.route('/backup',methods=['POST'])
def backup():
    if request.method=='POST':
        print("[{}] REPLICA [REQUEST] Tell backups to update".format(dt.now().time()))
        nt=json.loads(request.data)
        print("income data : "+str(nt))
        note_list.append(nt)
        print("[{}] REPLICA [REPLY] Acknowledge update".format(dt.now().time()))
        return json.dumps({"msg":"backup com"})
    return json.dumps({'msg':'NO'})

@app.route('/backup/<id>',methods=['DELETE','PUT','PATCH'])
def backupid(id):
    print("[{}] REPLICA [REQUEST] Tell backups to update".format(dt.now().time()))
    for i in note_list:
            print(str(i))
            if i.get('id')==int(id):
                print(i)
                data=i
                break

    if request.method=='PUT':
        nt=json.loads(request.data)
        if(nt.get('title')!=None):
            print(nt.get('title'))
            data['title']=nt.get('title')
            print(data.get('title'))
        else:
            data.pop('title')
        if(nt.get('body')!=None):
            data['body']=nt.get('body')
        else:
            data.pop('body')
        
        print("[{}] REPLICA [REPLY] Acknowledge update".format(dt.now().time()))
        return json.dumps({"msg":"backup com"})

    if request.method=='DELETE':
        note_list.remove(data)
        print("[{}] REPLICA [REPLY] Acknowledge update".format(dt.now().time()))
        return json.dumps({"msg":"backup com"})

    if request.method=='PATCH':
        nt=json.loads(request.data)
        if(nt.get('title')!=None):
            data['title']=nt.get('title')
        if(nt.get('body')!=None):
            data['body']=nt.get('body')
        print("[{}] REPLICA [REPLY] Acknowledge update".format(dt.now().time()))
        return json.dumps({"msg":"backup com"})
    
if __name__=='__main__':
    app.run(host='127.0.0.1',port=serviceport,debug=True)