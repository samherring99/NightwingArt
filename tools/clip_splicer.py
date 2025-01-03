from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import os
from random import uniform
import random

def detect_beats(audio_path):
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times

def get_random_clip_times(video_duration, used_times, min_duration=1, max_duration=2):
    max_start = video_duration - max_duration
    if max_start <= 0:
        return None, None
    
    attempts = 0
    while attempts < 50:
        start_time = random.uniform(0, max_start)
        duration = random.uniform(min_duration, max_duration)
        overlap = False
        for used_start, used_end in used_times:
            if not (start_time + duration <= used_start or start_time >= used_end):
                overlap = True
                break
                
        if not overlap:
            return start_time, duration
        attempts += 1
    
    return None, None

def create_beat_sync_video(video_folder, audio_path, output_path):
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mov')]
    if not video_files:
        raise Exception("No .mov files found in the specified folder")

    beat_times = detect_beats(audio_path)
    
    audio = AudioFileClip(audio_path)
    
    used_segments = {video: [] for video in video_files}
    
    video_clips = {}
    
    final_clips = []
    
    try:
        for video_file in video_files:
            video_path = os.path.join(video_folder, video_file)
            video_clips[video_file] = VideoFileClip(video_path)
        
        for beat_time in beat_times:
            video_file = random.choice(video_files)
            video = video_clips[video_file]
            
            start_time, duration = get_random_clip_times(
                video.duration,
                used_segments[video_file]
            )
            
            if start_time is None:
                continue

            used_segments[video_file].append((start_time, start_time + duration))
            
            clip = video.subclipped(start_time, start_time + duration).with_start(beat_time)
            final_clips.append(clip)
        
        final_video = concatenate_videoclips(final_clips, method="compose")
        
        final_video = final_video.with_audio(audio)
        
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
    finally:
        audio.close()
        for clip in video_clips.values():
            clip.close()
        for clip in final_clips:
            clip.close()
        try:
            final_video.close()
        except:
            pass

if __name__ == "__main__":
    video_folder = "/path/to/video/directory"
    audio_path = "/path/to/audio.mp3"
    output_path = "output_video.mp4"
    
    create_beat_sync_video(video_folder, audio_path, output_path)