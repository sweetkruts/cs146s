#!/usr/bin/env python3
"""
iReply: Intelligent iMessage Follow-up Agent
CLI interface for the alpha version
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

from ireply.config import Config
from ireply.imessage_reader import iMessageReader
from ireply.stale_detector import StaleDetector
from ireply.draft_generator import DraftGenerator


console = Console()


def display_header():
    console.print(Panel.fit(
        "[bold cyan]iReply[/bold cyan] - Intelligent iMessage Follow-up Agent\n"
        "[dim]Alpha Version 0.1.0[/dim]",
        border_style="cyan"
    ))


def validate_config() -> bool:
    if not Config.OPENAI_API_KEY:
        console.print("[red]Error:[/red] OPENAI_API_KEY not set")
        console.print("Please create a .env file with your API key")
        console.print("Example: OPENAI_API_KEY=sk-...")
        return False
    
    if not Path(Config.IMESSAGE_DB_PATH).exists():
        console.print(f"[red]Error:[/red] iMessage database not found at {Config.IMESSAGE_DB_PATH}")
        console.print("Make sure you're running this on macOS with Messages enabled")
        return False
    
    return True


def display_stale_conversations(stale_convos, reader):
    if not stale_convos:
        console.print("\n[green]✓[/green] No stale conversations found!")
        return
    
    console.print(f"\n[yellow]Found {len(stale_convos)} conversation(s) needing follow-up:[/yellow]\n")
    
    table = Table(box=box.ROUNDED)
    table.add_column("#", style="cyan", width=3)
    table.add_column("Contact/Chat", style="bold")
    table.add_column("Last Message", width=40)
    table.add_column("Hours Ago", justify="right", style="yellow")
    table.add_column("Context", style="dim", width=12)
    
    for idx, stale in enumerate(stale_convos, 1):
        chat = stale.chat
        contact = chat.display_name or chat.chat_identifier
        last_msg = chat.last_message.text or "[media]" if chat.last_message else "N/A"
        
        if len(last_msg) > 37:
            last_msg = last_msg[:37] + "..."
        
        # Check if conversation has text context
        history = reader.get_chat_history(chat.chat_id, limit=10)
        text_count = sum(1 for msg in history if msg.text and len(msg.text) > 5)
        context_info = f"{text_count} texts" if text_count > 0 else "reactions only"
        
        table.add_row(
            str(idx),
            contact,
            last_msg,
            f"{stale.hours_since_last_message:.1f}h",
            context_info
        )
    
    console.print(table)


def generate_and_show_drafts(stale_convos, reader, generator):
    console.print("\n[cyan]Generating follow-up drafts with GPT-4o...[/cyan]\n")
    console.print("[dim]Reading last 10 messages per conversation for context[/dim]\n")
    
    for idx, stale in enumerate(stale_convos, 1):
        chat = stale.chat
        contact = chat.display_name or chat.chat_identifier
        
        console.print(f"[bold]{idx}. {contact}[/bold]")
        
        # Get and analyze history
        history = reader.get_chat_history(chat.chat_id, limit=10)
        text_msgs = [msg for msg in history[-5:] if msg.text and len(msg.text) > 5]
        
        if text_msgs:
            console.print(f"[dim]📝 Context: Using {len(text_msgs)} recent text messages[/dim]")
            # Show preview of what AI sees
            for msg in text_msgs[-2:]:
                sender = "You" if msg.is_from_me else "Them"
                preview = msg.text[:50] + "..." if len(msg.text) > 50 else msg.text
                console.print(f"[dim]   {sender}: {preview}[/dim]")
        else:
            console.print("[dim]⚠️  Context: Reactions/media only (no text messages)[/dim]")
        
        with console.status("[dim]Calling GPT-4o API...[/dim]"):
            draft = generator.generate_followup(
                chat=chat,
                conversation_history=history,
                hours_since_last=stale.hours_since_last_message
            )
        
        console.print(Panel(
            draft,
            title="[cyan]AI-Generated Follow-up[/cyan]",
            border_style="green"
        ))
        console.print()


def main():
    display_header()
    
    if not validate_config():
        sys.exit(1)
    
    try:
        console.print("\n[cyan]Initializing iReply...[/cyan]")
        
        reader = iMessageReader(Config.IMESSAGE_DB_PATH)
        detector = StaleDetector(Config.STALE_THRESHOLD_HOURS)
        generator = DraftGenerator(Config.OPENAI_API_KEY)
        
        console.print(f"[dim]• Reading recent conversations (limit: {Config.MAX_CONVERSATIONS_TO_CHECK})[/dim]")
        chats = reader.get_recent_chats(limit=Config.MAX_CONVERSATIONS_TO_CHECK)
        
        console.print(f"[dim]• Analyzing for stale conversations (threshold: {Config.STALE_THRESHOLD_HOURS}h)[/dim]")
        stale_convos = detector.analyze_conversations(chats)
        
        display_stale_conversations(stale_convos, reader)
        
        if stale_convos:
            if Confirm.ask("\n[bold]Generate follow-up drafts?[/bold]", default=True):
                generate_and_show_drafts(stale_convos, reader, generator)
                
                console.print("\n[yellow]📊 Note:[/yellow] This alpha version only shows drafts.")
                console.print("[dim]• Drafts with text context are more specific[/dim]")
                console.print("[dim]• Reaction-only conversations get generic follow-ups[/dim]")
                console.print("[dim]• Automatic sending will be added in future versions[/dim]")
        
        console.print("\n[green]Done![/green]")
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()

