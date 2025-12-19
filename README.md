# rag_agent

Here’s a **brief, clean, GitHub-ready README** for this **Developer Tools Research Agent** project.
It explains the project clearly **without assuming the reader has seen internal files**, which is ideal since some code lives in `advanced_agent/`.

---

# 🔍 Developer Tools Research Agent (Agentic RAG Workflow)

This project is an **Agentic AI system** that autonomously researches **developer tools and platforms** and returns **structured, comparable insights** such as pricing models, tech stack, API availability, integrations, and recommendations.

The agent is built using a **custom workflow** that orchestrates reasoning, web research, and analysis in a single end-to-end pipeline.

---

## 🚀 What This Project Does

* Accepts a **developer tools query** from the terminal
* Automatically researches relevant companies and products
* Extracts **structured information** for each tool:

  * Website
  * Pricing model
  * Open-source status
  * Tech stack
  * Language support
  * API availability
  * Integration capabilities
* Produces **high-level recommendations** for developers

---

## 🧠 Architecture Overview

* **Workflow-driven agent design**
* Modular logic encapsulated inside `advanced_agent.workflow`
* Central `run(query)` method executes the full research pipeline
* Returns structured results instead of raw text
* Interactive CLI interface for fast experimentation

---

## ⚙️ How the Code Works (Brief)

1. **Environment Setup**
   Loads API keys and configuration using `python-dotenv`.

2. **Workflow Initialization**
   A `Workflow` object manages the entire research process.

3. **Interactive Query Loop**

   * User enters a developer tools query
   * Workflow processes the query end-to-end
   * Results are returned as structured objects

4. **Result Rendering**
   Displays company-level details and final recommendations in a readable format.

---

## 🛠️ Tech Stack

* **Python**
* **Agentic AI workflows**
* **Structured outputs (schema-based results)**
* **CLI-based interaction**
* **Environment-based configuration**

---

## ▶️ Running the Project

### 1️⃣ Install Dependencies

```bash
pip install python-dotenv
```

(Additional dependencies are handled inside the project modules.)

### 2️⃣ Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
FIRECRAWL_API_KEY=your_api_key
```

### 3️⃣ Run the Agent

```bash
python main.py
```

Exit anytime using:

```text
quit
```

---

## 📊 Example Output

```text
1. Company Name
   Website: https://example.com
   Pricing: Freemium
   Open Source: No
   Tech Stack: Python, React, AWS
   API: Available
   Integrations: GitHub, Slack
```

---

## 🌟 Why This Project Is Valuable

This project demonstrates:

* **Real-world Agentic AI design**
* **Autonomous research pipelines**
* **Structured LLM outputs (not just chat responses)**
* **Clean separation between workflow logic and UI**

It goes beyond basic RAG by focusing on **decision-oriented insights**.

---

## 🔮 Future Enhancements

* Multi-agent research workflows
* Vector database memory
* UI dashboard (Streamlit / Web)
* Tool comparison scoring


* Convert this into a **resume-optimized project description**
* Write **architecture documentation**
* Add **workflow diagrams**
* Make a **portfolio case study version**

