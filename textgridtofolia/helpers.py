import io
import json
from typing import Tuple

from praatio.tgio import (
    _dictionaryToTg,
    _parseNormalTextgrid,
    _parseShortTextgrid,
    _removeBlanks,
)


def _openTextgrid(fnFullPath, readRaw=False, readAsJson=False):
    """

    Function copied from praatio library so that it opens praat textgrid files with latin-1 encoding.

    Opens a textgrid for editing
    readRaw: points and intervals with an empty label '' are removed unless readRaw=True
    readAsJson: if True, assume the Textgrid is saved as Json rather than in its native format
    """

    with io.open(fnFullPath, "r", encoding="ISO-8859-1") as fd:
        data = fd.read()
    if readAsJson:
        tgAsDict = json.loads(data)
        textgrid = _dictionaryToTg(tgAsDict)
    else:
        data = data.replace("\r\n", "\n")

        caseA = "ooTextFile short" in data
        caseB = "item [" not in data
        if caseA or caseB:
            textgrid = _parseShortTextgrid(data)
        else:
            textgrid = _parseNormalTextgrid(data)

    if readRaw == False:
        for tierName in textgrid.tierNameList:
            tier = textgrid.tierDict[tierName]
            tier = _removeBlanks(tier)
            textgrid.replaceTier(tierName, tier)

    return textgrid


def begin_end_time(ts: float) -> Tuple[int, int, int, int]:
    round_3 = lambda x: round(x, 3)
    hours, ts = map(round_3, divmod(ts, 3600))
    minutes, ts = map(round_3, divmod(ts, 60))
    seconds, ts = map(round_3, divmod(ts, 1))
    miliseconds = ts * 1000
    return int(hours), int(minutes), int(seconds), int(miliseconds)
