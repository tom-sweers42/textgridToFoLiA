from itertools import groupby
from os import truncate

from .helpers import begin_end_time
from folia import main as folia
from praatio import tgio
from typing import List, Tuple
TEST_FILE = "../examples/uni_fn000029.hmi"
TEST_DOC = folia.Document(id="test")



def convert_text_grid_to_folia(text_grid_file: str, speakers: List[str], events_tiers: List[str], name: str) -> folia.Document:

    text_grid = tgio.openTextgrid(text_grid_file)
    doc = folia.Document(id=name)
    add_text_grid_speakers_to_folia(text_grid, speakers, doc)
    add_text_grid_events_to_folia(text_grid, events_tiers, doc)

    return doc


def add_text_grid_speakers_to_folia(text_grid: tgio.Textgrid, speakers: List[str], doc: folia.Document) -> folia.Document:
    """A function to convert a TextGrid file and add it to a FoLia Document as a conversation between
       speakers.

    Args:
        text_grid (tgio.TextGrid): TextGrid
        speakers ([str]): list of strings containing thje names of the Tiers that contain the speeck of the speakers
        doc (folia.Document): Existing folia Document to add the TextGrid Data to.

    Returns:
        folia.Document: The resulting document including the information from the TextGrid File text_grid_file
    """

    turns = find_turns(text_grid, speakers)
    speech = doc.add(folia.Speech)
    # print(turns)
    for turn in turns:
        turn_event = speech.add(folia.Event)
        turn_event.cls = "turn"
        for i, (ut, speaker) in enumerate(turn):
            if i == 0:
                turn_event.speaker = speaker
            utterance = turn_event.add(folia.Utterance)
            utterance.begintime = begin_end_time(ut.start)
            utterance.endtime = begin_end_time(ut.end)

            # TODO Replace split with Tokenizer!
            for word in ut.label.split(" "):
                if word != "":
                    utterance.add(folia.Word, word)
                else:
                    print(word)
    return doc


def add_text_grid_events_to_folia(text_grid: tgio.Textgrid, event_tiers: List[str], doc: folia.Document) -> None:
    speech = doc.add(folia.Speech)
    for event_tier_name in event_tiers:
        for tg_event in text_grid.tierDict[event_tier_name].entryList:
            event = speech.add(folia.Event, tg_event.label)
            event.cls = f"tg-event-{event_tier_name}"
            event.begintime = begin_end_time(tg_event[0])




def find_turns(text_grid: tgio.Textgrid, speakers: List[str]) -> List[List[Tuple[tgio.Interval, str]]]:
    """This function takes all the utterances in text_grid from speakers and orders
       them chronologically and groups them per speaker. To each utterance the speaker is also
       added in a tuple.

    Args:
        text_grid (tgio.Textgrid): The textgrid that contains the utterances
        speakers (List[str]): List of speakers

    Returns:
        List[List[Tuple[tgio.Interval, str]]]: The ordered grouped list
    """
    ordered_utterances = sorted(
        [
            (utterance, speaker)
            for utterances, speaker in [
                (text_grid.tierDict[speaker].entryList, speaker) for speaker in speakers
            ]
            for utterance in utterances
        ],
        key=lambda x: x[0].start,
    )
    return [
        [(utterance, speaker) for (utterance, speaker) in g]
        for k, g in (groupby(ordered_utterances, lambda x: x[1]))
    ]
