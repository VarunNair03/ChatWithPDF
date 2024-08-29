# This is an app for communicating with your PDFs

After cloning make sure you install the requirements mentioned in the requirements.txt by running the following command
```shell
pip install -r requirments.txt
```

Once installed you can run the app using the following command

```shell
streamlit run chatbot.py
```

Ensure that you have your environment variables setup in the following manner:

```env
GOOGLE_API_KEY = <your api key>
```

Currently I'm using google's gemini but you can switch that for any llms. 