import json

import pandas as pd
import config
import utils

def load_fertilizer_data() -> str:
    df = pd.read_csv(config.FERTILIZER_DATA_PATH).drop(columns=['Recommendation (kg/ha)'], axis=1)
    return utils.df_to_llm_csv(df)

def load_msp_data():
    with open(config.MSP_DATA_PATH, 'r') as f:
        data = json.load(f)
    lines = []
    for season, crops in data.items():
        lines.append("Season,Crop,Cost,MSP")
        for season, crops in data.items():
            for c in crops:
                lines.append(f"{season},{c['Crop']},{c['Cost of Production']},{c['MSP']}")

    return "\n".join(lines)
