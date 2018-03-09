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

class JsonTxIn:
	def __init__(self, _hashPrevOut, _indexPrevOut, _value):
		self.address = 'NO_ADDRESS' # complete this field later with second script pass
		self.hashPrevOut = _hashPrevOut
		self.indexPrevOut = _indexPrevOut
		self.value = _value

class JsonTxOut:
	def __init__(self, _address, _indexOut, _value):
		self.address = _address
		self.indexOut = _indexOut
		self.value = _value

class JsonTx:

	def __init__(self, _timestamp, _total_value, _tx_ins, _tx_outs, _txid):
		self.exchange_rate = 'NO_X_RATE' # get this value later from market data
		self.timestamp = _timestamp # get this field from block
		self.total_value = _total_value
		self.tx_ins = _tx_ins
		self.tx_outs = _tx_outs
		self.txid = _txid