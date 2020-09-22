#!/usr/bin/python
'''
Author: Filippo Falezza, <filippo dot falezza at outlook dot it>
Released under Gpl v3 ¢2020

System requirements:
isw (by YoyPa)
#intel-undervolt (not yet)

'''
import sys
from os import system
import argparse

PRG_NAME = 'Fan and Cpu Interface Tool'
TURBO_STATE = '/sys/devices/system/cpu/intel_pstate/no_turbo'
ISW_NAME = '16S3EMS1'
VERSION = '0.0.1'

class cpu:
    def turbo(string):
        # Option --silent, enables passive mode
        if string == '1' or '0':
            with open(TURBO_STATE,'w') as file:
                file.write(string)
                file.close()
        else:
            print("Value must be 0 or 1")

    ###TODO
    ###Add stuff to manage pkg power and undervolt

class fan:
    def off(string):
        # Option -f
        system("cp /etc/isw.conf.passive /etc/isw.conf && isw -w %s" %(ISW_NAME))
    
    ###TODO Add def fan.on function, to be called by "PRGNAME fan on" and fan of by "PRGNAME fan off"
    ###Could make it independent of isw...
    ###Should add stuff to manage max frequency of N cores using corefreqd or directly Instruction Registers

def main():
    #read input from command line, then execute the appropriate functions
    parser = argparse.ArgumentParser(prog=PRG_NAME, formatter_class = argparse.RawTextHelpFormatter,
                                     description='Tool to manage CPU and Fan settings. Currently works only on a MSI P15 A10SC. Still under heavy development and in need of improovements')
    parser.add_argument('-t', type = cpu.turbo, 
        action = "store", help = 'no_turbo settings,\n'
                                 '    1 to disable turbo, 0 to allow it\n')
    parser.add_argument('-f', type = fan.off,
        help = 'fans')
    parser.add_argument('-v', action = 'version', version = '%s version %s' %(PRG_NAME,VERSION),
                        help = 'Show current version')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
    parser.parse_args()

if __name__ == '__main__':
    main()

