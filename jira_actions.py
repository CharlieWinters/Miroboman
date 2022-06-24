from matplotlib.font_manager import json_dump
import rest
import config
from data_definer import dataSummary
import json

def comment_to_ticket(issue_key, comment, public=True):
    print(f"Commenting to {issue_key}")
    url = f"{config.jira_base_url}rest/api/3/issue/{issue_key}/comment"
    payload = json.dumps( {
        "body": {
            "version":1,"type":"doc","content":
            [
                {
                    "type":"paragraph",
                    "content": [
                        {
                            "type":"text",
                            "text":comment
                            }
                        ]
                    }
                ]
            },
            "properties":[
                {"key":"sd.public.comment",
                "value":{"internal":public}
                }
            ]
        }
    )
    try:
        post_comment = rest.post(url, payload)
        print(f"Comment status: {post_comment.status_code}")
        #print(f"Failure: {post_comment.content}")
    except Exception as err:
        raise err
