from pydantic import BaseModel, GetJsonSchemaHandler ,UUID4
from typing import Optional , List, Dict ,Annotated, AnyStr
import json as json
# datetime
from datetime import datetime
from Classifier import ApplyAI
from fastapi import HTTPException, status

from pydantic.json_schema import JsonSchemaValue



from models import UserRecord ,Base





class FolderList(BaseModel):
    """
    Represents the folderList inside the "folders" object.
    """
    folderList: List[str]

class TagList(BaseModel):
    """
    Represents the tagList inside the "tags" object.
    """
    tagList: List[str]

class UserEntry(BaseModel):
    """
    Represents the entire JSON structure.

    Args:
    - folders (FolderList, optional): The folders object with a list of strings.
    - tags (TagList, optional): The tags object with a list of strings.
    """
    folders: Optional[FolderList]
    tags: Optional[TagList]

class Classification(BaseModel):
    """
    Represents the classification object inside the "folders" object.

    Args:
    - classification (str): The classification string.
    """
    folder: Optional[str]
    tags: Optional[TagList]

class Saved_User(UserEntry):
    """
    Represents the entire USER structure, as saved in the database.

    """

    id : UUID4
    created_at : datetime
    last_login : datetime
    updated_at : datetime
    last_IP_origin : Optional[str]

    def do_classification(self,CONTENT,API_KEY):
        raw = ApplyAI(CONTENT,self.folders.folderList,self.tags.tagList,API_KEY)
        try  :
            classification = Classification(**raw)
        except Exception as e:
            d = {'error': f" {e}" , 'raw': raw}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)

        return classification













