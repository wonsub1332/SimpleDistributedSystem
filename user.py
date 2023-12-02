import json
import urllib.request
import requests

url="http://127.0.0.1:5002"


def getNote(id):
    tmp=url+'/note/'+str(id)
    r=requests.get(url=tmp)
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    print(data)

def getNoteAll():
    tmp=url+'/note'
    r=requests.get(url=tmp)
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    for i in data:
        print(i)

def postNote():
    tmp=url+'/note'
    inp={'title':"post memo",'body':'post memo body'}
    r=requests.post(url=tmp,data=json.dumps(inp))
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    print(data)

def putNote(id):
    tmp=url+'/note/'+str(id)
    inp={'title':"new memo"}
    r=requests.put(url=tmp,data=json.dumps(inp))
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    print(data)

def patchNote(id):
    tmp=url+'/note/'+str(id)
    inp={'body':"new memo body"}
    r=requests.patch(url=tmp,data=json.dumps(inp))
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    print(data)

def deleteNote(id):
    tmp=url+'/note/'+str(id)
    r=requests.delete(url=tmp)
    print("data: "+str(r.text))
    print("response: "+str(r))
    data=json.loads(r.text)
    print(data)


while True:
    print("============================================================================\n\n")
    op=input("전체 노트 1, ?번 노트 2, POST 노트 3, PUT 4, PATCH 5, DELETE 6,종료 q:")
    print("============================================================================\n")
    if op=='q':
        break
    elif op=='1': #전체 노트
        data=getNoteAll()
    elif op=='2': #노트 1개
        id=input("id : ")
        getNote(id)
    elif op=='3': #post 노트
        postNote()
    elif op=='4': #노트 수정(덮어쓰기)
        id=input("id : ")
        putNote(id)
    elif op=='5': #노트 중 일부 필드를 수정
        id=input("id : ")
        patchNote(id)
    elif op=='6': #노트 삭제
        id=input("id : ")
        deleteNote(id)
    else:
        print("try again")
