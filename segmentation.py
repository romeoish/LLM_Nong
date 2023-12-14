import base64
import json
import http.client

class CompletionExecutor_Seg:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/segmentation/004adffde5124bc1b4c822536d8d843c', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']['topicSeg']
        else:
            return 'Error'

def segmentation_text(text):
    completion_executor = CompletionExecutor_Seg(
        host='clovastudio.apigw.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY1aM5JpMNr1vYMQHOi/ifhUlI8DadYG/B7WrQXcfae6ENwjhBlll1AfPSjNxQOF/HhEZpbXGKTf1Y1EX7/36ZJ6fmTWKTIE6imyNWI4tsF/du7EUTA6y99vfE2aK6kDca/EYCCa5wKQkPf21VDUi0X5wPDIJyIVVT8eTausRz5/f',
        api_key_primary_val = 'UBwKtmApo6wH5wCrtUtp7AqxpnkNC9aLSWvxFNSE',
        request_id='2195cf44a6454fd39d25dbc84eb1c5de'
    )

    request_data = json.loads(
        f'{{"text":"{text}","alpha":-100.0,"segCnt":-1,"postProcess":true,'
        f'"postProcessMaxSize":600,"postProcessminSize":300}}', strict=False)

    response_text = completion_executor.execute(request_data)
    return response_text