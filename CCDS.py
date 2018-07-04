#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Guoliang Lin'
__date__ = '2018/7/04'

class CCDS:
    def __init__(self,listitems):
        assert isinstance(listitems,list)
        self.Chrom=listitems[0]
        self.gene=listitems[2]
        self.gene_id=listitems[3]
        self.ccds_id=listitems[4]
        self.cds_strand=listitems[6]
        self.cds_from=listitems[7]
        self.cds_to=listitems[8]
        self.cds_locations=listitems[9]

