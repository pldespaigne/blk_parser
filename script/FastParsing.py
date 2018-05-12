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

import time
import json
import hashlib

import Util
import JsonTx

def jsonDefault(obj):
	if isinstance(obj, set): return list(obj)
	return obj.__dict__

# more info on data structure here :
# Block 		: <https://en.bitcoin.it/wiki/Block>
# Block Header 	: <https://en.bitcoin.it/wiki/Block_hashing_algorithm>
# Transaction	: <https://en.bitcoin.it/wiki/Transaction>

def parse(path, block_index, tx_index):

	print('Parsing tx to JSON file', path, '. . .')
	time_start = time.time() # get starting time

	with open(path, 'w') as json_file: # open the output (json) file in writing mode

		with open(block_index.path, 'rb') as block_file: # open the input (.dat) file in reading binary mode

			tx_ins = []
			tx_outs = []

			in_prev_hash = []
			in_prev_index = []

			out_address = []
			out_index = []
			out_value = []

			current_block = -1

			for i in range(0, len(tx_index.byte_index)): # iterate over all the tx in the tx index
				# clearing
				tx_ins.clear()
				tx_outs.clear()

				in_prev_hash.clear()
				in_prev_index.clear()

				out_address.clear()
				out_value.clear()

				# parsing
				if current_block != tx_index.block_num[i]: # parsing timestamp (same timestamp for tx in the same block)
					current_block = tx_index.block_num[i]
					block_file.seek(block_index.byte_index[current_block] + 76) # magic num : 4, block size : 4, version : 4, previous hash : 32, merkle root : 32
					byte_time = block_file.read(4) # block timestamp : 4
					tx_timestamp = int.from_bytes(byte_time, byteorder='little')

				block_file.seek(tx_index.byte_index[i]) # parsing tx hash
				byte_tx = block_file.read(tx_index.tx_size[i])
				h_sha256 = hashlib.sha256()
				h_sha256.update(byte_tx)
				h_bytes = h_sha256.digest()
				h_sha256 = hashlib.sha256()
				h_sha256.update(h_bytes)
				tx_id_hash = h_sha256.hexdigest()
				tx_id = Util.formatHashString(tx_id_hash, True, True)
				if len(tx_id) != 66: print(tx_id_hash, tx_id)

				block_file.seek(tx_index.byte_index[i] + 4) # parsing number of tx inputs, tx version : 4
				byte_in_count = block_file.read(1) # reading the INPUT COUNT

				# check if varInt is on 1, 2, 4, or 8 bytes
				if(byte_in_count[0] == 253): # varInt is on 2 bytes AFTER the prefix
					byte_in_count = block_file.read(2)

				elif(byte_in_count[0] == 254): # varInt is on 4 bytes AFTER the prefix
					byte_in_count = block_file.read(4)

				elif(byte_in_count[0] == 255): # varInt is on 8 bytes AFTER the prefix
					byte_in_count = block_file.read(8)

				# else: # varInt was on 1 bytes, nothing to do

				in_count = int.from_bytes(byte_in_count, byteorder='little')
				ins = 0
				while ins < in_count:
					byte_hash = block_file.read(32) # previous tx hash : 32
					first_hash = hex(int.from_bytes(byte_hash, byteorder='big'))
					prev_hash = Util.formatPrevHashString(first_hash[2:], True, True)
					if(len(prev_hash) != 66 and len(prev_hash) != 2): print(byte_hash, first_hash, prev_hash)
					in_prev_hash.append(prev_hash)

					byte_prev_index = block_file.read(4) # previous tx index : 4
					prev_index = int.from_bytes(byte_prev_index, byteorder='little')
					in_prev_index.append(prev_index)

					byte_script_len = block_file.read(1) # reading the INPUT COUNT

					# check if varInt is on 1, 2, 4, or 8 bytes
					if(byte_script_len[0] == 253): # varInt is on 2 bytes AFTER the prefix
						byte_script_len = block_file.read(2)

					elif(byte_script_len[0] == 254): # varInt is on 4 bytes AFTER the prefix
						byte_script_len = block_file.read(4)

					elif(byte_script_len[0] == 255): # varInt is on 8 bytes AFTER the prefix
						byte_script_len = block_file.read(8)

					# else: # varInt was on 1 bytes, nothing to do

					script_len = int.from_bytes(byte_script_len, byteorder='little')
					block_file.read(script_len) # script : script_len
					block_file.read(4) # sequence : 4
					ins += 1

				byte_out_count = block_file.read(1) # reading the OUTPUT COUNT

				# check if varInt is on 1, 2, 4, or 8 bytes
				if(byte_out_count[0] == 253): # varInt is on 2 bytes AFTER the prefix
					byte_out_count = block_file.read(2)

				elif(byte_out_count[0] == 254): # varInt is on 4 bytes AFTER the prefix
					byte_out_count = block_file.read(4)

				elif(byte_out_count[0] == 255): # varInt is on 8 bytes AFTER the prefix
					byte_out_count = block_file.read(8)

				# else: # varInt was on 1 bytes, nothing to do

				out_count = int.from_bytes(byte_out_count, byteorder='little')
				outs = 0
				while outs < out_count:
					byte_value = block_file.read(8) # value : 8
					value = int.from_bytes(byte_value, byteorder='little')
					out_value.append(value)

					out_index.append(outs)

					byte_script_len = block_file.read(1) # reading the INPUT COUNT
					
					# check if varInt is on 1, 2, 4, or 8 bytes
					if(byte_script_len[0] == 253): # varInt is on 2 bytes AFTER the prefix
						byte_script_len = block_file.read(2)

					elif(byte_script_len[0] == 254): # varInt is on 4 bytes AFTER the prefix
						byte_script_len = block_file.read(4)

					elif(byte_script_len[0] == 255): # varInt is on 8 bytes AFTER the prefix
						byte_script_len = block_file.read(8)

					# else: # varInt was on 1 bytes, nothing to do

					script_len = int.from_bytes(byte_script_len, byteorder='little')
					byte_script = block_file.read(script_len) # script : script_len
					script = Util.intToHexString(int.from_bytes(byte_script, byteorder='big'), False, False)

					address_hex = Util.getDataFromHexStringScript(script)
					if(len(address_hex) == 130):
						address_hex = Util.pubKStringToAddress(address_hex)
					elif(len(address_hex) == 40):
						address_hex = Util.base58Check(address_hex)
					else:
						address_hex = 'UNABLE_TO_PARSE_ADDRESS'

					out_address.append(address_hex)
					outs += 1
				
				tx_total_value = 0
				for outs in range(0, len(out_value)):
					tx_total_value += out_value[outs] # sum of outs values

				for ins in range(0, len(in_prev_hash)):
					if in_prev_hash[ins] == '0x':
						tx_ins.append(JsonTx.JsonTxIn('MINING_REWARD', in_prev_hash[ins], -1, tx_total_value))
					elif len(in_prev_hash) == 1:
						tx_ins.append(JsonTx.JsonTxIn('NO_ADDRESS', in_prev_hash[ins], in_prev_index[ins], tx_total_value)) # if there is only 1 input its value is the total value of the tx
					else:
						if len(in_prev_hash[ins]) != 66: print(in_prev_hash[ins], len(in_prev_hash[ins]))
						tx_ins.append(JsonTx.JsonTxIn('NO_ADDRESS', in_prev_hash[ins], in_prev_index[ins], 'NO_VALUE'))
				for outs in range(0, len(out_value)):
					tx_outs.append(JsonTx.JsonTxOut(out_address[outs], out_index[outs], out_value[outs]))
				tx = JsonTx.JsonTx('NO_X_RATE', tx_timestamp, tx_total_value, tx_ins, tx_outs, tx_id)

				json_str = json.dumps(tx, default=jsonDefault)
				json_file.write(json_str + '\n')

		block_file.closed # close the file

	json_file.closed # close the file
	time_end = time.time()
	print('end of parsing in', time_end - time_start, 's')
