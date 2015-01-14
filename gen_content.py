__author__ = 'zdvitas'
from lab2.models import *
import os
import random

for j in range(1,30):
    user = Person(name=os.urandom(2).encode('hex'), login=os.urandom(2).encode('hex'), password=os.urandom(2).encode('hex'))
    user.save()

    for i in range(1,20):
        pc = Computer(owner=user , count = 1, cabinet = 21, type = "pc", name=os.urandom(2).encode('hex'),
                      place=os.urandom(2).encode('hex'),mac= os.urandom(2).encode('hex'), processor=os.urandom(2).encode('hex'),
                      ram = 1024, year= 2004, notes = os.urandom(2).encode('hex'))
        pc.save()



Comps = Computer.objects.all()

for i in range(100):
    prog = Program(name=os.urandom(5).encode('hex'), version = os.urandom(1).encode('hex'),
                   customer=os.urandom(3).encode('hex'),date_of_install= datetime.now())
    prog.save()

Progs = Program.objects.all()

for i in range(len(Comps)):
    ran = random.randint(1, 20)
    for j in range(15):
        Comps[i].programs.add(Progs[ran+j])