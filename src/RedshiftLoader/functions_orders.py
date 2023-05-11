from typing import List

def convert_to_list_of_dictionary(list_of_data: List, key_names: List):
    '''
    convert a list of lists into a list of dictionaries with keys
    '''

    dict_list = []
    for order_list in list_of_data:
        dict_element = dict(zip(key_names, order_list))
        dict_list.append(dict_element)
    
    return dict_list

def collape_same_transactions_into_one(order_dict_list: List):
    '''
    collapse dictionaries of the same transaction into one dictionary that has the key 'orders' with a list of dictionaries 
    and each dictionary has 'product_name', 'product_size' and 'order_qty'
    '''
    
    new_order_dict_list = []
    for order_dict in order_dict_list:
        single_order_dict = {'product_name': order_dict['product_name'], 
                              'product_size': order_dict['product_size'],
                              'order_qty': order_dict['order_qty']}
        if len(new_order_dict_list) > 0 and order_dict['temp_order_id'] == new_order_dict_list[-1]['temp_order_id']:
            new_order_dict_list[-1]['orders'].append(single_order_dict)
        else:
            order_dict['orders'] = [single_order_dict]
            del order_dict['product_name']
            del order_dict['product_size']
            del order_dict['order_qty']
            new_order_dict_list.append(order_dict)

    return new_order_dict_list