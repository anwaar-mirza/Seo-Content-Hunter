import sys
import asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
import streamlit as st
from dotenv import load_dotenv
from brain import AIAgent
from essentials import prompt_templete,divide_list
from crawling import WebCrawler
from request_content import GetContentByRequest
import time

load_dotenv()

if "initilize" not in st.session_state:
    st.session_state.results = []
    st.session_state.bot = None
    st.session_state.crawl = None
    st.session_state.content = None
    st.session_state.initilize = True


st.set_page_config(
    page_title="🔍 SEO Contact Hunter | Find Emails & Phone Numbers Fast",
    page_icon="📧",
    layout="wide"
)


st.title("🔍 SEO Contact Hunter")
st.caption("🚀 Turn any keyword into a list of **verified emails & phone numbers** — perfect for outreach and lead generation.")
st.markdown("---")
groq_api = st.text_input("🔑 Enter Your GROQ API Key", type="password", placeholder="Paste your API key here...")
if groq_api:
    st.session_state.bot = AIAgent(GROQ_API_KEY=groq_api, prompt_templete=prompt_templete)
    st.session_state.crawl = WebCrawler(serp_api="929816dd33654e829640437a7c729e5e105885c36683d39fb8912980b3c0bd3e")
    st.session_state.content = GetContentByRequest()
    search_box = st.text_input(
        "💡 Enter a Keyword or Niche",
        placeholder="e.g., digital marketing agencies in New York"
    )
    if search_box:
        # search_box = search_box.lower().replace(" ", "+")
        with st.spinner("🕵️ Crawling the web and gathering contacts... Please wait"):
            # st.session_state.crawl.handle_threading(keyword=search_box)
            st.session_state.crawl.serp_api_search(search_box)
            fr = [_result['link'] for _result in st.session_state.crawl.final_results]
            fr = [r for r in fr if "google.com" not in r and "youtube.com" not in r and "linkedin.com" not in r and "facebook.com" not in r and "twitter.com" not in r and "instagram.com" not in r and "tiktok.com" not in r]
            fr = [r.split('?')[0] if "?" in r else r for r in fr]
        st.text_area(
            "📋 Web Crawling Results",
            value='\n'.join(fr),
            height=300
        )
        fr = list(set(fr))
        st.write(f"✅ {len(fr)} unique results found.")
        scraped_results = ["start"]
        for idx, link in enumerate(fr):
            sp = [str(s) for s in scraped_results]
            text_content = st.session_state.content.get_content(link)
            if text_content:
                ai_result = st.session_state.bot.get_final_response(query=text_content)
                scraped_results.append(ai_result)
            time.sleep(1)
            st.text_area(
            f"📋 Final Results for {link}",
            value=str(scraped_results[-1]),
            height=300,
            key=f"text_area_{idx}"
            )



            

