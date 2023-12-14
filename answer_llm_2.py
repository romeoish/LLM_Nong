import requests

class CompletionExecutor:
    def _send_request(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8'
        }

        # Initialize result variable
        result = None

        try:
            # Use requests.post for making an HTTP POST request
            # Base model /testapp/v1/chat-completions/HCX-002
            # Tunning model
            response = requests.post(
                f"{self._host}/testapp/v1/chat-completions/HCX-002",
                headers=headers, json=completion_request, stream=False
            )

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                result = response.json()
            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.RequestException as e:
            # Handle exceptions, log, or raise accordingly
            print(f"Request failed: {e}")

        return result


    def execute(self, completion_request):
        res = self._send_request(completion_request)

        if res['status']['code'] == '40103':
            # Check whether the token has expired and reissue the token.
            self._access_token = None
            return self.execute(completion_request)
        elif res['status']['code'] == '20000':
            return res['result']['message']['content']
        else:
            return 'Error'
        
def answer_llm2(user_text):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY2W+zUGmm5SHgsDJBy5F7SFNuVY1tJcJTyhUXLrTnekZA/u1pZ4oBJHvLUdIsvlF7IuPFlGGtnb832hcmD+YIJbrR9NUMFBsJ5TMyrl94jBAQ2amx/sFbZWnHAsqeuxxWMkUq0qXdhIUJ/VMhvlGCacQtF6NOAIpnGFb+7MURctOL5RYpMpwUwrB2LEgz8CMbWMKLGxpeliSD1a7IYTafiU=',
        api_key_primary_val='UBwKtmApo6wH5wCrtUtp7AqxpnkNC9aLSWvxFNSE',
        request_id='2a83d1218c534c27a648616e64ed9abb'
    )

    preset_text = [{"role":"system","content":"-주어진 [정보]들을 읽고 [질문]에 답변을 작성해줘\n-주어진 [정보]에서만 답변을 만들어줘\n-[질문]에 대해서만 답변해\n-[질문]에 해당되는 정보가 없으면 질문에 해당되는 정보가 없다고 대답해줘"},
                   {"role":"user","content": user_text}]
    
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 1000,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }

    response_text = completion_executor.execute(request_data)
    return response_text