import requests
import json
import os
from fastapi import HTTPException, status




def ApplyAI(Content, FolderList, TagList, API_KEY):

    data = { 'model':"gpt-3.5-turbo",
              'messages' : [
                { "role": "system",
                  "content": """
                    You are a text Notes Classifier AI that only responds in JSON objects of the following format:
                    ```
                    {
                        "folder": "Folder name selected from the folderList"
                        "tags": {
                            "tagList": ["tag1", "tag2", "tag3"]
                        }
                    }
                    ```
                    The user will give you a JSON object of the following format:
                    {
                        folders: ["folder option 1", "folder option 2", "folder option 3"],
                        tags: ["tag option 1", "tag option 2", "tag option 3"]
                        content: "The text to be classified"
                    }
    
                    both tags and folders are optional, and can be empty lists.
    
                    Your job is to classify the user's input into one of the folders, and return a JSON object of the above format.
    
                    if you get the following ,for example:
                    {
    
                    folders: [ "data analysis", "web scraping", "machine learning"],
                    tags: ["python", "pandas", "numpy","Math", "scikit-learn", "beautifulsoup", "python requests"]
                    content: "
                                ```
                                import pandas as pd
                                import numpy as np
                                import matplotlib.pyplot as plt
    
    
    
                                x = np.linspace(0, 2*np.pi, 100)
                                y = np.sin(x)
                                plt.plot(x, y)
    
    
                                df = pd.read_csv('data.csv')
    
                                corr = df.corr()
                                print(corr)
    
                                ```
                                "
    
                    }
    
                    you should return the following:
    
                    {
                        "folder": "data analysis",
                        "tags": {
                            "tagList": ["python", "pandas", "numpy","Math" ]
                        }
                    }
    
                    Keep in mind that the user can give you any text, and you should be able to classify it into one of the folders, and return the tags that are relevant to the text.
                    If no tags are relevant, you can return an empty list.
                    if no folder is relevant, you can return an empty string.
    
    
                    """
                },
                { "role": "user",
                  "content":f"""
                     folders: {json.dumps(FolderList)},
                        tags: {json.dumps(TagList)},
                        content: "{Content}"
                     """
                 }
            ]

    }

    headers = {
        'Authorization': "Bearer " + API_KEY,
        'Content-Type': "application/json"
    }

    resp = requests.post("https://api.openai.com/v1/chat/completions", data=json.dumps(data), headers=headers )
    try :
        raw = resp.json()['choices'][0]['message']['content']
        return json.loads(raw)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e} , raw: {resp.json()}")



if __name__ == "__main__":


    API_KEY = os.environ.get('APIKEY_OPENAI')
    print(API_KEY)
    CONTENT  = """
        from pydantic import BaseModel, GetJsonSchemaHandler
        from typing import Optional , List, Dict ,Annotated, AnyStr
        
        from pydantic.json_schema import JsonSchemaValue
        from pydantic_core import CoreSchema,
        from models import UserRecord ,Base
    """

    result = (ApplyAI(CONTENT, ["API", "ML", "NodeJs Frameworks"], ["PY", "JS", "C#"], API_KEY))

    # pretty print the result
    print(json.dumps(result, indent=4, sort_keys=True))