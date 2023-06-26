#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl

Provided as an illustration of the basic communication interface
for grbl. When grbl has finished parsing the g-code block, it will
return an 'ok' or 'error' response. When the planner buffer is full,
grbl will not send a response until the planner buffer clears space.

G02/03 arcs are special exceptions, where they inject short line 
segments directly into the planner. So there may not be a response 
from grbl for the duration of the arc.

---------------------
The MIT License (MIT)

Copyright (c) 2012 Sungeun K. Jeon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
---------------------
"""
import serial.tools.list_ports
import time
import sys


# Open grbl serial port


s = serial.Serial(sys.argv[1], 115200)
time.sleep(1)  # Allow some time for the serial connection to be established

# Open g-code file
config = ["$100=50", "$101=22.25", "$110=1300", "$111=2000", "$120=500", "$121=500", "G92 X0 Y0 Z0"]
f = ["G21"]

# Wake up grbl
s.write("\r\n\r\n".encode('utf-8'))
time.sleep(2)  # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

s.write('?'.encode('utf-8'))  # Request position
response = s.readline().decode('utf-8').strip()  # Read the response
print(f'Response: {response}')

# Extract the X, Y, and Z coordinates
position = response.replace('>', '').split('WCO:')[1].split(',')[:3]
x, y, z = [float(coord) for coord in position]


def run_command(command):
    l = command.strip()  # Strip all EOL characters for consistency
    print('Sending: ' + l)
    s.write((l + '\n').encode('utf-8'))  # Send g-code block to grbl
    read_response()


def read_response():
    response = s.readline().decode('utf-8').strip()  # Read the response from the CNC machine
    print(response)


def draw_x(position):
    comms = []
    if position == '1':
        comms = ['G0 X55 Y55',
                    'M3 S1',
                    'G4 P.1',
                    'G1 F1500 X85 Y85',
                    'M3 S0',
                    'G4 P.1',
                    'G0 X55 Y85',
                    'M3 S1',
                    'G4 P.1',
                    'G1 F1500 X85 Y55',
                    'M3 S0',
                    'G4 P.1',]
    elif position == '2':
        comms = ['G0 X95 Y55',
                    'M3 S1',
                    'G4 P.1',
                    'G1 F1500 X125 Y85',
                    'M3 S0',
                    'G4 P.1',
                    'G0 X95 Y85',
                    'M3 S1',
                    'G4 P.1',
                    'G1 F1500 X125 Y55',
                    'M3 S0',
                    'G4 P.1',]
    elif position == '3':
        comms = ['G0 X135 Y55',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X165 Y85',
					'M3 S0',
					'G4 P.1',
					'G0 X135 Y85',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X165 Y55',
					'M3 S0',
					'G4 P.1',]
    elif position == '4':
        comms = [
					'G0 X55 Y95',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X85 Y125',
					'M3 S0',
					'G4 P.1',
					'G0 X55 Y125',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X85 Y95',
					'M3 S0',
					'G4 P.1',]
    elif position == '5':
        comms = ['G0 X95 Y95',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X125 Y125',
					'M3 S0',
					'G4 P.1',
					'G0 X95 Y125',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X125 Y95',
					'M3 S0',
					'G4 P.1',
        ]
    elif position == '6':
        comms = ['G0 X135 Y95',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X165 Y125',
					'M3 S0',
					'G4 P.1',
					'G0 X135 Y125',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X165 Y95',
					'M3 S0',
					'G4 P.1',]
    elif position == '7':
        comms = ['G0 X55 Y135',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X85 Y165',
					'M3 S0',
					'G4 P.1',
					'G0 X55 Y165',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X85 Y135',
					'M3 S0',
					'G4 P.1',]
    elif position == '8':
        comms = ['G0 X95 Y135',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X125 Y165',
					'M3 S0',
					'G4 P.1',
					'G0 X95 Y165',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X125 Y135',
					'M3 S0',
					'G4 P.1',]
    elif position == '9':
        comms = ['G0 X135 Y135',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X165 Y165',
					'M3 S0',
					'G4 P.1',
					'G0 X135 Y165',
					'M3 S1',
					'G4 P.1',
					'G1 F1500 X165 Y135',
					'M3 S0',
					'G4 P.1',]

    for c in comms:
        run_command(c)


def draw_o(position):
    comms = []
    if position == '1':
        comms = ['G0 X55 Y70',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X55 Y70 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25 ',]
    elif position == '2':
        comms = ['G0 X95 Y70',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X95 Y70 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25 ',]
    elif position == '3':
        comms = ['G0 X135 Y70',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X135 Y70 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25 ',]
    elif position == '4':
        comms = ['G0 X55 Y110',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X55 Y110 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25 ',]
    elif position == '5':
        comms = ['G0 X95 Y110',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X95 Y110 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25 ',]
    elif position == '6':
        comms = ['G0 X135 Y110',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X135 Y110 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25',]
    elif position == '7':
        comms = ['G0 X55 Y150',
					'M3 S1 ',
					'G4 P0.25',
					'G2 X55 Y150 I15 J0 F1500',
					'M3 S0 ',
					'G4 P0.25 ',]
    elif position == '8':
        comms = [
            'G0 X95 Y150',
            'M3 S1 ',
            'G4 P0.25',
            'G2 X95 Y150 I15 J0 F1500',
            'M3 S0 ',
            'G4 P0.25 ',
        ]
    elif position == '9':
        comms = [
            'G0 X135 Y150',
            'M3 S1',
            'G4 P0.25',
            'G2 X135 Y150 I15 J0 F1500',
            'M3 S0 ',
            'G4 P0.25',
        ]

    for c in comms:
        run_command(c)


def draw_field():
    comms = [		'M3 S0'
					'G0 X50 Y50',
					'M3 S1',
					'G4 P0.25',
					'G1 X50 Y170 F1500',
					'G1 X170 Y170 F1500',
					'G1 X170 Y50 F1500',
					'G1 X48 Y50 F1500',
					'M3 S0',
					'G4 P0.25',
					'G0 X90 Y50',
					'M3 S1',
					'G4 P0.25',
					'G1 X90 Y170 F1500',
					'M3 S0',
					'G4 P0.25',
					'G0 X130 Y170',
					'M3 S1',
					'G4 P0.25',
					'G1 X130 Y50 F1500',
					'M3 S0',
					'G4 P0.25',
					'G0 X50 Y90',
					'M3 S1',
					'G4 P0.25',
					'G1 X170 Y90 F1500',
					'M3 S0',
					'G4 P0.25',
					'G0 X170 Y130',
					'M3 S1',
					'G4 P0.25',
					'G1 X50 Y130 F1500',
					'M3 S0',
					'G4 P0.25',
					'G0 X0 Y0',]
    for c in comms:
        run_command(c)

def draw_row(n):
    n=int(n)
    run_command(f'G0 X{70+(n-1)*40} Y50')
    run_command(f'M3 S1')
    run_command(f'G4 P0.25')
    run_command(f'G1 X{70+(n-1)*40} Y170 F1500')
    run_command(f'M3 S0')
    run_command(f'G4 P0.25')
    run_command('G0 X0 Y0')

def draw_col(n):
    n=int(n)
    run_command(f'G0 X50 Y{75+(n-1)*40}')
    run_command(f'M3 S1')
    run_command(f'G4 P0.25')
    run_command(f'G1 X170 Y{75+(n-1)*40} F1500')
    run_command(f'M3 S0')
    run_command(f'G4 P0.25')
    run_command('G0 X0 Y0')

def draw_diagonal(n):
    if n == '1':
        run_command(f'G0 X60 Y60')
        run_command(f'M3 S1')
        run_command(f'G4 P0.25')
        run_command(f'G1 X160 Y160 F1500')
        run_command(f'M3 S0')
        run_command(f'G4 P0.25')
        run_command('G0 X0 Y0')
    elif n == '2':
        run_command(f'G0 X160 Y60')
        run_command(f'M3 S1')
        run_command(f'G4 P0.25')
        run_command(f'G1 X60 Y160 F1500')
        run_command(f'M3 S0')
        run_command(f'G4 P0.25')
        run_command('G0 X0 Y0')

for line in config:
    run_command(line)

what_to_draw = sys.argv[2]

if what_to_draw == 'field':
    draw_field()
elif what_to_draw == 'x' or what_to_draw == 'X':
    pos = sys.argv[3]
    draw_x(pos)
elif what_to_draw == 'o' or what_to_draw == 'O':
    pos = sys.argv[3]
    draw_o(pos)
elif what_to_draw == 'row':
    pos = sys.argv[3]
    draw_row(pos)
elif what_to_draw == 'col':
    pos = sys.argv[3]
    draw_col(pos)
elif what_to_draw == 'diagonal':
    pos = sys.argv[3]
    draw_diagonal(pos)

run_command('G0 Y0')
run_command('G0 X0')
# Close file and serial port
s.close()
