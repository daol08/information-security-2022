# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError
from hashlib import new

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    #print(ord(input) - ord('A'))
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    global rotor1, rotor2, rotor3,rotor3_left, rotor2_left, rotor1_left

    #reverse_list = reversed(SETTINGS["WHEELS"])
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    if reverse== False:
        # pass the first rotor3
        p_index = ord(input) - ord('A')
        input = rotor3_left[p_index]
        input_index = ord(input) - ord('A')
        input = rotor3["wire"][input_index]
        #print("pass rotor3: "+ input+"\n")
        #pass the second rotor2
        input_index = rotor3_left.find(input)
        input = rotor2_left[input_index]
        input_index = ord(input) - ord('A')
        input = rotor2["wire"][input_index]
        #print("pass rotor2: "+ input+"\n")
        #pass the third rotor1
        input_index = rotor2_left.find(input)
        input = rotor1_left[input_index]
        input_index = ord(input) - ord('A')
        input = rotor1["wire"][input_index]

        p_index = rotor1_left.find(input)
        input = SETTINGS["ETW"][p_index]
        #print("pass rotor1: "+ input+"\n")
        
        return input

    #reverse order
    else:
        #print("after reflection: "+input+"\n")
        p_index = ord(input) - ord('A')
        input = rotor1_left[p_index]
        input_index = rotor1["wire"].find(input)
        input = SETTINGS["ETW"][input_index]
        #print("pass rotor1: "+ input+"\n")

        p_index = rotor1_left.find(input)
        input = rotor2_left[p_index]
        input_index = rotor2["wire"].find(input)
        input = SETTINGS["ETW"][input_index]
        #print("pass rotor2: "+ input+"\n")

        p_index = rotor2_left.find(input)
        input = rotor3_left[p_index]
        input_index = rotor3["wire"].find(input)
        input = SETTINGS["ETW"][input_index]
        #print("pass rotor3: "+ input+"\n")

        p_index = rotor3_left.find(input)
        input = SETTINGS["ETW"][p_index]
        return input


# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    global  rotor3_left, rotor2_left, rotor1_left
    #실행 시 rotor3 부터 하나씩 올라가야함 + norch 부분이 걸리면 다음 로터도 회전
    if SETTINGS["WHEEL_POS"][2] == SETTINGS["WHEELS"][2]['turn']:
        if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]['turn']:
            SETTINGS["WHEEL_POS"][1] += 1
            rotor2_left = positioning(SETTINGS["WHEEL_POS"][2])
            SETTINGS["WHEEL_POS"][2] += 1
            rotor3_left = positioning(SETTINGS["WHEEL_POS"][2])
        else:
            SETTINGS["WHEEL_POS"][1] += 1
            rotor2_left = positioning(SETTINGS["WHEEL_POS"][1])
    if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]['turn']:
        SETTINGS["WHEEL_POS"][0] += 1
        rotor1_left = positioning(SETTINGS["WHEEL_POS"][0])
    else:
        SETTINGS["WHEEL_POS"][2] += 1
        rotor3_left = positioning(SETTINGS["WHEEL_POS"][2])

    pass

plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)
global  rotor1, rotor2, rotor3, rotor3_left, rotor2_left, rotor1_left

rotor3 = SETTINGS["WHEELS"][2]
rotor2 = SETTINGS["WHEELS"][1]
rotor1 = SETTINGS["WHEELS"][0]

def positioning(pos):
    str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if pos>26:
        pos = pos%26
    str = str[pos:]+str[0:pos]
    return str

rotor3_left = positioning(SETTINGS["WHEEL_POS"][2])
rotor2_left = positioning(SETTINGS["WHEEL_POS"][1])
rotor1_left = positioning(SETTINGS["WHEEL_POS"][0])

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')

