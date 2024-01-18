import ray
from ray import serve
from fastapi import FastAPI
app = FastAPI()
from textblob import TextBlob

serve.start(http_options= { 
    "host": "0.0.0.0", 
    "port": "8000"
})

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 1})
class RAYFastAPIDeployment:
    
    @app.get("/check")
    def __call__(self, request):
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

app = RAYFastAPIDeployment.bind()
serve.run(app)
