#ITER CODAC PLC SPSS s7Async reverse
#55.C4 DTS Ioffe inst

import binascii
from calendar import month
import datetime
from encodings import utf_8
from msvcrt import kbhit
from re import M
import socket
import struct
import sys
import time

PLC_IP = '172.16.19.220'

#DateTime BCD for CubMon variant
def bcd2int (bcd):
    return  (bcd&0xF) + (bcd>>4)*10

def revbit(x):
    return ((x & 0x00FF) << 8) | (x >> 8)

#CODAC receive States and send Config packets
def codac_stateconf(ss): 
    rcv_data = ss.recv(1024)
    if rcv_data:
        print('stat rcv ok: ', end='')

    #rcv_data = s.recv(1024).decode('UTF-8', errors='ignore');

    print("|%x| "    % struct.unpack('>I',   rcv_data[0:4]),  end='') #FixPattern Header int=49315840
    print(" len=%d " % struct.unpack('>H' ,  rcv_data[4:6]),  end='') #FixPattern Header int=49315840, Length,
    print(" ver=%s " % (rcv_data[8:24]).decode('UTF-8', errors='ignore'), end='') #IF version, skip 2b simatic
    print(" ac=%d "  % struct.unpack('>H'  , rcv_data[48:50]),end='') #AliveCounter
        
    ddd = struct.unpack('>BBBBBBB',rcv_data[50:57])                   #Date_And_Time BCD
    print( datetime.datetime(2000+bcd2int(ddd[0]),bcd2int(ddd[1]),bcd2int(ddd[2]),\
                             bcd2int(ddd[3]),bcd2int(ddd[4]),bcd2int(ddd[5]),ddd[6]), end='')

    print(" <%d> " % struct.unpack('>H',rcv_data[58:60]), end='')     #PayLoad
    print(" |%x| " % struct.unpack('>I',rcv_data[60:64]))             #FixPattern Footer int=4245651455
        
    msg = struct.pack('>hi2cfhibbI16s',i,456,b'v',b'k',8.12,0x321,0x7654,22,1,0x1234,b'vovka eat kids!')
    #print ('msg: ', binascii.hexlify(msg, '.'))
    msg = struct.pack('>H',i)
    if ss.send(msg):
        print ('cfg send ok : <%d>' % i)

#CODAC send command packet
def codac_command(sc):
    msg = struct.pack('>4B', i&0x01, (i&0x02)>>1, (i&0x04)>>2, (i&0x08)>>3)
    if sc.send(msg):
        print ('cmnd send ok:', msg)

#receive States and send Config packets
def codac_event(se): 
    rcv_data = se.recv(1024)
    if rcv_data:
        print('event rcv ok: ', end='')

    print("|%x| " % struct.unpack('>I',rcv_data[0:4]), end='') #FixPattern Header int=49315840
    ddd = struct.unpack('>BBBBBBB',rcv_data[4:11])                        #Date_And_Time BCD
    print( datetime.datetime(2000+bcd2int(ddd[0]),bcd2int(ddd[1]),bcd2int(ddd[2]),\
                             bcd2int(ddd[3]),bcd2int(ddd[4]),bcd2int(ddd[5]),ddd[6]), end='')       
    print(" fc=%d " % struct.unpack('>H',rcv_data[12:14]), end='')
    print(format(revbit(rcv_data[14]),'08b')+"'", end='')  #payload
    print(format(revbit(rcv_data[15]),'08b'), end='')  #payload
    print(" len=%d " % struct.unpack('>H',rcv_data[16:18]), end='') #len
    print(" |%x| " % struct.unpack('>I',rcv_data[20:24]))           #FixPattern Footer int=4245651455

#main cycle
def codac_conn(ss,sc,se):
    global i
    i=100
    while i:
        print (f'#{i}')
        codac_stateconf(ss)
        codac_command  (sc)
        codac_event    (se)

        i=i-1
        time.sleep(5)

#CODAC PLC open three soscets
if __name__ == "__main__":
    print('CODAC PLC SPSS protocol test, 55C4, Ioffe inst., Russia')

    ss = socket.socket()
    ss.connect((PLC_IP, 2000))
 
    sc = socket.socket()
    sc.connect((PLC_IP, 2001))

    se = socket.socket()
    se.connect((PLC_IP, 2002))

    codac_conn(ss,sc,se)

    ss.close()
    sc.close()
    se.close()

    #-=EOF=-

#    sock_rcv()

#server side socket
def sock_rcv():
    print('ip_sock_rcv')
    s = socket.socket()
    s.bind('172.16.19.55', 12344)
    s.listen(5)
    while True:
        r, addr = s.accept()
        print("conn {}".format(str(addr)))
        rcv_data = ''
        while (rcv_data != 'ex' ):
            rcv_data = r.recv(1024).decode('UTF-8', errors='ignore');
            print(rcv_data)
        r.sendall(b'fuk u!')
        r.close()
        print("discon {}".format(str(addr)))

