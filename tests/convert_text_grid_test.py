import unittest

from folia.main import Utterance
from praatio.tgio import openTextgrid

from textgridtofolia.convert_text_grid import add_text_grid_speakers_to_folia

from praatio import tgio

from folia import main as folia
import tempfile
import shutil
import os
class TestConvertTextGridMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def create_text_grid(self):
        tg = tgio.Textgrid()

        speaker_1_utterances = [
            (0.0, 1.0, "This is utterance 1."),
            (1.1, 2.1, "This is utterance 2."),
            (4.0, 5.0, "This is utterance 3.")
        ]

        speaker_2_utterances = [
            (2.2, 3.2, "This is utterance a."),
            (3.3, 3.9, "This is utterance b."),
            (5.1, 7.0, "This is utterance c.")
        ]

        speaker_1_tier = tgio.IntervalTier('speaker_1', speaker_1_utterances)
        speaker_2_tier = tgio.IntervalTier('speaker_2', speaker_2_utterances)

        tg.addTier(speaker_1_tier)
        tg.addTier(speaker_2_tier)
        self.filename = os.path.join(self.test_dir, "test.TextGrid")
        tg.save(self.filename)

    def test_convert_text_grid_to_folia(self):

        assert_doc = folia.Document(id="test")

        assert_speech = assert_doc.add(folia.Speech)
        assert_event = assert_speech.add(folia.Event)
        assert_event.set = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0,0,0,0)
        utterance.endtime = (0,0,1,0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "1.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0,0,1,100)
        utterance.endtime = (0,0,2,100)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "2.")


        assert_event = assert_speech.add(folia.Event)
        assert_event.set = "turn"
        assert_event.speaker = "speaker_2"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0,0,2,200)
        utterance.endtime = (0,0,3,200)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "a.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0,0,3,300)
        utterance.endtime = (0,0,3,900)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "b.")

        assert_event = assert_speech.add(folia.Event)
        assert_event.set = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0,0,4,0)
        utterance.endtime = (0,0,5,0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "3.")

        assert_event = assert_speech.add(folia.Event)
        assert_event.set = "turn"
        assert_event.speaker = "speaker_2"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0,0,5,100)
        utterance.endtime = (0,0,7,0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "c.")

        self.create_text_grid()

        speakers = ["speaker_1", "speaker_2"]
        doc = folia.Document(id="test")

        tg = tgio.openTextgrid(self.filename)
        add_text_grid_speakers_to_folia(tg, speakers, doc)

        print(doc.xmlstring())
        print(assert_doc.xmlstring())


        self.assertEqual(doc, assert_doc)
        self.assertEqual(doc.xmlstring(), assert_doc.xmlstring())



