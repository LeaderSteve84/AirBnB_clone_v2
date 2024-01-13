#!/usr/bin/python3 

from fabric.api import task

@task
def hello():
    print("Hello from Fabric!")
