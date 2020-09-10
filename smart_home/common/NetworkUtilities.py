import re
import smart_home.common.Constants as Constants

def extract_ip_address(data):
    # Get IP address
    match = re.match(Constants.IP_FORMAT_REGEX, data)

    # Return IP address
    return match.group(1)
