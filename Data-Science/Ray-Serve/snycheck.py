import ray
from ray import serve
from textblob import TextBlob
from ray.serve.handle import RayServeSyncHandle
import os
os.environ["RAY_SERVE_USE_NEW_HANDLE_API"]="1"

# runtime_env = {"pip": ["textblob"], "env_vars":{"HTTP_PROXY": "http://10.78.90.46:80", "HTTPS_PROXY": "http://10.78.90.46:80", "http_proxy": "http://10.78.90.46:80", "https_proxy": "http://10.78.90.46:80"}}
# ray.init(address="ray://kuberay-head-svc.kuberay:10001", ignore_reinit_error=True, runtime_env=runtime_env)

ray.init(address="ray://kuberay-head-svc.kuberay:10001", ignore_reinit_error=True)
serve.start(http_options= { 
    "host": "0.0.0.0", 
    "port": "8000"
})

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 2})
class RayServeSyncHandleDeployment:
    async def __call__(self, request):
        try:
            from textblob import TextBlob
            import traceback
            if request.query_params["input_text"] != None:
                text = request.query_params["input_text"]
            else:
                text = '''
            The titular threat of The Blob has always struck me as the ultimate movie
            monster: an insatiably hungry, amoeba-like mass able to penetrate
            virtually any safeguard, capable of--as a doomed doctor chillingly
            describes it--"assimilating flesh on contact.
            Snide comparisons to gelatin be damned, it's a concept with the most
            devastating of potential consequences, not unlike the grey goo scenario
            proposed by technological theorists fearful of
            artificial intelligence run rampant.
            '''
            blob = TextBlob(text)
            blob.tags
            blob.noun_phrases
            res = list()
            for sentence in blob.sentences:
                res.append(sentence.sentiment.polarity)
            return res
        except Exception as error:
            print("Exception", error)
            print(traceback.format_exc())

app = RayServeSyncHandleDeployment.bind()
handle: RayServeSyncHandle = serve.run(app,host="0.0.0.0",port="8000")