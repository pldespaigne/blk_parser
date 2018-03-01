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

def printLegal():
	print()
	print('blk_parser  Copyright (C) 2018  DESPAIGNE Pierre-Louis')
	print()
	print('This program comes with ABSOLUTELY NO WARRANTY.')
	print('This is free software, and you are welcome to redistribute it under certain conditions.')
	print('For details read the LICENSE.txt file or visit <http://www.gnu.org/licenses/>')
	print()

def intToHexString(val, invert=True, swap=True):
	temp_hex = list(str(hex(val)))
	temp_hex = temp_hex[2:]#delete the '0x' at the begining
	if invert: temp_hex = temp_hex[::-1]#invert string ('hello'-> 'olleh')
	if swap:
		i = 0#swap char 2 by 2 ('abcdef' -> 'badcfe')
		while i < len(temp_hex)-1:
			a = temp_hex[i]
			b = temp_hex[i+1]
			temp_hex[i] = b
			temp_hex[i+1] = a
			i += 2
	res = ''.join(temp_hex)
	return '0x'+res

def printHexScript(script):
	res = ''
	i = 2
	while i < len(script) - 1:
		a = script[i]
		b = script[i+1]

		# constants
		if(a + b == '00') : res += ' OP_FALSE '
		# TODO add pushdata 01-4b
		elif(a == '0' or a == '1' or a == '2' or a == '3'):
			i+=2
			strHex = '0x' + a + b
			intValue = int(strHex, 16)
			res += ' PUSHDATA('+str(intValue)+') '
			j = 0
			while j < intValue * 2:
				res += script[i+j]
				j += 1
			i += j - 2
		elif(a + b == '40' or a + b == '41' or a + b == '42' or a + b == '43'):
			i+=2
			strHex = '0x' + a + b
			intValue = int(strHex, 16)
			res += ' PUSHDATA('+str(intValue)+') '
			j = 0
			while j < intValue * 2:
				res += script[i+j]
				j += 1
			i += j - 2
		elif(a + b == '44' or a + b == '45' or a + b == '46' or a + b == '47'):
			i+=2
			strHex = '0x' + a + b
			intValue = int(strHex, 16)
			res += ' PUSHDATA('+str(intValue)+') '
			j = 0
			while j < intValue * 2:
				res += script[i+j]
				j += 1
			i += j - 2
		elif(a + b == '48' or a + b == '49' or a + b == '4a' or a + b == '4b'):
			i+=2
			strHex = '0x' + a + b
			intValue = int(strHex, 16)
			res += ' PUSHDATA('+str(intValue)+') '
			j = 0
			while j < intValue * 2:
				res += script[i+j]
				j += 1
			i += j - 2
		elif(a + b == '4c') : res += ' OP_PUSHDATA1 '
		elif(a + b == '4d') : res += ' OP_PUSHDATA2 '
		elif(a + b == '4e') : res += ' OP_PUSHDATA4 '
		elif(a + b == '4f') : res += ' OP_1NEGATE '
		elif(a + b == '51') : res += ' OP_TRUE '
		# TODO 52-60
		# flow control
		elif(a + b == '61') : res += ' OP_NOP '
		elif(a + b == '63') : res += ' OP_IF '
		elif(a + b == '64') : res += ' OP_NOTIF '
		elif(a + b == '67') : res += ' OP_ELSE '
		elif(a + b == '68') : res += ' OP_ENDIF '
		elif(a + b == '69') : res += ' OP_VERIFY '
		elif(a + b == '6a') : res += ' OP_RETURN '
		#stack
		elif(a + b == '6b') : res += ' OP_TOTALSTACK '
		elif(a + b == '6c') : res += ' OP_FROMALTSTACK '
		elif(a + b == '73') : res += ' OP_IFDUP '
		elif(a + b == '74') : res += ' OP_DEPTH '
		elif(a + b == '75') : res += ' OP_DROP '
		elif(a + b == '76') : res += ' OP_DUP '
		elif(a + b == '77') : res += ' OP_NIP '
		elif(a + b == '78') : res += ' OP_OVER '
		elif(a + b == '79') : res += ' OP_PICK '
		elif(a + b == '7a') : res += ' OP_ROLL '
		elif(a + b == '7b') : res += ' OP_ROT '
		elif(a + b == '7c') : res += ' OP_SWAP '
		elif(a + b == '7d') : res += ' OP_TUCK '
		elif(a + b == '6d') : res += ' OP_2DROP '
		elif(a + b == '6e') : res += ' OP_2DUP '
		elif(a + b == '6f') : res += ' OP_3DUP '
		elif(a + b == '70') : res += ' OP_2OVER '
		elif(a + b == '71') : res += ' OP_2ROT '
		elif(a + b == '72') : res += ' OP_2SWAP '
		#splice
		elif(a + b == '7e') : res += ' OP_CAT* '# * = disable
		elif(a + b == '7f') : res += ' OP_SUBSTR* '
		elif(a + b == '80') : res += ' OP_LEFT* '
		elif(a + b == '81') : res += ' OP_RIGHT* '
		elif(a + b == '82') : res += ' OP_SIZE '
		#bitwise logic
		elif(a + b == '83') : res += ' OP_INVERT* '
		elif(a + b == '84') : res += ' OP_AND* '
		elif(a + b == '85') : res += ' OP_OR* '
		elif(a + b == '86') : res += ' OP_XOR* '
		elif(a + b == '87') : res += ' OP_EQUAL '
		elif(a + b == '88') : res += ' OP_EQUALVERIFY '
		#arithmetic
		elif(a + b == '8b') : res += ' OP_1ADD '
		elif(a + b == '8c') : res += ' OP_1SUB '
		elif(a + b == '8d') : res += ' OP_2MUL* '
		elif(a + b == '8e') : res += ' OP_2DIV* '
		elif(a + b == '8f') : res += ' OP_NEGATE '
		elif(a + b == '90') : res += ' OP_ABS '
		elif(a + b == '91') : res += ' OP_NOT '
		elif(a + b == '92') : res += ' OP_0NOTEQUAL '
		elif(a + b == '93') : res += ' OP_ADD '
		elif(a + b == '94') : res += ' OP_SUB '
		elif(a + b == '95') : res += ' OP_MUL* '
		elif(a + b == '96') : res += ' OP_DIV* '
		elif(a + b == '97') : res += ' OP_MOD* '
		elif(a + b == '98') : res += ' OP_LSHIFT* '
		elif(a + b == '99') : res += ' OP_RSHIFT* '
		elif(a + b == '9a') : res += ' OP_BOOLAND '
		elif(a + b == '9b') : res += ' OP_BOOLOR '
		elif(a + b == '9c') : res += ' OP_NUMEQUAL '
		elif(a + b == '9d') : res += ' OP_NUMEQUALVERIFY '
		elif(a + b == '9e') : res += ' OP_NUMNOTEQUAL '
		elif(a + b == '9f') : res += ' OP_LESSTHAN '
		elif(a + b == 'a0') : res += ' OP_GREATERTHAN '
		elif(a + b == 'a1') : res += ' OP_LESSTHANOREQUAL '
		elif(a + b == 'a2') : res += ' OP_GREATERTHANOREQUAL '
		elif(a + b == 'a3') : res += ' OP_MIN '
		elif(a + b == 'a4') : res += ' OP_MAX '
		elif(a + b == 'a5') : res += ' OP_WITHIN '
		#crypto
		elif(a + b == 'a6') : res += ' OP_RIPEMD160 '
		elif(a + b == 'a7') : res += ' OP_SHA1 '
		elif(a + b == 'a8') : res += ' OP_SHA256 '
		elif(a + b == 'a9') : res += ' OP_HASH160 '
		elif(a + b == 'aa') : res += ' OP_HASH256 '
		elif(a + b == 'ab') : res += ' OP_CODESEPARATOR '
		elif(a + b == 'ac') : res += ' OP_CHECKSIG '
		elif(a + b == 'ad') : res += ' OP_CHECKSIGVERIFY '
		elif(a + b == 'ae') : res += ' OP_CHECKMULTISIG '
		elif(a + b == 'af') : res += ' OP_CHECKMULTISIGVERIFY '
		#locktime
		elif(a + b == 'b1') : res += ' OP_CHECKLOCKTIMEVERIFY '
		elif(a + b == 'b2') : res += ' OP_CHECKSEQUENCEVERIFY '
		#pseudo words
		elif(a + b == 'fd') : res += ' OP_PUBKEYHASH '
		elif(a + b == 'fe') : res += ' OP_PUBKEY '
		elif(a + b == 'ff') : res += ' OP_INVALIDOPCODE '
		#reserved words
		elif(a + b == '50') : res += ' OP_RESERVED '
		elif(a + b == '62') : res += ' OP_VER '
		elif(a + b == '65') : res += ' OP_VERIF '
		elif(a + b == '66') : res += ' OP_VERNOTIF '
		elif(a + b == '89') : res += ' OP_RESERVED1 '
		elif(a + b == '8a') : res += ' OP_RESERVED2 '
		elif(a + b == 'b0') : res += ' OP_NOP1 '
		elif(a + b == 'b3') : res += ' OP_NOP4 '
		elif(a + b == 'b4') : res += ' OP_NOP5 '
		elif(a + b == 'b5') : res += ' OP_NOP6 '
		elif(a + b == 'b6') : res += ' OP_NOP7 '
		elif(a + b == 'b7') : res += ' OP_NOP8 '
		elif(a + b == 'b8') : res += ' OP_NOP9 '
		elif(a + b == 'b9') : res += ' OP_NOP910 '

		else : res += a + b

		i +=2
	return res