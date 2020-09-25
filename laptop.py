#!/usr/bin/python
'''
Author: Filippo Falezza, <filippo dot falezza at outlook dot it>
Released under Gpl v3 ¢2020

System requirements:
isw (by YoyPa)
#intel-undervolt (not yet)

'''
import sys
from numpy import array
from os import system
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import argparse

PRG_NAME = 'Fan and Cpu Interface Tool'
TURBO_STATE = '/sys/devices/system/cpu/intel_pstate/no_turbo'
ISW_NAME = '16S3EMS1'
VERSION = '0.0.1'

###TODO
# needs sudo permissions to run, could implement some udev(?) rules to avoid this.
# graphical interface
# make this as a library to have it run on the graphical (Qt5(?)) interfacegparse.


class cpu:
	def turbo(string):
		# Option --silent, enables passive mode
		if string == '1' or '0':
			with open(TURBO_STATE,'w') as file:
				file.write(string)
				file.close()
		else:
			print("Value must be 0 or 1")


#why the hell thhe undervolt function is executed twice???
	def undervolt(string):
##Decided to use sys.argv for now, it's simpler to debug:
###TODO switch to argparse to manage arguments
#		print(type(string))
#		arg_ = list()
#		for element in string.split():
#			arg_.append(element)
		sys_types = ["cpu", "igpu", "cache", "agent", "analog", "digital"]
		subsys = None
		if sys.argv[2] in sys_types:
			subsys = (sys_types.index(sys.argv[2]))
			print(subsys) ###DBG
		else: raise ValueError
		try:
			uv_value = int(sys.argv[3])
			print(int(sys.argv[3])) ###DBG
		except ValueError:
			print("wrong value")
			return 1
		##DEBUG
		print(sys.argv)
#		print("args[]", args[:])
#		print("args", args)
#		print("susbsys", subsys)
		
		sys_value = format(0xFFE00000&( (round(uv_value*1.024)&0xFFF) <<21), '08x') #given on 'https://github.com/mihic/linux-intel-undervolt'
		print(sys_value) ###DBG
		print("wrmsr 0x150 0x80000%s11%s" %(subsys,sys_value)) ###DBG
		system("wrmsr 0x150 0x80000%s11%s" %(subsys,sys_value))
		
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
	parser = ArgumentParser(prog=PRG_NAME, formatter_class = RawTextHelpFormatter,
		description='Tool to manage CPU and Fan settings. Currently works only on a MSI P15\
		A10SC. Still under heavy development and in need of improvements')
	parser.add_argument('-t', type = cpu.turbo, action = "store", 
		help = 'no_turbo settings,\n' ' 1 to disable turbo, 0 to allow it\n')
	parser.add_argument('-u', type = cpu.undervolt, nargs = 2,
		help = "undervolt cpu")
	parser.add_argument('-f', type = fan.off, help = 'fans')
	parser.add_argument('-v', action = 'version', version = '%s version %s' %(PRG_NAME,VERSION),
						help = 'Show current version')
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
	args=parser.parse_args()

if __name__ == '__main__':
	main()

