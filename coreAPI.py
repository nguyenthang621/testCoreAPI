from jsonrpc_requests import Server
import jsonrpc_requests
import sys
import jwt
import datetime
from pathlib import Path 
# Get the parent directory of the current script file (2 levels up from the script's location).
# sys.path.insert(0, str(Path(__file__).parents[1]))
from config import config

def get_coreapi():
    coreapi_unauthorized = Server(config.COREAPI_SERVER)
    print(config.COREAPI_USERNAME)
    print(config.COREAPI_PASSWORD)
    result = coreapi_unauthorized.iam.auth.jwt.authenticate(
        login=config.COREAPI_USERNAME,
        password=config.COREAPI_PASSWORD
    )
    token = result['token']
    coreapi = Server(config.COREAPI_SERVER, headers={'Authorization': f'Bearer {token}'})
    try:
        coreapi.clients.search(limit=1)
        return coreapi
    except:
        return False


def check_token_avaiable():
    '''
    Check if the JWT token is available and still valid.

    This function retrieves the JWT token from the specified config_section and config_assisged_name in the configuration file. 
    If the token has expired, a new JWT token is generated using the 'generate_jwt_token' function and returned. 
    If the token is still valid, the original JWT token is returned.

    Parameters:
        config_section (str): The config_section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_assisged_name (str): The name of the token variable in the specified config_section. Default is 'jwt_token'.

    Returns:
        str: The JWT token, either the original token if it is still valid, or a new token if the original token has expired or encountered decoding errors.

    Raises:
        jwt.exceptions.DecodeError: If there is an error while decoding the JWT token.
        configparser.NoSectionError: If the specified config_section is not found in the configuration.
    '''
    try:
        jwt_token = config.JWT_TOKEN
        decoded_data = jwt.decode(jwt=jwt_token, algorithms=['HS256'], options={'verify_signature': False})
        datetime_expire = datetime.datetime.fromtimestamp(decoded_data['exp'])

        if datetime.datetime.now() > datetime_expire:
            return generate_jwt_token()
        return jwt_token
    except jwt.exceptions.DecodeError:
        return generate_jwt_token()



def generate_jwt_token():
    '''
    Generate a new JWT token by authenticating with the coreAPI server.

    This function attempts to authenticate with the coreAPI server using the specified login and password (VCS_LOGIN and VCS_PASSWORD constants). 
    If the authentication is successful, the JWT token is obtained from the response and stored in the specified config_section and config_assisged_name using the 'conf.write_token_to_config' function.

    Parameters:
        config_section (str): The config_section name in the configuration file where the new JWT token will be stored. Default is 'coreAPI_Token'.
        config_assisged_name (str): The name of the token variable in the specified config_section. Default is 'jwt_token'.

    Returns:
        str: The newly generated JWT token.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
        jsonrpc_requests.jsonrpc.JSONRPCError: If there is an error in the JSON-RPC response from the server.
    '''
    try:
        coreapi_unauthorized = Server(config.COREAPI_SERVER)
        print(f"{config.COREAPI_SERVER=}")
        result = coreapi_unauthorized.iam.auth.jwt.authenticate(
            login=config.COREAPI_USERNAME,
            password=config.COREAPI_PASSWORD
        )
        jwt_token = result['token']
        config.write_to_env_file(key='jwt_token', value=jwt_token)
        return jwt_token
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return e
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return e
    except jsonrpc_requests.jsonrpc.JSONRPCError as e:
        return e


def coreapi_clients_get(client_id: int = 0):
    '''
    Get client information from the coreAPI server using the provided client ID.

    This function queries the coreAPI server to get information about the client with the specified 'client_id'.

    Parameters:
        config_section (str): The config_section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_config_assisged_name (str): The name of the token variable in the specified config_section. Default is 'jwt_token'.
        client_id (int): The ID of the client to retrieve information for.

    Returns:
        dict: A dictionary containing the information about the client obtained from the coreAPI server.
              If the client with the specified ID is not found, an exception is returned.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
    '''
    try:
        jwt_token = check_token_avaiable()

        coreapi = Server(
            config.COREAPI_SERVER,
            headers={
                'Authorization': 'Bearer {}'.format(jwt_token)
            }
        )

        result = coreapi.clients.get(id=client_id)
        return result
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return e
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return e
    
    
def coreapi_clients_search(is_limit = False, limit: int = 0):
    '''
    Search for clients infomation in the coreAPI server using the provided options.

    The function searches for clients based on the provided options. If is_limit is False, the API will return all client's information, else it will return the number of client information according to the 'limit' variable.

    Parameters:
        config_section (str): The section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_assigned_name (str): The name of the token variable in the specified section. Default is 'jwt_token'.
        is_limit (bool): A flag indicating whether to apply a limit on the number of results.
                         If True, the 'limit' parameter is used to specify the maximum number of results.
                         If False, no limit is applied. Default is False.
        limit (int): The maximum number of results to return. This parameter is only used if 'is_limit' is True.
                     Default is 0, which means no limit is applied.

    Returns:
        list: A list of dictionaries, each containing information about clients that matches the search criteria.
              If no clients match the search criteria, an empty list is returned.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
    '''
    try:
        # jwt_token = check_token_avaiable()

        # coreapi = Server(
        #     config.COREAPI_SERVER,
        #     headers={
        #         'Authorization': 'Bearer {}'.format(jwt_token)
        #     }
        # )

        coreapi = get_coreapi()
        if is_limit:
            result = coreapi.clients.search(limit=limit)
        else:
            result = coreapi.clients.search(limit = 10000)
        return result
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return e
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return e
    

def coreapi_accounts_search(client_id: int = 0):
    '''
    Search for accounts associated with a client in the coreAPI server.

    The function searches for accounts associated with the specified 'client_id'.

    Parameters:
        config_section (str): The section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_assigned_name (str): The name of the token variable in the specified section. Default is 'jwt_token'.
        client_id (int): The ID of the client for which to search associated accounts.

    Returns:
        list: A list of dictionaries, each containing information about the accounts which is associated with the client.
              If no accounts are associated with the client, an empty list is returned.
              If the client with the specified ID is not found, an exception is returned.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
    '''
    try:
        # jwt_token = check_token_avaiable()

        # coreapi = Server(
        #     config.COREAPI_SERVER,
        #     headers={
        #         'Authorization': 'Bearer {}'.format(jwt_token)
        #     }
        # )
        coreapi = get_coreapi()

        result = coreapi.clients.accounts.search(clients_id=client_id)
        return result
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return e
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return e
    

def coreapi_accounts_search_list(is_limit = False, limit: int = 0):
    '''
    Search for a list accounts in the coreAPI server based on the provided options.

    The function searches for alist of accounts based on the provided options.

    Parameters:
        config_section (str): The section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_assigned_name (str): The name of the token variable in the specified section.Default is 'jwt_token'.
        is_limit (bool): A flag indicating whether to apply a limit on the number of results.
                         If True, the 'limit' parameter is used to specify the maximum number of results.
                         If False, no limit is applied. Default is False.
        limit (int): The maximum number of results to return. This parameter is only used if 'is_limit' is True.
                     Default is 0, which means no limit is applied.

    Returns:
        list: A list of dictionaries, each containing information about an account that matches the search criteria.
              If no accounts match the search criteria, an empty list is returned.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
    '''
    try:
        # jwt_token = check_token_avaiable()
        # print(f"{config.COREAPI_SERVER}")
        # coreapi = Server(
        #     config.COREAPI_SERVER,
        #     headers={
        #         'Authorization': 'Bearer {}'.format(jwt_token)
        #     }
        # )
        coreapi = get_coreapi()

        if is_limit:
            result = coreapi.clients.accounts.search(limit=limit)
        else:
            result = coreapi.clients.accounts.search()
        return result
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return e
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return e
    

def coreapi_accounts_get(account_id: int = 0): 
    '''
    Get account information from the coreAPI server using the provided account ID.

    The function queries the coreAPI server to get information about the account with the specified 'account_id'.

    Parameters:
        config_section (str): The section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_assigned_name (str): The name of the token variable in the specified section. Default is 'jwt_token'.
        account_id (int): The ID of the account to retrieve information for.

    Returns:
        list: A list of dictionary containing the information about the account obtained from the coreAPI server.
              If the account with the specified ID is not found, an exception is returned.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
    '''
    try:
        # jwt_token = check_token_avaiable()

        # coreapi = Server(
        #     config.COREAPI_SERVER,
        #     headers={
        #         'Authorization': 'Bearer {}'.format(jwt_token)
        #     }
        # )

        coreapi = get_coreapi()

        result = coreapi.clients.accounts.get(id=account_id)
        return result
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return e
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return e
    
def coreapi_clients_authenticate(user: str = '', password: str = ''):
    '''
    Authenticate a user with the coreAPI server and check if the user has the required admin role.

    This function authenticates an admin user with 'All Resellers' in Reseller field (VCS_ADMIN and VCS_ADMIN_PASSWORD constants) with the coreAPI server to obtain an JWT token. 
    Then, authenticate the user with the specified 'user' (username) and 'password'. 
    If the user is successfully authenticated. Then use admin user which is authenticated before to check if the user has the admin role (VCS_ADMIN_ROLES_NAME), the function returns True; otherwise, it returns False.

    Parameters:
        config_section (str): The config_section name in the configuration file where the JWT token is stored. Default is 'coreAPI_Token'.
        config_config_assisged_name (str): The name of the token variable in the specified config_section. Default is 'jwt_token'.
        user (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        bool: True if the user is authenticated and has the required admin role; otherwise, False.

    Raises:
        jsonrpc_requests.jsonrpc.TransportError: If there is a transport-related error while communicating with the coreAPI server.
        jsonrpc_requests.jsonrpc.ProtocolError: If there is a protocol-level error during the communication.
    '''
    try:
        coreapi_unauthorized = Server(config.VCS_COREAPI)

        # this will be used to check user role
        admin_login = coreapi_unauthorized.iam.auth.jwt.authenticate(
            login=config.VCS_ADMIN,
            password=config.VCS_ADMIN_PASSWORD
        )
        jwt_token = admin_login['token']

        coreapi = Server(
            config.VCS_COREAPI,
            headers={
                'Authorization': 'Bearer {}'.format(jwt_token)
            }
        )

        # check the valid login
        user_login = coreapi_unauthorized.iam.auth.jwt.authenticate(
            login=user,
            password=password
        )

        if user_login:
            result = coreapi.iam.users.search(login=user)
            roles_name = result[0]['roles_name']
            if roles_name == config.VCS_ADMIN_ROLES_NAME:
                return True
            else:
                return False
        return False
    except jsonrpc_requests.jsonrpc.TransportError as e:
        return False
    except jsonrpc_requests.jsonrpc.ProtocolError as e:
        return False

import requests  
import json
def request_token():
    url = 'http://10.155.19.150:3080'
    json={
    "jsonrpc": "2.0",
    "method": "iam.auth.jwt.authenticate",
    "params": {
        "login": "servicecontrol",
        "password": "Vcs@2023"
    },
    "id": 1
    }
    headers = {'Content-Type': 'application/json'}
    
    return requests.post(url, headers=headers, json=json).json()['result']['token']

def get_xdrs():
    url = 'http://10.155.19.150:3080'
    json={
    "jsonrpc": "2.0",
    "method": "reports.xdrs_list.query",
    "params": {
        "return_fields":["src_party_id_ext","dst_party_id_ext","start_time","stop_time","volume","subscriber_host","subscriber_id"], 
        "filters": {"origin": "orig", "billed_clients_id": 13, "date": ["2023-11-01 10:59:15", "2023-11-23 10:59:17"]}, # custom tham số
        "limit": 10
    },
    "id": 1
    }

    headers = {'Content-Type': 'application/json','Authorization': "Bearer "+request_token()}
    
    print(requests.post(url, headers=headers, json=json).json())
    

if __name__ == '__main__':

    print('------------------------------------------------------------')
    print('Welcome to coreAPI')
    print(get_xdrs())
    # print(generate_jwt_token())
    # print(coreapi_clients_get(36))
    # print(coreapi_clients_search())
    # print(coreapi_accounts_search_list())
    # print(coreapi_accounts_search(27))


