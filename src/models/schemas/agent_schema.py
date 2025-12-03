from typing import  List, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    route: str
    language: str
    retrieved_docs: List[str]
    sql_query: str
    sql_results: str
    output_text: str
    retry_nl_to_sql: str
    repair_count: int
    plan : str
    use_dspy : bool