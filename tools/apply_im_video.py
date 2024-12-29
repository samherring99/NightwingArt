import subprocess
import os
from moviepy import VideoFileClip, ImageSequenceClip
import tempfile
import shutil
from PIL import Image
import numpy as np

def apply_effects_to_frame(input_path, output_path):
    temp_path = input_path.replace('.jpg', '_temp.jpg')
    
    subprocess.run([
        'magick',
        input_path,
        '-modulate', '100,300',
        temp_path
    ], check=True)
    
    subprocess.run([
        'magick',
        temp_path,
        '-quality', '10',
        output_path
    ], check=True)
    
    os.remove(temp_path)

def process_video_with_effects(input_video_path, output_video_path, fps=30):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_frames_dir = os.path.join(temp_dir, 'input_frames')
        output_frames_dir = os.path.join(temp_dir, 'output_frames')
        os.makedirs(input_frames_dir)
        os.makedirs(output_frames_dir)
        
        try:
            video = VideoFileClip(input_video_path)
            original_fps = video.fps
            
            print(f"Extracting frames from video...")
            
            frame_count = 0
            for i, frame in enumerate(video.iter_frames()):
                frame_path = os.path.join(input_frames_dir, f"frame_{i:06d}.jpg")
                # Convert frame to PIL Image and save
                frame_rgb = Image.fromarray(np.uint8(frame))
                frame_rgb.save(frame_path, quality=95)
                frame_count = i + 1
            
            print(f"Processing {frame_count} frames with ImageMagick effects...")
            
            for i in range(frame_count):
                if i % 10 == 0:
                    print(f"Processing frame {i}/{frame_count}...")
                
                input_path = os.path.join(input_frames_dir, f"frame_{i:06d}.jpg")
                output_path = os.path.join(output_frames_dir, f"frame_{i:06d}.jpg")
                apply_effects_to_frame(input_path, output_path)
            
            print("Reconstructing video from processed frames...")
            
            processed_frames = sorted([
                os.path.join(output_frames_dir, f)
                for f in os.listdir(output_frames_dir)
                if f.endswith('.jpg')
            ])
            
            processed_clip = ImageSequenceClip(processed_frames, fps=original_fps)
            
            if video.audio is not None:
                processed_clip = processed_clip.with_audio(video.audio)
            
            processed_clip.write_videofile(
                output_video_path,
                codec='libx264',
                audio_codec='aac' if video.audio is not None else None
            )
            
            video.close()
            processed_clip.close()
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise
        
        print("Processing complete!")

if __name__ == "__main__":
    input_video = "/path/to/input.mp4"
    output_video = "/path/to/output.mp4"
    
    process_video_with_effects(input_video, output_video)