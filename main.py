import re
from pprint import pprint
import csv


def read_adress_book(file):
    with open(file, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def update_people(contacts_list):
    contacts_list_new =[]
    for contact in contacts_list:
        pattern = r'[\s,]'
        full_name = (re.split(pattern, ' '.join(contact[:3])))[:3]
        info = contact[3:]
        contact = full_name + info
        contacts_list_new.append(contact)
    return contacts_list_new

def update_numbers(contacts_list):
    contacts_list_new = []
    for contact in contacts_list:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?\-?\s*(\d{3})\-?'\
                r'(\d{2})\-?(\d+)(\s*)\(*([доб.]*)?\s*(\d{4})?\)*'
        phone_exist = re.search(pattern, contact[-2])
        if phone_exist is not None:
            result = re.sub(pattern, r'+7(\2)\3-\4-\5\6\7\8', contact[-2])
            contact[-2] = result
        contacts_list_new.append(contact)
    return contacts_list_new


def merge(contacts_list):
    contacts_to_del = []
    for contact in contacts_list:
        pattern = ', '.join([contact[0], (contact[1])])
        cut = contacts_list.index(contact) + 1
        for element in contacts_list[cut:]:
            full_name = ', '.join([element[0], (element[1])])
            result = re.search(pattern, full_name)
            if result is not None:
                if contact[2] == '':
                    contact[2] = element[2]
                if contact[3] == '':
                    contact[3] = element[3]
                if contact[4] == '':
                    contact[4] = element[4]
                if contact[5] == '':
                    contact[5] = element[5]
                if contact[6] == '':
                    contact[6] = element[6]
                contacts_to_del.append(element)
    contacts_list_new = [contact for contact in contacts_list if contact not in contacts_to_del]
    return contacts_list_new


def save_to_file(contacts_list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    fixed_contacts = read_adress_book('phonebook11_raw.csv')
    fixed_contacts = update_people(fixed_contacts)
    fixed_contacts = update_numbers(fixed_contacts)
    fixed_contacts = merge (fixed_contacts)
    save_to_file(fixed_contacts)



