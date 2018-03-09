# Bitcoin blk_parser
# 
# A Python tool for parsing the blk files of the Bitcoin blockchain
# Wrote for college project at UCBL (University Lyon 1)
#
# Author : Pierre-Louis DESPAIGNE
# 
# Copyright (C) 2018  DESPAIGNE Pierre-Louis
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import time

import Cli
import Util
import FastParsing

from BlockIndex import BlockIndex
from TxIndex import TxIndex

Cli.printLegal()

running = True
block_index = None
tx_index = None
block = None
tx = None
input_file = '../data/blk00000.dat'
output_file = '../result/tx00000.json'

while running:
	command = input('blk_parser > ')
	command = command.split(' ')

	############################################################################
	if len(command) == 1:
		if command[0] == 'quit' or command[0] == 'quit()' or command[0] == 'q' or command[0] == 'exit' or command[0] == 'exit()':
			running = False
		elif command[0] == 'help' or command[0] == 'h' or command[0] == 'man':
			Cli.printHelp()
		else:
			Cli.unknownCommand(command)

	############################################################################
	elif len(command) == 2:
		if command[0] == 'index':
			if command[1] == 'block':
				block_index = BlockIndex(input_file)
			elif command[1] == 'tx':
				if block_index == None: block_index = BlockIndex(input_file)
				tx_index = TxIndex(block_index)
			else:
				Cli.unknownCommand(command)
		elif command[0] == 'input':
			input_file = command[1]
		elif command[0] == 'parse':
			if command[1] != 'd': output_file = command[1]
			if os.path.isfile(output_file):
				ans = input('The file will be overwritten, are you sure (Y/n) ?')
				if ans != 'Y': continue
			if block_index == None: block_index = BlockIndex(input_file)
			if tx_index == None: tx_index = TxIndex(block_index)
			FastParsing.parse(output_file, block_index, tx_index)
		else:
			Cli.unknownCommand(command)

	############################################################################
	elif len(command) == 3:
		if command[0] == 'show':
			if command[1] == 'block':
				if command[2] == 'index':
					if block_index == None: block_index = BlockIndex(input_file)
					block_index.print()
				else:
					if block_index == None: block_index = BlockIndex(input_file)
					i = int(command[2])
					block = block_index.parseBlock(i)
					block.print()
			elif command[1] == 'tx':
				if command[2] == 'index':
					if block_index == None: block_index = BlockIndex(input_file)
					if tx_index == None: tx_index = TxIndex(block_index)
					tx_index.print()
				else:
					if block_index == None: block_index = BlockIndex(input_file)
					if tx_index == None: tx_index = TxIndex(block_index)
					i = int(command[2])
					tx = tx_index.parseTx(i)
					tx.print()
			elif command[1] == 'input':
				if command[2] == 'file':
					print('input file :', input_file)
				else:
					Cli.unknownCommand(command)
			else:
				Cli.unknownCommand(command)
		else:
			Cli.unknownCommand(command)

	############################################################################
	else:
		Cli.unknownCommand(command)
	