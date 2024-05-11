import telebot
from telebot import types
from database import sql, db
import configure
import threading
import inspect

client = telebot.TeleBot(configure.config['token'])
lock = threading.Lock()

from shop import handle_mybuy
from myprofile import handle_myprofile
from edit_buy import *
from remove_buy import *
from add_buy import handle_addbuy
from buy import *
from admin import handle_getprofile
from donate import *
from getcid import handle_getcid
from help import handle_helpcmd
from access import *
from money import *
from teh import *
from ot import *
from getid import handle_getiduser
from add_location import *

callbacks = {
    'editbuynewnametovaryes': handle_editbuy_name_new_callback,
    'editbuynewnametovarno': handle_editbuy_name_new_callback,
    'editbuynewpricetovaryes': handle_editbuy_price_new_callback,
    'editbuynewpricetovarno': handle_editbuy_price_new_callback,
    'editbuynewtovartovaryes': handle_editbuy_tovar_new_callback,
    'editbuynewtovartovarno': handle_editbuy_tovar_new_callback,
    'editbuynewimagetovaryes': handle_editbuy_image_new_callback,
    'editbuynewimagetovarno': handle_editbuy_image_new_callback,
    'editbuynewdescriptiontovaryes': handle_editbuy_description_new_callback,
    'editbuynewdescriptiontovarno': handle_editbuy_description_new_callback,
    'editbuyname': handle_editbuy_first_callback,
    'editbuyprice': handle_editbuy_first_callback,
    'editbuytovar': handle_editbuy_first_callback,
    'editbuyimage': handle_editbuy_first_callback,
    'editbuydescription': handle_editbuy_first_callback,
    'removebuytovaryes': handle_removebuy_callback,
    'removebuytovarno': handle_removebuy_callback,
    'confirm_order' : handle_confirm_order,
    'order_confirmed' : handle_order_confirmation,
    'donateyes': handle_donate_result,
    'donateno': handle_donate_result,
    'donatepaid': handle_donateyes_paid,
    'setaccessyes': handle_access_user_gave_access,
    'setaccessno': handle_access_user_gave_access,
    'givemoneyyes': handle_money_gave_money_user,
    'givemoneyno': handle_money_gave_money_user,
    'tehsend': handle_teh_callback,
    'tehno': handle_teh_callback,
    # 'sendmsgtouseryes': handle_sendmsgtouser_callback,
    # 'sendmsgtouserno': handle_sendmsgtouser_callback,
    'addlocation': handle_send_district_choice_message,
    'addproductlocation': handle_productlocation_callback,
    'addlocphoto': handle_addloc_photo,
    'generallocphoto': handle_general_location_photo,
    'detaillocphoto': handle_detailed_location_photo,
    'addlocprocess': handle_location_input,
}

def handle_callback(call):
    cid = call.message.chat.id
    uid = call.from_user.id

    if call.data == 'profile':
        handle_myprofile(call, sql, client)
    elif call.data == 'help':
        handle_helpcmd(call, client, lock, sql)
    elif call.data == 'buy':
        handle_buy(call.message, client, sql)
    elif call.data == 'donate':
        handle_donate(call, client, sql)
    elif call.data == 'mybuy':
        handle_mybuy(call, sql, client)
    elif call.data == 'teh':
        handle_teh(call, client)
    elif call.data == 'addlocation':
        handle_send_district_choice_message(call, client, sql, lock)
    elif call.data == 'getprofile':
        handle_getprofile(call, sql, client)
    elif call.data == 'access':
        handle_setaccess(call, client, sql, db)
    elif call.data == 'giverub':
        handle_givemoney(call, sql, client)
    elif call.data == 'getid':
        handle_getiduser(call, client, sql)
    elif call.data == 'getcid':
        handle_getcid(call, client)
    elif call.data == 'addbuy':
        handle_addbuy(call, client, lock, sql, db)
    elif call.data == 'editbuy':
        handle_editbuy(call, client, sql, lock)
    elif call.data == 'rembuy':
        handle_removebuy(call, client, sql, lock)
    elif call.data == 'ot':
        handle_sendmsgtouser(call, client, sql)
    else:
        for condition, handler in callbacks.items():
            if call.data.startswith(condition):

                args_count = len(inspect.signature(handler).parameters)
                
                if args_count == 3:
                    handler(call, client, sql)          
                elif args_count == 4:
                    handler(call, client, sql, db)
                
@client.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    print(call.data)
    handle_callback(call)
