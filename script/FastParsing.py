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

import JsonTx

def jsonDefault(obj):
	if isinstance(obj, set): return list(obj)
	return obj.__dict__

def parse(path, block_index, tx_index):

	print('Parsing tx to JSON file', path, '. . .')
	time_start = time.time()

	with open(path, 'w') as json_file:

		with open(block_index.path, 'rb') as block_file:

			tx_ins = []
			tx_outs = []

			in_prev_hash = []
			in_prev_index = []
			in_value = []

			out_address = []
			out_index = []
			out_value = []

			for i in range(0, len(tx_index.byte_index)):
				# clearing
				tx_ins.clear()
				tx_outs.clear()

				in_prev_hash.clear()
				in_prev_index.clear()
				in_value.clear()

				out_address.clear()
				out_value.clear()

				# parsing

				tx_timestamp = 1472603865
				tx_total_value = 16498824
				tx_id = '996204358e3d73996167623dfa1ac82806bbbf8cb8ad53aeb4aa2546b076e840'

				in_prev_hash.append('6dbc7f680e9bfdf28c88fba7cd3e75a7efc74d9728793c1e9736b1ab086b5299')
				in_prev_index.append(0)
				in_value.append(16528824)

				out_address.append('1dtS6Snh4r5U4tZGxKnhEL3GsP99FSm1w')
				out_index.append(0)
				out_value.append(14898235)

				######### NO_RELEASE
				out_address.append('1PcgGm4yyYovt4pwnCo47R89yycLvab8En')
				out_index.append(1)
				out_value.append(1600589)
				##############

				for ins in range(0, len(in_value)):
					tx_ins.append(JsonTx.JsonTxIn(in_prev_hash[ins], in_prev_index[ins], in_value[ins]))
				for outs in range(0, len(out_value)):
					tx_outs.append(JsonTx.JsonTxOut(out_address[outs], out_index[outs], out_value[outs]))
				tx = JsonTx.JsonTx(tx_timestamp, tx_total_value, tx_ins, tx_outs, tx_id)

				json_file.write(json.dumps(tx, default=jsonDefault) + '\n')

		block_file.closed # close the file

	json_file.closed # close the file
	time_end = time.time()
	print('end of parsing in', time_end - time_start, 's')
