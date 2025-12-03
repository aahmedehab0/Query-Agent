from langgraph.graph import StateGraph , START , END 
from tools import PromptGenerator , SQLHelper
from models.schemas import AgentState
import sqlite3
import json



class QueryAgent:
    def __init__(self, llm, dspy_model , vectorstore
                 , nl2sql_arabic, nl2sql_english , db_path):
        
        self.llm = llm
        self.vectorstore = vectorstore
        self.dspy_model = dspy_model
        self.nl2sql_arabic = nl2sql_arabic
        self.nl2sql_english = nl2sql_english
        self.db_path = db_path

        self.prompt_generator = PromptGenerator()
        self.sql_helper = SQLHelper()
        self.graph = self.build_graph()

    def router_node(self , state: AgentState) -> AgentState:
        question = state.get ("question" , "")

        prompt = self.prompt_generator.router_prompt(question = question)
        
        message = self.llm.invoke(prompt)
        route = message.content.strip().lower()

        # fallback on keywords
        if "rag" in route:
            state["route"] = "rag"
        elif "sql" in route:
            state["route"] = "sql"
        elif "hybrid" in route:
            state["route"] = "hybrid"
            
        else:
            state["route"] = "hybrid"  

        print("route:", state["route"])
        return state
    
    def planner_node(self , state: AgentState) -> AgentState:
        print ("planer...")

        question = state.get ("question" , "")
        prompt = self.prompt_generator.planner_prompt(question = question)
        result = self.llm.invoke(prompt).content
        state["plan"] = result
        return state
    

    def retrieve_docs_node(self , state: AgentState) -> AgentState:
        print("Retrieving from docs...")

        question = state.get ("question" , "")
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        docs = retriever.invoke(question)

        if not docs or len(docs) == 0:
            state["retrieved_docs"] =  ["I found no relevant information"]
            return state

        results = []
        for i, doc in enumerate(docs):
            results.append(f"Document {i+1}:\n{doc.page_content}\n\n")

        state["retrieved_docs"] = results
        return state
    

    def nl_to_sql_node(self , state: AgentState) -> AgentState:
        print("query to sql...")
        question = state.get("question" , "")
        lang = state.get("language", "en")
        repair_count = state.get("repair_count", 0)
        use_dspy = state.get("use_dspy", True)

        if repair_count > 0:
            sql_results = state.get("sql_results", "error")
            sql_query = state.get("sql_query", "")
            prompt = self.prompt_generator.sql_repair_prompt (question , sql_query , sql_results)
            
        else:
            if use_dspy :
                print ("using dspy ...")
                if lang == "ar":
                    sql_query  = str (self.nl2sql_arabic (question).sql)
                else : 
                    sql_query = str (self.nl2sql_english (question).sql)
            else:
                db_schema = self.sql_helper.get_db_schema(db_schema = self.db_path)

                prompt = self.prompt_generator.sql_prompt  (db_schema = db_schema , 
                                                            question = question)
                sql_query = self.llm.invoke(prompt).content.strip()
    
        print (sql_query)

        sql_query = self.sql_helper.extract_select_query (sql_query)
        state["sql_query"] = sql_query
        
        return state
    

    def sql_executor_node(self , state: AgentState) -> AgentState:

        print("sql execution...")

        sql_query = state.get("sql_query" , "")

        if not sql_query:
            state["sql_results"] = sql_query
            return state

        try:
            db = sqlite3.connect(self.db_path)
            db.row_factory = sqlite3.Row
            cursor = db.cursor()

            cursor.execute(sql_query)
            rows = cursor.fetchall()

            results_list = [dict(r) for r in rows]
            state["sql_results"] = json.dumps(
                results_list, 
                ensure_ascii=False, 
                indent=2
            )

        except Exception as e:
            state["sql_results"] = f"Error: {str(e)}"

        return state
    

    def repair_loop_node(self , state: AgentState) -> AgentState:
    
        sql_results = state.get("sql_results", "")
        route = state.get("route")
        repair_count = state.get("repair_count", 0)
        
        is_error = (
            not sql_results or 
            sql_results == "" or 
            (isinstance(sql_results, str) and sql_results.startswith("Error:"))
        )

        if route in ["sql", "hybrid"] and is_error:
            repair_count += 1
            state["repair_count"] = repair_count

            if repair_count < 3:
                state["retry_nl_to_sql"] = "sql wrong"
                return state

            state["sql_results"] = "No answer found on DB"

        state["retry_nl_to_sql"] = "sql right"
        return state
    
    
    def synthesizer_node(self , state: AgentState) -> AgentState:
        print("Synthesizer...")

        sql_results = state.get("sql_results", "")
        retrieved_docs = state.get("retrieved_docs", [])
        question = state.get("question", "")  
        
        synthesized_output = ""  
        synthesized_output += f"Question: {question}\n\n"
        
        if sql_results and sql_results != "":
            synthesized_output += "Results from database:\n"
            synthesized_output += sql_results + "\n\n"

        if retrieved_docs:
            synthesized_output += "\nRelevant documents:\n"
            for i, doc in enumerate(retrieved_docs):
                synthesized_output += f"Document {i+1}: {doc}\n"

        if not synthesized_output:
            synthesized_output = "No results found."

        prompt = self.prompt_generator.synthesized_prompt(synthesized_output)

        output_text = self.llm.invoke(prompt).content
        state["output_text"] = output_text

        return state

    def build_graph(self):
        graph = StateGraph(AgentState)

        # Nodes
        graph.add_node("router", self.router_node)
        graph.add_node("planner", self.planner_node)
        graph.add_node("retrieve_docs", self.retrieve_docs_node)
        graph.add_node("nl_to_sql", self.nl_to_sql_node)
        graph.add_node("sql_executor", self.sql_executor_node)
        graph.add_node("repair_loop", self.repair_loop_node)
        graph.add_node("synthesizer", self.synthesizer_node)

        # Entry
        graph.set_entry_point("router")

        # Router edges
        graph.add_conditional_edges(
            "router",
            lambda state: state["route"],
            {
                "rag": "planner",
                "sql": "planner",
                "hybrid": "planner"
            }
        )

        # Planner edges
        graph.add_conditional_edges(
            "planner",
            lambda state: state["route"],
            {
                "rag": "retrieve_docs",
                "sql": "nl_to_sql",
                "hybrid": "retrieve_docs"
            }
        )

        # Retrieve docs edges
        graph.add_conditional_edges(
            "retrieve_docs",
            lambda state: state["route"],
            {
                "rag": "synthesizer",
                "hybrid": "nl_to_sql"
            }
        )

        graph.add_edge("nl_to_sql", "sql_executor")

        graph.add_edge("sql_executor", "repair_loop")

        graph.add_conditional_edges(
            "repair_loop",
            lambda state: state.get("retry_nl_to_sql","sql right"),
            {
                "sql wrong": "nl_to_sql",      
                "sql right": "synthesizer"     
            }
        )

        # Synthesizer → END
        graph.add_edge("synthesizer", END)

        # Compile
        return graph.compile()
