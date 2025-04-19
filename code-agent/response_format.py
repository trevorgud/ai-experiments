response_format = {
    "format": {
        "type": "json_schema",
        "name": "fs_action",
        "schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["tree", "file", "done"]
                },
                "params": {
                    "type": "object",
                    "anyOf": [
                        {   # ---- tree params --------------------
                            "properties": {
                                "start": { "type": "string" },
                                "depth": { "type": "integer" }
                            },
                            "required": ["start", "depth"],
                            "additionalProperties": False
                        },
                        {   # ---- file params --------------------
                            "properties": {
                                "path": { "type": "string" }
                            },
                            "required": ["path"],
                            "additionalProperties": False
                        },
                        {   # ---- done params --------------------
                            "properties": {
                                "final_answer": { "type": "string" }
                            },
                            "required": ["final_answer"],
                            "additionalProperties": False
                        }
                    ]
                }
            },
            "required": ["action", "params"],   # <-- both keys must exist
            "additionalProperties": False
        }
    }
}
