# agent_logic.py

from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub # <-- ADD THIS IMPORT

# Impor klien yang sudah diinisialisasi dari config.py
from config import llm, exa_client, GOOGLE_API_KEY

# === TOOLS DEFINITION ===

@tool
def describe_image(image_b64: str) -> str:
    """
    Menerima gambar dalam format base64 string dan mengembalikan deskripsi teks dari makanan di gambar.
    Gunakan alat ini pertama kali untuk mengidentifikasi nama makanan dari gambar.
    """
    vision_llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key=GOOGLE_API_KEY)
    msg = vision_llm.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": "Identifikasi nama makanan dalam gambar ini seakurat mungkin dalam Bahasa Indonesia. Jawab dengan singkat, hanya nama makanannya."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"},
                ]
            )
        ]
    )
    return msg.content

@tool
def search_nutrition_info(food_name: str) -> str:
    """
    Gunakan alat ini untuk mencari informasi nutrisi (kalori, protein, lemak, karbohidrat) dari nama makanan yang sudah diidentifikasi.
    Berikan query pencarian yang detail dalam Bahasa Indonesia.
    """
    try:
        query = f"estimasi detail nutrisi (kalori, protein, lemak, karbohidrat) untuk satu porsi {food_name}"
        search_results = exa_client.search_and_contents(
            query,
            num_results=3,
            text={"include_html_tags": False, "max_characters": 2000}
        )
        formatted_results = "\n\n".join(
            [f"Sumber {i+1}:\n{res.text}" for i, res in enumerate(search_results.results)]
        )
        return formatted_results
    except Exception as e:
        return f"Terjadi kesalahan saat mencari: {e}"

# === AGENT CREATION ===

def create_agent():
    """Fungsi utama untuk membuat dan merakit agent."""
    tools = [describe_image, search_nutrition_info]

    # --- REPLACE THE OLD PROMPT WITH THIS LINE ---
    # Pull the standard ReAct agent prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react-chat")
    # ---------------------------------------------

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    return agent_executor