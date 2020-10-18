from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fuzzywuzzy import fuzz
from pydantic import parse_obj_as
import requests

from datetime import datetime, timedelta
import asyncio

from db import schemas, models
from db.db import get_db
from api.orders.controllers import create_order_with_items, get_all_orders_by_store_id
from api.items.controllers import get_items_by_store_id
from api.tables.controllers import get_tables_by_store_id, get_available_tables, delete_all_tables_by_store_id,\
    is_available, get_table_by_id, reserve_table
from db.schemas import User
from etc.usrmng import fastapi_users

router = APIRouter()


@router.post('/item/name')
def check_name(request: Request, db: Session = Depends(get_db)):
    chatbot_input = asyncio.run(request.json())
    session_info = chatbot_input['sessionInfo']
    selected_item = session_info['parameters']['itemname']
    all_items = get_items_by_store_id(db, 1)
    perfect_item = None
    perfect_item_score = 0
    for curr_item in all_items:
        fuzz_ratio = fuzz.ratio(curr_item.name.lower(), selected_item.lower())
        if perfect_item_score < fuzz.ratio(curr_item.name.lower(), selected_item.lower()) >= 90:
            perfect_item = curr_item
            perfect_item_score = fuzz_ratio
    if perfect_item is None:
        session_info['parameters']['tracker'] = False
    else:
        session_info['parameters']['tracker'] = True
        session_info['parameters']['payload']['order_items'].append({'item_id': perfect_item.id, 'quantity': session_info['parameters']['itemquantity']})
    print(session_info)
    session_info['parameters']['itemname'] = None
    session_info['parameters']['itemquantity'] = None
    session_info['parameters']['checkbox'] = None
    print("here")
    print(session_info)
    return {'sessionInfo': session_info}


@router.post('/reservation/check')
def check_availability(request: Request, db: Session = Depends(get_db)):
    chatbot_input = asyncio.run(request.json())
    session_info = chatbot_input['sessionInfo']
    st_dict = session_info['parameters']['starttime']
    duration_dict = session_info['parameters']['duration']
    start_time = datetime(year=int(st_dict['year']), month=int(st_dict['month']), day=int(st_dict['day']), hour=int(st_dict['hours']), minute=int(st_dict['minutes']), second=int(st_dict['seconds']))
    duration = timedelta(minutes=sum([duration_dict['amount'] if duration_dict['unit'] == 'min' else 0, 60 * duration_dict['amount'] if duration_dict['unit'] == 'h' else 0]))
    end_time = start_time + duration
    store_tables = get_tables_by_store_id(db, 1)
    perfect_table = None
    for curr_table in store_tables:
        if curr_table.cap >= session_info['parameters']['numpeople'] and is_available(db, curr_table.id, start_time, end_time):
            perfect_table = curr_table
            break
    session_info['parameters']['payload'] = session_info['parameters'].get('payload', {})
    session_info['parameters']['payload']['table_id'] = perfect_table.id if perfect_table is not None else None
    session_info['parameters']['payload']['start_time'] = start_time.isoformat()
    session_info['parameters']['payload']['end_time'] = end_time.isoformat()
    session_info['parameters']['payload']['order_items'] = []

    session_info['parameters']['starttime'] = None
    session_info['parameters']['duration'] = None
    session_info['parameters']['numpeople'] = None

    print(session_info)
    return {"sessionInfo": session_info}


@router.post('/reservation/checkout')
def order_checkout(request: Request, db: Session = Depends(get_db)):
    chatbot_input = asyncio.run(request.json())
    session_info = chatbot_input['sessionInfo']
    payload = session_info['parameters']['payload']
    table_id = payload['table_id']
    requests.post('http://localhost:8000/auth/register', json={"email": session_info['parameters']['email'], "password": 'password'})
    user = db.query(models.UserTable).filter_by(email=session_info['parameters']['email']).first()
    reservation_with_order = parse_obj_as(schemas.ReservationWithOrderItems, payload)
    if not is_available(db, table_id, reservation_with_order.start_time, reservation_with_order.end_time):
        session_info['parameters']['payload']['success'] = False
    else:
        order_id, _ = create_order_with_items(db, str(user.id), get_table_by_id(db, table_id).store_id, reservation_with_order.order_items)
        reserve_table(db, table_id, str(user.id), reservation_with_order, order_id)
        # print(order_id)
        session_info['parameters']['payload']['success'] = True
    print(session_info)
    return {"sessionInfo": session_info}


@router.post('/item/suggest')
def get_item_suggestions(request: Request, db: Session = Depends(get_db)):
    chatbot_input = asyncio.run(request.json())
    session_info = chatbot_input['sessionInfo']
    payload = session_info['parameters']['payload']
    items = [x['item_id'] for x in payload['order_items']]
    new_items = [x for x in get_items_by_store_id(db, 1) if x.id not in items]
    highest_score_item = max(new_items, key=lambda x: x.score)
    payload['highest_score_item'] = {"item_id": highest_score_item.id, "name": highest_score_item.name, "quantity": 1}
    return {"sessionInfo": session_info, "fulfillment_response": {"messages": ""}}
