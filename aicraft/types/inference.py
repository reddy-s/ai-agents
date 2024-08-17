from pydantic import BaseModel


class InferenceConfig(BaseModel):
    identifier: str
    file_suffix: str
    n_gpu_layers: int = -1
    verbose: bool = False
    n_ctx: int = 4096
    chat_format: str = "chatml"


class InferenceResponse(BaseModel):
    role: str
    content: BaseModel


class InferenceRequest(BaseModel):
    messages: list[dict]
    response_format: type[BaseModel]
    max_new_tokens: int = 1024
    temperature: float = 0.6
    top_p: float = 0.9


class FunctionCallRequest(BaseModel):
    messages: list[dict]
    tools: list[dict]
    tool_choice: str = "auto"


class FunctionCall(BaseModel):
    name: str
    arguments: dict


class FunctionCallResponse(BaseModel):
    role: str
    calls: list[FunctionCall]

    class Config:
        arbitrary_types_allowed = True
