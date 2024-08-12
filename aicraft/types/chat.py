from pydantic import BaseModel
from enum import Enum
from .analysers import HobuCustomerConversationPreference
import math


class Roles(Enum):
    """
    An enumeration representing the roles of entities in a chat or document system.

    Attributes:
    ----------
    user : str
        The role of the user in the chat or document system.

    assistant : str
        The role of the assistant in the chat or document system.
    """

    user = "user"
    assistant = "assistant"


class ChatGenerationResponse(BaseModel):
    """
    A model representing the response generated by a Model.

    Attributes:
    ----------
    role : str
        The role of the entity generating the response. Typically, this could be 'user' or 'assistant'

    content : str
        The content of the response message. This is the text in markdown format that is generated by the chat system.
    """

    role: str
    content: str


class ContentType(Enum):
    """
    An enumeration representing various content types that can be used in a chat or document system.

    Attributes:
    ----------
    TEXT : str
        Plain text content type, represented as "text/plain".

    MARKDOWN : str
        Markdown formatted content type, represented as "text/markdown".

    JSON : str
        JSON formatted content type, represented as "text/json".

    SQL : str
        SQL formatted content type, represented as "text/sql".
    """

    TEXT = "text/plan"
    MARKDOWN = "text/markdown"
    JSON = "text/json"
    SQL = "text/sql"


class Element(BaseModel):
    """
    A model representing an element with specific content and its associated metadata.

    Attributes:
    ----------
    content : str
        The main content of the element, which could be plain text, Markdown, JSON, or SQL, depending on the content type.

    contentType : ContentType
        An enumeration value representing the type of content (e.g., plain text, Markdown, JSON, SQL).

    model : str
        The name or identifier of the model associated with this element. This could refer to a machine learning model, a document model, or any other relevant model in use.

    Config:
    -------
    arbitrary_types_allowed : bool
        A Pydantic configuration option that allows the use of arbitrary types in the model. This is set to `True` to permit the use of the `ContentType` enum.
    """

    content: str
    contentType: ContentType
    model: str

    def __init__(self, content: str, content_type: ContentType, model: str):
        super().__init__(content=self.add_completion_if_missing(content), contentType=content_type, model=model)

    @staticmethod
    def add_completion_if_missing(content: str):
        if not content.endswith(('.', '?', '!')):
            content += '.'
        return content

    class Config:
        arbitrary_types_allowed = True


class UserMessage(BaseModel):
    """
    A model representing a message sent by a user, including their role and the elements of the message content.

    Attributes:
    ----------
    role : str
        The role of the message sender. This is typically "user" and defaults to this value.

    elements : list[Element]
        A list of `Element` objects representing the various parts of the message content. Each element could contain text, code, or data in different formats, as specified by its content type.
    """

    role: str = "user"
    elements: list[Element]

    class Config:
        arbitrary_types_allowed = True


class AssistantMessage(BaseModel):
    """
    A model representing a message generated by an assistant, including the assistant's role and the elements of the message content.

    Attributes:
    ----------
    role : str
        The role of the message sender, which is "assistant" by default.

    elements : list[Element]
        A list of `Element` objects representing the various parts of the assistant's message content. Each element can include different types of content such as text, Markdown, JSON, or SQL.
    """

    role: str = "assistant"
    elements: list[Element]

    class Config:
        arbitrary_types_allowed = True


class Conversation(BaseModel):
    """
    A model representing a conversation, which consists of a sequence of messages exchanged between a user and an assistant.

    Attributes:
    ----------
    messages : list[UserMessage | AssistantMessage]
        A list of messages in the conversation. Each message can either be a `UserMessage` or an `AssistantMessage`, representing the communication between the user and the assistant.
    """

    messages: list[UserMessage | AssistantMessage] = []
    prompt_pairs: int = 0

    def get_messages_for_prompt(self, last_n=5) -> list[dict[str, str]]:
        messages = []
        for message in self.messages[-last_n:]:
            role = message.role
            context = []
            for e in message.elements:
                if e.contentType in [
                    ContentType.MARKDOWN,
                    ContentType.TEXT,
                    ContentType.SQL,
                    ContentType.JSON,
                ]:
                    context.append(e.content)
            messages.append({"role": role, "content": "\n".join(context)})
        return messages

    def add_message(self, message: UserMessage | AssistantMessage):
        self.messages.append(message)
        self.prompt_pairs = math.ceil(len(self.messages) / 2)

    class Config:
        arbitrary_types_allowed = True


class UserState(BaseModel):
    """
    A model representing the state of a user, which includes the current conversation they are engaged in.

    Attributes:
    ----------
    conversation : Conversation
        The ongoing conversation involving the user. This conversation is represented by a `Conversation` object, which contains a sequence of messages exchanged between the user and an assistant.
    """

    conversation: Conversation = Conversation()
    preferences: HobuCustomerConversationPreference = (
        HobuCustomerConversationPreference()
    )

    class Config:
        arbitrary_types_allowed = True
