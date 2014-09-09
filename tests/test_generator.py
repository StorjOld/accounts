# -*- coding: utf-8 -*-
from accounts.generator import to62, generate

def test_to62():
    idx = [1, 20, 35, 50, 71]
    assert ''.join(to62(i) for i in idx) == '1KZo\x84'

def test_generate(patch_urandom):
    assert generate() == 'oiFyR2NcMvaSiNDf'
