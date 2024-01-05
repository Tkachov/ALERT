import dat1lib
import dat1lib.crc32 as crc32
#import dat1lib.types.nodegraph
import dat1lib.types.autogen
import dat1lib.types.sections.nodegraph.guessed
import json
import sys

DEBUG = True

def fix_array_field(j, field):
	if field not in j:
		j[field] = []
	else:
		if not isinstance(j[field], list):
			j[field] = [j[field]]
	return j

def fix_ids(j, node_mappings):
	if isinstance(j, list):
		return [fix_ids(x, node_mappings) for x in j]

	if isinstance(j, dict):
		for k in j:
			if k in ["Id", "SourceNodeId", "SourcePlugId", "TargetNodeId", "TargetPlugId"]:
				node_id = j[k]
				if node_id not in node_mappings:
					if DEBUG:
						print(f"[!] 0x{node_id:016x} was not found in mappings")
						found = False
						for k2 in node_mappings:
							if node_mappings[k2] == node_id:
								found = True
								print(f"\tbut it's found in mappings originals")
					continue

				node_id = node_mappings[node_id]
				node_id = f"0x{node_id:016x}"
				j[k] = node_id

			else:
				j[k] = fix_ids(j[k], node_mappings)

	return j

def reconstruct(asset):
	header = asset.dat1.get_section(dat1lib.types.sections.nodegraph.guessed.HeaderSection.TAG)
	graph_type_hash = header.root["GraphTypeHash"]
	graph_type_hashes = { # crc32.hash(x, False)
		0x1E213EA9: "MissionGraphGameDef"
	}

	#

	mappings = asset.dat1.get_section(dat1lib.types.sections.nodegraph.guessed.MappingsSection.TAG)
	j = mappings.root
	j = fix_array_field(j, "OriginalAssets")
	j = fix_array_field(j, "IdMappings")

	assets_count = len(j["OriginalAssets"])
	if DEBUG:
		if assets_count != 1:
			print(f"[!] OriginalAssets count == {assets_count} (expected == 1)")

	orig_assets = set()
	orig_graphs = set()
	for mapping in j["IdMappings"]:
		orig_assets.add(mapping["OriginalAssetId"])
		orig_graphs.add(mapping["OriginalEmbeddedGraphId"])

	if DEBUG:
		if len(orig_assets) != 1:
			print(f"[!] different OriginalAssetId count == {len(orig_assets)} (expected == 1)")
		if len(orig_assets) != assets_count:
			print(f"[!] different OriginalAssetId count == {len(orig_assets)} (expected to be equal to OriginalAssets == {assets_count})")

		if len(orig_graphs) != 1:
			print(f"[!] different OriginalEmbeddedGraphId count == {len(orig_graphs)} (expected == 1)")
		if 0xFFFFFFFFFFFFFFFF not in orig_graphs:
			print(f"[!] none of the OriginalEmbeddedGraphId == 0xffffffffffffffff")

	node_mappings = {}
	for mapping in j["IdMappings"]:
		if mapping["OriginalEmbeddedGraphId"] != 0xFFFFFFFFFFFFFFFF: # TODO: these probably turn into `"SubGraphs": {}`
			continue

		node_mappings[mapping["FlattenedId"]] = mapping["OriginalId"]

	#

	graph_node = {
		"Id": "0xffffffffffffffff",
		"Type": "kNodeGraph"
	}

	#

	known_field_names = ["AndNodes", "Comments", "DebugChainEndNodes", "DebugChainStartNodes", "EndArcNodes", "InitNode", "MissionNodes", "OrNodes", "StartArcNodes"]
	field_name_hashes = {crc32.hash(x, False): x for x in known_field_names}

	nodes_list = asset.dat1.get_section(dat1lib.types.sections.nodegraph.guessed.NodesListSection.TAG)
	for n in nodes_list.root["Nodes"]:		
		field_name_hash = n["FieldNameHash"]
		field_name = field_name_hashes.get(field_name_hash, f"0x{field_name_hash:08x}")
		if field_name not in graph_node:
			graph_node[field_name] = {}

		node_hash = n["BuiltNodeDataBufferNameHash"]
		node_section = asset.dat1.get_section(node_hash)
		if node_section is None:
			if DEBUG:
				print(f"[!] {node_hash:08X} was not found")
			continue

		content = node_section.root
		content = fix_ids(content, node_mappings)
		node_id = content["Id"]
		graph_node[field_name][node_id] = content

	#

	graph_node["Connections"] = {}

	connections_list = asset.dat1.get_section(dat1lib.types.sections.nodegraph.guessed.ConnectionsSection.TAG)
	for c in connections_list.root["Connections"]:
		c = fix_ids(c, node_mappings)
		node_id = c["Id"]
		graph_node["Connections"][node_id] = c
		# TODO: maybe remove "Pins" from `c`? at least if == []
	
	#

	return {
		"NodeGraphCollection":
		{
			"MainGraph": graph_node,
			"Type": graph_type_hashes.get(graph_type_hash, f"0x{graph_type_hash:08x}")
		},
		"VaultMetaData":
		{
			"CreatedBy": "?",
			"LastModifiedBy": "?"
		},
		"Version": "1.1"
	}

def breaklines(j):
	result = ""
	for l in j.splitlines():
		if l.endswith(": {"):
			indent = 0
			for c in l:
				if c == ' ':
					indent += 1
				else:
					break

			result += l[:-2]
			result += "\n"
			result += " "*indent
			result += "{\n"
		else:
			result += l
			result += "\n"
	return result

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <filename>".format(argv[0]))
		print("")
		print("Reconstructs built .nodegraph into .json representation")
		return

	#

	fn = argv[1]
	asset = None
	try:
		with open(fn, "rb") as f:
			asset = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		return

	#
	
	if asset is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return

	if not isinstance(asset, dat1lib.types.autogen.NodeGraph):
		print("[!] Not a .nodegraph")
		return

	#

	nodegraph = reconstruct(asset)

	j = json.dumps(nodegraph, indent=2, sort_keys=True)
	j = breaklines(j)
	with open(fn + ".json", "w") as f:
		f.write(j)

if __name__ == "__main__":
	main(sys.argv)	
