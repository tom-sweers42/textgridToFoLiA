import os
import shutil
import tempfile
import unittest

from folia import main as folia
from folia.main import Utterance
from praatio import tgio
from praatio.tgio import openTextgrid
from textgridtofolia.convert_text_grid import (
    add_text_grid_events_to_folia,
    add_text_grid_speakers_to_folia,
    convert_text_grid_to_folia,
)


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
            (4.0, 5.0, "This is utterance 3."),
        ]

        speaker_2_utterances = [
            (2.2, 3.2, "This is utterance a."),
            (3.3, 3.9, "This is utterance b."),
            (5.1, 7.0, "This is utterance c."),
        ]

        speaker_1_tier = tgio.IntervalTier("speaker_1", speaker_1_utterances)
        speaker_2_tier = tgio.IntervalTier("speaker_2", speaker_2_utterances)

        tg.addTier(speaker_1_tier)
        tg.addTier(speaker_2_tier)

        event_list = [(1.0, "EVENT 1"), (1.2, "EVENT 2")]

        event_tier = tgio.PointTier("EVENTS", event_list)
        tg.addTier(event_tier)
        self.filename = os.path.join(self.test_dir, "test.TextGrid")
        tg.save(self.filename)

    def test_add_text_grid_to_folia(self):

        assert_doc = folia.Document(id="test")

        assert_speech = assert_doc.add(folia.Speech)
        dialog_event = assert_speech.add(folia.Event)
        dialog_event.cls = "dialog"

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 0, 0)
        utterance.endtime = (0, 0, 1, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "1.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 1, 100)
        utterance.endtime = (0, 0, 2, 100)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "2.")

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_2"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 2, 200)
        utterance.endtime = (0, 0, 3, 200)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "a.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 3, 300)
        utterance.endtime = (0, 0, 3, 900)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "b.")

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 4, 0)
        utterance.endtime = (0, 0, 5, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "3.")

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_2"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 5, 100)
        utterance.endtime = (0, 0, 7, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "c.")

        self.create_text_grid()

        speakers = ["speaker_1", "speaker_2"]
        doc = folia.Document(id="test")
        doc_dialog_speech = doc.add(folia.Speech)
        tg = tgio.openTextgrid(self.filename)
        add_text_grid_speakers_to_folia(tg, speakers, doc_dialog_speech)

        self.assertEqual(doc, assert_doc)
        self.assertEqual(doc.xmlstring(), assert_doc.xmlstring())

    def test_add_text_grid_to_folia_one_speaker(self):

        assert_doc = folia.Document(id="test")

        assert_speech = assert_doc.add(folia.Speech)
        dialog_event = assert_speech.add(folia.Event)
        dialog_event.cls = "dialog"

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 0, 0)
        utterance.endtime = (0, 0, 1, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "1.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 1, 100)
        utterance.endtime = (0, 0, 2, 100)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "2.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 4, 0)
        utterance.endtime = (0, 0, 5, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "3.")

        self.create_text_grid()

        speakers = ["speaker_1"]
        doc = folia.Document(id="test")
        doc_dialog_speech = doc.add(folia.Speech)

        tg = tgio.openTextgrid(self.filename)
        add_text_grid_speakers_to_folia(tg, speakers, doc_dialog_speech)

        self.assertEqual(doc, assert_doc)
        self.assertEqual(doc.xmlstring(), assert_doc.xmlstring())

    def test_add_text_grid_events_to_folia(self):

        assert_doc = folia.Document(id="test")

        assert_speech = assert_doc.add(folia.Speech)
        tg_event_event = assert_speech.add(folia.Event)
        tg_event_event.cls = "text-grid-events"

        assert_event = tg_event_event.add(folia.Event)
        assert_event.cls = "tg-event-EVENTS-EVENT 1"
        assert_event.begintime = (0, 0, 1, 0)

        assert_event = tg_event_event.add(folia.Event)
        assert_event.cls = "tg-event-EVENTS-EVENT 2"
        assert_event.begintime = (0, 0, 1, 200)

        self.create_text_grid()

        event_tiers = ["EVENTS"]
        doc = folia.Document(id="test")
        events = doc.add(folia.Speech)

        tg = tgio.openTextgrid(self.filename)
        add_text_grid_events_to_folia(tg, event_tiers, events)

        self.assertEqual(doc, assert_doc)
        self.assertEqual(doc.xmlstring(), assert_doc.xmlstring())

    def test_convert_text_grdid_to_folia(self):

        assert_doc = folia.Document(id="test")

        assert_speech = assert_doc.add(folia.Speech)
        dialog_event = assert_speech.add(folia.Event)
        dialog_event.cls = "dialog"

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 0, 0)
        utterance.endtime = (0, 0, 1, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "1.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 1, 100)
        utterance.endtime = (0, 0, 2, 100)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "2.")

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_2"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 2, 200)
        utterance.endtime = (0, 0, 3, 200)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "a.")

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 3, 300)
        utterance.endtime = (0, 0, 3, 900)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "b.")

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_1"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 4, 0)
        utterance.endtime = (0, 0, 5, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "3.")

        assert_event = dialog_event.add(folia.Event)
        assert_event.cls = "turn"
        assert_event.speaker = "speaker_2"

        utterance = assert_event.add(folia.Utterance)
        utterance.begintime = (0, 0, 5, 100)
        utterance.endtime = (0, 0, 7, 0)

        utterance.add(folia.Word, "This")
        utterance.add(folia.Word, "is")
        utterance.add(folia.Word, "utterance")
        utterance.add(folia.Word, "c.")

        tg_event_event = assert_speech.add(folia.Event)
        tg_event_event.cls = "text-grid-events"

        assert_event = tg_event_event.add(folia.Event)
        assert_event.cls = "tg-event-EVENTS-EVENT 1"
        assert_event.begintime = (0, 0, 1, 0)

        assert_event = tg_event_event.add(folia.Event)
        assert_event.cls = "tg-event-EVENTS-EVENT 2"
        assert_event.begintime = (0, 0, 1, 200)

        self.create_text_grid()

        speakers = ["speaker_1", "speaker_2"]
        event_tiers = ["EVENTS"]

        doc = convert_text_grid_to_folia(self.filename, speakers, event_tiers, "test")

        self.assertEqual(doc, assert_doc)
        self.assertEqual(doc.xmlstring(), assert_doc.xmlstring())
