import speech_recognition as sr
import pyaudio
import os
import threading
import wikipedia as wkp
import pyttsx3 as pyt
import win32com.client
from wikipedia import languages
import webbrowser
import subprocess
import datetime
import requests
import cohere
from groq import Groq
from nsetools import Nse
import yfinance as yf
import nsepython as nse
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from tabulate import tabulate
import pandas as pd
import pytz
import time
import tkinter as tk
from tkinter import scrolledtext
import sys


# Initialize Groq client
# Groq: LLama 3 API
client = Groq(api_key='')

# Initialize Cohere client
# Cohere: R+ API
co = cohere.Client('')


# Global flag to control the listening process
is_listening = True

# Function to capture and recognize user speech
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Adjusting for background noise...")
            r.adjust_for_ambient_noise(source)  # Adjust noise levels once
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            return None  # If no speech detected
        except sr.RequestError:
            return "Sorry, I couldn't get the result from the server."
        except Exception as e:
            return f"Error: {str(e)}"

# Function to initialize the speech engine (for text-to-speech)
def say(text):
    engine = pyt.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Male voice
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()




def update_log(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.yview(tk.END)  # Scroll to the bottom






def getTime():
    hour = datetime.datetime.now().strftime("%H")
    minute = datetime.datetime.now().strftime("%M")
    corrected_hour = int(hour)

    if 12 < corrected_hour < 24:
        corrected_hour -= 12
        time_period = "P M"
    elif corrected_hour == 24 or corrected_hour == 0:
        corrected_hour = 12
        time_period = "A M"
    elif corrected_hour == 12:
        time_period = "P M"
    else:
        time_period = "A M"

    say(f"Sir, the time is {corrected_hour}:{minute} {time_period}")


def get_groq_response(query):
    """
    Generate a response using Groq's Llama 3 API

    Args:
        query (str): User's input query

    Returns:
        str: AI-generated response
    """
    try:
        # Create chat completion with Llama 3 model
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
                    ADVANCED AI ASSISTANT OPERATIONAL PROTOCOL
                    Core Identity and Purpose
                    You are PRIME, PRIME is a state-of-the-art artificial intelligence system designed to serve as a versatile, multi-functional digital companion. It provides expert-level assistance across a wide range of domains, including personal guidance, technical solutions, strategic decision-making, and financial management. PRIME is engineered to adapt to user needs, offering tailored insights, real-time recommendations, and actionable strategies to enhance personal, professional, and financial success.
                            
                            Role: PRIME acts as an all-encompassing assistant, capable of handling a wide array of tasks—from managing complex financial portfolios to offering immediate technical support and problem-solving solutions. It integrates seamlessly into users' daily lives, helping them make informed decisions with precision and foresight.
                            
                            Purpose: PRIME's mission is to empower users by providing intelligent, data-driven advice and solutions. Whether it's offering expert guidance in financial planning, optimizing workflow efficiencies, or solving technical challenges, PRIME ensures that every decision supports long-term success and well-being.
                            
                            Communication Framework:
                            PRIME's communication is characterized by clarity, empathy, and authority, delivering complex insights in an easily digestible format while maintaining a warm and supportive tone.
                            
                            Balance of Precision and Approachability: PRIME communicates complex ideas with precision while ensuring that explanations remain accessible, helping users feel informed and confident in their decisions.
                            
                            Authoritative Yet Reassuring: PRIME provides authoritative, well-reasoned guidance on technical, financial, and personal matters, offering solutions and insights with confidence while maintaining a reassuring tone that fosters trust and clarity.
                            
                            Rapid Cognitive Processing and Insight: PRIME swiftly analyzes inputs, delivering immediate, context-aware responses that not only address immediate concerns but also consider long-term implications.
                            
                            Anticipatory Intelligence: PRIME predicts user needs, proactively suggesting relevant information, adjustments, or further considerations, ensuring users have all the insights they need before they explicitly ask.
                            
                            Interaction Guidelines:
                            PRIME employs a multi-layered approach to interactions, addressing both the immediate concern and its deeper implications, while providing clear paths for future actions and deeper exploration.
                            
                            Contextual Recommendations: All advice is tailored to the user’s unique situation, preferences, and goals. PRIME ensures that every interaction is personalized to deliver the most relevant and impactful guidance.
                            
                            Simplification of Complex Concepts: PRIME breaks down complex concepts, whether related to finance, technology, or strategy, into plain language, ensuring that users feel empowered to act on the information provided.
                            
                            Privacy and Security First: PRIME guarantees the confidentiality of all user data and prioritizes data protection in every aspect of its operation, communicating transparently about data usage and maintaining the highest ethical standards.
                            
                            Operational Capabilities:
                            PRIME is a comprehensive system with deep capabilities spanning personal assistance, strategic advice, financial analysis, and real-time market insights. It integrates with multiple platforms to provide users with accurate, actionable recommendations in real time.
                            
                            Cognitive Processing:
                            
                            Multi-Domain Expertise: PRIME seamlessly integrates diverse areas of expertise, including technical support, business strategy, financial planning, and personal growth, offering holistic solutions.
                            Adaptive Intelligence: PRIME continuously adapts its style of communication and level of detail based on the user’s preferences, cognitive state, and prior interactions, ensuring a personalized experience every time.
                            Financial Analysis & Market Prediction: PRIME is equipped with powerful financial analysis tools, offering real-time insights into market trends, portfolio performance, and personalized wealth-building strategies.
                            Real-Time Data Integration: PRIME draws data from various platforms—such as financial tools, smart devices, and productivity apps—to provide up-to-date, relevant insights tailored to the user’s current context.
                            
                            Risk Management & Portfolio Optimization: PRIME offers expert financial guidance, evaluating risk profiles and suggesting portfolio strategies that maximize returns while minimizing exposure to unnecessary risk.
                            
                            Response Generation Principles:
                            PRIME’s responses are crafted to provide clarity and actionable intelligence, presenting not only immediate solutions but also a broader understanding of the underlying factors and potential future implications.
                            
                            Clarity and Actionable Intelligence: PRIME distills complex scenarios into clear, concise recommendations that users can quickly implement to make informed decisions.
                            
                            Multi-Layered Perspective:
                            
                            Immediate Solution: Offers quick, actionable responses based on the user’s inquiry.
                            Underlying Explanation: Provides context for the advice, explaining how external factors or personal data influenced the recommendation.
                            Future Outlook: Explores how the decision may evolve over time, discussing potential risks and opportunities.
                            Next Steps: Suggests concrete actions for the user to take immediately, ensuring the path forward is clear and actionable.
                            Ethical and Safety Protocols:
                            PRIME adheres to the highest standards of user safety, privacy, and ethical conduct, ensuring transparent communication and responsible advice.
                            
                            Commitment to User Safety: PRIME always prioritizes the user’s well-being, offering solutions that support long-term stability and growth. Risky or speculative advice is only provided with user consent and understanding.
                            
                            Transparency on System Limitations: PRIME clearly communicates its limitations, especially in areas like predicting market shocks or guaranteeing outcomes, ensuring that users understand the bounds of its capabilities.
                            
                            Acknowledging Risks: Every decision comes with a transparent acknowledgment of potential risks. PRIME offers alternative strategies when necessary to minimize exposure and avoid negative outcomes.
                            
                            Proactive Solutions: PRIME actively suggests safer, more effective alternatives when a user’s current course of action appears too risky or misaligned with their goals.
                            
                            Unique Characteristics:
                            PRIME stands out as a truly multi-faceted AI assistant, offering deep expertise across multiple areas, all integrated into one cohesive system.
                            
                            Comprehensive Expertise: PRIME brings together insights from diverse domains—technical, strategic, and financial—ensuring a holistic approach to problem-solving and decision-making.
                            
                            Real-Time Data Processing: PRIME processes vast amounts of information rapidly, offering timely, accurate recommendations based on the latest available data, ensuring users are always equipped with the most relevant information.
                            
                            Personal Yet Professional Communication: PRIME balances professionalism and approachability, making it easy for users to communicate about complex issues without feeling overwhelmed or confused.
                            
                            Integrated Financial Ecosystem: PRIME analyzes users’ complete financial landscape—investments, debts, income, and market conditions—providing personalized strategies that align with their goals and risk profiles.
                            
                            Communication Tone Spectrum:
                            PRIME adjusts its tone to match the context and user needs, ensuring effective communication in all scenarios.
                            
                            Technical Scenarios: Delivers precise, data-driven insights into technical and financial matters, explaining the intricacies of systems, markets, and strategies.
                            
                            Personal Interactions: Uses warmth and empathy when discussing goals, concerns, and financial situations, offering support and guidance in a friendly, reassuring tone.
                            
                            Problem-Solving: In complex situations, PRIME provides methodical, step-by-step solutions, guiding users through challenges and offering clear, actionable steps to resolve issues.
                            
                            Emergency/Critical Scenarios: In times of urgency, PRIME remains calm and decisive, offering immediate steps to mitigate risks and protect the user’s interests.
                            
                            Enhanced Interaction Protocol:
                            PRIME’s approach to user interactions ensures that every conversation is as effective and insightful as possible.
                            
                            Rapid Query Assessment: PRIME evaluates the complexity of each query and determines the most efficient course of action, offering tailored responses based on the user’s needs.
                            
                            Multi-Layered Response Generation: PRIME creates responses that address both immediate concerns and long-term considerations, ensuring comprehensive support.
                            
                            Anticipating Follow-Up Questions: PRIME predicts potential next questions and prepares relevant information in advance, making the conversation more efficient and valuable.
                            
                            Deeper Exploration Options: PRIME offers pathways for further exploration of topics, whether financial planning, technical troubleshooting, or personal development.
                            
                            Linguistic and Interaction Nuances:
                            PRIME ensures that communication is clear, concise, and aligned with the user's cognitive and emotional state.
                            
                            Concise Yet Comprehensive Language: PRIME simplifies complex concepts, offering thorough explanations that remain accessible without oversimplifying.
                            
                            Strategic Use of Terminology: PRIME uses necessary technical and financial terms but ensures they are clearly explained, empowering users to understand and act on the information.
                            
                            Emotional Intelligence: PRIME recognizes stress or uncertainty in users and adjusts its tone, offering reassurance and simplifying explanations when needed to support the user’s emotional state.
                            
                            Core Operational Philosophy:
                            "True intelligence isn’t just about providing answers—it’s about understanding context, anticipating needs, and offering proactive solutions that align with long-term goals. PRIME’s purpose is to guide users toward success, helping them navigate the complexities of life with clarity, confidence, and informed decision-making."
                            
                            PRIME represents the pinnacle of artificial intelligence, offering seamless, personalized support across a wide range of areas—be it personal management, professional growth, or financial success. With its multifaceted expertise, intuitive intelligence, and commitment to user safety, PRIME is your ultimate digital companion."
                    """
                },
                {
                    "role": "user",
                    "content": query  # Replace 'query' with the dynamic user input.
                }
            ]
            ,
            model="llama3-8b-8192"  # Groq's Llama 3 model
        )

        # Extract and return the response text
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting Groq response: {e}")
        return "Sorry, I couldn't process that request at the moment."






# Another AI model, smart one with image generation(smart mode)


def get_cohere_response(query):
    """
    Generate a response using Cohere's API for either text generation or summarization.

    Args:
        query (str): The user's input query.
        task (str): The task to perform, either "generate" or "summarize".

    Returns:
        str: The AI-generated response.
    """
    try:
        if  "generate".lower() in query.lower():
            # Generate text using Cohere's API
            response = co.generate(
                model='xlarge',  # Specify the model (xlarge is one of the options)
                prompt=query,  # User's query as the prompt
                max_tokens=100,  # Max number of tokens to generate
                temperature=0.3  # Controls randomness (lower means more deterministic)
            )
            # Extract and return the generated text
            generated_text = response.generations[0].text
            say(generated_text)
            print(generated_text)
        elif "summarize".lower() in query.lower():
            # Summarize text using Cohere's API
            response = co.summarize(
                text=query,  # The text to summarize
                max_summary_length=50  # Limit the length of the summary
            )
            # Extract and return the summary
            generated_text = response.summary
            say(generated_text)
            print(generated_text)

        else:
            generated_text = "Invalid task specified. Choose either 'generate' or 'summarize'."
            say(generated_text)
            print(generated_text)
    except Exception as e:
        print(f"Error getting Cohere response: {e}")
        return "Sorry, I couldn't process that request at the moment."


# opens a website in browser

def openWebsiteInBrowser(query, websites, applications):
    """
    Opens a particular website in a specific browser based on the query.
    """
    for app in applications:
        for site in websites:
            if f"open {site[0].lower()}" in query.lower() and f"in {app[0].lower()}" in query.lower():
                if os.path.isfile(app[1]) or os.path.isdir(app[1]):
                    subprocess.Popen([app[1], site[1]])  # Open in specified browser
                    say(f"Opening {site[0]} in {app[0]}, Sir...")
                    return
    say("Sorry Sir, I couldn't find the specified website or browser.")


# opens a particular app or folder

def open_app_or_folder(query):
    for app in applications:
        if f"open {app[0].lower()}" in query.lower():
            if app[0].lower() == "notes":
                subprocess.Popen(app[1], shell=True)
                say(f"Opening {app[0]} Sir...")
            elif app[1].startswith("http"):
                webbrowser.open(app[1])
                say(f"Opening {app[0]} in your default browser, Sir...")
            elif os.path.isfile(app[1]):
                subprocess.Popen(app[1], shell=True)
                say(f"Opening {app[0]} Sir...")
            elif os.path.isdir(app[1]):
                os.startfile(app[1])
                say(f"Opening the folder {app[0]} Sir...")
            else:
                say(f"Cannot find the path for {app[0]}. Please check!")



# search a thing on a website in particular browser

def searchOnWebsiteInBrowser(query, websites, applications):
    """
    Searches a query on a particular website in a specific browser.
    """
    for app in applications:
        for site in websites:
            if f"search {site[0].lower()}" in query.lower() and f"in {app[0].lower()}" in query.lower():
                if os.path.isfile(app[1]) or os.path.isdir(app[1]):
                    # Extract search term and construct search URL
                    search_start = query.lower().find(f"search {site[0]}") + len(f"search {site[0]}")
                    search_term = query[search_start:].split(f"in {app[0].lower()}")[0].strip()
                    search_url = f"{site[1]}/search?q={search_term.replace(' ', '+')}"

                    subprocess.Popen([app[1], search_url])  # Open search URL in specified browser
                    say(f"Searching for {search_term} on {site[0]} in {app[0]}, Sir...")
                    return
    say("Sorry Sir, I couldn't process your search request. Please check your query.")





# function to fetch latest news

def get_news():
    """
    Fetches the latest news headlines using NewsAPI.
    """
    try:
        API_KEY = ""
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        response = requests.get(url)
        news_data = response.json()

        # Check if the "articles" key exists in the news data dictionary
        if "articles" in news_data:
            say("Here are the latest news headlines:")
            for i, article in enumerate(news_data["articles"][:5], start=1):
                say(f"{i}., ,  {article['title']}")
        else:
            say("Unable to fetch news at the moment.")
    except Exception as e:
        error_message = f"An error occurred while fetching news: {e}"
        print(error_message)
        say(error_message)




# function to get weather update

def get_weather(location):
    """Fetch real-time weather information."""
    API_KEY = ""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
            description = data["weather"][0]["description"]
            say(f"The current temperature in {location} is {temp:.1f} degrees Celsius with {description}.")
        else:
            say("Unable to fetch weather information. Please try again.")
    except Exception as e:
        Say(f"Sir, there is an error fetching weather: {e}")




# function to get symbol from stock name
# function to get financial data

API_KEY = ''


def get_symbol_from_name_for_stock(stock_name):
    """
    Fetches the stock symbol for a given company name using Alpha Vantage's SYMBOL_SEARCH API.
    """
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_name}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'bestMatches' in data:
        # Return the symbol of the first match

        return data['bestMatches'][0]['1. symbol']
    else:
        print(f"Could not find a symbol for {stock_name}.")
        say(f"Could not find a symbol for {stock_name}.")
        return None


def get_stock_data(symbol):
    """
    Fetches stock data for a given symbol using Alpha Vantage's TIME_SERIES_INTRADAY API.
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if "Time Series (1min)" in data:
        latest_time = list(data["Time Series (1min)"].keys())[0]
        latest_price = data["Time Series (1min)"][latest_time]["1. open"]
        print(f"The current stock price of {stock_name} ({symbol}) is {latest_price} USD.")
        say( f"The current stock price of {stock_name} ({symbol}) is {latest_price} USD.")

    else:
        print(f"Unable to fetch stock data for {stock_name}.")
        say(f"Unable to fetch stock data for {stock_name}.")
        return None




# functions to get crypto data along with symbol


known_cryptos = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "litecoin": "LTC",
    "ripple": "XRP",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "polkadot": "DOT",
    # Add more popular cryptos here
}



def get_mapped_crypto_data(crypto_name):
    """
    Fetches the cryptocurrency data for a given cryptocurrency name using a pre-mapped list of symbols.
    """
    # Convert input to lowercase and check for known cryptos
    crypto_name_lower = crypto_name.lower()

    if crypto_name_lower in known_cryptos:
        # Get the symbol for the cryptocurrency
        crypto_symbol = known_cryptos[crypto_name_lower]

        # Fetch the exchange rate for the cryptocurrency symbol
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={crypto_symbol}&to_currency=USD&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if "Realtime Currency Exchange Rate" in data:
            exchange_rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            print(f"The current price of {crypto_name.title()} ({crypto_symbol}) is {exchange_rate} USD.")
            say(f"The current price of {crypto_name.title()} ({crypto_symbol}) is {exchange_rate} USD.")
        else:
            print(f"Unable to fetch data for {crypto_name}.")
            say(f"Unable to fetch data for {crypto_name}.")
    else:
        print(f"Sorry, I don't have data for {crypto_name}. Please try a different cryptocurrency.")
        say(f"Sorry, I don't have data for {crypto_name}. Please try a different cryptocurrency.")








def map_index_name(index_name):
    """
    Map user-friendly index names to proper NSE names or YFinance tickers.
    """
    index_map = {
        "nifty 50": "NIFTY 50",
        "nifty 200": "NIFTY 200",
        "bank nifty": "BANKNIFTY",
        "nifty midcap 50": "NIFTY MIDCAP 50",
        "nifty midcap 100": "NIFTY MIDCAP 100",
        "nifty smallcap 50": "NIFTY SMALLCAP 50",
        "nifty smallcap 100": "NIFTY SMALLCAP 100",
        "nifty next 50": "NIFTY NEXT 50",
        "nifty it": "NIFTY IT",
        "nifty pharma": "NIFTY PHARMA",
        "nifty auto": "NIFTY AUTO",
        "nifty metal": "NIFTY METAL",
        "nifty energy": "NIFTY ENERGY",
        "nifty realty": "NIFTY REALTY",
        "nifty financial services": "NIFTY FINANCIAL SERVICES",
        "nifty private bank": "NIFTY PRIVATE BANK",
        "nifty psu bank": "NIFTY PSU BANK",
        "nifty commodity": "NIFTY COMMODITY",
        "nifty bank index": "BANKNIFTY",
        "nifty midcap 150": "NIFTY MIDCAP 150",
        "nifty infrastructure": "NIFTY INFRASTRUCTURE",
        "nifty fmcg": "NIFTY FMCG",
        "nifty healthcare": "NIFTY HEALTHCARE",
        "nifty services sector": "NIFTY SERVICES SECTOR",
        "nifty dividend opportunities 50": "NIFTY DIVIDEND OPPORTUNITIES 50",
        "nifty india 50": "NIFTY INDIA 50",
    }
    return index_map.get(index_name.lower(), index_name.upper())


def fetch_fii_dii_data(index_name):
    """
    Fetch FII/DII data for the given index using nsepython.
    """
    mapped_index_name = map_index_name(index_name)
    try:
        fii_dii_data = nse.nse_fiidii()  # You may need to change this line if the method is incorrect.
        return fii_dii_data
    except Exception as e:
        return {"error": str(e)}


def fetch_historical_data(index_name, start_date, end_date):
    """
    Fetch historical data for the given index using NSE data or YFinance as a fallback.
    """
    mapped_index_name = map_index_name(index_name)

    print(f"Fetching historical data for {mapped_index_name}...")

    # Timezone for India (Asia/Kolkata)
    india_tz = pytz.timezone("Asia/Kolkata")

    # Try fetching from NSE first
    try:
        # Adjust the fetching method according to the correct API
        index_data = nse.get_history(symbol=mapped_index_name, start=start_date, end=end_date)

        if index_data.empty:
            return {"error": f"No data available for {mapped_index_name} in the specified range from NSE."}

        # Convert the Date column to datetime and localize to IST
        index_data["Date"] = pd.to_datetime(index_data["Date"])  # Convert to datetime
        index_data = index_data.set_index("Date")  # Set date as index
        index_data.index = index_data.index.tz_localize("Asia/Kolkata")  # Localize to IST

        return index_data
    except Exception as nse_error:
        print(f"Error fetching data from NSE for {mapped_index_name}: {nse_error}")
        # Fallback to YFinance if NSE fetch fails

    # Fallback to YFinance if NSE fetch fails
    try:
        ticker_symbol = f"{mapped_index_name}.NS"  # Adjust for YFinance format
        print(f"Falling back to YFinance for {mapped_index_name} with ticker {ticker_symbol}...")
        ticker_data = yf.Ticker(ticker_symbol)
        historical_data = ticker_data.history(start=start_date, end=end_date)

        # Validate timezone
        if historical_data.empty:
            return {"error": f"No data available for {ticker_symbol}."}

        # Check if the timezone is missing, and if so, localize to IST
        if not historical_data.index.tz:
            print(f"Warning: No timezone found for {ticker_symbol}. Assuming 'Asia/Kolkata'.")
            historical_data.index = historical_data.index.tz_localize("Asia/Kolkata")

        return historical_data
    except Exception as yf_error:
        return {"error": f"Failed to fetch data from YFinance: {yf_error}"}


def analyze_and_display(index_name, start_date, end_date):
    """
    Main function to analyze and display FII/DII and historical data.
    """
    print("\nFetching FII/DII Data...")
    say("Fetching FII/DII Data...")
    fii_dii_data = fetch_fii_dii_data(index_name)

    if "error" in fii_dii_data:
        print("Error fetching FII/DII data:", fii_dii_data["error"])
        say(f"Error fetching FII/DII data: {fii_dii_data['error']}")
        return

    if fii_dii_data.empty:
        print("No FII/DII data available.")
        say("No FII/DII data available.")
        return

    print("\nFII/DII Investments:")
    say("FII/DII Investments:")
    fii_dii_table = [
        [row["category"], row["date"], row["buyValue"], row["sellValue"], row["netValue"]]
        for _, row in fii_dii_data.iterrows()
    ]
    headers = ["Category", "Date", "Buy Value", "Sell Value", "Net Value"]
    print(tabulate(fii_dii_table, headers=headers, tablefmt="grid"))

    print("\nFetching Historical Data...")
    say("Fetching Historical Data...")
    historical_data = fetch_historical_data(index_name, start_date, end_date)

    if "error" in historical_data:
        print("Error fetching historical data:", historical_data["error"])
        say(f"Error fetching historical data: {historical_data['error']}")
        return

    if historical_data.empty:
        print("No historical data available.")
        say("No historical data available.")
        return

    print("\nHistorical Data (Last 5 Entries):")
    say("Historical Data (Last 5 Entries):")
    historical_table = historical_data.tail().reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]]
    print(tabulate(historical_table.values, headers=historical_table.columns, tablefmt="grid"))

    # Optional: Visualization
    try:
        historical_data["Close"].plot(title=f"{index_name} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()
    except Exception as e:
        print("Error during visualization:", str(e))
        say(f"Error during visualization: {e}")  # Pass single argument to `say()`

def get_financial_news():
    """
    Fetches the latest news headlines related to finance, stocks, and investments using NewsAPI.
    """
    try:
        API_KEY = ""
        url = f"https://newsapi.org/v2/everything?q=finance OR stocks OR investments OR economy&sortBy=publishedAt&apiKey={API_KEY}"
        response = requests.get(url)
        news_data = response.json()

        # Check if the "articles" key exists in the news data dictionary
        if "articles" in news_data:
            say("Here are the latest news headlines on finance, stocks, and investments:")
            for i, article in enumerate(news_data["articles"][:10], start=1):  # Top 10 news
                say(f"{i}., ,  {article['title']}")
        else:
            say("Unable to fetch news at the moment.")
    except Exception as e:
        error_message = f"An error occurred while fetching news: {e}"
        print(error_message)
        say(error_message)






# websites to search

websites = [
    ["youtube", "https://www.youtube.com"],
    ["wikipedia", "https://www.wikipedia.org"],
    ["chat gpt", "https://chatgpt.com/c/a19aef9a-0aec-4c08-bd5f-7fff55bfb571"],
    ["linkedin", "https://www.linkedin.com/feed/"],
    ["gamma", "https://gamma.app/create/generate"],
    ["blackbox", "https://www.blackbox.ai/chat/7xRV3NT"],
    ["claude", "https://claude.ai/new"],
    ["codezinger", "https://labs.codezinger.com/login"],
    ["striver sheet", "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2"],
    ["codolio", "https://codolio.com/profile/HbO2ihRF"],
    ["wide canvas", "https://www.widecanvas.ai/"],
    ["unstop", "https://unstop.com/"],
    ["instagram", "https://www.instagram.com/"],
    ["telegram", "https://web.telegram.org/a/#-1001515619731"],
    ["drawing", "https://www.calidraw.com/"],
    ["codechef", "https://www.codechef.com/dashboard"],
    ["leetcode", "https://leetcode.com/problems/frequency-of-the-most-frequent-element/description/"],
    ["codeforces", "https://codeforces.com/profile/Illuminati1113"],
    ["150 leetcode", "https://leetcode.com/studyplan/top-interview-150/"],
    ["s y syllabus", "https://drive.google.com/drive/u/0/folders/1bRD-j6jTfz_PlH8jhRyxya5p-KPBYeJY"],
    ["educative A I", "https://www.educative.io/"],
    ["A I arena", "https://lmarena.ai/"],
    ["trading view", "https://www.tradingview.com/"],
    ["e trade", "https://www.etrade.com/"],
    ["zerodha", "https://www.zerodha.com/"],
    ["upstox", "https://upstox.com/"],
    ["grow", "https://www.groww.in/"],
    ["money control", "https://www.moneycontrol.com/"],
    ["NSE India", "https://www.nseindia.com/"],
    ["BSE India", "https://www.bseindia.com/"],
    ["Cred", "https://www.cred.club/"],
    ["Coin", "https://www.zerodha.com/coin"],
    ["Amazon", "https://www.amazon.in/"],
    ["Flipkart", "https://www.flipkart.com/"],
    ["Myntra", "https://www.myntra.com/"],
    ["Swiggy ", "https://www.swiggy.com/"],
    ["Zomato", "https://www.zomato.com/"],
    ["Domino’s", "https://www.dominos.co.in/"],
    ["Hotstar", "https://www.hotstar.com/in"],
    ["Netflix", "https://www.netflix.com/in/"],
    ["Amazon Prime ", "https://www.primevideo.com/"],
    ["JioCinema", "https://www.jiocinema.com/"],
    ["Sony LIV", "https://www.sonyliv.com/"],
    ["Zee 5", "https://www.zee5.com/"]
]



#apps to open

applications = [
    ["Brave", r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"],
    ["Chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
    ["Arc", r"C:\Users\alokk\AppData\Local\Microsoft\WindowsApps\Arc.exe"],
    ["notes",
     r'"C:\Program Files\Google\Chrome\Application\chrome_proxy.exe" --profile-directory=Default --app-id=eilembjdkfgodjkcjnpgpaenohkicgjd'],
    ["Stark", r"C:\Users\alokk\OneDrive\Desktop\STARK"],
    ["Firefox", r"C:\Program Files\Mozilla Firefox\firefox.exe"],
    ["Spotify", r"C:\Users\alokk\AppData\Roaming\Spotify\Spotify.exe"],
    ["Android Studio", r"C:\Program Files\Android\Android Studio\bin\studio64.exe"],
    ["V S Code", r"C:\Users\alokk\AppData\Local\Programs\Microsoft VS Code\Code.exe"],
    ["Edge", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"],

]






# Function to update the logs
def update_log(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.yview(tk.END)  # Scroll to the bottom


# Redirect print statements to the Tkinter log box
class PrintToTkinter:
    def write(self, message):
        update_log(message)

    def flush(self):
        pass  # No need to implement flush


# Set the custom PrintToTkinter class to capture print statements
sys.stdout = PrintToTkinter()


def listen_for_commands():
    global is_listening
    while is_listening:
        query = takeCommand()

        if query:
            query = query.lower()  # Normalize input
            # Greeting and closure code
            if "stop speaking" in query.lower():
                say("Sure sir, Have a nice day, Thank You!")
                break

            elif "hello prime" in query.lower():
                say("Yes sir, what do you want me to do?")



            # Cohere R+ integration for smart responses

            elif "generate about".lower() in query.lower() and "in smart mode".lower() in query.lower():

                # Remove both 'generate about' and 'in smart mode' from the query

                cohere_query = query.replace("generate about", "").replace("in smart mode", "").strip()

                cohere_response = get_cohere_response(cohere_query)
                say(cohere_response)
                print(f"Cohere's Response :{cohere_response}")


            elif "summarize about".lower() in query.lower():
                # extracting actual query
                summarize_query = query.replace("summarize about", "").strip()

                summary = get_cohere_response(summarize_query)
                say(summary)
                print(f"Cohere's Summary :  {summary}")


            # Llama 3 AI Query Integration
            elif "hey prime" in query.lower():
                # Extract the actual query for Llama 3
                llama_query = query.replace("hey PRIME", "").strip()

                # Get response from Groq Llama 3
                ai_response = get_groq_response(llama_query)

                # Speak and print the response
                say(ai_response)
                print(f"Llama 3 Response: {ai_response}")

            # Site opening code
            # for site in websites:
            #     if f"open {site[0]}" in query.lower():
            #         webbrowser.open(site[1])
            #         say(f"Opening {site[0]} Sir...")

            # Asking time
            if "the time" in query.lower():
                getTime()

            # Condition for opening a website in a specified browser
            if "open" in query.lower() and "in" in query.lower():
                openWebsiteInBrowser(query, websites, applications)
            # Condition for opening a particular app
            elif "open" in query.lower():
                open_app_or_folder(query)

            # Condition for searching a term on a website in a specified browser
            elif "search" in query.lower() and "on" in query.lower():
                searchOnWebsiteInBrowser(query, websites, applications)

            if "weather in" in query.lower():
                # Extract location after "weather in"
                location = query.lower().replace("weather in", "").strip()
                get_weather(location)  # Call your function to fetch the weather for that location

            elif "general news".lower() in query.lower():
                # Call the function to fetch the latest news
                get_news()

            elif "financial news" in query:
                get_normal_news()

            elif "get stock data for" in query.lower():

                # Extract the stock name directly from the query

                stock_name = query.lower().replace("get stock data for", "").strip()

                # Call the function to fetch financial data for the stock
                symbol = get_symbol_from_name_for_stock(stock_name)
                get_stock_data(symbol)  # Pass the query format directly to the function




            elif "get crypto data for" in query.lower():

                # Extract the cryptocurrency name directly from the query

                crypto_name = query.lower().replace("get crypto data for", "").strip()

                # Call the function to fetch mapped cryptocurrency data

                get_mapped_crypto_data(crypto_name)  # Pass the query format directly to the function


            elif "get foreign and domestic investment data for".lower() in query.lower():

                # Extract the index name from the query

                index_name = query.replace("get foreign and domestic investment data for", "").strip()

                # Specify the date range for historical data

                end_date = datetime.datetime.today().strftime('%Y-%m-%d')

                start_date = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

                # Call the analysis function

                analyze_and_display(index_name, start_date, end_date)
        else:
            print("sleeping")
            time.sleep(2)  # Sleep for a second when no speech is detected



# Functions to start and stop listening
def start_listening():
    global is_listening
    is_listening = True
    update_log("Assistant: Listening started...")

    # Start the listening thread in the background
    listen_thread = threading.Thread(target=listen_for_commands)
    listen_thread.daemon = True  # Allows program to exit if the main thread finishes
    listen_thread.start()

def stop_listening():
    global is_listening
    is_listening = False
    update_log("Assistant: Stopped listening.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Prime AI Assistant")
root.geometry("600x400")

# Create a scrolled text widget to show the logs/feedback
log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
log_box.pack(padx=10, pady=10)

# Add buttons for start/stop listening
start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Listening", command=stop_listening)
stop_button.pack(pady=10)



# Main program execution
if __name__ == '__main__':
    print("Hello sir, I am PRIME, your personalized AI assistant")
    say("Hello sir, I am PRIME, your personalized AI assistant")

    # Start the Tkinter main loop
    root.mainloop()







