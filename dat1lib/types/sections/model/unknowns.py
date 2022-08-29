import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class x7CA37DA0_Entry(object):
	def __init__(self, data):
		self.unknowns = struct.unpack("<" + "I"*12, data)

class x7CA37DA0_Section(dat1lib.types.sections.Section):
	TAG = 0x7CA37DA0
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 48
		count = len(data)//ENTRY_SIZE
		self.entries = [x7CA37DA0_Entry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} structs".format(self.TAG, len(self.entries))

###

class x811902D7_Section(dat1lib.types.sections.Section):
	TAG = 0x811902D7
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		size1, = struct.unpack("<I", data[:4])
		self.uints = utils.read_struct_N_array_data(data[4:], size1/4 - 1, "<I")

		size2 = len(data) - size1
		self.shorts = utils.read_struct_N_array_data(data[size1:], size2/2, "<H") # includes indexes ranges where indexes go from 0 to N, where N is amount of quintuples from 0x0AD3A708

	def get_short_suffix(self):
		return "? ({}, {})".format(len(self.uints), len(self.shorts))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} uints \t {:6} shorts".format(self.TAG, len(self.uints), len(self.shorts))

###

class xDCC88A19_Section(dat1lib.types.sections.Section):
	TAG = 0xDCC88A19
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.vectors = [struct.unpack("<ffff", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "vectors? ({})".format(len(self.vectors))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Vectors?     | {:6} vectors".format(self.TAG, len(self.vectors))

###

class xDF9FDF12_Section(dat1lib.types.sections.Section):
	TAG = 0xDF9FDF12
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		# (0, 70, 0, 2)

	def get_short_suffix(self):
		return "0-70-0-2? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0-70-0-2?    | {:6} tuples".format(self.TAG, len(self.entries))

###

class xB7380E8C_Section(dat1lib.types.sections.Section):
	TAG = 0xB7380E8C
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# some unique numbers from 0, but with some gaps
		# for example, 146 numbers from 0 up to 220
		self.indexes = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "indexes? ({})".format(len(self.indexes))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Some Indexes | {:6} indexes".format(self.TAG, len(self.indexes))

###

class xC5354B60_Section(dat1lib.types.sections.Section): # aka model_mirror_ids
	TAG = 0xC5354B60
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# some offset-like numbers in "mostly" increasing order
		# (sometimes value returns back to a smaller number and continues to increase)
		self.offsets = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "offsets? ({})".format(len(self.offsets))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Some Offsets | {:6} offsets".format(self.TAG, len(self.offsets))

###

class x283D0383_Section(dat1lib.types.sections.Section): # aka model_built
	TAG = 0x283D0383
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 0x283D0383 seems to be some model info that has things like bounding box and global model scaling?
		# (global scaling is that number that is likely 0.00024. Int vertex positions are converted to floats and multiplied by this.
		self.values = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "model_built? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | model_built? | {:6} shorts".format(self.TAG, len(self.values))

###

class x3250BB80_Section(dat1lib.types.sections.Section): # aka model_material
	TAG = 0x3250BB80
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data) // 2 // ENTRY_SIZE
		self.string_offsets = [struct.unpack("<QQ", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]		

		ENTRY_SIZE = 16
		data2 = data[count * ENTRY_SIZE:]
		self.quadruples = [struct.unpack("<IIII", data2[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		# ?, ?, ?, 0

	def get_short_suffix(self):
		return "materials ({})".format(len(self.quadruples))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Materials    | {:6} materials".format(self.TAG, len(self.quadruples))

		for i, q in enumerate(self.quadruples):
			matfile = self._dat1.get_string(self.string_offsets[i][0])
			matname = self._dat1.get_string(self.string_offsets[i][1])

			print ""
			print "  - {:<2}  {}".format(i, matfile)
			print "        {}".format(matname)
			print "        {:08X}  {:08X}  {:08X}  {}".format(q[0], q[1], q[2], q[3])
		print ""

"""
typedef struct
{
    uint hash;
    uint unk04; // increasing small number
    int parent; // -1 if none
    uint unk0C; // always 0
    float m3x4[12];
        // 1 0 0
        // 0 1 0
        // 0 0 1
        // 0 0 0
} LocatorDefinition;

typedef struct
{
    float x,y,z,w;
} Vector4f <read=ReadVector4f>;

string ReadVector4f(Vector4f& v)
{
    string s;
    SPrintf(s, "(%1.3f %1.3f %1.3f %1.3f)", v.x, v.y, v.z, v.w);
    return s;
}

///

    // model_look
    if (tag == 0x6EB7EFC)
    {
        local uint count = size / 2;
        SPrintf(name, "model_look (%d shorts)", count);
        short values[count] <bgcolor=cLtPurple>;
    }
    // Index buffer
    else if (tag == INDEXBUF_SECTION)
    {
        local uint count = size / 2;
        SPrintf(name, "Index Buf (%d indexes)", count);

        // Indices are weird in that instead of storing the indices directly, the indices are instead delta encoded.
        // that is, each index is a sum of the current "delta index" and all the prior delta indices.
        // For example, the true i(3) is actually di(0) + di(1) + di(2) + di(3).
        short deltaIndexes[count] <bgcolor=cLtGreen>;
    }

    else if (tag == 0x0AD3A708)
    {
        // local uint count = size / 4;
        uint count <bgcolor=cLtPurple>;
        uint unkU04 <bgcolor=cLtPurple>;
        uint unkU08 <bgcolor=cLtPurple>;
        uint unkU0C <bgcolor=cLtPurple>;

        SPrintf(name, "0AD3A708 (%d quintuples)", count);

        typedef struct
        {
            uint unk00;
            uint unk04;
            uint unk08;
            uint unk0C;
            uint offsetLike; // small, increasing by powers of 2 (I've seen 512, 128 or 64)
        } Quintuple;

        Quintuple quintuples[count] <bgcolor=cLtPurple>;
        
        // uint values[count] <bgcolor=cLtPurple>;
    }

    // model_joint
    else if (tag == 0x15DF9D3B)
    {
        local uint count = size / 16;
        SPrintf(name, "model_joint (%d structs)", count);

        typedef struct
        {
            short parent; // -1
            short index;
            short unkS04; // some other index? usually 0, but sometimes some other small value (less than count of joints, if I'm not mistaken)
            short unkS06; // size?
            uint hash;
            uint offset; // increasing in some non-regular increments, starts non-zero
        } Joint;

        Joint joints[count] <bgcolor=cLtPurple>;
    }

    // ?
    else if (tag == 0x380A5744)
    {
        uint unk[16] <bgcolor=cLtPurple>;

        typedef struct
        {
            uint unkU00;
            int unkU04; // offset-like
        } UnknownPair;

        local uint count = 0;
        local uint end = offset + size + modelOffset;
        while (FTell() < end) {
            ++count;
            UnknownPair pair <bgcolor=cDkPurple>;
            if (pair.unkU04 == -1) break;
        }

        typedef struct
        {
            uint unkU00;
            uint unkU04; // not offset-like
        } UnknownPair2;

        local uint count2 = 0;
        while (FTell() < end) {
            ++count2;
            UnknownPair2 pair2 <bgcolor=cLtPurple>;
            if (pair2.unkU04 == (uint)-1) break;
        }

        local uint count3 = 0;
        if (FTell() < end) {
            count3 = (end - FTell())/4;
            uint rest[count3] <bgcolor=cDkPurple>;
        }

        SPrintf(name, "380A5744 (%d pairs, %d pairs, %d uints)", count, count2, count3);
    }

    // ?
    else if (tag == 0x6B855EED)
    {
        // 6B855EED has the same byte size as 5CBA9DE9
        // 6B855EED looks like a bunch of uints, 5CBA9DE9 has a lot of 0s
        local uint count = size / 4;
        SPrintf(name, "6B855EED (%d uints)", count);
        uint values[count] <bgcolor=cLtPurple>;
    }

    // Not really figured out; seems to have a lot of matrices. Maybe bone related?
    else if (tag == 0x707F1B58)
    {
        SPrintf(name, "Matrixes?");
        uint unkU00; // always 16?
        uint sectionSize;
        uint count1;
        uint count2;
        float rest[sectionSize / 4 - 5];
        uint count3;
        if (size > sectionSize) {
            short indexes[(size - sectionSize)/2]; // unicode strings with \n??? (ends with \n\n)
        }
    }

    // Not really figured out; Vertexes data
    else if (tag == VERTEXES_SECTION)
    {
        /*
        local uint count = size / 16;
        SPrintf(name, "Vertexes (%d verts)", count);
        VertexOld vertexes[count];
        */

        // seems to be the vertex data densely packed as shorts
        SPrintf(name, "Vertexes? (%d shorts)", size/2);
        short vertexData[size / 2];
    }
    // Not really figured out; "model_skin_batch"
    else if (tag == 0xC61B1FF5)
    {
        uint unkU00;
        uint unkU04;
        uint unkU08;
        uint sectionSize;

        typedef struct
        {
            uint realOffsetLike;
            uint unkU04; // == 0
            short unkU08; // == 0
            short uncompressedSizeLike;
            short compressedSizeLike;
            short compressedOffsetLike;
        } SkinRelated;

        SkinRelated rest[(size - 16) / 16];
        SPrintf(name, "model_skin_batch? (%d items)", (size-16)/16);
    }
"""
