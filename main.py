import PySimpleGUI as sg
import secrets
import string
import re
import string
import random

def init_layout(height, width):
    input_text_column = [
        [sg.Text("Inputed text")],
        [sg.Multiline(size=(height, width), key='IN_TEXTBOX')],
        [sg.InputText(key="Browse_text"), sg.Button("Browse"), sg.Button("Clear textboxes")]
    ]

    encrypted_text_column = [
        [sg.Text("Encrypted text")],
        [sg.Multiline(size=(height, width), key="ENC_TEXTBOX")],
        [sg.Button("Encrypt"), sg.Button("Save encrypted file")]
    ]

    decrypted_text_column = [
        [sg.Text("Decrypted text")],
        [sg.Multiline(size=(height, width), key="DEC_TEXTBOX")],
        [sg.Button("Decrypt"), sg.Button("Save decrypted file")]
    ]

    layout = [
        [
            sg.Column(input_text_column),
            sg.VSeperator(),
            sg.Column(encrypted_text_column),
            sg.VSeperator(),
            sg.Column(decrypted_text_column),
        ]
    ]
    return layout

def clear_event(window):
    window.find_element('IN_TEXTBOX').Update('')
    window.find_element('ENC_TEXTBOX').Update('')
    window.find_element('DEC_TEXTBOX').Update('')
    window.find_element('Browse_text').Update('')

random_key = ""

alphabets = "abcdefghijklmnopqrstuvwxyz1234567890.,:;' "

letter_to_index = dict(zip(alphabets,range(len(alphabets))))
index_to_letter = dict(zip(range(len(alphabets)),alphabets))

encrypted_text = ""

def encryption(msg):
    encrypted = ""
    global random_key
    random_key = ''.join(secrets.choice(string.ascii_lowercase)
    for i in range(len(msg)))
    try:
        for i in range(len(msg)):
            number = (letter_to_index[msg[i]] + letter_to_index[random_key[i]]) % len(alphabets)
            if number > len(alphabets):
                number -= len(alphabets)

            encrypted += index_to_letter[number]
    except:
     sg.popup('ERROR!', 'Dictionary is not suitable for encryption')
     return

    global encrypted_text
    encrypted_text = encrypted
    return encrypted

def decryption(cipher):
    decrypted = ""
    for i in range(len(cipher)):
        number = (letter_to_index[cipher[i]] - letter_to_index[random_key[i]])%len(alphabets)
        if number < 0 :
            number += len(alphabets)
        decrypted +=index_to_letter[number]
    return decrypted

def decrypt_text(window, values):
    if len(window.find_element('ENC_TEXTBOX').get()) == 1:
        sg.popup('ERROR!', 'Empty encrypted text column')
    else:
        string = values['ENC_TEXTBOX']
        chiper = string.rstrip()
        decrypted = decryption(chiper)
        window.find_element('DEC_TEXTBOX').Update(decrypted)

def encrypt_text(window, values):
    if len(window.find_element('IN_TEXTBOX').get()) == 1:
        sg.popup('ERROR! Empty string', 'Please fill in the field or check the content of the file!')
    else:
        string = values['IN_TEXTBOX']
        msg = string.rstrip()
        msg = msg.lower()
        encrypted = encryption(msg)
        window.find_element('ENC_TEXTBOX').Update(encrypted)

def load_file(window, values):
    string = values['Browse_text']
    if string == '':
        sg.popup('ERROR! Empty string', 'Please choose file!')
    else:
        try:
            with open(string, 'r') as file:
                data = file.read().replace('\n', ' ')
                window.find_element('IN_TEXTBOX').Update(data)
        except IOError:
            sg.popup('ERROR!', 'No such file exists')

def save_file (window, values, key_textbox):
    if len(window.find_element(key_textbox).get()) == 1:
        sg.popup('ERROR! Empty string', 'No data to save')
    else:
        text = values[key_textbox]
        name = ''.join(secrets.choice(string.ascii_lowercase) for i in range(5))
        file = open(name + ".txt", "w")
        file.write(text)
        file.close()
        sg.popup('DONE', 'The file ' + name + '.txt' + ' has been saved to the root directory of the project')

def main():
    layout = init_layout(40, 20)
    window = sg.Window('LAB_1', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Clear textboxes':
            clear_event(window)
        if event == 'Encrypt':
            encrypt_text(window, values)
        if event == 'Decrypt':
            decrypt_text(window, values)
        if event == 'Browse':
            load_file(window, values)
        if event == 'Save encrypted file':
            save_file(window, values, 'ENC_TEXTBOX')
        if event == 'Save decrypted file':
            save_file(window, values, 'DEC_TEXTBOX')

if __name__ == "__main__":
    main()

