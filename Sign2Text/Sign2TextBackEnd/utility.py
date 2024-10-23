import re

ACCEPTED_TYPES = ['image']
ACCEPTED_FORMATS = ['png', 'jpg', 'jpeg']

def get_file_format_from_info_text(info_text=''):
    _, file_type, file_format, _ = [info.lower() for info in re.split(r"[\W_]+", info_text) if info]

    if file_type not in ACCEPTED_TYPES:
        raise ValueError('Provided file must be an image.')
    
    if file_format not in ACCEPTED_FORMATS:
        raise ValueError('Provided file must be of valid formats.')
    
    return file_format