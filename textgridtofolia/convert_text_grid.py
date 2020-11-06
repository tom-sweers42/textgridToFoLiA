from itertools import groupby
from os import truncate

from textgridtofolia.helpers import begin_end_time

from folia import main as folia
from praatio import tgio

TEST_FILE = "../examples/uni_fn000029.hmi"
TEST_DOC = folia.Document(id="test")


def convert_text_grid_to_folia(text_grid_file, speakers, doc):

    text_grid = tgio.openTextgrid(text_grid_file)
    turns = find_turns(text_grid, speakers)
    print(turns)
    speech = doc.add(folia.Speech)
    for turn in turns:
        turn_event = speech.add(folia.Event)
        turn_event.set = "turn"
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


def find_turns(text_grid, speakers):
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


