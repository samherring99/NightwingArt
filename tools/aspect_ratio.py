from moviepy import VideoFileClip

def resize_and_crop(input_path, output_path, target_width=1440):
    video = VideoFileClip(input_path, audio=True)
    
    target_height = int(target_width * 3/4)
    
    w, h = video.size
    
    current_ratio = w / h
    target_ratio = 4/3
    
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        y1 = 0
        cropped = video.cropped(x1=x1, y1=y1, x2=x1+new_w, y2=h)
    else:
        new_h = int(w / target_ratio)
        x1 = 0
        y1 = (h - new_h) // 2
        cropped = video.cropped(x1=x1, y1=y1, x2=w, y2=y1+new_h)
    
    final = cropped.resized((target_width, target_height))
    
    final.write_videofile(output_path, 
                         codec='libx264',
                         audio_codec='aac',
                         temp_audiofile="temp-audio.m4a",
                         remove_temp=True)
    
    video.close()
    final.close()

if __name__ == "__main__":
    input_file = "/path/to/input_video.mp4"
    output_file = "/path/to/output_video.mp4"
    resize_and_crop(input_file, output_file)