from openai import OpenAI
from typing import Optional
from .imessage_reader import Chat, Message


class DraftGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
    
    def generate_followup(
        self,
        chat: Chat,
        conversation_history: list[Message],
        hours_since_last: float
    ) -> str:
        is_group_chat = len(chat.participants) > 1
        
        context = self._build_context(
            chat=chat,
            history=conversation_history,
            hours_since=hours_since_last,
            is_group=is_group_chat
        )
        
        prompt = self._build_prompt(context, is_group_chat)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=256,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            draft = response.choices[0].message.content.strip()
            return draft
        
        except Exception as e:
            return f"[Error generating draft: {str(e)}]"
    
    def _build_context(
        self,
        chat: Chat,
        history: list[Message],
        hours_since: float,
        is_group: bool
    ) -> str:
        lines = []
        
        chat_type = "group chat" if is_group else "1:1 conversation"
        lines.append(f"Chat type: {chat_type}")
        
        if chat.display_name:
            lines.append(f"Chat name: {chat.display_name}")
        
        if is_group:
            lines.append(f"Participants: {', '.join(chat.participants)}")
        else:
            lines.append(f"Contact: {chat.chat_identifier}")
        
        lines.append(f"\nTime since last message: {hours_since:.1f} hours")
        lines.append(f"\nRecent conversation (oldest to newest):")
        
        for msg in history[-5:]:
            sender = "You" if msg.is_from_me else msg.handle_id
            text = msg.text or "[media/reaction]"
            lines.append(f"{sender}: {text}")
        
        return "\n".join(lines)
    
    def _build_prompt(self, context: str, is_group: bool) -> str:
        tone_instruction = (
            "casual and friendly for group chats"
            if is_group
            else "polite but not overly formal"
        )
        
        return f"""You are helping draft a follow-up message for an iMessage conversation that hasn't received a reply.

{context}

Generate a brief, natural follow-up message that:
1. Is {tone_instruction}
2. Acknowledges the delay without being pushy or annoying
3. Gently nudges for a response
4. Is SHORT (1-2 sentences max)
5. Sounds like something a real person would text

Do not include quotes or explanations - just output the message text that should be sent."""

