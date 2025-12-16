from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
import mcp.server.stdio
import json
import os

# Dictionary to store our notes in memory
notes = {}
NOTES_FILE = "notes.json"

# Load existing notes if file exists
if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)

# Create the server instance
app = Server("notes-server")


# Define a resource handler - lists all available notes
@app.list_resources()
async def list_resources() -> list[Resource]:
    """List all available notes as resources"""
    return [
        Resource(
            uri=f"note:///{name}",
            name=f"Note: {name}",
            mimeType="text/plain",
            description=f"A note named {name}",
        )
        for name in notes.keys()
    ]


# Define a resource reader - reads a specific note
@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read the content of a specific note"""
    # Extract note name from URI (note:///my-note -> my-note)
    name = uri.replace("note:///", "")

    if name in notes:
        return notes[name]
    else:
        raise ValueError(f"Note '{name}' not found")


# Define a tool - create or update a note
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "create_note":
        note_name = arguments["name"]
        content = arguments["content"]

        # Save note
        notes[note_name] = content

        # Persist to file
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)

        return [
            TextContent(type="text", text=f"Note '{note_name}' created successfully!")
        ]

    elif name == "delete_note":
        note_name = arguments["name"]

        if note_name in notes:
            del notes[note_name]

            # Persist to file
            with open(NOTES_FILE, "w") as f:
                json.dump(notes, f, indent=2)

            return [
                TextContent(
                    type="text", text=f"Note '{note_name}' deleted successfully!"
                )
            ]
        else:
            return [TextContent(type="text", text=f"Note '{note_name}' not found!")]

    else:
        raise ValueError(f"Unknown tool: {name}")


# Define available tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="create_note",
            description="Create or update a note with given name and content",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the note"},
                    "content": {"type": "string", "description": "Content of the note"},
                },
                "required": ["name", "content"],
            },
        ),
        Tool(
            name="delete_note",
            description="Delete a note by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the note to delete",
                    }
                },
                "required": ["name"],
            },
        ),
    ]


# Run the server
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
