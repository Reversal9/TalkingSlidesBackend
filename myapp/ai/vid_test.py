from django.test import LiveServerTestCase
import requests
'''
Fake a webhook test for generate_video.
'''

EXPORT_PATH = "~/tmp/test_video.mp4"
USER_PROMPT = "Professor standing in front of a whiteboard."
APP_NAME = "video-generator"

class VideoGenerationTest(LiveServerTestCase):
    def test_video_generation(self):
        webhook_url = f"{self.live_server_url}/webhook/"
        modal_url = f"https://{APP_NAME}.modal.run/create_video_from_text"

        payload = {
            "export_path": "/tmp/test_video.mp4",
            "webhook_url": webhook_url,
            "user_prompt": f"{USER_PROMPT}"
        }

        response = requests.post(modal_url, json=payload)

        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result.get("status"), "pending")

        print("Test Passed! Video generation job started successfully.")