import google.generativeai as genai

genai.configure(api_key="AIzaSyClU1kbMDQSrFpElxtjodJtrPkQraur_8k")

try:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content("Hello")
    print(response.text)
except Exception as e:
    print("Error:", e)
