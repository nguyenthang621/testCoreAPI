import os 
from dotenv import load_dotenv, set_key
from pathlib import Path

load_dotenv()

# SBC
HOSTNAME = os.getenv('hostname')
USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')

# FILE
REMOTE_PATH = os.getenv('remote_path')
RETRY_ATTEMPS = os.getenv('retry_attemps')
RETRY_DELAY = os.getenv('retry_delay')
LOCAL_PATH = os.getenv('local_path')

METADATA_PATH = os.getenv('metadata_path')
CDR_FILENAME_FORMAT = os.getenv('cdr_filename_format')
OUTPUT_FILE_EXTENSION = os.getenv('output_file_extension')

# CORE API
COREAPI_SERVER =  os.getenv('coreapi_server')
COREAPI_USERNAME =  os.getenv('coreapi_username')
COREAPI_PASSWORD =  os.getenv('coreapi_password')
JWT_TOKEN =  os.getenv('jwt_token')


# CDR 
ACCT_START_CDR_LENGTH = os.getenv('acc_start_cdr_length')
ACCT_STOP_CDR_LENGTH = os.getenv('acc_stop_cdr_length')
ORG_TRUNK_ACC_START = os.getenv('ori_trunk_group_acc_start_field')
ORG_TRUNK_ACC_STOP = os.getenv('ori_trunk_group_acc_stop_field')

ACCOUNTING_START = os.getenv('acc_start_value')
ACCOUNTING_STOP = os.getenv('acc_stop_value')

ACCOUTING_STATUS = os.getenv('acc_status_field')

CONNECT_TIME_START = os.getenv('cisco_connect_time_start_field')
CONNECT_TIME_STOP = os.getenv('cisco_connect_time_stop_field')

TIMEZONE_MAPPING_FILE_PATH = os.getenv('timezone_mapping_file_path')
CDR_TIMEZONE = os.getenv('cdr_timezone')

XDR_FILTER_TIMEZONE = os.getenv('filter_timezone')


# VCS
VCS_COREAPI = os.getenv('vcs_coreapi')
VCS_LOGIN = os.getenv('vcs_login')
VCS_PASSWORD = os.getenv('vcs_password')
VCS_ADMIN = os.getenv('vcs_admin')
VCS_ADMIN_PASSWORD= os.getenv('vcs_admin_password')
VCS_ADMIN_ROLES_NAME = os.getenv('vcs_admin_roles_name')



def write_to_env_file(key, value, env_file_path='./config/.env'):
    try:
        existing_data = {}
        if os.path.exists(env_file_path):
            with open(env_file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        existing_data[k.strip()] = v.strip()

        existing_data[key] = str(value)

        with open(env_file_path, "w") as f:
            for k, v in existing_data.items():
                f.write(f"{k} = {v}\n")
    except Exception as e:
        return e
    


if __name__ == '__main__':
    print(HOSTNAME)
    print(USERNAME)




