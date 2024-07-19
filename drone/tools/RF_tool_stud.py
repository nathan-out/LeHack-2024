#!/usr/bin/env python3
#===================================================
#  Hardsploit API - By Opale Security
#  www.opale-security.com || www.hardsploit.io
#  License: GNU General Public License v3
#  License URI: http://www.gnu.org/licenses/gpl.txt
#===================================================

from sys import argv
import time
import threading
import cmd
import signal
from enum import Enum

from hardsploit.core import HardsploitAPI, HardsploitError, HardsploitUtils
from hardsploit.modules import NRF24L01EmuXN297

class XN297:

    # xn297 scramble table
    SCRAMBLE = (
        0xE3, 0xB1, 0x4B, 0xEA, 0x85, 0xBC, 0xE5, 0x66,
        0x0D, 0xAE, 0x8C, 0x88, 0x12, 0x69, 0xEE, 0x1F,
        0xC7, 0x62, 0x97, 0xD5, 0x0B, 0x79, 0xCA, 0xCC,
        0x1B, 0x5D, 0x19, 0x10, 0x24, 0xD3, 0xDC, 0x3F,
        0x8E, 0xC5, 0x2F, 0xAA, 0x16, 0xF3, 0x95 )
           
    # scrambled, standard mode crc xorout table
    CRC_XOROUT_SCRAMBLED = (
        0x0000, 0x3448, 0x9BA7, 0x8BBB, 0x85E1, 0x3E8C,
        0x451E, 0x18E6, 0x6B24, 0xE7AB, 0x3828, 0x814B,
        0xD461, 0xF494, 0x2503, 0x691D, 0xFE8B, 0x9BA7,
        0x8B17, 0x2920, 0x8B5F, 0x61B1, 0xD391, 0x7401,
        0x2138, 0x129F, 0xB3A0, 0x2988, 0x23CA, 0xC0CB,
        0x0C6C, 0xB329, 0xA0A1, 0x0A16, 0xA9D0 )

    _ADDR_SIZE = 5

    _PREAMBLE = [0x71, 0x0F, 0x55]

    _PAIRING_ADDR = [0x01, 0x01, 0x01, 0x01, 0x06]

    _IS_CRC = 0

class PAYLOAD:
    def __init__(self, name, addr, payload):
        self.name = name
        self.addr = addr
        self.payload = payload

class CLI(cmd.Cmd):

    prompt = ">>>"
    intro = """
|====================================================================|
|Hardsploit RF attack tool designed to emulated XN297 with NRF24L01  |
|====================================================================|
|CTRL D to quit                                                      |
|CTRL C to stop a command                                            |
|                                                                    |
|chan  [channel min] [channel max]                                   |
|sniff [channel]                                                     |
|craft [name] [address] [payload]                                    |
|spoof [name] [channel] [number of repeats]                          |
|disp                                                                |
|help  [command]                                                     |
|====================================================================|
    """


    def do_chan(self, arg):
        
        """chan [int : channel min] [int : channel max]\n
        Scan selected frequency band and returns active channels
        The channel corresponds to the offset in MHz added to 2.4GHz
        Channel values : [0..126]"""
        global running
        try:
            cmin, cmax = map(int, arg.split())
        except ValueError:
            print("chan [int : channel min] [int : channel max]")
            return
        if not 1 < cmax < 127 or cmin >= cmax :
            print("Channel must be less than 126, with cmin < cmax")
            return

        print(f"Scanning channels from {cmin} to {cmax} :")

        for channel in range(cmin,cmax):
            nrf.change_channel(channel)
            nrf.set_tx_rx_mode(NRF24L01EmuXN297.TXRX_OFF)
            nrf.set_tx_rx_mode(NRF24L01EmuXN297.RX_EN)
            nrf.flush_rx()
            
            timeoutValue = 1
            timeBegin = time.time()
            running = True
            while running:
                if time.time() - timeBegin > timeoutValue:
                    print(f"Channel {channel} ..." )
                    break
                data = nrf.read()
                if len(data) > 0:
                    print(f"Valid data found on channel {channel}")
                    break
            if not running:
                break

    def do_sniff(self, arg):
        """sniff [int : channel]\n
        Sniff data on selected channel
        Address is 5 bytes in hexadecimal, separated with comma
        Address is optionnal : if not mentionned, the sniffer will return all packets regardless of the address"""
        global running
        try:
            chan, addr = arg.split() + ["all"]*(2-len(arg.split())) #if addr not present, assign to default value 
            chan = int(chan)
        except ValueError:
            print("Wrong parameters : sniff [channel] [address (opt) : format : AA,BB,CC,DD,EE]")
            return
        if not 1 < chan < 127 :
            print("Channel must be less than 0x126")
            return
        if addr != "all":
            try:
                addr = getIntList(addr)
                if len(addr)!=5:
                    raise ValueError
            except ValueError:
                print("str[5] : address (opt), format : AA,BB,CC,DD,EE")
                return

        print(f"Sniffing payload on channel {chan}, addr = {addr} :")
        nrf.change_channel(chan)
        nrf.write_reg(NRF24L01EmuXN297._11_RX_PW_P0, 10 + XN297._ADDR_SIZE)
        nrf.set_tx_rx_mode(NRF24L01EmuXN297.TXRX_OFF)
        nrf.set_tx_rx_mode(NRF24L01EmuXN297.RX_EN)
        nrf.flush_rx()
        print("   CHANNEL    |    ADDRESS     |            PAYLOAD            ")
        print("==============================================================")
        running = True
        while running:
            data = nrf.read()
            if len(data) > 0:
                procData = getProcessedRxData(data)
                if addr == "all" or getIntList(addr) == procData[0]:
                   printRxData(chan, procData)        

                
    def do_craft(self, arg):
        
        """craft [str : name] [str[5] : address, format : AA,BB,CC,DD,EE] [str[] : payload]\n
        Craft your custom packet
        Address is 5 bytes in hexadecimal, separated with comma
        Payload follows the same format with a maximum of 32 bytes
        Crafting a packet with an existing name will modify the old packet"""
        global global_payload_dict
        try:
            name, addr, payload = arg.split()
            intAddr, intPayload = getIntList(addr), getIntList(payload)
        except ValueError:
            print("Wrong parameters :\ncraft [str : name] [str[5] : address, format : AA,BB,CC,DD,EE] [str[] : payload]")
            return
        if len(intAddr) != 5:
            print("\r\x1b[31mWrong parameters :\x1b[0m\nAddress size should be 5")
            return
        global_payload_dict.update({name : [intAddr, intPayload]})
        print(f"{name} packet crafted :")
        print("  NAME     |    ADDRESS     |        PAYLOAD        ")
        print("===========================================================")
        print(f"{name} {' ' * (10 - len(name))}| {getHexString(intAddr)} | {getHexString(intPayload)}")

    def do_disp(self, line):
        """disp
        Display all saved packets"""
        global global_payload_list
        if global_payload_dict:
            print("  NAME     |    ADDRESS     |        PAYLOAD        ")
            print("===========================================================")
            for name, packet in global_payload_dict.items():
                print(f"{name} {' ' * (10 - len(name))}| {getHexString(packet[0])} | {getHexString(packet[1])}")
        else :
            print("No packets crafted, please use craft command")


    def do_spoof(self, arg):
        """    spoof [str : name] [int : channel] [int : number of repeats]\n
        Send crafted packets to selected channel n times"""
        global global_payload_dict
        global running
        try:
            name, chan, repeats = arg.split()
            chan, repeats = int(chan), int(repeats)
        except ValueError:           
            print("\r\x1b[31mWrong parameters :\x1b[0m\nspoof [str : name] [int : channel] [int : number of repeats]")
            return
        if not 1 < chan < 127 :
            print("Channel must be less than 126")
            return
        nrf.change_channel(chan)
        nrf.set_tx_rx_mode(NRF24L01EmuXN297.TXRX_OFF)
        nrf.set_tx_rx_mode(NRF24L01EmuXN297.TX_EN)
        nrf.flush_tx()
        try :
            addr, payload = global_payload_dict.get(name)
        except:
            print(f"{name} is not a valid packet name. disp to display crafted packets")
            return
        print(f"{repeats} {name} packets sending on channel {chan}")
        print("   CHANNEL    |    ADDRESS     |            PAYLOAD            ")
        print("==============================================================")
        i = 0
        running = True
        while running and i < repeats:
            sendPacket(chan, addr, payload)
            printTxData(chan, [addr, payload])
            i = i+1

    def complete_spoof(self, text, line, begidx, endidx):
        global global_payload_dict
        if not text:
            completions = [ f
                            for f in global_payload_dict.keys()
                            ]
        else:
            completions = [ f
                            for f in global_payload_dict.keys()
                            if f.startswith(text)
                            ]
        return completions

    def do_EOF(self, line):
        return True

def exit_loop(signal, frame):
    global running
    running = False

#################  Hardsploit  ###################


def callbackProgress(percent, startTime, endTime):
    print(f"\r\x1b[31mUpload of FPGA firmware in progress : {percent}%\x1b[0m")


#################  Utils  ###################


def bitReverse(data):
    reversedData = data[:]
    for i in range(len(data)):
        binbyte = format(data[i], '08b')
        reversedData[i] = int(binbyte[::-1], 2)
    return reversedData

def byteReverse(data):
    copy = data[:]
    copy.reverse()
    return copy


def getHexString(intArray, isValidCRC = True):
    hexArray = ['{:02X}'.format(i) for i in intArray]
    hexString = ' '.join(hexArray)
    if not isValidCRC :
        hexString = "\033[0;31m" + hexString + "\033[0m"
    return hexString

def getIntList(hex_str):
    hex_values = hex_str.split(",")
    int_list = [int(value, 16) for value in hex_values]
    return int_list

#################  RX  ###################


def setRxAddress(address):
    if (3 <= len(address) <= 5):
        return nrf.write_reg_multi(NRF24L01EmuXN297._0A_RX_ADDR_P0, address)
    else :
        raise ValueError("Address must be 3, 4 or 5 bytes long")

def getProcessedRxData(data):

    slicedData = [data[:XN297._ADDR_SIZE],data[XN297._ADDR_SIZE:]]
    scAddress = slicedData[0]
    scPayload = slicedData[1]

    usAddress = getScrambled(scAddress, 0)
    usPayload = getScrambled(scPayload, XN297._ADDR_SIZE)

    revAddress = byteReverse(usAddress)
    revPayload = bitReverse(usPayload)

    return [revAddress, revPayload]

def printRxData(channel,procData):
    address, payload = procData
    """
    if not isValidCRC:
        localCRCString = getHexString(localCRC) + " |"
    else :
        localCRCString = ""
    """
    print(f"<--Channel {channel} | {getHexString(address)} | {getHexString(payload)} ")
    


#################  TX  ###################

def setTxAddress(address):
    if (3 <= len(address) <= 5):
        return nrf.write_reg_multi(NRF24L01EmuXN297._10_TX_ADDR, address)
    else :
        raise ValueError("Address must be 3, 4 or 5 bytes long")

def printTxData(channel,procData):
    address, payload = procData 
    print(f"<--Channel {channel} | {getHexString(address)} | {getHexString(payload)}") 

def getProcessedTxData(address, payload):
    revAddress = byteReverse(address)
    revPayload = bitReverse(payload)

    scAddress = getScrambled(revAddress, 0)
    scPayload = getScrambled(revPayload, XN297._ADDR_SIZE)

    return [scAddress, scPayload]

def sendPacket(chan, addr, payload):
    packet = getProcessedTxData(addr, payload)     
    nrf.send(packet[0] + packet[1])
    time.sleep(0.011)


#################  Scrambling ###################


def getScrambled(scData, offset):
    dataLength = len(scData)
    usData = scData[:]
    for i in range(dataLength):
        usData[i] = scData[i] ^ XN297.SCRAMBLE[i + offset]
    return usData



###################################################################################
##################################  MAIN  #########################################
###################################################################################


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_loop)
    
    print(f"Number of hardsploit detected :{HardsploitUtils.getNumberOfBoardAvailable()}")

    HardsploitAPI.callbackProgress = callbackProgress

    hardsploit = HardsploitAPI()
    hardsploit.getAllVersions()

    if len(argv) <= 1 or argv[1] != "nofirmware":
        hardsploit.loadFirmware("SPI")

    # HARDSPLOIT                    NRF24L01
    # SPI_CLK   (pin A0)      ===>    SCK
    # SPI_CS    (pin A1)      ===>    CSN
    # SPI_MOSI  (pin A2)      ===>    MOSI
    # SPI_MISO  (pin A3)      ===>    MISO
    # SPI_PULSE (pin A4)      ===>    CE

    try:
        nrf = NRF24L01EmuXN297(hardsploit)
        if nrf.reset():
            nrf.init_drone() # generic config
        else:
            raise RuntimeError("NRF24L01 not found")
    except HardsploitError.HARDSPLOIT_NOT_FOUND:
        print("[!] Hardsploit not found")
    except HardsploitError.USB_ERROR:
        print("[!] USB Error")

    nrf.write_reg(NRF24L01EmuXN297._03_SETUP_AW, 0x01)
    setRxAddress(byteReverse(XN297._PREAMBLE))
    setTxAddress(byteReverse(XN297._PREAMBLE))
    

    global_payload_dict = dict()

    CLI().cmdloop()
