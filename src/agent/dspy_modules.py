import dspy

class NLToSQLModule(dspy.Module):
    def __init__(self, retriever, schema):
        super().__init__()
        self.retriever = retriever
        
        class NLToSQLSignature(dspy.Signature):
            f"""Database Schema: {schema}
            Convert natural language to SQL query."""
            question: str = dspy.InputField()
            sql: str = dspy.OutputField()
        
        self.generator = dspy.Predict(NLToSQLSignature)
    
    def forward(self, question):
        similar = self.retriever.get_similar(question, k=2)
        examples = "\n".join([f"Q: {ex.question}\nSQL: {ex.answer}" for ex in similar])
        full_q = f"{examples}\n\nQ: {question}"
        return self.generator(question=full_q)