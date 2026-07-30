"""
State schema for VLearn Tutor Agent.
"""

from typing import TypedDict, List, Dict, Annotated, Optional
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    user_question: str
    slide_context: str
    current_page: int
    slide_title: str
    messages: Annotated[List[Dict], add_messages]
    slide_search_result: Optional[str]
    web_search_result: Optional[str]
    paper_search_result: Optional[str]
    final_answer: Optional[str]
    citations: Optional[List[str]]
    needs_web_search: bool
    needs_paper_search: bool
    mode: str
    error: Optional[str]
