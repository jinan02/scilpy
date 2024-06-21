#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from scil_search_keywords import _stem_keywords, _stem_text

def test_help_option(script_runner):
    ret = script_runner.run('scil_search_keywords.py', '--help')
    assert ret.success


def test_no_verbose(script_runner):
    ret = script_runner.run('scil_search_keywords.py', 'mti')
    assert ret.success


def test_verbose_option(script_runner):
    ret = script_runner.run('scil_search_keywords.py', 'mti', '-v')
    assert ret.success


def test_not_find(script_runner):
    ret = script_runner.run('scil_search_keywords.py', 'toto')
    assert ret.success

def test_stem_keywords():
    keywords = ['converting', 'conversion', 'convert']
    expected_stems = ['convert', 'convers', 'convert']
    assert _stem_keywords(keywords) == expected_stems

def test_stem_text():
    text = 'converting conversion convert'
    expected_stemmed_text = 'convert convers convert'
    assert _stem_text(text) == expected_stemmed_text