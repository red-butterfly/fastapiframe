# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2020-02-15
@function:
test ping 
'''
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from databases.mysql_model import TestModel
from databases.mongo_model import TestCol
from schemas.test_item import TestInItem, TestOutItem, ResponseItem

router = APIRouter()


@router.get("/testget")
async def test_get():
    return {'msg': 'test get sucess!'}


@router.post("/testmysql", response_model=ResponseItem)
async def create_item(item: TestInItem, db: TestModel=Depends()):
    try:
        db.create_model(item)
    except Exception as e:
        return HTTPException(status_code=404, detail=str(e))
    return ResponseItem(**{'msg': 'create ok'})


@router.get("/testmysql/{name}", response_model=TestOutItem)
async def create_item(name: str, db: TestModel=Depends()):
    item = db.get_model(name)
    return TestOutItem(**item)


@router.post("/testmongo", response_model=ResponseItem)
async def create_item(item: TestInItem, db: TestCol=Depends()):
    try:
        db.create_lang(item)
    except Exception as e:
        return HTTPException(status_code=404, detail=str(e))
    return ResponseItem(**{'msg': 'create ok'})


@router.get("/testmongo/{name}")
async def create_item(name: str, db: TestCol=Depends()):
    item = db.find_lang(name)
    return item