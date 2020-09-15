import probablepeople
import pandas as pd
import json

def name_classifier(input_file, output_file):
    data = pd.read_excel('2020-07-30 12-49-08.786143-assessor.xlsx')
    data.fillna('', inplace=True)
    owner_names = data['Owners Names']
    buyer_names = data['Last Buyers Names']

    output = {'Owners': [], 'Buyers': []}


    corporate_list = ["CO", "LLC", "TRUST", "LL", "LP", "DEPARTMENT", "PLAN", "OF", "INC", "FAMILY", "PROPERTIES",
                      "REVOCABLE", "ESTATES", "&", "INVESTMENTS"]

    for name in owner_names:
        if not name:
            output['Owners'].append({
                'Last Name': '',
                'MIddle Name': '',
                'First Name': ''
            })
        else:

            name = name.split(', ')
            valid_name = [{} for _ in range(len(name))]
            for num in range(len(name)):
                name_split = name[num].split(' ')
                if not any([sub_name in name_split for sub_name in corporate_list]):
                    name_original = name[num]
                    if len(name_split) > 1:
                        if len(name_split[1]) == 1:
                            name_split[0], name_split[-1] = name_split[-1], name_split[0]
                            name[num] = " ".join(name_split)
                        else:
                            name_temp = name_split[1:]
                            name_temp.append(name_split[0])
                            name[num] = " ".join(name_temp)

                    try:
                        parse = probablepeople.tag(name[num])
                        parsed_name = parse[0]
                        parsed_type = parse[1]

                        if parsed_type == "Person":
                            if 'LastName' in parsed_name.keys():
                                valid_name[num]['LastName'] = parsed_name['LastName']
                            elif 'Surname' in parsed_name.keys():
                                valid_name[num]['LastName'] = parsed_name['Surname']
                            elif 'LastInitial' in parsed_name.keys():
                                valid_name[num]['LastName'] = parsed_name['LastInitial']
                            else:
                                valid_name[num]['LastName'] = ''

                            if 'MiddleName' in parsed_name.keys():
                                valid_name[num]['MiddleName'] = parsed_name['MiddleName']
                            elif 'MiddleInitial' in parsed_name.keys():
                                valid_name[num]['MiddleName'] = parsed_name['MiddleInitial']
                            else:
                                valid_name[num]['MiddleName'] = ''

                            if 'GivenName' in parsed_name.keys():
                                valid_name[num]['FirstName'] = parsed_name['GivenName']
                            elif 'FirstInitial' in parsed_name.keys():
                                valid_name[num]['FirstName'] = parsed_name['FirstInitial']
                            else:
                                valid_name[num]['FirstName'] = ''

                        elif parsed_type == "Household":
                            valid_name[num] = parsed_name

                        # the name is categorized as "Corporation" after shifting
                        # then we use TBD(To Be Decided): original name
                        else:
                            valid_name[num] = {"TBD": name_original}

                    except probablepeople.RepeatedLabelError as e:
                        valid_name[num] = {'original name': e.original_string,
                                           'parsed name': e.parsed_string}

                # the name is categorized as "Corporation" by our definition
                else:
                    try:
                        parse = probablepeople.tag(name[num])
                        parsed_name = parse[0]
                        # parsed_type = parse[1]

                        valid_name[num] = parsed_name

                    except probablepeople.RepeatedLabelError as e:
                        valid_name[num] = {'original name': e.original_string,
                                           'parsed name': e.parsed_string}

            output['Owners'].append(valid_name)


    for name in buyer_names:
        if not name:
            output['Owners'].append({
                'Last Name': '',
                'MIddle Name': '',
                'First Name': ''
            })
        else:

            name = name.split('/ ')
            valid_name = [{} for _ in range(len(name))]
            for num in range(len(name)):
                name_split = name[num].split(' ')
                if not any([sub_name in name_split for sub_name in corporate_list]):
                    name_original = name[num] * 1
                    if len(name_split) > 1:
                        if len(name_split[1]) == 1:
                            name_split[0], name_split[-1] = name_split[-1], name_split[0]
                            name[num] = " ".join(name_split)
                        else:
                            name_temp = name_split[1:]
                            name_temp.append(name_split[0])
                            name[num] = " ".join(name_temp)

                    try:
                        parse = probablepeople.tag(name[num])
                        parsed_name = parse[0]
                        parsed_type = parse[1]

                        if parsed_type == "Person":
                            if 'LastName' in parsed_name.keys():
                                valid_name[num]['LastName'] = parsed_name['LastName']
                            elif 'Surname' in parsed_name.keys():
                                valid_name[num]['LastName'] = parsed_name['Surname']
                            elif 'LastInitial' in parsed_name.keys():
                                valid_name[num]['LastName'] = parsed_name['LastInitial']
                            else:
                                valid_name[num]['LastName'] = ''

                            if 'MiddleName' in parsed_name.keys():
                                valid_name[num]['MiddleName'] = parsed_name['MiddleName']
                            elif 'MiddleInitial' in parsed_name.keys():
                                valid_name[num]['MiddleName'] = parsed_name['MiddleInitial']
                            else:
                                valid_name[num]['MiddleName'] = ''

                            if 'GivenName' in parsed_name.keys():
                                valid_name[num]['FirstName'] = parsed_name['GivenName']
                            elif 'FirstInitial' in parsed_name.keys():
                                valid_name[num]['FirstName'] = parsed_name['FirstInitial']
                            else:
                                valid_name[num]['FirstName'] = ''

                        elif parsed_type == "Household":
                            valid_name[num] = parsed_name

                        # the name is categorized as "Corporation" after shifting
                        # then we use TBD(To Be Decided): original name
                        else:
                            valid_name[num] = "TBD: " + name_original

                    except probablepeople.RepeatedLabelError as e:
                        valid_name[num] = {'original name': e.original_string,
                                           'parsed name': e.parsed_string}

                # the name is categorized as "Corporation" by our definition
                else:
                    try:
                        parse = probablepeople.tag(name[num])
                        parsed_name = parse[0]
                        # parsed_type = parse[1]

                        valid_name[num] = parsed_name

                    except probablepeople.RepeatedLabelError as e:
                        valid_name[num] = {'original name': e.original_string,
                                           'parsed name': e.parsed_string}

            output['Buyers'].append(valid_name)

    with open(output_file, 'w') as outfile:
        json.dump(output, outfile)


if __name__ == "__main__":
    name_classifier(input_file='2020-07-30 12-49-08.786143-assessor.xlsx', output_file='output.json')

    