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

def unknownCommand(command):
		print('Unknown command :', command)
		printHelp()

def printLegal():
	print()
	print('blk_parser  Copyright (C) 2018  DESPAIGNE Pierre-Louis')
	print()
	print('This program comes with ABSOLUTELY NO WARRANTY.')
	print('This is free software, and you are welcome to redistribute it under certain conditions.')
	print('For details read the LICENSE.txt file or visit <http://www.gnu.org/licenses/>')
	print()

def printHelp():
	print('-- Help --')
	print('help : show this message')
	print('quit : quit blk_parser')
	print('index <PATH> : build index from the blk file pointed in <PATH>')
	print('show [block] <VALUE> : print an object, ex: > show block 42')
	print()