from typing import Dict, List

import folia.main as folia
from folia import fql
from pynlpl.formats import cql

import json

NEG_EX_FILE = "./negation_annotation/negation_cues"

AFFIX_NEG_FILE = "./negation_annotation/affixal_negation_cues.json"

def open_negation_cues(filename=NEG_EX_FILE):
    with open(filename) as negation_cue_file:
        b = '\b'
        return rf"{'|'.join(['^'+cue[:-1]+'$' for cue in negation_cue_file.readlines()])}"

def open_affixal_negation_cues(filename=AFFIX_NEG_FILE):
    with open(filename) as f:
        return json.loads(f.read())


def automatic_negation_cue_annotation(doc: folia.Document, cue_file: str = NEG_EX_FILE):
    reg_ex = open_negation_cues(cue_file)
    query = fql.Query(f"SELECT w WHERE text MATCHES {reg_ex}")
    words = query(doc)

    for word in words:
        utterance = word.parent.parent.parent
        modal_layer = list(utterance.select(folia.ModalitiesLayer))
        if not modal_layer:
            modal_layer = utterance.add(folia.ModalitiesLayer)
        else:
            modal_layer = modal_layer[0]
        modal = modal_layer.add(folia.Modality)
        modal.cls = "negation"
        modal.add(folia.Cue, word)


def automatic_affixal_negation_cue_annotation(
    doc: folia.Document, affix_neg_file: str = AFFIX_NEG_FILE):
    affix_neg_dict = open_affixal_negation_cues(affix_neg_file)
    reg_ex = rf"{'|'.join(affix_neg_dict.keys())}"
    query = fql.Query(f"SELECT w WHERE text MATCHES {reg_ex}")
    words = query(doc)

    for word in words:
        utterance = word.parent.parent.parent
        modal_layer = list(utterance.select(folia.ModalitiesLayer))
        if not modal_layer:
            modal_layer = utterance.add(folia.ModalitiesLayer)
        else:
            modal_layer = modal_layer[0]
        morph_layer = word.add(folia.MorphologyLayer)
        index = affix_neg_dict[word.text()]
        if index >= 0:
            neg_affix = word.text()[:index]
            neg_morpheme = morph_layer.add(folia.Morpheme, neg_affix)
            rest = word.text()[index:]
            morph_layer.add(folia.Morpheme, rest)
        else:
            rest = word.text()[:index]
            morph_layer.add(folia.Morpheme, rest)
            neg_affix = word.text()[index:]
            neg_morpheme = morph_layer.add(folia.Morpheme, neg_affix)

        modal = modal_layer.add(folia.Modality)
        modal.cls = "negation"
        modal.add(folia.Cue, neg_morpheme)
