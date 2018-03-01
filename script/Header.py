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

import Util

class Header:
	def __init__(self, bytes_header):
		bytes_version = bytes_header[:4]
		bytes_rest = bytes_header[4:]

		bytes_prev_block_id = bytes_rest[:32]
		bytes_rest = bytes_rest[32:]

		bytes_merkle_root = bytes_rest[:32]
		bytes_rest = bytes_rest[32:]

		bytes_time = bytes_rest[:4]
		bytes_rest = bytes_rest[4:]

		bytes_bits = bytes_rest[:4]
		bytes_rest = bytes_rest[4:]

		bytes_nonce = bytes_rest

		self.version = int.from_bytes(bytes_version, byteorder='little')

		self.prev_block_id = Util.intToHexString(int.from_bytes(bytes_prev_block_id, byteorder='big'))

		self.merkle_root = Util.intToHexString(int.from_bytes(bytes_merkle_root, byteorder='big'), False, False)
		self.time = int.from_bytes(bytes_time, byteorder='little')
		self.bits = int.from_bytes(bytes_bits, byteorder='little')
		self.nonce = int.from_bytes(bytes_nonce, byteorder='little')

	def print(self):
		print('Header :')
		print('       version', self.version)

		# print('       >', hex(self.prev_block_id))
		print('       id du block precedent', self.prev_block_id)

		print('       merkle root', self.merkle_root)
		print('       time', self.time)
		print('       bits', self.bits)
		print('       nonce', self.nonce)