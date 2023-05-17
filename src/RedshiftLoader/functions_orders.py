from typing import List

def convert_to_list_of_dictionary(list_of_data: List, key_names: List):
    """
    Convert a list of lists of data into a list of dictionaries wth key names
    Args:
        list_of_data: list, a list of list of each order
        key_names: list, a list of key names
        e.g. 
            [[1, '25/04/2021', '23:10', 'Mochafield', 'Flavoured iced latte - Caramel', 'Large', 3.25, 12.95,'CASH'],
            [1, '25/04/2021', '23:10', 'Mochafield', 'Flat white', 'Regular', 2.15, 12.95,'CASH']]
    Return:
        e.g.
            [{'temp_transaction_id': 1, 'order_data': '25/04/2021', 'transaction_time': '23:10', 'branch_name': 'Mochafield', 
            'product_name': 'Flavoured iced latte - Caramel', 'product_size': 'Large', 'product_price' : 3.25, 'total_amount': 12.95, 'payment_method_id': 'CASH'},
            {'temp_transaction_id': 1, 'order_data': '25/04/2021', 'transaction_time': '23:10', 'branch_name': 'Mochafield', 
            'product_name': 'Flat white', 'product_size': 'Regular', 'product_price' : 2.15, 'total_amount': 12.95, 'payment_method_id': 'CASH'}]
    
    """

    dict_list = []
    for order_list in list_of_data:
        dict_element = dict(zip(key_names, order_list))
        dict_list.append(dict_element)
    
    return dict_list

def collape_same_transactions_into_one(order_dict_list: List):
    """
    Group product_name, product_size, order_qty by temp_transaction_id 
    and make them in a list under 'orders_list' key.

    Args:
        order_dict_list: list, a list of dictionaries that contain informaiton about one particular item order
        e.g. 
            [
                {'temp_transaction_id': 1, 
                'order_data': '25/04/2021', 
                'transaction_time': '23:10', 
                'branch_name': 'Mochafield', 
                'product_name': 'Flavoured iced latte - Caramel', 'product_size': 'Large', 'product_price' : 3.25, 
                'total_amount': 12.95, 
                'payment_method_id': 'CASH'},
            
                {'temp_transaction_id': 1, 
                'order_data': '25/04/2021', 
                'transaction_time': '23:10', 
                'branch_name': 'Mochafield', 
                'product_name': 'Flat white', 'product_size': 'Regular', 'product_price' : 2.15, 
                'total_amount': 12.95, 
                'payment_method_id': 'CASH'}
            ]
    Return:
        e.g.
            [
                {'temp_transaction_id': 1, 
                'order_data': '25/04/2021', 
                'transaction_time': '23:10', 
                'branch_name': 'Mochafield', 
                'orders_list': [
                                    {'product_name': 'Flavoured iced latte - Caramel', 'product_size': 'Large', 'product_price' : 3.25}, 
                                    {'product_name': 'Flat white', 'product_size': 'Regular', 'product_price' : 2.15,}
                                ]
                'total_amount': 12.95, 'payment_method_id': 'CASH'}
            ]
    
    """
    
    new_order_dict_list = []
    for order_dict in order_dict_list:
        single_order_dict = {'product_name': order_dict['product_name'], 
                              'product_size': order_dict['product_size'],
                              'order_qty': order_dict['order_qty']}
        if len(new_order_dict_list) > 0 and \
            order_dict['temp_transaction_id'] == new_order_dict_list[-1]['temp_transaction_id']:
            new_order_dict_list[-1]['orders_list'].append(single_order_dict)
        else:
            order_dict['orders_list'] = [single_order_dict]
            del order_dict['product_name']
            del order_dict['product_size']
            del order_dict['order_qty']
            new_order_dict_list.append(order_dict)

    return new_order_dict_list

def get_unique_orders_dictinaries(record_index: int, from_path: str, list_of_data: List):
    """
    Convert a list of lists of data into a list of dictionaries wth key names.
    Group product_name, product_size, and order_qty by temp_transaction_id 
    and make them in a list under 'orders_list' key.
    Args:
        list_of_data: list, a list of list of each order
        key_names: list, a list of key names
        e.g. 
            [[1, '25/04/2021', '23:10', 'Mochafield', 'Flavoured iced latte - Caramel', 'Large', 3.25, 12.95,'CASH'],
            [1, '25/04/2021', '23:10', 'Mochafield', 'Flat white', 'Regular', 2.15, 12.95,'CASH']]
    Return:
        e.g.
            [
                {'temp_transaction_id': 1, 
                'order_data': '25/04/2021', 
                'transaction_time': '23:10', 
                'branch_name': 'Mochafield', 
                'orders_list': [
                                    {'product_name': 'Flavoured iced latte - Caramel', 'product_size': 'Large', 'product_price' : 3.25}, 
                                    {'product_name': 'Flat white', 'product_size': 'Regular', 'product_price' : 2.15,}
                                ]
                'total_amount': 12.95, 'payment_method_id': 'CASH'}
            ]
    
    """
    
    # set key names
    key_names = ['temp_transaction_id', 'transaction_date', 'transaction_time', 'branch_name', 
                    'product_name', 'product_size', 'product_price', 'order_qty', 
                    'total_amount', 'payment_method']

    # convert list into diction with column names
    order_dict_list = convert_to_list_of_dictionary(list_of_data, key_names)

    # collapse the same transactions into one list
    unique_order_dict_list = collape_same_transactions_into_one(order_dict_list)

    return unique_order_dict_list