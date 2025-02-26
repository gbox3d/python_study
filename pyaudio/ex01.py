#%%
import pyaudio # pip install pyaudio

print(f"pyaudio 버전: {pyaudio.__version__}")   # pyaudio 버전 확인

#%%
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

print("사용 가능한 마이크 디바이스:")
print("-" * 50)

for i in range(num_devices):
    device_info = p.get_device_info_by_index(i)
    
    # 입력 채널이 있는 디바이스만 선택 (마이크)
    if device_info.get('maxInputChannels') > 0:
        print(f"디바이스 ID {i}: {device_info.get('name')}")
        print(f"  채널 수: {device_info.get('maxInputChannels')}")
        print(f"  기본 샘플 레이트: {device_info.get('defaultSampleRate')}")
        print("-" * 50)

p.terminate()

# %%
