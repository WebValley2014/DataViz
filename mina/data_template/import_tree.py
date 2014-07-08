import matplotlib
# matplotlib.use('Qt4Agg')
matplotlib.use('tkagg')

import ete2
from ete2 import Tree, TreeNode, TreeStyle
from ete2 import coretype

try:	
	from ete2 import faces
	from ete2 import AttrFace
	from ete2 import TreeStyle
	from ete2 import TextFace, NodeStyle, SVG_COLORS
except ImportError:
	pass


def tree_to_phyloxml (ete_tree):
	"""
	Convert an Ete2 tree to PhyloXML.

	:Parameters:
	ete_tree
	An Ete2 format tree

	:Returns:
	PhyloXML markup as text

	"""
	from cStringIO import StringIO
	buffer = StringIO()

	def visit_node (node, buf, indent=0):
		buf.write (" " * indent)
		buf.write ("<clade>\n")
		buf.write (" " * (indent+1))
		buf.write ("<name>%s</name>\n" % node.name )
		buf.write (" " * (indent+1))
		buf.write ("<branch_length>%s</branch_length>\n" % node.dist)
		buf.write (" " * (indent+1))
		buf.write ("<confidence type='branch_support'>%s</confidence>\n" % node.support)
		for c in node.get_children():
			visit_node(c, buf, indent=indent+1)
		buf.write (" " * indent)
		buf.write ("</clade>\n")

	buffer.write ("<phyloxml xmlns:phy='http://www.phyloxml.org/1.10/phyloxml.xsd'>\n")
	buffer.write ("<phylogeny>\n")
	# buffer.write ("<name>test_tree</name>\n")

	visit_node (ete_tree.get_tree_root(), buffer)

	buffer.write ("</phylogeny>\n")
	buffer.write ("</phyloxml>\n")

	return buffer.getvalue()
#

def search_by_name(node, name):
	matches = []
	for i in node.children:
		if i.name == name:
			# print i
			return i			
	return None
#


t = Tree()



filename = './PRE_ML/names.txt'
associations = {}
h = open(filename, 'r')
for i in h:
	i = i.strip()
	i = i.split("\t")
	j = i[1].split(";")
	current = t
	# associations[i[0]] = 
	for k in range(0,len(j)):
		# print k
		pos = search_by_name(current, j[k])
		if pos == None:
			print "Adding " + j[k]
			# print pos
			pos = current.add_child(TreeNode())
			pos.dist=0.2
			pos.name = j[k]
			pos.alias = i[0]
		current = pos
h.close()



def my_layout(node):

	style2 = NodeStyle()
	style2["fgcolor"] = "#000000"
	style2["shape"] = "circle"
	# style2["vt_line_color"] = "#0000aa"
	# style2["hz_line_color"] = "#0000aa"
	# style2["vt_line_width"] = 2
	# style2["hz_line_width"] = 2
	# style2["vt_line_type"] = 1 # 0 solid, 1 dashed, 2 dotted
	# style2["hz_line_type"] = 1
	node.img_style = style2
 	node.img_style["bgcolor"] = "LightSteelBlue"

	if node.is_leaf():
		# If terminal node, draws its name
		# name_faces = AttrFace("name")
		node.img_style["size"] = 40
		# node.img_style["shape"] = "sphere"
		node.img_style["fgcolor"] = "#FFFFFF"
		# node.img_style["fgcolor"] = "#9db0cf"
		# node.img_style["bgcolor"] = "#9db0cf"
		# node.img_style["faces_bgcolor"] = "#9db0cf"
		# node.img_style["bgcolor"] = "#9db0cf"
		# node.img_style["bgcolor"] = "#9db0cf"
		pass
	else:
		# If internal node, draws label with smaller font size
		# name_faces = AttrFace("name", fsize=15)
		# Adds the name face to the image at the preferred position
		# faces.add_face_to_node(name_faces, node, column=0, position="branch-top")
		# tempo = faces.ImgFace(plot_folder + "/" + node.name + '.jpg')
		# faces.add_face_to_node(tempo, node, column=0, position="branch-bottom")
		node.img_style["size"] = 40
		node.img_style["shape"] = "sphere"
		node.img_style["fgcolor"] = "#FFFFFF"

	tempt = AttrFace('name', fsize=80)
	tempt.fgcolor = "Black"
	tempt.margin_top = 10
	tempt.margin_right = 10
	tempt.margin_left = 10
	tempt.margin_bottom = 10
	tempt.opacity = 0.5 # from 0 to 1
	tempt.inner_border.width = 1 # 1 pixel border
	tempt.inner_border.type = 1  # dashed line
	tempt.border.width = 1
	# tempt.background.color = "LightGreen"
	# tempt.penwidth = 40
	node.add_face(tempt, column=0, position="branch-top")
#




def build_vis():
	ts = TreeStyle()
	ts.mode = "c"
	ts.arc_start = 0 # 0 degrees = 3 o'clock
	ts.arc_span = 360
	ts.layout_fn = my_layout # Use custom layout
	return ts
#


# ts = TreeStyle()
ts = build_vis()
# ts.show_leaf_name = True
# ts.mode = "c"
# ts.arc_start = -180 # 0 degrees = 3 o'clock
# ts.arc_span = 180

for node in t.traverse("postorder"):
	if node.name == "NoName":
		pass
	else:
	# print node
		temp = node.name
  		node.name = node.alias
  		node.alias = temp

t.write(features=["name", "dist", "alias"], outfile="prova2.nw", format=1)
A = tree_to_phyloxml(t)
text_file = open("prova.xml", "w")
text_file.write(A)
text_file.close()
from Bio import Phylo
Phylo.convert('prova2.nw', 'newick', 'prova3.xml', 'phyloxml')

t.show(tree_style=ts)
