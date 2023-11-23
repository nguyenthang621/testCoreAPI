# import os
# import configparser


# def read_config(config_path=None, config_file_name='ServiceControl.cfg'):
#     """
#     Reads the configuration file and returns a ConfigParser object containing the configuration data.

#     Parameters:
#         config_path (str, optional): The path to the configuration file. If not provided, the default path is used.
#         config_file_name (str, optional): The name of the configuration file if 'config_path' is not provided.
#                                           Default is 'ServiceControl.cfg'.

#     Returns:
#         config (ConfigParser): A ConfigParser object containing the configuration data.

#     Raises:
#         FileNotFoundError: If the configuration file does not exist.
#     """
#     if config_path is None:
#         config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file_name)

#     if os.path.isfile(config_path):
#         config = configparser.ConfigParser()
#         config.read(config_path)
#         return config
#     else:
#         raise FileNotFoundError(f"The file '{config_path}' does not exist.")


# def config_keys(config_section:str, config_path=None, config_file_name='ServiceControl.cfg'):
#     """
#     Retrieve all the keys within the specified section of a configuration file.

#     This function reads the configuration file located at 'config_path' (or the default location if 'config_path' is not
#     provided) using the 'configparser' library. It then retrieves all the keys within the specified 'config_section'
#     and returns them as a list.

#     Parameters:
#         config_section (str): The section name in the configuration file from which to retrieve the keys.
#         config_path (str, optional): The path to the configuration file. If not provided, the default location 'ServiceControl.cfg' in the same directory as the script is used.
#         config_file_name (str, optional): The name of the configuration file if 'config_path' is not provided. Default is 'ServiceControl.cfg'.

#     Returns:
#         list: A list containing all the keys within the specified 'config_section' of the configuration file.

#     Raises:
#         FileNotFoundError: If the specified 'config_path' does not exist.
#     """
#     if config_path is None:
#         config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file_name)
#     if os.path.isfile(config_path):
#         config = configparser.ConfigParser()
#         config.read(config_path)

#         keys = [key for key in config[config_section]]
#         return keys
#     else:
#         raise FileNotFoundError(f"The file '{config_path}' does not exist.")


# def check_config_section(config_path=None, config_section:str='', config_file_name='ServiceControl.cfg'):
#     """
#     Check if a specific section exists in the specified configuration file.

#     This function reads the configuration file located at 'config_path' (or the default location if 'config_path' is not
#     provided) using the 'configparser' library. It then checks if the specified 'config_section' exists within the
#     configuration file.

#     Parameters:
#         config_path (str, optional): The path to the configuration file. If not provided, the default location 'ServiceControl.cfg' in the same directory as the script is used.
#         config_section (str): The section name to check if it exists within the configuration file.
#         config_file_name (str, optional): The name of the configuration file if 'config_path' is not provided. Default is 'ServiceControl.cfg'.

#     Returns:
#         tuple: A tuple containing two elements:
#                - The first element is a boolean indicating if the 'config_section' exists in the configuration file.
#                - The second element is the path to the configuration file used for the check.

#     Example:
#         exists, path = check_config_section(config_section='coreAPI_Token')
#         if exists:
#             print(f"The section 'coreAPI_Token' exists in the configuration file at: {path}")
#         else:
#             print(f"The section 'coreAPI_Token' does not exist in the configuration file at: {path}")
#     """
#     if config_path is None:
#         dir_path = os.path.dirname(os.path.abspath(__file__))
#         config_path = os.path.join(dir_path, config_file_name)
#     config = configparser.ConfigParser()
#     if os.path.isfile(config_path):
#         config.read(config_path)
#         sections = config.sections()
#         for sec in sections:
#             if config.has_section(config_section):
#                 return True, config_path
#     return False, config_path


# def write_token_to_config(config_path=None, config_section:str='', name_to_assign:str='' ,token:str=''):
#     """
#     Writes a token value to the specified configuration file and section.

#     If the specified 'config_section' does not exist in the configuration file, the function adds the section before
#     setting the token value. 

#     Parameters:
#         config_path (str, optional): The path to the configuration file. If not provided, the default path is used.
#         config_section (str): The section name in the configuration file where the token value will be stored.
#         name_to_assign (str): The name of the token variable in the specified section.
#         token (str): The token value to be written to the configuration file.

#     Returns:
#         bool: True if the token value was successfully written to the configuration file.
#     """
#     check, config_path = check_config_section(config_section=config_section)
#     config = configparser.ConfigParser()

#     config.read(config_path)
#     if check is False:
#         config.add_section(config_section)
#     config.set(config_section, name_to_assign, token)

#     with open(config_path, 'w') as file:
#         config.write(file)

#     return True