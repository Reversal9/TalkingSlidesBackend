import requests
import modal
import diffusers
from dotenv import load_dotenv

load_dotenv()
sync_api_key = os.getenv("SYNC_API_KEY")
sync_url = "https://api.sync.so/v2/generate"
MINUTES = 60

image = (
    # check python version
    modal.Image.debian_slim(python_version="3.11")
     .apt_install("git")
     .pip_install(
        "accelerate==0.33.0",
        "diffusers==0.31.0",
        "fastapi[standard]==0.115.4",
        "huggingface-hub[hf_transfer]==0.25.2",
        "sentencepiece==0.2.0",
        "torch==2.5.1",
        "torchvision==0.20.1",
        "transformers~=4.44.0",
     )
     .env(
         {
             "HF_HUB_ENABLE_HF_TRANSFER": "1",
             "HF_DEBUG": "1",
             "HF_HOME": "/ai",
         }
     )
)

app = modal.App(name="video-generator")
with image.imports():
    import torch
    from diffusers import DiffusionPipeline
    from diffusers.utils import export_to_video
# try to use GPU acceleration
class GenerateVideo:
    @app.function(
        image=image,
        timeout = 10 * MINUTES,
    )
    def create_video_from_text(export_path, user_prompt):
        input_prompt = """
        A helpful instructor giving a lecture.
        """.strip() + "\n" + {user_prompt}
        
        pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", 
                                                torch_dtype=torch.float16, 
                                                variant="fp16")
        pipe.enable_model_cpu_offload()
        # memory optimization
        # https://github.com/huggingface/diffusers/issues/6869#issuecomment-1929569492
        pipe.unet.enable_forward_chunking(chunk_size=1, dim=1)
        pipe.enable_vae_slicing()
        video_frames = pipe(input_prompt, num_frames=24).frames[0]
        try:
            video_path = export_to_video(video_frames, fps=10, output_video_path=export_path)
            payload = {"status" : "success", "video_path" : video_path}
        except Exception as e: 
            payload = {"status" : "error", "video_path" : str(e)} 

        return payload


    def run_sync(video_url, audio_url, webhook_url):
        payload = {
            "model": "lipsync-1.7.1",
            "input": [
                {
                    "type": "video",
                    "url": video_url
                },
                {
                    "type": "audio",
                    "url": audio_url
                }
            ],
            "options": {
                "pads": [0, 5, 0, 0],
                "speedup": 2,
                "output_format": "mp4",
                "sync_mode": "cutoff",
                "fps": 25,
                "output_resolution": [1080, 720],
                "active_speaker": True
            },
            "webhookUrl": webhook_url
        }
        headers = {
            "x-api-key": sync_api_key,
            "Content-Type": "application/json"
        }

        response = requests.request("POST", sync_url, json=payload, headers=headers)

        print(response.text)
    
    