class PromptGenerator :

    def router_prompt (self , question : str):
        prompt_lines = [
        "You are a routing model.",
        "Your job is to classify the user question into one of these routes:",
        "- 'sql' → if the question requires structured data from database tables.",
        "- 'rag' → if the question needs external knowledge, document lookup, or explanations.",
        "- 'hybrid' → if the question requires both SQL data and additional context or explanation.",
        "",
        "Rules:",
        "1. The user question might be in any language."
        "2. Output ONLY one word: sql, rag, or hybrid.",
        "3. Do NOT explain your reasoning.",
        "4. If the question mixes SQL data with explanation → choose 'hybrid'.",
        "5. If the information is not stored in SQL tables → choose 'rag'.",
        "6. If the question is purely about database fields or structured data → choose 'sql'.",
        "Question:",
        question,
        "",
        "Output format:",
        "route: <sql|rag|hybrid>"
        ]
        return  "\n".join(prompt_lines)
    
    def planner_prompt (self , question : str):
        prompt_lines = [
            "Create a step-by-step plan to answer the following question:",
            "question might be in any language."
            "",
            "Question:",
            question,
            "",
            "Return the plan as a numbered list."
        ]
        return  "\n".join(prompt_lines)
    
    def sql_prompt (self , db_schema , question):
        prompt_lines = [
        "You MUST generate a SQL query ONLY using the tables and columns inside this schema:",
        db_schema,
        "Before generating SQL, you MUST:",
        "1) Extract the meaning of the question.",
        "2) Map the extracted meaning to the correct tables and columns EXACTLY as they appear in the schema.",
        "3) If any required table or column does NOT exist in the schema, return exactly:",
        "ERROR: Missing schema information",
        "Do NOT add assumptions. Do NOT invent tables. Do NOT invent columns",
        "Question:",
        question,
        "",
        "output only sql query if generated",
        "Write a correct SQL query to answer the question. ",
        ]
        return  "\n".join(prompt_lines)
    
    def sql_repair_prompt (self , question , sql_query , sql_results):

        prompt_lines= [
            "You are an expert SQL developer. A SQL query was generated for the following question:",
            "Question:", 
            question,
            "The generated SQL query is:",
            sql_query,
            "When executing this query, the following error occurred:",
            sql_results,
            "Please correct the SQL query so that it runs successfully on the database schema provided,",
            "keeping the logic of the question intact. Return only the corrected SQL query, without explanations or extra text."
            ]
        return "\n".join(prompt_lines)
    
    def synthesized_prompt(self , synthesized_output):
        prompt_lines = [
        "You are an expert SQL/Answer generator. Improve and clean up the following output.",
        synthesized_output,
        "⚠️ IMPORTANT RULES:",
        "1. Output ONLY the final answer. Do NOT include 'Answer:', explanations, or any other text.",
        "2. Start the output directly with the answer content.",
        "3. Remove any extra formatting, comments, or markdown.",
        "4. The output should be exactly what the user expects to see as the final result.",
        "5. if you don't have sql answer don't generate it "
        ]
    
        return "\n".join(prompt_lines)
