import os
import shutil
import tempfile
import unittest

import folia.main as folia
from negation_annotation.negation_annotation import (
    automatic_affixal_negation_cue_annotation,
    automatic_negation_cue_annotation,
)


class TestConvertNegationAnnotationMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def create_test_document(self) -> folia.Document:
        doc = folia.Document(id="test")
        speech = doc.add(folia.Speech)
        dialog = speech.add(folia.Event)
        dialog.cls = "dialog"
        round = dialog.add(folia.Event)
        round.cls = "round"
        turn = round.add(folia.Event)
        turn.cls = "turn"
        utt = turn.add(folia.Utterance)
        utterance_str = "Dit is niet een voorbeeld van negatie ."
        for word in utterance_str.split(" "):
            utt.add(folia.Word, word)

        turn = round.add(folia.Event)
        turn.cls = "turn"
        utt = turn.add(folia.Utterance)
        utterance_str = "Dit is een onaardig voorbeeld van negatie ."
        for word in utterance_str.split(" "):
            utt.add(folia.Word, word)
        round = dialog.add(folia.Event)
        round.cls = "round"
        turn = round.add(folia.Event)
        turn.cls = "turn"
        utt = turn.add(folia.Utterance)
        utterance_str = "Dit is niet niet een voorbeeld van negatie ."
        for word in utterance_str.split(" "):
            utt.add(folia.Word, word)

        self.filename = os.path.join(self.test_dir, "test.xml")
        doc.save(self.filename)

    def create_test_neg_document(self) -> folia.Document:
        doc = folia.Document(id="test")
        speech = doc.add(folia.Speech)
        dialog = speech.add(folia.Event)
        dialog.cls = "dialog"
        round = dialog.add(folia.Event)
        round.cls = "round"
        turn = round.add(folia.Event)
        turn.cls = "turn"
        utt = turn.add(folia.Utterance)
        utt.add(folia.Word, "Dit")
        utt.add(folia.Word, "is")
        neg = utt.add(folia.Word, "niet")
        utt.add(folia.Word, "een")
        utt.add(folia.Word, "voorbeeld")
        utt.add(folia.Word, "van")
        utt.add(folia.Word, "negatie")
        utt.add(folia.Word, ".")


        turn = round.add(folia.Event)
        turn.cls = "turn"
        utt = turn.add(folia.Utterance)
        utt.add(folia.Word, "Dit")
        utt.add(folia.Word, "is")
        utt.add(folia.Word, "een")
        affix = utt.add(folia.Word, "onaardig")
        utt.add(folia.Word, "voorbeeld")
        utt.add(folia.Word, "van")
        utt.add(folia.Word, "negatie")
        utt.add(folia.Word, ".")

        modal_layer = round.add(folia.ModalitiesLayer)
        modality = modal_layer.add(folia.Modality)
        modality.cls = "negation"
        modality.add(folia.Cue, neg)

        morphene_layer = affix.add(folia.MorphologyLayer)
        neg = morphene_layer.add(folia.Morpheme, "on")
        morphene_layer.add(folia.Morpheme, "aardig")
        # modal_layer = round.add(folia.ModalitiesLayer)
        modality = modal_layer.add(folia.Modality)
        modality.cls = "negation"
        modality.add(folia.Cue, neg)
        round = dialog.add(folia.Event)
        round.cls = "round"
        turn = round.add(folia.Event)
        turn.cls = "turn"
        utt = turn.add(folia.Utterance)
        utt.add(folia.Word, "Dit")
        utt.add(folia.Word, "is")
        neg_1 = utt.add(folia.Word, "niet")
        neg_2 = utt.add(folia.Word, "niet")
        utt.add(folia.Word, "een")
        utt.add(folia.Word, "voorbeeld")
        utt.add(folia.Word, "van")
        utt.add(folia.Word, "negatie")
        utt.add(folia.Word, ".")

        modal_layer = round.add(folia.ModalitiesLayer)
        modality = modal_layer.add(folia.Modality)
        modality.cls = "negation"
        modality.add(folia.Cue, neg_1)
        modality = modal_layer.add(folia.Modality)
        modality.cls = "negation"
        modality.add(folia.Cue, neg_2)

        self.filename_neg = os.path.join(self.test_dir, "test_2.xml")
        doc.save(self.filename_neg)

    def test_automatic_negation_cue_annotation(self):
        self.create_test_document()
        doc = folia.Document(file=self.filename)
        automatic_negation_cue_annotation(doc, "niet")
        automatic_affixal_negation_cue_annotation(doc, {"onaardig": 2})

        self.create_test_neg_document()
        neg_doc = folia.Document(file=self.filename_neg)
        print(doc.xmlstring())
        print(neg_doc.xmlstring())
        self.assertEqual(doc.xmlstring(), neg_doc.xmlstring())
