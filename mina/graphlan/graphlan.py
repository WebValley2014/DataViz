#!/usr/bin/env python

#------------------------------------------------------------------------------
# NAME: graphlan.py
# DESCRIPTION:  GraPhlAn is a python program for creating images of circular 
#               cladogram starting from a tree given in PhyloXML format. The 
#               PhyloXML input tree can be formatted and annotated using the 
#               graphlan_annotate.py script.
#
# Author:   Nicola Segata
# email:    nsegata@hsph.harvard.edu
#
#
#------------------------------------------------------------------------------

__author__ = 'Nicola Segata (nsegata@hsph.harvard.edu)'
__version__ = '0.9.6'
__date__ = '16 April 2014'


from sys import argv
from argparse import ArgumentParser
from src.graphlan_lib import CircTree as CTree
import math

def read_params(args):
    parser = ArgumentParser(description= "GraPhlAn "+__version__+" ("+__date__+") "
                                         "AUTHORS: "+__author__)
    arg = parser.add_argument

    arg('intree', type=str, default = None, metavar='input_tree',
        help = "the input tree in PhyloXML format " )
    arg('outimg', type=str, default = None, metavar='output_image',
        help = "the output image, the format is guessed from the extension "
               "unless --format is given. Available file formats are: png, "
               "pdf, ps, eps, svg" )
    arg('--format', choices=['png','pdf','ps','eps','svg'], default=None, 
        type = str, metavar=['output_image_format'],
        help = "set the format of the output image (default none meaning that "
               "the format is guessed from the output file extension)")
    arg('--warnings', default=1, type=int,
        help = "set whether warning messages should be reported or not (default 1)")
    arg('--positions', default=0, type=int,
        help = "set whether the absolute position of the points should be reported on "
               "the standard output. The two cohordinates are r and theta")
    arg('--dpi', default=72, type=int, metavar='image_dpi',
        help = "the dpi of the output image for non vectorial formats")
    arg('--size', default=7.0, type=float, metavar='image_size',
        help = "the size of the output image (in inches, default 7.0)")
    arg('--pad', default=0.5, type=float, metavar='pad_in',
        help = "the distance between the most external graphical element and "
               "the border of the image")
    arg( '-v','--version', action='version', version="GraPhlAn version "+__version__+" ("+__date__+")", 
        help="Prints the current GraPhlAn version and exit" )
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = read_params( argv )
    ctree = CTree( args['intree'], args['warnings'] )
    ctree.positions = args['positions']
    ctree.draw( args['outimg'], 
                out_format = args['format'], 
                out_dpi = args['dpi'],
                out_size = args['size'],
                out_pad = args['pad'] )


# old way: extract coordinates from graphlan class
    stringa = "{\n\"data\":[ "
    coords = zip(ctree._t,ctree._r)
    names = []

    ids = range(0,len(coords))
    for i in range(0, len(coords)):
        angle = coords[i][0]
        r = coords[i][1]
        idc = ids[i]
        x=r*math.cos(angle)
        y=r*math.sin(angle)
        print r, angle, x, y
        cstringa = "\n" + "{" 
        cstringa = cstringa + "\"id\": " + str(idc)
        cstringa = cstringa + ", \"name\": " + "NoName"
        cstringa = cstringa + ", \"x\": " + str(x)
        cstringa = cstringa + ", \"y\": " + str(y)
        cstringa = cstringa + ", \"rank\": " + str(0)
        cstringa = cstringa + ", \"childs\": " + "[0]"
        cstringa = cstringa + "},"
        stringa = stringa + cstringa
    stringa  = stringa[0:-1] + "\n]}\n"
    print stringa
    text_file = open("prova_json.txt", "w")
    text_file.write(stringa)
    text_file.close()


# new way: extract coordinates from Phylogeny class


    filename = '../data_template/PRE_ML/OUTPUT/X_l2r_l2loss_svc_SVM_std_featurelist.txt'
    associations = {}
    h = open(filename, 'r')
    for i in h:
        i = i.strip()
        i = i.split("\t")
        j = i[1]
        k = i[2]
        associations[j] = k
    h.close()

    albero = ctree.tree
    stringa = "{\n\"data\":[ "
    dati = []
    nomi = {}
    whole = []
    whole.append(albero.clade)
    cid = 0
    albero.clade.id = cid
    cid += 1
    while len(whole) > 0:
        current = whole.pop()
        tempo = []
        for i in current.clades:
            i.id = cid
            tempo.append(i.id)
            cid += 1
            whole.append(i)
        dati.append((current.id, current.name, current.r, current.theta, tempo))
    # print dati
    print associations

    for i in range(0, len(dati)):
        angle = dati[i][3]
        r = dati[i][2]
        idc = dati[i][0]
        name = dati[i][1]
        rank = 0
        if name in associations:
            rank = associations[name]
            print rank
        children = dati[i][4]
        x=r*math.cos(angle)
        y=r*math.sin(angle)
        # print r, angle, x, y
        cstringa = "\n" + "{" 
        cstringa = cstringa + "\"id\": " + str(idc)
        cstringa = cstringa + ", \"name\": " + str(name)
        cstringa = cstringa + ", \"x\": " + str(x)
        cstringa = cstringa + ", \"y\": " + str(y)
        cstringa = cstringa + ", \"rank\": " + str(rank)
        cstringa = cstringa + ", \"childs\": " + str(children)
        cstringa = cstringa + "},"
        stringa = stringa + cstringa
    stringa  = stringa[0:-1] + "\n]}\n"
    # print stringa
    text_file = open("prova_json_2.txt", "w")
    text_file.write(stringa)
    text_file.close()

