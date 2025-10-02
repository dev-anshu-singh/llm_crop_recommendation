import pandas as pd
from datetime import datetime

def df_to_llm_csv(df: pd.DataFrame) -> str:
    lines = []
    # header
    lines.append(",".join(df.columns))
    # rows
    for _, row in df.iterrows():
        lines.append(",".join(str(v) for v in row.values))
    return "\n".join(lines)


def get_retrieved_context(retriever, query: str) -> str:
    retrieved_doc = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in retrieved_doc)

def get_current_date(x):
    """Get current date"""
    return datetime.now().strftime("%Y-%m-%d")
