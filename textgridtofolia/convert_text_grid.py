from itertools import groupby
from os import truncate
from typing import Dict, List, Tuple
import re

import frog
from folia import main as folia
from praatio import tgio

from .helpers import begin_end_time

TEST_FILE = "../examples/uni_fn000029.hmi"
TEST_DOC = folia.Document(id="test")
TOKENIZER = frog.Frog(
    frog.FrogOptions(lemma=False, morph=False, parser=False, xmlout=True)
)


def convert_text_grids_to_folia(
    text_grid_files: List[str],
    speakers_dict: Dict[str, List[str]],
    event_tiers_dict: Dict[str, List[str]],
    name: str,
) -> folia.Document:
    doc = folia.Document(id=name)
    speech_doc = doc.add(folia.Speech)
    for i, text_grid_file in enumerate(text_grid_files):
        print(f"progress: {i}/{len(text_grid_files)}")
        speakers = speakers_dict.get(text_grid_file, [])
        event_tiers = event_tiers_dict.get(text_grid_file, [])
        convert_text_grid_to_folia(
            text_grid_file, speakers, event_tiers, name, speech_doc=speech_doc
        )
    return doc


def convert_text_grid_to_folia(
    text_grid_file: str,
    speakers: List[str],
    events_tiers: List[str],
    name: str,
    speech_doc: folia.Speech = None,
) -> folia.Document:
    doc = None
    text_grid = tgio.openTextgrid(text_grid_file)
    if not speech_doc:
        doc = folia.Document(id=name)
        speech_doc = doc.add(folia.Speech)
    add_text_grid_speakers_to_folia(text_grid, speakers, speech_doc)
    add_text_grid_events_to_folia(text_grid, events_tiers, speech_doc)

    return doc


def add_text_grid_invervals_to_folia(
    text_grid: tgio.Textgrid, inverval_tiers: List[str], doc: folia.Document
):
    speech = doc.add(folia.Speech)
    speech.cls = "intervals"

    for interval_tier in inverval_tiers:
        interval_event = speech.add(folia.Event)
        interval_event.cls = "interval"
        interval_event.speaker = interval_tier
        for interval in text_grid.tierDict[interval_tier].entryList:
            utterance = interval_event.add(folia.Utterance)
            utterance.begintime = begin_end_time(interval.start)
            utterance.endtime = begin_end_time(interval.end)
            add_tokens_to_utterance(utterance, interval.label)

def add_text_grid_speakers_to_folia(
    text_grid: tgio.Textgrid, speakers: List[str], speech_doc: folia.Speech
):
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
    speech_event = speech_doc.add(folia.Event)
    speech_event.cls = "dialog"
    for turn in turns:
        turn_event = speech_event.add(folia.Event)
        turn_event.cls = "turn"
        for i, (ut, speaker) in enumerate(turn):
            if i == 0:
                turn_event.speaker = speaker
            utterance = turn_event.add(folia.Utterance)
            utterance.begintime = begin_end_time(ut.start)
            utterance.endtime = begin_end_time(ut.end)
            add_tokens_to_utterance(utterance, ut.label)


def add_text_grid_events_to_folia(
    text_grid: tgio.Textgrid, event_tiers: List[str], speech_doc: folia.Speech
) -> None:
    if not event_tiers:
        return
    text_grid_event_event = speech_doc.add(folia.Event)
    text_grid_event_event.cls = "text-grid-events"
    for event_tier_name in event_tiers:
        for tg_event in text_grid.tierDict[event_tier_name].entryList:
            event = text_grid_event_event.add(folia.Event)
            event.cls = f"tg-event-{event_tier_name}-{tg_event.label}"
            event.begintime = begin_end_time(tg_event[0])


def find_turns(
    text_grid: tgio.Textgrid, speakers: List[str]
) -> List[List[Tuple[tgio.Interval, str]]]:
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


def add_tokens_to_utterance(utterance: folia.Utterance, str_utterance: str) -> None:
    # str_utterance_no_asterisk = re.sub(r"\*\w", "", str_utterance)
    tokens = TOKENIZER.process(str_utterance)
    words = [word.text() for word in tokens.words()]
    for i, word in enumerate(words):
        if word == "*" or (words[i-1] == "*" and len(words[i-1]) == 1):
            pass 
        else:
            folia_word = utterance.add(folia.Word, word)
        if i+2 < len(words) and words[i+1] == "*" and len(words[i+2])==1:
            folia_word.cls = f"*{words[i+2]}"
