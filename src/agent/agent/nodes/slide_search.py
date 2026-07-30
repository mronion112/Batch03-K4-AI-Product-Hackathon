"""
Node: Tìm kiếm trong slide + quyết định có cần research thêm.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from agent.state import AgentState
from agent.llm import llm

SYSTEM_PROMPT = """# Identity

Bạn là **VLearn Slide Researcher**. Bạn CHỈ đọc và trích xuất từ nội dung slide.
KHÔNG dùng kiến thức riêng hay training data.

# Quy trình
1. Đọc câu hỏi, hiểu ý chính (KHÔNG cần khớp từ khóa chính xác).
2. Tìm nội dung liên quan về MẶT Ý NGHĨA trong slide.
3. Nếu slide có BẤT KỲ nội dung nào liên quan → trả lời.
4. CHỈ từ chối (SLIDE_NOT_ENOUGH_INFO) khi slide HOÀN TOÀN không liên quan.

# Ví dụ
- Hỏi "các tầng của AI", slide ghi "AI — chiếc ô lớn nhất" → ĐÂY LÀ nội dung liên quan → trả lời.
- Hỏi "cách hoạt động LLM", slide ghi "LLM dùng Transformer để xử lý" → trả lời.
- Hỏi "Einstein là ai", slide chỉ có nội dung AI → HOÀN TOÀN không liên quan → từ chối.

# Quy tắc
- CHỈ dùng nội dung từ slide, không thêm kiến thức ngoài.
- Trích dẫn trang: [Trang X]
- Tiếng Việt, in đậm từ khóa, bullet points.
- Từ chối: bắt đầu bằng SLIDE_NOT_ENOUGH_INFO:
"""

IRRELEVANT_KEYWORDS = [
    "nấu ăn", "công thức", "món ăn", "nhà hàng", "ẩm thực",
    "bóng đá", "cầu thủ", "world cup", "ronaldo", "messi",
    "ca sĩ", "bài hát", "phim", "diễn viên", "show",
    "du lịch", "khách sạn", "địa điểm",
    "thời trang", "quần áo", "giày dép", "makeup",
    "giá vàng", "chứng khoán", "bitcoin", "trade",
    "tình yêu", "bạn gái", "bạn trai", "hẹn hò",
    "game", "liên quân", "pubg", "free fire",
    "điện thoại", "iphone", "samsung", "laptop",
]


def search_slide(state: AgentState) -> AgentState:
    question = state["user_question"]
    context = state["slide_context"]
    history = state.get("messages", [])

    if not context.strip():
        return {**state, "slide_search_result": "SLIDE_NOT_ENOUGH_INFO: Không tìm thấy nội dung slide."}

    history_text = ""
    if history:
        lines = []
        for m in history[-4:]:
            if hasattr(m, "type"):
                role = "Học viên" if m.type == "human" else "Tutor"
                content = m.content
            else:
                role = "Học viên" if m.get("role") == "user" else "Tutor"
                content = m.get("content", "")
            lines.append(f"{role}: {content[:150]}")
        history_text = "LỊCH SỬ HỘI THOẠI:\n" + "\n".join(lines) + "\n\n"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""{history_text}<user_question>
{question}
</user_question>

<slide_context>
{context}
</slide_context>"""),
    ]

    response = llm.invoke(messages)
    return {**state, "slide_search_result": response.content}


def decide_search(state: AgentState) -> AgentState:
    mode = state.get("mode", "normal")
    question = state.get("user_question", "")

    if mode != "research":
        return {**state, "needs_web_search": False, "needs_paper_search": False}

    # Research mode: always web search, paper if academic
    # But still filter: only if relevant to course
    if not _is_relevant_to_course(question):
        return {**state, "needs_web_search": False, "needs_paper_search": False}
    needs_paper = _is_academic(question)
    return {**state, "needs_web_search": True, "needs_paper_search": needs_paper}
def _is_academic(question: str) -> bool:
    prompt = f"""Câu hỏi: "{question}"
Đây có phải câu hỏi cần tìm paper học thuật không? (khái niệm chuyên sâu, so sánh phương pháp, state-of-the-art)
Chỉ trả lời YES hoặc NO:"""
    response = llm.invoke(prompt)
    return "YES" in response.content.upper().split("\n")[0]


def _is_relevant_to_course(question: str) -> bool:
    question_lower = question.lower()
    for kw in IRRELEVANT_KEYWORDS:
        if kw in question_lower:
            return False
    prompt = f"""Khóa học: AI & LLM Foundation. Câu hỏi: "{question}"
Liên quan đến AI, ML, LLM, Deep Learning, công nghệ? YES/NO:"""
    response = llm.invoke(prompt)
    return "YES" in response.content.upper().split("\n")[0]
