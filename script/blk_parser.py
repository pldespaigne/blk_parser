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

from BlockIndex import BlockIndex

Cli.printLegal()

running = True
block_index = None
block = None

while running:
	command = input('blk_parser > ')
	command = command.split(' ')
	if len(command) == 1:
		if command[0] == 'quit' or command[0] == 'q' or command[0] == 'exit':
			running = False
		elif command[0] == 'help':
			Cli.printHelp()
		else:
			Cli.unknownCommand(command)

	elif len(command) == 2:
		if command[0] == 'index':
			# block_index = BlockIndex('../data/blk00000.dat')
			block_index = BlockIndex(command[1])

			# block42 = block_index.parseBlock(42)
			# block42.print()
		else:
			Cli.unknownCommand(command)
	elif len(command) == 3:
		if command[0] == 'show':
			if command[1] == 'block':
				i = int(command[2])
				block = block_index.parseBlock(i)
				block.print()
			else:
				Cli.unknownCommand(command)
		else:
			Cli.unknownCommand(command)
	else:
		Cli.unknownCommand(command)
	