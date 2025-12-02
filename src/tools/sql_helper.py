import sqlite3
import re
import json
import dspy


class SQLHelper:

    def get_db_schema(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        
        schema_info = []
        for table_name, in tables:
            columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
            column_names = [col[1] for col in columns]
            schema = f"{table_name} ({', '.join(column_names)})"

            schema_info.append(schema)
        
        conn.close()
        return "\n".join (schema_info)
    

    def extract_select_query(output):
        """
        Extract only a SELECT SQL query from model output.
        Returns the query as a string, or None if not found.
        """
        match = re.search(r"SELECT\b.*?;", output, re.IGNORECASE | re.DOTALL)
        if match:
            sql_query = match.group(0).strip()
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            return sql_query
        else:
            return None
        

    def load_jsonl(path):
        data = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line))
        return data


    def load_dspy_dataset (dataset):
        examples = []
        for i  in range (len (dataset)):
            
            examples.append (dspy.Example(question = dataset[i].get ("question")
                                        , answer = dataset[i].get ("sql"))
                        )
        return examples