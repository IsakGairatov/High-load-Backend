from locust import HttpUser, task, between

class FileUploadUser(HttpUser):
    wait_time = between(1, 2)
    headers = {
        "Authorization": "Bearer <>"
    }

    @task
    def upload_file(self):
        files = {'file': open('text.txt', 'rb')}
        self.client.post('upload/', files=files)
