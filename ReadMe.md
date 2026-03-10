# Motivation Behind this project

While completing a course on RAG and Agentic AI, I faced certain issues with my bank, however could not find a way to contact them since their lines were only open only on workdays till 5pm and my work (like most people's) lasts atleast till that time if not longer. I thought to myself .... surely a bot could update my details. This made me think about how I can apply the aforementioned concepts to this use case.

# Mr Banks

So, I introduce, Mr Banks, the helpful financial chatbot. Mr Banks will aim to use LLMs and their natural language & reasoning capabilities in a secure way, by using various tools at its disposal. This projects will be largely focused at the backend AI system. I will explicitly use types in functions and tools where applicable. Although in python these are optional, for an AI agent this is crucial information.

The backbone for reasoning will be Gemini API, provided generously by Google within their free tier development under certain constraints, I will use many other models during development since different models have different capabilites and rate limits. Additionally, models used within smaller agents will be hosted on my PC using Ollama.

# Capabilities and Features

1. Before making any features, I must check for any prompt injections. Therefore, I have carefully programmed Mr.Bank's persona to NOT have the primary goal as a "helpful" chatbot. Instead its primary goal is to prevent fraud. With Gemini's reasoning, this prevents many attempts to breach the security protocols outright.

    ![images/readme/primitive_pen_testing.png](images/readme/primitive_pen_testing.png )


# *WIP*

2. As a first feature Mr. Banks must be able to fetch user details and verify their credentials. This is potentially the most critical step as an error here could have far reaching consequences for cybersecurity, fraud and the bank's financial reposibility. If I was shipping this feature in production, this would contain a human-in-the loop system or other proven credential checking mechanisms currrently in use. However for this project, Mr. Banks will verify all credentials using a deterministic tool so that it cannot simply be "convinced".


3. Tool calling

    ![alt text](images/readme/primitive_tool_calling.png)

