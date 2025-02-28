import pyaudio
import wave
import numpy as np
import webrtcvad
import struct
import time
from datetime import datetime
import os
from scipy.fftpack import fft

class ImprovedVoiceRecorder:
    def __init__(self, debug_mode=False):
        # 오디오 설정
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # WebRTC VAD는 8000, 16000, 32000, 48000Hz만 지원
        self.CHUNK = 480  # VAD에 적합한 프레임 크기 (30ms)
        self.SILENCE_THRESHOLD = 3.0  # 무음 감지 임계값 (초)
        self.VOICE_THRESHOLD = 300    # 음성 감지 임계값 (환경에 따라 조정)
        
        # VAD 설정
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(0)  # 가장 엄격한 모드로 설정 (0: 낮음 ~ 3: 높음)
        
        # 상태 변수
        self.recording = False
        self.frames = []
        self.silence_frames = 0
        self.consecutive_speech = 0
        self.required_speech_frames = 3  # 약 0.09초 동안 연속 감지 필요 (감지 시간 단축)
        self.output_dir = "recordings"
        self.debug_mode = debug_mode
        
        # 주파수 분석용 설정
        self.human_freq_low = 85    # 사람 목소리 주파수 범위 (Hz)
        self.human_freq_high = 255
        
        # 스무딩을 위한 변수
        self.smoothed_rms = 0
        self.smoothing_factor = 0.3  # 낮을수록 부드러워짐
        
        # 출력 디렉토리 생성
        os.makedirs(self.output_dir, exist_ok=True)
        
        # PyAudio 초기화
        self.p = pyaudio.PyAudio()
        
    def start(self):
        """녹음 시스템 시작"""
        print("개선된 음성 감지 시스템 시작... (종료하려면 Ctrl+C를 누르세요)")
        
        # 마이크 스트림 열기
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        # 캘리브레이션 실행
        self.calibrate()
        
        try:
            while True:
                # 오디오 데이터 읽기
                audio_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                
                # 음성 감지 (복합적 방법)
                is_speech = self.detect_speech(audio_data)
                
                # 연속적인 음성 프레임 카운팅
                if is_speech:
                    self.consecutive_speech += 1
                else:
                    self.consecutive_speech = 0
                
                # 일정 기간 이상 연속해서 음성이 감지되면 녹음 시작
                if self.consecutive_speech >= self.required_speech_frames and not self.recording:
                    self.start_recording()
                
                if self.recording:
                    # 데이터 저장
                    self.frames.append(audio_data)
                    
                    # 중요: 녹음 중지 로직 수정 - 음성 감지 조건과 동일한 조건 사용
                    is_silent = not is_speech  # 음성 감지와 동일한 로직 사용
                    
                    # 음성 감지 여부에 따라 무음 카운터 갱신
                    if not is_silent:
                        self.silence_frames = 0
                    else:
                        self.silence_frames += 1
                    
                    # 무음 지속 시간 계산 (초)
                    silence_duration = (self.silence_frames * self.CHUNK) / self.RATE
                    
                    # 디버그 출력에 무음 시간 표시
                    if self.debug_mode and self.recording:
                        print(f" [무음: {silence_duration:.1f}/{self.SILENCE_THRESHOLD:.1f}초]", end="")
                    
                    # 지정된 시간 이상 무음이면 녹음 종료
                    if silence_duration >= self.SILENCE_THRESHOLD:
                        self.stop_recording()
        
        except KeyboardInterrupt:
            print("\n프로그램 종료")
            
        finally:
            self.cleanup()
    
    def calibrate(self):
        """주변 환경 소음을 측정하여 임계값 자동 조정 - 확장 버전"""
        print("환경 소음 측정 중... (10초)")
        samples = []
        
        # 10초 동안 샘플 수집 (5초에서 10초로 증가)
        for _ in range(int(self.RATE / self.CHUNK * 10)):
            audio_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            rms = self.get_rms(audio_data)
            samples.append(rms)
        
        # 배경 소음 레벨 계산 (하위 80%의 평균 사용)
        samples.sort()
        valid_samples = samples[:int(len(samples) * 0.8)]  # 상위 20% 제외 (일시적 소음 제거)
        background_noise = np.mean(valid_samples)
        noise_std = np.std(valid_samples)
        
        # 임계값 설정 (배경 소음 + 표준편차의 4배)
        self.VOICE_THRESHOLD = background_noise + noise_std * 4.0
        
        print(f"측정 완료. 배경 소음 레벨: {background_noise:.2f}")
        print(f"음성 감지 임계값: {self.VOICE_THRESHOLD:.2f}로 설정됨")
    
    def detect_speech(self, audio_data):
        """개선된 음성 감지 로직"""
        # WebRTC VAD로 음성 감지
        try:
            vad_result = self.vad.is_speech(audio_data, self.RATE)
        except:
            vad_result = False
        
        # RMS 기반 감지
        rms = self.get_rms(audio_data)
        self.smoothed_rms = self.smoothing_factor * rms + (1 - self.smoothing_factor) * self.smoothed_rms
        rms_result = self.smoothed_rms > self.VOICE_THRESHOLD
        
        # 주파수 분석 기반 감지
        freq_result = self.check_human_freq(audio_data)
        
        # 디버그 모드에서는 상세 정보 출력
        if self.debug_mode:
            status = "🔴" if self.recording else "⚪"
            # 각 조건별 아이콘 표시
            vad_icon = "✓" if vad_result else "✗"
            rms_icon = "✓" if rms_result else "✗"
            freq_icon = "✓" if freq_result else "✗"
            speech = "🗣️" if ((vad_result and rms_result) or (rms_result and freq_result) or (vad_result and freq_result)) else "  "
            
            # 디버그 정보 상세 출력
            print(f"{status} VAD: {vad_icon}, RMS: {rms_icon}({self.smoothed_rms:.1f}/{self.VOICE_THRESHOLD:.1f}), FREQ: {freq_icon}, CNT: {self.consecutive_speech} {speech}", end='\r')
        
        # 통합 결과: VAD가 true이면서 RMS나 주파수 중 하나라도 true여야 함 (더 엄격한 조건)
        speech_detected = vad_result and (rms_result or freq_result)
        return speech_detected
    
    def check_human_freq(self, audio_data):
        """사람 목소리 주파수 대역 확인"""
        try:
            # 데이터를 float32로 변환
            count = len(audio_data) // 2
            format_str = "%dh" % count
            shorts = struct.unpack(format_str, audio_data)
            data = np.array(shorts).astype(np.float32) / 32768.0  # 정규화
            
            # FFT 수행
            fft_data = fft(data)
            # 주파수 성분 계산
            fft_freqs = np.fft.fftfreq(len(data), 1.0/self.RATE)
            
            # 사람 목소리 주파수 대역의 파워 계산
            voice_freq_mask = (fft_freqs >= self.human_freq_low) & (fft_freqs <= self.human_freq_high)
            all_freq_power = np.sum(np.abs(fft_data))
            
            if all_freq_power == 0:
                return False
                
            voice_freq_power = np.sum(np.abs(fft_data[voice_freq_mask]))
            voice_power_ratio = voice_freq_power / all_freq_power
            
            # 사람 목소리 대역의 파워가 전체의 10% 이상이면 사람 목소리로 판단 (20% → 10%로 완화)
            return voice_power_ratio > 0.1
            
        except Exception as e:
            if self.debug_mode:
                print(f"주파수 분석 오류: {e}")
            return True  # 오류 시 기본값으로 True 반환
    
    def get_rms(self, audio_data):
        """오디오 데이터의 RMS(Root Mean Square) 값 계산"""
        count = len(audio_data) // 2
        format_str = "%dh" % count
        try:
            shorts = struct.unpack(format_str, audio_data)
            shorts_array = np.array(shorts).astype(np.float32)
            sum_squares = np.sum(shorts_array ** 2)
            rms = np.sqrt(max(0, sum_squares / count))
            return rms
        except Exception as e:
            if self.debug_mode:
                print(f"RMS 계산 오류: {e}")
            return 0
    
    def start_recording(self):
        """녹음 시작"""
        self.recording = True
        self.frames = []
        self.silence_frames = 0
        print("\n음성 감지! 녹음 시작..." + " " * 40)
    
    def stop_recording(self):
        """녹음 중지 및 파일 저장"""
        if self.recording and len(self.frames) > 0:
            self.recording = False
            print("녹음 중지, 파일 저장 중..." + " " * 40)
            
            # 현재 시간을 파일 이름으로 사용
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"recording_{timestamp}.wav")
            
            # WAV 파일로 저장
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            
            print(f"녹음 파일 저장 완료: {filename}")
            print("다시 음성 감지 대기 중...")
    
    def cleanup(self):
        """리소스 정리"""
        if hasattr(self, 'stream') and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
        
        self.p.terminate()


if __name__ == "__main__":
    # 디버그 모드를 활성화하려면 True로 설정
    recorder = ImprovedVoiceRecorder(debug_mode=True)
    recorder.start()