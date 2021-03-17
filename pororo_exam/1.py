#%%
import IPython
from pororo import Pororo
from scipy.io.wavfile import write
import numpy as np
# import simpleaudio as sa

#%%
tts = Pororo("tts", lang="multi")

#%%
# Typical TTS
wave = tts("안녕하세요 저는 십삼번입니다", lang="ko")
# IPython.display.Audio(wave, rate=22050)ss# %%
print(wave)
# %%
# scaled = np.int16(wave/np.max(np.abs(wave)) * 32767)
write('test.wav',22050,wave)

# %%
# Ensure that highest value is in 16-bit range
audio = wave * (2**15 - 1) / np.max(np.abs(wave))
# Convert to 16-bit data
audio = audio.astype(np.int16)

write('test.wav',22050,audio)

# %%
