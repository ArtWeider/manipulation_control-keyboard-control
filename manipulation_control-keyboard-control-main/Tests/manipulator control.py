import telnetlib as telnet


tn = telnet.Telnet('192.168.137.182', '23')
print("CONNECTED")
while True:
    text = input("Cords: ")
    splitted = text.split(" ")
    tn.write(f'X{splitted[0]} Y{splitted[1]} Z{splitted[2]} Q{splitted[3]}'.encode('utf-8'))