This folder contains code (packaged into a Docker Container) to auto-label a single image using groundingDino

To run locally:
1. Go to handler.py and uncomment the section to write data to a json file (RunPod expects a 'test_input.json' file when running the script locally)
2. Navigate to the terminal and run `cd inference/RunPod` & `docker-compose up`

To deploy to RunPod:
https://www.notion.so/tapwayops/Deploy-groundingDino-onto-RunPod-1dfb42ac18914222a99b71c278248de5?pvs=4

To test serverless deployment:
1. Create a `.env` file with the env variable `RUNPOD_API_KEY=<your_RunPod_api_key>`
2. Navigate to `test_single.py` to autolabel 1 image or `test_multi.py` to autolabel many images
3. (optional) Put your own image(s) into the folder under `data/samples/` (if using `test_single.py`, make sure to change the `img` variable to your image filename)
4. Navigate to the terminal and run `cd inference/RunPod` & `python3 test_single.py` or `python3 test_multi.py`
5. View your images at `data/output/`

General Info on RunPod:
https://www.notion.so/tapwayops/Research-into-serverless-deployment-providers-31a9caa0875247fc870a68ad9cb9c706?pvs=4
