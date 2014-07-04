import configparser

def ini_parser(input_file):
    """
        input parameter: file name. eg: test.ini
        output type: list

        usage: iniParset(input_file.ini)
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(input_file)
    section_dict = {}
    output_list = []
    method = ""
    api = ""
    total_section = config.sections()
    for sSection in total_section:
        method = sSection.split()[0]
        api = sSection.split()[1]
        is_GET = False
        if method == "GET":
            is_GET = True
        # json_url=""; "json"; "urlencode";
        specific_key = "" 
        # set json_url ( json OR urlencode )
        for item in config.items(sSection):
            if is_GET == True and item[0] == "input_format":
                raise Exception("Error: GET with 'input_format'.")
            if item[0] == "input_type" and item[1] == "urlencode":
                json_url = "urlencode"
            if item[0] == "input_type" and item[1] == "json":
                json_url = "json"
        for item in config.items(sSection):
            key = temp_key = item[0]
            value = item[1].replace("\n", "")
            # handle specific case: urlencode OR json
            if key == "input_format" and json_url == "urlencode":
                temp_value = urlencode_format(value)
            elif key == "input_format" and json_url == "json":
                temp_value = json_format(value)
            elif key == "headers":
                temp_value = headers_format(value)
            elif key == "url_params":
                temp_value = url_params_format(value)
            else: 
                temp_value = value
            section_dict.update({temp_key: temp_value})
        section_dict.update({'method': method})
        section_dict.update({'api': api})
        output_list.append(section_dict.copy())
        section_dict.clear()
    return output_list

# json_format return json-like string
def json_format(value):
    value = value.replace("\n", "")
    return value

# headers_format return dictionary
def headers_format(value):
    output_value = {}
    value_list = value.split("\n")
    for i in value_list:
        data = i.split(":")
        output_value.update({data[0]: data[1].strip()}) 
    return output_value

# url_params_format return dictionary
def url_params_format(value):
    value = value.replace(")",") ")
    output_value = {}
    for i in value.split(" "):
        pair = i.split("=")
        key = pair[0]
        if pair[0] != "":
            temp_value = pair[1]
            temp_value = temp_value.replace("(", "")
            temp_value = temp_value.replace(")", "")
            value_list = temp_value.split(",")
            first = value_list[0]
            second = value_list[1]
            if first == "":
                first = None
            if second == "":
                second = None
            else:
                if first == "int":
                    second = int(second)
                elif first == "float":
                    second = float(second)
                else:
                    second = bool(second)
            # empty means essential, essential is True
            output_value.update({key: (first, second)})
    return output_value


# urlencode_format return dictionary
def urlencode_format(value):
    value = value.replace(")", ") ")
    output_value = {}
    for i in value.split(" "):
        pair = i.split("=")
        key = pair[0]
        if pair[0] != "":
            temp_value = pair[1]
            temp_value = temp_value.replace("(", "")
            temp_value = temp_value.replace(")", "")
            value_list = temp_value.split(",")
            first = value_list[0]
            second = value_list[1]
            third = value_list[2]
            if first == "":
                first = None
            if second == "":
                second = None
            else:
                if first == "int":
                    second = int(second)
                elif first == "float":
                    second = float(second)
                else:
                    second = bool(second)
            # empty means essential, essential is True
            if third == "":
                third = True
            else:
                third = False
            output_value.update({key:(first, second, third)})
    return output_value
