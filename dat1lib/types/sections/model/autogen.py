# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class x00823787_Section(dat1lib.types.sections.Section):
	TAG = 0x00823787
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 20 occurrences in 38298 files
		# size = 4
		#
		# examples: 8401B7F8A3E0B9EA

		# MM
		# 5 occurrences in 37147 files
		# size = 4
		#
		# examples: 8401B7F8A3E0B9EA

		# RCRA
		# 1 occurrence in 11387 files
		# size = 4
		#
		# examples: B96A7BCD7B18CD03
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "00823787 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 00823787     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x14D8B13C_Section(dat1lib.types.sections.Section):
	TAG = 0x14D8B13C
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 14976
		#
		# examples: 98E675D6ADB2647B

		# MM: none
		# RCRA: none
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "14D8B13C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 14D8B13C     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x27CA5246_Section(dat1lib.types.sections.Section):
	TAG = 0x27CA5246
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 31 occurrences in 38298 files
		# size = 9084..770184 (avg = 315614.7)
		#
		# examples: 858060AD687726AF (min size), 9870FFAD9BAF955A (max size)

		# MM
		# 22 occurrences in 37147 files
		# size = 6780..552492 (avg = 216997.0)
		#
		# examples: B9375A5CB8F67F59 (min size), AE2EF67016D7F15D (max size)

		# RCRA
		# 32 occurrences in 11387 files
		# size = 11580..144132 (avg = 39973.5)
		#
		# examples: B058D14A4867F1DC (min size), ADE5909F821E9DDE (max size)

		# occurs with 3C9DABDF, B25B3163 and BB7303D5 (hero-related?)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "27CA5246 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 27CA5246     | {:6} entries".format(self.TAG, len(self.entries)))

#

class ModelSplineSubsetsSection(dat1lib.types.sections.Section):
	TAG = 0x3C9DABDF # Model Spline Subsets
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 31 occurrences in 38298 files
		# size = 2512..15072 (avg = 8386.8)
		#
		# examples: 858060AD687726AF (min size), 857EF55F37F5BDCF (max size)

		# MM
		# 22 occurrences in 37147 files
		# size = 1256..13816 (avg = 5652.0)
		#
		# examples: B900A23DAB6FC4E5 (min size), 90B61AD0494B91C9 (max size)

		# RCRA
		# 32 occurrences in 11387 files
		# size = 1256..10048 (avg = 4121.2)
		#
		# examples: B058D14A4867F1DC (min size), 93E189C6F48429E9 (max size)

		# occurs with 27CA5246, B25B3163 and BB7303D5 (hero-related?)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Model Spline Subsets ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Spline Sbsts | {:6} entries".format(self.TAG, len(self.entries)))

#

class x5A39FAB7_Section(dat1lib.types.sections.Section):
	TAG = 0x5A39FAB7
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 558 occurrences in 8780 files
		# size = 32..544 (avg = 90.8)
		#
		# examples: 00B7CEF1 (min size), 165E0270 (max size)

		# MSMR
		# 64 occurrences in 38298 files
		# size = 38..1414 (avg = 388.9)
		#
		# examples: 8A9C0AD7B6F3BBF4 (min size), 8C00E8BCEACF88E5 (max size)

		# MM
		# 67 occurrences in 37147 files
		# size = 36..1206 (avg = 308.8)
		#
		# examples: A1069ACB1E139D38 (min size), 9D359A612792272C (max size)

		# RCRA
		# 7 occurrences in 11387 files
		# size = 83..198 (avg = 119.1)
		#
		# examples: 9AB50DD637FCB81C (min size), 857A448B59682A9D (max size)
		pass

	def get_short_suffix(self):
		return "5A39FAB7 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5A39FAB7     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class x5240C82B_Section(dat1lib.types.sections.Section):
	TAG = 0x5240C82B # Model Skin Joint Remap
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 2 occurrences in 8780 files
		# size = 2794..6014 (avg = 4404.0)
		#
		# examples: 4C49135A (min size), 7E3E18BC (max size)

		# MSMR
		# 77 occurrences in 38298 files
		# size = 256..14816 (avg = 4554.5)
		#
		# examples: AA3C0092DD64C101 (min size), BB6E44C6B57852B0 (max size)

		# MM
		# 57 occurrences in 37147 files
		# size = 352..24432 (avg = 4961.2)
		#
		# examples: 8934293C3B736C99 (min size), 8DDE07945B10DDB3 (max size)

		# RCRA
		# 7 occurrences in 11387 files
		# size = 48..17606 (avg = 4947.7)
		#
		# examples: 81816E860EDFD542 (min size), 9DBD177615255CDC (max size)
		pass

	def get_short_suffix(self):
		return "5240C82B ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5240C82B     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class xBCE86B01_Section(dat1lib.types.sections.Section):
	TAG = 0xBCE86B01
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 124 occurrences in 38298 files
		# size = 32..352 (avg = 51.8)
		#
		# examples: 80B239C44ED6722A (min size), AFD77FCE52114B83 (max size)

		# MM
		# 1079 occurrences in 37147 files
		# size = 32..256 (avg = 58.9)
		#
		# examples: 80B239C44ED6722A (min size), 843E29054D67A0C9 (max size)

		# RCRA
		# 22 occurrences in 11387 files
		# size = 32..96 (avg = 62.5)
		#
		# examples: 9D59C7A0B7E53396 (min size), 8EE15CCA7C59D9E7 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BCE86B01 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BCE86B01     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x5D5CF541_Section(dat1lib.types.sections.Section):
	TAG = 0x5D5CF541
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 14976
		#
		# examples: 98E675D6ADB2647B

		# MM: none
		# RCRA: none
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "5D5CF541 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5D5CF541     | {:6} entries".format(self.TAG, len(self.entries)))
#

class x855275D7_Section(dat1lib.types.sections.Section):
	TAG = 0x855275D7
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 157 occurrences in 38298 files
		# size = 64..412 (avg = 227.9)
		#
		# examples: A2107CD6FA00E037 (min size), AB6E2F9441080649 (max size)

		# MM
		# 125 occurrences in 37147 files
		# size = 52..412 (avg = 239.5)
		#
		# examples: 88502C6A9234D319 (min size), 852550BEA67DB69C (max size)

		# RCRA
		# 3 occurrences in 11387 files
		# size = 52
		#
		# examples: 8FDFEE4F0DE15B03
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "855275D7 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 855275D7     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x8A84E4D6_Section(dat1lib.types.sections.Section):
	TAG = 0x8A84E4D6
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 157 occurrences in 38298 files
		# size = 60..109008 (avg = 10777.9)
		#
		# examples: A2107CD6FA00E037 (min size), 86B8B887A2871FCA (max size)

		# MM
		# 119 occurrences in 37147 files
		# size = 7782..80396 (avg = 11192.3)
		#
		# examples: 88C590C09F485410 (min size), 9C60BD754686CCD0 (max size)

		# RCRA
		# 3 occurrences in 11387 files
		# size = 3038..173126 (avg = 79947.3)
		#
		# examples: A34022B94277F04C (min size), 9C5362B8A9CC9A48 (max size)
		pass

	def get_short_suffix(self):
		return "8A84E4D6 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 8A84E4D6     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class xADD1CBD3_Section(dat1lib.types.sections.Section):
	TAG = 0xADD1CBD3
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3 occurrences in 38298 files
		# size = 704..2720 (avg = 2048.0)
		#
		# examples: AF3AC54D239CD584 (min size), A296B03EFEBF937A (max size)

		# MM
		# 8 occurrences in 37147 files
		# size = 272..7376 (avg = 2014.0)
		#
		# examples: A5C689C1931043C1 (min size), 947DA54544D4B270 (max size)

		# RCRA
		# 20 occurrences in 11387 files
		# size = 512..27312 (avg = 4854.4)
		#
		# examples: B18E53297CBFE008 (min size), 9BA94D1544DB197D (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "ADD1CBD3 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ADD1CBD3     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xB25B3163_Section(dat1lib.types.sections.Section):
	TAG = 0xB25B3163
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 31 occurrences in 38298 files
		# size = 47296..7250416 (avg = 2263386.3)
		#
		# examples: 858060AD687726AF (min size), B29BA0754ACB0151 (max size)

		# MM
		# 22 occurrences in 37147 files
		# size = 37416..2160024 (avg = 1281548.3)
		#
		# examples: AFF1551441CECF20 (min size), 90B61AD0494B91C9 (max size)

		# RCRA
		# 32 occurrences in 11387 files
		# size = 41280..821080 (avg = 181088.5)
		#
		# examples: 82B59DE522052F6E (min size), ADE5909F821E9DDE (max size)

		# occurs with 27CA5246, 3C9DABDF and BB7303D5 (hero-related?)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "B25B3163 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B25B3163     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xCD903318_Section(dat1lib.types.sections.Section):
	TAG = 0xCD903318
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 5 occurrences in 38298 files
		# size = 68..232 (avg = 131.6)
		#
		# examples: A2107CD6FA00E037 (min size), 857EF55F37F5BDCF (max size)

		# MM
		# 116 occurrences in 37147 files
		# size = 66..192 (avg = 103.6)
		#
		# examples: 88502C6A9234D319 (min size), 857EF55F37F5BDCF (max size)

		# RCRA
		# 3 occurrences in 11387 files
		# size = 68
		#
		# examples: 8FDFEE4F0DE15B03
		pass

	def get_short_suffix(self):
		return "CD903318 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | CD903318     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class xBB7303D5_Section(dat1lib.types.sections.Section):
	TAG = 0xBB7303D5
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 31 occurrences in 38298 files
		# size = 6056..513456 (avg = 210409.8)
		#
		# examples: 858060AD687726AF (min size), 9870FFAD9BAF955A (max size)

		# MM
		# 22 occurrences in 37147 files
		# size = 4520..368328 (avg = 144664.7)
		#
		# examples: B9375A5CB8F67F59 (min size), AE2EF67016D7F15D (max size)

		# RCRA
		# 32 occurrences in 11387 files
		# size = 7720..96088 (avg = 26649.0)
		#
		# examples: B058D14A4867F1DC (min size), ADE5909F821E9DDE (max size)

		# occurs with 27CA5246, 3C9DABDF and B25B3163 (hero-related?)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BB7303D5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BB7303D5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x244E5823_Section(dat1lib.types.sections.Section):
	TAG = 0x244E5823
	TYPE = 'Model2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# MM
		# 7 occurrences in 37147 files
		# size = 7817536..21428704 (avg = 16584059.4)
		#
		# examples: BCD67D43B36CFC72 (min size), B55DDB974D9B893D (max size)

		# RCRA: none
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "244E5823 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 244E5823     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x42349A17_Section(dat1lib.types.sections.Section):
	TAG = 0x42349A17
	TYPE = 'Model2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# MM
		# 7 occurrences in 37147 files
		# size = 457196..925444 (avg = 719911.4)
		#
		# examples: BCD67D43B36CFC72 (min size), A6E98A5F0D076856 (max size)

		# RCRA: none
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "42349A17 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 42349A17     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x665DA362_Section(dat1lib.types.sections.Section):
	TAG = 0x665DA362
	TYPE = 'Model2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# MM
		# 5 occurrences in 37147 files
		# size = 8..16 (avg = 9.6)
		#
		# examples: 91F969BBCAC9B677 (min size), 8B8CEB2BD47457F3 (max size)

		# RCRA
		# 371 occurrences in 11387 files
		# size = 8..16 (avg = 8.6)
		#
		# examples: 80103711336A7261 (min size), 8003870B38BB24C5 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "665DA362 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 665DA362     | {:6} entries".format(self.TAG, len(self.entries)))
