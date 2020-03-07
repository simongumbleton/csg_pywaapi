import soundfile as sf
import numpy


def OpenAudioFile(filename):
    audiofile = sf.SoundFile(filename)
    return audiofile

def GetChannels(filename):
    audiofile = OpenAudioFile(filename)
    return audiofile.channels

def GetSamplerate(filename):
    audiofile = OpenAudioFile(filename)
    return audiofile.samplerate


