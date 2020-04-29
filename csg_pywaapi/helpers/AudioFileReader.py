import soundfile as sf


def OpenAudioFile(filename):
    audiofile = sf.SoundFile(filename)
    return audiofile

def GetChannels(filename):
    audiofile = OpenAudioFile(filename)
    return audiofile.channels

def GetSamplerate(filename):
    audiofile = OpenAudioFile(filename)
    return audiofile.samplerate


