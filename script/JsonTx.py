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


# simple definition of json structure (see example below)

class JsonTxIn:
	def __init__(self, _address, _hashPrevOut, _indexPrevOut, _value):
		self.address = _address # get this value later by readdressing
		self.hashPrevOut = _hashPrevOut
		self.indexPrevOut = _indexPrevOut
		self.value = _value # get this value later by readdressing

class JsonTxOut:
	def __init__(self, _address, _indexOut, _value):
		self.address = _address
		self.indexOut = _indexOut
		self.value = _value

class JsonTx:

	def __init__(self, _exchange_rate, _timestamp, _total_value, _tx_ins, _tx_outs, _txid):
		self.exchange_rate = _exchange_rate # get this value later from market data
		self.timestamp = _timestamp # get this field from block
		self.total_value = _total_value
		self.tx_ins = _tx_ins
		self.tx_outs = _tx_outs
		self.txid = _txid



# EXAMPLE OF A JSON TRANSACTION

# {
# 	"exchange_rate": "NO_X_RATE",
# 	"timestamp": 1231731025,
# 	"total_value": 5000000000,
# 	"tx_ins": [
# 		{
# 			"address": "NO_ADDRESS",
# 			"hashPrevOut": "0x0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9",
# 			"indexPrevOut": 0,
# 			"value": 5000000000
# 		}
# 	],
# 	"tx_outs": [
# 		{
# 			"address": "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
# 			"indexOut": 0,
# 			"value": 1000000000
# 		},
# 		{
# 			"address": "12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S",
# 			"indexOut": 0,
# 			"value": 4000000000
# 		}
# 	],
# 	"txid": "0xf4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"
# }