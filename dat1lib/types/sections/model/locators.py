import dat1lib.types.sections
import io
import struct

class LocatorsMapSection(dat1lib.types.sections.UintUintMapSection): # aka model_locator_lookup
	TAG = 0x731CBC2E
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.UintUintMapSection.__init__(self, data, container)

	def get_short_suffix(self):
		return "locators map ({})".format(len(self._map))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Locators Map | {:6} locators".format(self.TAG, len(self._map))

"""

    // Some locator-related pairs
    else if (tag == 0x9A434B29)
    {
        typedef struct
        {
            uint unk00;
            uint unk04;
        } LocatorPair;

        local uint count = (size - 16) / 8;
        SPrintf(name, "Locator-related? (%d items)", count);
        uint sectionSize;
        uint unkU04; // always 32?
        uint unkU08; // small
        uint unkU0C; // small, approx. *2 of unkU08
        LocatorPair rest[count];
    }
    // List of locator definitions
    else if (tag == LOCATORS_SECTION)
    {
        local uint count = size / 64;
        SPrintf(name, "Locator Defs (%d items)", count);
        LocatorDefinition locators[count];
    }

"""
