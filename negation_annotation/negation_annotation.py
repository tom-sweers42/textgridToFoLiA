from typing import Dict, List

import folia.main as folia
from folia import fql
from pynlpl.formats import cql

NEG_REG_EX = r"niet|nee|geen|nooit"

AFFIX_NEG_DICT = {
    "onaardig": 2,
    "onverwachte": 2,
    "onverschillig": 2,
    "onvoorziene": 2,
    "onmisbaar": 2,
    "indirect": 2,
    "zoutloos": -4,
    "trouweloos": -4,
    "suikerloos": -4,
    "glutenvrij": -4,
    "suikervrij": -4,
}


def automatic_negation_cue_annotation(doc: folia.Document, reg_ex: str = NEG_REG_EX):
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
    doc: folia.Document, affix_neg_dict: Dict[str, int] = AFFIX_NEG_DICT
):
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
