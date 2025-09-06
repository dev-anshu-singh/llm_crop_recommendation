from pydantic import BaseModel, Field
from typing import Dict,List,Annotated,Optional

#input schema
class UserInput(BaseModel):
    latitude: Annotated[float, Field(...,ge=-90, le=90, description='latitude of the location')]
    longitude: Annotated[float, Field(..., ge=-180, le=180, description='longitude of the location')]
    farm_plot_size: Annotated[Optional[float], Field(None, gt=0, description='Farm plot size available for cultivation in hactares.')]
    irrigation_type: Annotated[Optional[List[str]],Field(None, description='List of available irrigation facilities.')]
    previous_crop: Annotated[Optional[str],Field(None, description='previous crop planed at the lang where cultivation is intended')]
    soil_test_values: Annotated[Optional[Dict[str,float]],Field(None, description='Nutritional value of the soil')]
    excluded_crops: Annotated[Optional[str], Field(None, description='Crops you do not want the model to suggest')]


class RecommendationResponse(BaseModel):
    rank: int = Field(..., description="Rank of the crop based on suitability (1 = best).")
    crop_name: str = Field(..., description="Name of the recommended crop.")
    reason: str = Field(..., description="Explanation on why the crop is suitable.")
    
class RecommendationResponses(BaseModel):
    recommendation: List[RecommendationResponse] = Field(..., description='List of recommended crops in ranked order.')
