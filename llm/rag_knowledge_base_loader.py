from langchain_community.document_loaders import JSONLoader
import json
import config


def load_agro_zone_knowledge_base():
    loader = JSONLoader(
        file_path=config.AGRO_ZONE_DATA_PATH,
        jq_schema=".zones[]",
        text_content=False  # ✅ important: allows dicts
    )

    agro_zone_docs = loader.load()

    for doc in agro_zone_docs:
        zone_data = json.loads(doc.page_content)

        doc.metadata = {
            "type": "agro_climatic_zone_docs",
            "zone": zone_data["name"],
            "region": zone_data["region"]
        }

    return agro_zone_docs


# print("Docs loaded:", len(agro_zone_docs))
# print("Example Doc Metadata:\n", agro_zone_docs[0].metadata)
# print("Example Doc Content:\n", agro_zone_docs[0].page_content)
