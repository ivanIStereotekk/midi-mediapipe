import socket
import time
import rtmidi
import re
from rtmidi import *
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON


class MidiServer(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MidiServer, cls).__new__(cls)
            return cls.instance

    def __init__(self):
        self.MIDIOUT = rtmidi.MidiOut()

    def play_midi(self, NOTE, PORT):
        with (self.MIDIOUT.open_port(PORT) if self.MIDIOUT.get_ports() else
              self.MIDIOUT.open_virtual_port("My virtual output")):
            self.MIDIOUT.send_message([NOTE_ON, NOTE, 112])
            time.sleep(0.1)
            self.MIDIOUT.send_message([NOTE_OFF, NOTE, 0])
            time.sleep(0.1)


CENTER_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']





midi_inst = MidiServer()
if __name__ == '__main__':
    print('MIDI Server is OK!')
    HOST = '127.0.0.1'
    PORT = 65432
    
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
        skt.bind((HOST, PORT))
        skt.listen()
        conn, addr = skt.accept()
        with conn:
            print('Connected by', addr)
            while True:
                bytes_data = conn.recv(1024)
                data_string = bytes_data.decode('utf-8')
                digits_one = re.findall('\d', data_string)
                digits_two = re.findall('\d[0-9]', data_string)
                digits_three = re.findall('\d[0-9][0-9]', data_string)
                midi_inst.play_midi(int(digits_two[0]), int(digits_one[0]))


