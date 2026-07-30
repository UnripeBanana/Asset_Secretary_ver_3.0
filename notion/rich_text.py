def rich_text(value):
    return {
        "rich_text": [
            {
                "type": "text",
                "text": {
                    "content": str(value) if value else ""
                }
            }
        ]
    }
