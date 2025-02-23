import generate_text
import generate_audio
import generate_video
import requests

def create_temp_file(filename, content):
    temp_path = default_storage.save(f"temp/{filename}", content)
    return temp_path

def compile_video(filename, webhook_url):
    temp_speech_file = create_temp_file("audiofile", )
    try:
        pdf_text = generate_text.parse_pdf(filename=filename)
        script_text = generate_text.generate_script(pdf_text)
        
        diffusion_payload = generate_video.create_video_from_text(temp_vid_path, "")
        generate_audio(script_text, temp_speech_path)
        
        if diffusion_payload.status == "ERROR": 
            return {"status": "ERROR", "message": "Failed to create video"}
    
        generate_video.run_sync(temp_vid_path, temp_speech_path, webhook_url)
        return {"status": "SUCCESS", "message": "Video compilation completed successfully"}

    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
    