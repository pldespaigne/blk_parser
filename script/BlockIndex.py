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

class BlockIndex:

	def __init__(self, _path):
		self.path = _path
		self.size = 0
		self.byte_index = []
		self.block_size = []

	def appendBlock(self, _byte_index, _block_size):
		self.byte_index.append(_byte_index)
		self.block_size.append(_block_size)
		self.size += 1

	def print(self):
		for i in range(0, self.size):
			print('block', i, 'starting at', self.byte_index[i], 'with a size of', self.block_size[i], 'byte(s)')