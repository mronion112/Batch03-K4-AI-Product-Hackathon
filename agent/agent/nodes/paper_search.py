"""
Node: Paper search — tìm kiếm paper học thuật trên arXiv.
"""

from agent.state import AgentState
from agent.tools import arxiv_search
from agent.llm import llm


def search_papers(state: AgentState) -> AgentState:
    question = state["user_question"]
    
    prompt = f"""Trích xuất 2-3 từ khóa học thuật chính (tiếng Anh) từ câu hỏi.
Chỉ trả về từ khóa cách nhau bằng khoảng trắng, không dấu phẩy, không giải thích.
Câu hỏi: {question}
Từ khóa:"""
    
    keywords = llm.invoke(prompt).content.strip()
    papers = arxiv_search(keywords, max_results=3)
    
    if not papers:
        return {**state, "paper_search_result": ""}

    lines = []
    for i, p in enumerate(papers, 1):
        authors = ", ".join(p.get("authors", [])[:3])
        lines.append(
            f"{i}. **{p['title']}**\n"
            f"   {authors}\n"
            f"   {p['summary'][:300]}...\n"
            f"   📎 [{p.get('pdf_url', '')}]({p.get('pdf_url', '')})"
        )
    
    return {**state, "paper_search_result": "\n\n".join(lines)}
