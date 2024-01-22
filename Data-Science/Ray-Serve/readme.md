## Please follow the steps to run this ray serve experiment on you environment

## Follow the guidelines to understand kernel experiment:

1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image or any image, initialize Jupiter notebook service.
3. Choice the kernel RAY
3. Import all required packages, user define functions, initialize global objects. 
    NOTE: To activate the customized RAY kernel please follow the below steps
    1. open the bash
    2. run the command " jupyter kernelspec list"
    3. choice the RAY kernel path
    4. cat kernel.json
    5. select only the "source /opt/conda/etc/profile.d/conda.sh && conda activate ray", paste in bash and press enter. the follow the bellow points.
    6. source /opt/conda/etc/profile.d/conda.sh && conda activate ray
    7. pip list
    8. export HTTP_PROXY="http://10.78.90.46:80" && export HTTPS_PROXY="http://10.78.90.46:80" && export https_proxy="http://10.78.90.46:80" && export http_proxy="http://10.78.90.46:80"
    FYI, if the serving notebook not working as expected please run the following commands on top of HEAD Node and Worker Node:
    9. pip install TextBlob
    10. python -m textblob.download_corpora
4. Procure serving files "check.py" and "snycheck.py" same location where notebook persisted, once the files are loaded successfully
5. run the notebook.
10. Reference and Conclusion I have updated the real-world statistics and survey details, have a look.

## Reference:
https://docs.ray.io/en/latest/serve/index.html