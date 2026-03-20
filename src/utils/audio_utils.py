import pyaudio
import wave
from src.config.settings import AUDIO_RATE, AUDIO_CHANNELS, AUDIO_CHUNK

# 全局变量，用于控制录音是否中断
is_recording_active = True

def stop_recording():
    """停止录音的函数，设置全局变量为False"""
    global is_recording_active
    is_recording_active = False

def reset_recording_state():
    """重置录音状态为True，准备下一次录音"""
    global is_recording_active
    is_recording_active = True

def record_audio(duration, filepath, rate=AUDIO_RATE, channels=AUDIO_CHANNELS, chunk=AUDIO_CHUNK):
    """录制音频并保存为WAV文件（增加异常处理+返回值）"""
    global is_recording_active
    try:
        p = pyaudio.PyAudio()
        # 校验音频设备是否可用
        if p.get_device_count() == 0:
            raise Exception("无可用音频输入设备")

        stream = p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )
        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            # 检查是否被中断
            if not is_recording_active:
                break
            data = stream.read(chunk, exception_on_overflow=False)  # 防止缓冲区溢出
            frames.append(data)

        # 安全关闭流
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 保存文件
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        return True  # 录音成功
    except Exception as e:
        # 清理资源
        try:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            if 'p' in locals():
                p.terminate()
        except:
            pass
        raise Exception(f"录音失败: {str(e)}")