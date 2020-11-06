from folia import main as folia
from praatio import tgio

TEST_FILE = "../examples/uni_fn000029.hmi"
TEST_DOC = folia.Document(id="test")


def convert_text_grid_to_folia(text_grid_file, speaker_1, speaker_2, doc):
    # doc = folia.Document(id=text_grid_file)

    text_grid = tgio.openTextgrid(text_grid_file)
    speaker_1_tier = text_grid.tierDict[speaker_1]
    speaker_2_tier = text_grid.tierDict[speaker_2]

    turns = find_turns(speaker_1_tier, speaker_2_tier)
    speech = doc.add(folia.Speech)
    for turn in turns:
        turn_event = speech.add(folia.Event)
        turn_event.set = "turn"
        for i, ut in enumerate(turn):
            if i == 0:
                i_div = q_div
            else:
                i_div = a_div
            utterance = i_div.add(folia.Utterance)
            utterance.begintime = begin_end_time(ut.start)
            utterance.endtime = begin_end_time(ut.end)
            for word in ut.label.split(" "):
                if word != "":
                    utterance.add(folia.Word, word)
                else:
                    print(word)
    return doc

def find_turns(q_tier, a_tier):
    turns = []
    f_index = 0
    l_index = 0
    for j, question in enumerate(q_tier.entryList):
        #         print(f'{f_index} -- {l_index}')
        for i, answer in enumerate(a_tier.entryList[f_index:]):
            if (
                j + 1 < len(q_tier.entryList)
                and answer.start >= q_tier.entryList[j + 1].start
            ):
                #                 print(f'q: {j}, a: {f_index + i}')
                l_index = f_index + i
                break
            elif j + 1 == len(q_tier.entryList):
                l_index = f_index + i
                break

        turns.append([question] + a_tier.entryList[f_index:l_index])
        f_index = l_index
    return turns


def begin_end_time(ts):
    hours, ts = divmod(ts, 3600)
    minutes, ts = divmod(ts, 60)
    seconds, ts = divmod(ts, 1)
    miliseconds = ts * 1000
    return hours, minutes, seconds, miliseconds


#     utterances = []
#     neg_utterances = []
#     paths = []
#     contexts = []
#     for subdir, dirs, files in os.walk(DIRECTORY):
#         for file in files:
#             if file.endswith(".hmi"):
#                 if str(file).split('.')[0] in senior_id_list:
#                     hmi_file_path = os.path.join(subdir,file)
#                     paths.append(hmi_file_path)
#                     tg = tgio.openTextgrid(hmi_file_path)
#                     tg_nxxxx = tg.tierDict[tg.tierNameList[1]]
#                     text = doc.add(folia.Speech)
#                     text.speaker = "sdfs"
#                     for ut in tg_nxxxx.entryList:
#                         context = find_context(ut, tg.tierDict["TTS"] ,tg_nxxxx)
#                         div = text.add(folia.Division)
#                         for c in context[1]:
#                             div.set = "turn"
#                             utterance = div.add(folia.Utterance)
#                             utterance.begintime = begin_end_time(ut.start)
#                             utterance.endtime = begin_end_time(ut.end)
#                             for word in c.label.split(" "):
#                                 if word != "":
#                                     utterance.add(folia.Word, word)
#                                 else:
#                                     print(word)
