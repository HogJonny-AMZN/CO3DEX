---
layout: post
title: "Natural Language Infrastructure: Making BATS AI-Callable"
summary: "After building a distributed DCC orchestration system, I made it controllable through natural language. Here's how Model Context Protocol (MCP) integration turned BATS into infrastructure that Claude Desktop, Cursor, and VS Code Copilot can operate."
author: hogjonny
date: "2026-04-08 00:00:00 -0600"
modified_date: "2026-04-08 00:00:00 -0600"
category: python
thumbnail: /assets/img/posts/2026-04-15-natural-language-infrastructure-mcp.png
keywords: python,mcp,ai,natural-language,claude,cursor,vscode,fastmcp,grpc,orchestration,dcc,automation
permalink: /blog/natural-language-infrastructure-mcp/
usemathjax: false
---

# Welcome to the Co3deX

Hello and welcome to the CO3DEX, a blog of my Journeys in Real-time 3D Graphics and Technical Art. My name is Jonny Galloway, I am a polymath technical art leader who bridges art, tools, engine, AI and product. I work as a Principal Technical Artist and tools/engine specialist with 30+ years in AAA game development, working across content, design, production, and technology.

## Natural Language Infrastructure: Making BATS AI-Callable

---

## TL;DR (5-Minute Version)

**The Setup:** In [Part 3](/blog/distributed-orchestration-bats/), I built BATS: a distributed gRPC orchestration system for Maya/Houdini (and other DCC) workers. It worked great for batch processing, giving me 6.7x-40x speedups on parallel workloads.

**The Problem:** Using BATS required:
- Writing Python scripts to submit jobs via gRPC
- Polling logs or watching the UI for status
- Editing JSON files to configure workers
- Reading documentation to remember API signatures

**The Realization:** AI assistants (Claude Desktop, Cursor, VS Code Copilot) can call tools through Model Context Protocol (MCP). What if BATS exposed itself as MCP tools?

**The Solution:** Built 20 BATS MCP tools across 3 categories (job management, orchestrator control, worker configuration). Now I can say "Submit 10 Maya jobs for these hero swords" and Claude handles the gRPC calls.

**The Results:**
- Natural language job submission instead of writing scripts
- Conversational monitoring ("Show me failed jobs from today")
- Voice-controlled orchestrator management
- Self-healing configurations ("Add Blender support with 4 workers")

**Core Lesson:** Infrastructure doesn't have to be code-first. MCP transforms technical APIs into natural language interfaces that AI can operate. It's not replacing developers... it's making infrastructure conversational.

**Read on for:** MCP architecture, FastMCP implementation patterns, production integration, lessons learned, and what happens when infrastructure becomes a conversation.

---

## The Integration Challenge

BATS worked well. The distributed orchestration handled hundreds of concurrent DCC jobs. I could submit work through Python scripts or the Mock Editor UI.

But there was friction.

**Example workflow (before MCP):**

1. Artist: "I need 5 hero sword variants with different blade lengths"
2. TA (me): Opens VS Code
3. TA: Writes Python script:

   ```python
   import grpc
   from job_orchestrator.protos import job_pb2, orchestrator_pb2_grpc

   channel = grpc.insecure_channel('localhost:50051')
   stub = orchestrator_pb2_grpc.ExternalJobAPIStub(channel)

   for i, length in enumerate([1.2, 1.5, 1.8, 2.0, 2.3]):
       request = job_pb2.JobRequest(
           dcc_type="maya",
           execution_mode=job_pb2.ExecutionMode.HEADLESS,
           module_path="job_orchestrator.jobs.examples.maya.generate_hero_sword",
           parameters={
               "asset_name": f"hero_sword_variant_{i+1}",
               "blade_length": str(length),
               "output_dir": "D:/Assets/Weapons",
               "export_fbx": "True"
           },
           priority=5
       )
       response = stub.SubmitJob(request)
       print(f"Submitted: {response.job_id}")
   ```

4. TA: Runs script
5. TA: Opens system tray monitor to check status
6. TA: 10 minutes later, tells artist the assets are ready

**Time:** 5-10 minutes (mostly context switching and boilerplate)

**What I wanted:**

1. Artist: "I need 5 hero sword variants with different blade lengths"
2. Me (to Claude): "Submit 5 Maya jobs for hero swords with blade lengths 1.2, 1.5, 1.8, 2.0, 2.3"
3. Claude: [calls `bats_submit_job()` 5 times, monitors progress]
4. Claude: "✓ All 5 jobs completed successfully. Assets in D:/Assets/Weapons"

**Time:** 30 seconds

The difference? AI handles the boilerplate. I describe what I want in natural language, AI translates to API calls.

---

## What is Model Context Protocol (MCP)?

**MCP** is Anthropic's protocol for exposing tools to AI assistants. Think of it as a plugin system for Claude... you write Python functions, decorate them with `@mcp.tool()`, and Claude can call them.

Four moving parts:

- **MCP Server:** Your code — exposes tools that AI can discover and call
- **MCP Client:** The AI assistant (Claude Desktop, Cursor, VS Code) that calls them
- **Transport:** stdio (pipes) for local use, HTTP+SSE for remote
- **Tools:** The decorated Python functions themselves

**Simple example:**

```python
from mcp import FastMCP

mcp = FastMCP("MyTools")

@mcp.tool()
def get_current_weather(location: str) -> dict:
    """Get the current weather for a location.
    
    Args:
        location: City name (e.g., "Seattle, WA")
    
    Returns:
        dict with temperature, conditions, humidity
    """
    # Your API call here
    return {"temp": 72, "conditions": "sunny", "humidity": 45}

# Start server (stdio mode for Claude Desktop)
mcp.run()
```

**Claude Desktop config:**

```json
{
  "mcpServers": {
    "my_tools": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

Now when you chat with Claude Desktop, it can call `get_current_weather()` automatically when you ask about weather.

**Why MCP matters for infrastructure:**

Before MCP, my infrastructure was just gRPC endpoints and CLI scripts. I kept docs around to remember the signatures. I wrote Python to call them. Every new operation meant opening VS Code and writing boilerplate.

With MCP, the infrastructure becomes tools with descriptions... AI reads those descriptions and calls the right endpoints. I just say what I want.

**Describe intent, not implementation.** That's the whole shift.

---

## BATS MCP Architecture

I designed 20 tools across 3 categories:

### 1. Job Management Tools (7 tools)

**Core operations:**

- `bats_submit_job` - Submit new DCC job (Maya/Houdini/Python) with script or module
- `bats_submit_python_job` - Shorthand for submitting pure Python jobs
- `bats_get_job_result` - Poll until complete and retrieve output
- `bats_cancel_job` - Stop a running job
- `bats_list_jobs` - Query jobs with filters (status, priority, date range)

**Monitoring:**

- `bats_get_pool_status` - Check worker availability (idle/busy/crashed counts)
- `bats_list_worker_types` - Discover which DCC worker types are configured

### 2. Orchestrator Control Tools (6 tools)

**Lifecycle:**

- `bats_start_orchestrator` - Start BATS swarm with logging options
- `bats_start_orchestrator_with_tray` - Start with system tray monitor
- `bats_stop_orchestrator` - Graceful shutdown

**Health & Config:**

- `bats_get_orchestrator_status` - Check if orchestrator is running
- `bats_get_orchestrator_config` - View current settings (ports, worker pools)
- `bats_list_tools` - Discover all available BATS tools (introspection)

### 3. Worker Configuration Tools (7 tools)

**DCC Support:**

- `bats_list_configured_workers` - Show all configured worker types and pool sizes
- `bats_get_worker_type_template` - Get a pre-built config template for a DCC (e.g., Blender)
- `bats_add_worker_type` - Register a new DCC worker type from a config template
- `bats_remove_worker_type` - Remove a worker type from the registry

**Worker Pools & Paths:**

- `bats_update_worker_pool_sizes` - Scale headless/GUI worker counts up or down
- `bats_add_dcc_path` - Register an executable path for a DCC type

**Validation:**

- `bats_validate_worker_config` - Check a worker config for errors before applying it

### The Tool Hierarchy

```
BATS MCP Server
├── Job Management (day-to-day operations)
│   ├── Submit/Monitor/Cancel jobs
│   └── Query job history
├── Orchestrator Control (admin operations)
│   ├── Start/Stop/Restart
│   └── Configuration management
└── Worker Configuration (infrastructure setup)
    ├── Add DCC support
    ├── Scale worker pools
    └── Customize environments
```

**Design principle:** Each tool does one thing well. Natural language composition handles complexity.

**Example composition:**

> **Me:** "Submit 10 Maya jobs and show me which workers are idle"
>
> **Claude:** [calls `bats_submit_job()` 10 times, then `bats_get_pool_status()`]

Two tools, composed through natural language.

---

## Implementation: FastMCP + gRPC

### The MCP Server Structure

```python
# mcp_server/server.py
from mcp.server.fastmcp import FastMCP
from mcp_server.client.grpc_client import OrchestratorGrpcClient
from mcp_server.tools.job_tools import register_job_tools
from mcp_server.tools.orchestrator_tools import register_orchestrator_tools
from mcp_server.tools.worker_config_tools import register_worker_config_tools

# Initialize FastMCP server with instructions for AI context
mcp = FastMCP(
    name="bats-orchestrator",
    instructions="BATS (Background Automation Task Swarm) — Distributed DCC job orchestration..."
)

# Shared gRPC client (singleton, lazy-connected)
_client: OrchestratorGrpcClient | None = None

async def _get_client() -> OrchestratorGrpcClient:
    """Return the shared gRPC client, auto-connecting on first use."""
    if _client is None:
        raise RuntimeError("gRPC client not initialized")
    if _client._channel is None:
        await _client.connect()
    return _client

@mcp.tool(name="bats_submit_job")
async def submit_job(
    dcc_type: str,
    script: str = "",
    module_path: str = "",
    entry_point: str = "main",
    parameters: dict[str, str] | None = None,
    execution_mode: str = "HEADLESS",
    priority: int = 5,
    input_files: list[str] | None = None,
    output_files: list[str] | None = None,
) -> dict:
    """Submit a DCC job to BATS orchestrator.
    
    Use this tool to submit Maya, Houdini, or Python jobs for processing.
    Jobs run in worker pools and execute Python modules with parameters.
    
    Args:
        dcc_type: DCC type - must be "maya", "houdini", or "python"
        module_path: Python module path (e.g., "job_orchestrator.jobs.examples.maya.generate_hero_sword")
        parameters: Job parameters as key-value dict (all values must be strings)
        priority: Job priority 0-10 (higher = more urgent, default: 5)
        execution_mode: "headless" for batch processing (default) or "gui" for viewport work
        job_id: Optional custom job ID (auto-generated if not provided)
    
    Returns:
        dict with job_id, status, message
        
    Example:
        bats_submit_job(
            dcc_type="maya",
            module_path="job_orchestrator.jobs.examples.maya.generate_hero_sword",
            parameters={"blade_length": "1.5", "output_dir": "D:/Assets"}
        )
    """
    stub = get_orchestrator_stub()
    
    # Convert execution_mode string to enum
    exec_mode = job_pb2.ExecutionMode.HEADLESS if execution_mode == "headless" else job_pb2.ExecutionMode.GUI
    
    # Build request
    request = job_pb2.JobRequest(
        dcc_type=dcc_type,
        execution_mode=exec_mode,
        module_path=module_path,
        parameters=parameters,
        priority=priority
    )
    
    if job_id:
        request.job_id = job_id
    
    # Submit job via gRPC
    response = stub.SubmitJob(request)
    
    return {
        "job_id": response.job_id,
        "status": response.status,
        "message": response.message
    }

@mcp.tool(name="bats_get_job_result")
async def get_job_result(
    job_id: str,
    timeout_seconds: int = 300
) -> dict:
    """Wait for a job to complete and return its result.
    
    Use this tool after submitting a job to poll until completion and get output.
    Blocks until the job finishes or timeout is reached.
    
    Args:
        job_id: Job ID from bats_submit_job response
        timeout_seconds: Maximum wait time in seconds (default: 300)
    
    Returns:
        dict with job_id, status, output_files, logs, error (if failed)
        
    Example:
        bats_get_job_result(job_id="job_abc123", timeout_seconds=600)
    """
    client = await _get_client()
    return await client.get_job_result(job_id, timeout=timeout_seconds)

@mcp.tool()
def bats_list_jobs(
    status_filter: str = None,
    limit: int = 10
) -> dict:
    """List recent jobs with optional filtering.
    
    Use this tool to see job history, find failed jobs, or check queue depth.
    
    Args:
        status_filter: Optional status filter - "QUEUED", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"
        limit: Maximum number of jobs to return (default: 10, max: 100)
    
    Returns:
        dict with jobs list and total count
        
    Example:
        bats_list_jobs(status_filter="FAILED", limit=5)
    """
    stub = get_orchestrator_stub()
    
    query = job_pb2.JobListQuery(limit=min(limit, 100))
    
    if status_filter:
        query.status_filter = status_filter
    
    response = stub.ListJobs(query)
    
    jobs = []
    for job in response.jobs:
        jobs.append({
            "job_id": job.job_id,
            "dcc_type": job.dcc_type,
            "status": job_pb2.JobStatus.Name(job.status),
            "priority": job.priority,
            "progress": job.progress,
            "created_at": job.created_at.ToDatetime().isoformat() if job.created_at else None
        })
    
    return {
        "jobs": jobs,
        "total": response.total_count
    }

@mcp.tool()
def bats_get_pool_status() -> dict:
    """Get the status of all DCC worker pools.
    
    Use this tool to check worker availability, see which jobs are running,
    and identify crashed workers.
    
    Returns:
        dict with worker pool status for each DCC type
        
    Example:
        bats_get_pool_status()
    """
    stub = get_orchestrator_stub()
    
    # Query pool status
    response = stub.GetPoolStatus(job_pb2.PoolQuery())
    
    pools = {}
    for dcc_type, pool in response.pools.items():
        pools[dcc_type] = {
            "total_workers": pool.total_workers,
            "ready_workers": pool.ready_workers,
            "busy_workers": pool.busy_workers,
            "crashed_workers": pool.crashed_workers,
            "workers": [
                {
                    "worker_id": w.worker_id,
                    "status": w.status,
                    "current_job_id": w.current_job_id if w.current_job_id else None
                }
                for w in pool.workers
            ]
        }
    
    return pools

def main():
    # Initialize shared gRPC client
    global _client
    _client = OrchestratorGrpcClient(host="localhost", port=50051)

    # Register all tool groups
    register_job_tools(mcp, _get_client)
    register_orchestrator_tools(mcp, _get_client)
    register_worker_config_tools(mcp)

    # Run in stdio mode (for Claude Desktop / Cursor)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### Key Implementation Patterns

**1. Comprehensive Docstrings**

The docstring is the thing. AI reads it to figure out WHAT a tool does and WHEN to reach for it:

```python
@mcp.tool()
def bats_submit_job(...) -> dict:
    """Submit a DCC job to BATS orchestrator.
    
    Use this tool to submit Maya, Houdini, or Python jobs for processing.
    Jobs run in worker pools and execute Python modules with parameters.
    
    Args:
        dcc_type: DCC type - must be "maya", "houdini", or "python"
        ...
    
    Returns:
        dict with job_id, status, message
        
    Example:
        bats_submit_job(...)
    """
```

That "Use this tool to..." line is doing real work — it's what tips Claude toward reaching for this function.

**2. Type Hints**

FastMCP uses type hints to generate JSON schemas for AI:

```python
async def submit_job(
    dcc_type: str,                        # AI knows this is a string
    priority: int = 5,                    # AI knows this is int with default
    parameters: dict[str, str] | None,    # AI knows this is string→string mapping
) -> dict:                                # AI knows the return type
```

**3. Error Handling**

Tools return structured errors instead of raising exceptions:

```python
@mcp.tool(name="bats_submit_job")
async def submit_job(dcc_type: str, ...) -> dict:
    try:
        client = await _get_client()
        # ... gRPC call ...
    except grpc.RpcError as e:
        return {
            "error": "Failed to connect to orchestrator",
            "details": str(e),
            "suggestion": "Check if orchestrator is running with bats_get_orchestrator_status()"
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "details": str(e)
        }
```

Claude picks up the `suggestion` field and turns it into "try running `bats_start_orchestrator()` first" — users never see raw error codes.

**4. Environment Configuration**

Connection settings come from environment variables:

```python
ORCHESTRATOR_HOST = os.getenv("BATS_ORCHESTRATOR_HOST", "localhost")
ORCHESTRATOR_PORT = os.getenv("BATS_ORCHESTRATOR_PORT", "50051")
```

This allows the same MCP server to connect to different orchestrators (local dev, staging, production).

---

## Claude Desktop Integration

### Configuration

```json
// %APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "bats": {
      "command": "D:/path/to/bats/.venv/Scripts/python.exe",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "BATS_ORCHESTRATOR_HOST": "localhost",
        "BATS_ORCHESTRATOR_PORT": "50051"
      }
    }
  }
}
```

**After restart, Claude sees 20 BATS tools.**

### Real Conversations

**Example 1: Batch Job Submission**

> **Me:** Submit 5 Maya jobs to generate hero swords with blade lengths 1.2, 1.5, 1.8, 2.0, and 2.3 meters. Output to D:/Assets/Weapons.

> **Claude:** I'll submit 5 Maya jobs for hero sword generation with varying blade lengths.
>
> [Calling `bats_submit_job()` 5 times...]
>
> ✓ All 5 jobs submitted successfully:
> - job_a1b2c3: blade_length=1.2
> - job_d4e5f6: blade_length=1.5  
> - job_g7h8i9: blade_length=1.8
> - job_j0k1l2: blade_length=2.0
> - job_m3n4o5: blade_length=2.3
>
> Assets will be saved to D:/Assets/Weapons. Would you like me to monitor their progress?

**Example 2: Troubleshooting**

> **Me:** Why aren't my jobs running?

> **Claude:** Let me check the orchestrator and worker status.
>
> [Calling `bats_get_orchestrator_status()`...]  
> Orchestrator: Running ✓
>
> [Calling `bats_get_pool_status()`...]
>
> Issue found: All Maya workers are busy (4/4), and you have 12 jobs queued.
>
> Options:
> 1. Wait for current jobs to complete (~5 minutes based on progress)
> 2. Scale up worker pool with `bats_update_worker_pool_sizes("maya", headless_count=8)`
> 3. Cancel low-priority jobs to free workers
>
> What would you like to do?

**Example 3: Configuration**

> **Me:** Add Blender support with 4 headless workers

> **Claude:** I'll configure Blender as a new DCC type in BATS.
>
> [Calling `bats_get_worker_type_template("blender")`...]  
> Retrieved Blender worker config template.
>
> [Calling `bats_add_dcc_path("blender", "C:/Program Files/Blender Foundation/Blender 4.1/blender.exe")`...]  
> Registered Blender executable path.
>
> [Calling `bats_add_worker_type("blender", <template config>)`...]  
> Registered Blender worker type.
>
> [Calling `bats_update_worker_pool_sizes("blender", headless_count=4)`...]  
> Set pool: 4 headless Blender workers.
>
> [Calling `bats_stop_orchestrator()`... then `bats_start_orchestrator()`...]  
> Orchestrator restarted to apply configuration.
>
> ✓ Blender support is now active. You can submit jobs with `dcc_type="blender"`.

**The key difference:** I describe what I want, Claude figures out the tool sequence.

---

## Production Integration Lessons

### Lesson 1: Tool Discovery is Critical

Initially, Claude didn't know when to use certain tools. I added `bats_list_tools()` for introspection:

```python
@mcp.tool()
def bats_list_tools() -> dict:
    """List all available BATS MCP tools and their purposes.
    
    Use this tool when the user asks "What can BATS do?" or when you need
    to discover available operations.
    
    Returns:
        dict with tool categories and descriptions
    """
    return {
        "job_management": {
            "bats_submit_job": "Submit new DCC job",
            "bats_get_job_status": "Check job progress",
            "bats_get_job_result": "Retrieve completed output",
            "bats_cancel_job": "Stop running job",
            "bats_list_jobs": "Query job history",
            "bats_get_pool_status": "Check worker availability"
        },
        "orchestrator_control": {
            "bats_start_orchestrator": "Start BATS swarm",
            "bats_start_orchestrator_with_tray": "Start with system tray monitor",
            "bats_stop_orchestrator": "Graceful shutdown",
            # ... etc
        }
    }
```

Now when I ask "What can you do with BATS?", Claude calls this tool and explains accurately.

### Lesson 2: Stdout Must Be Clean

MCP uses stdio transport (stdin/stdout). Any print statements break the protocol:

```python
# ❌ BREAKS MCP:
print(f"Connecting to orchestrator at {ORCHESTRATOR_HOST}...")

# ✅ USE LOGGING:
import logging
logger = logging.getLogger(__name__)
logger.info(f"Connecting to orchestrator at {ORCHESTRATOR_HOST}")
```

Logging goes to stderr, which doesn't interfere with MCP protocol on stdout.

### Lesson 3: Connection Lifecycle Matters

Original code opened a new gRPC channel per tool call:

```python
@mcp.tool()
async def submit_job(...):
    channel = grpc.insecure_channel(...)  # New connection every call
    stub = ExternalJobAPIStub(channel)
    # ...
```

This caused 30-50ms overhead per call. For batch operations (5-10 jobs), that's 300-500ms wasted.

#### Fix: Shared client singleton with lazy connect

```python
# Module-level singleton, initialized at startup
_client: OrchestratorGrpcClient | None = None

async def _get_client() -> OrchestratorGrpcClient:
    if _client._channel is None:
        await _client.connect()  # Connect once, reuse forever
    return _client
```

All tools call `_get_client()` instead of creating their own channel. Batch operations went from 500ms to 50ms.

### Lesson 4: Protobuf Serialization is Tricky

Returning raw protobuf messages to FastMCP caused serialization errors:

```python
# ❌ FAILS:
@mcp.tool()
def bats_list_jobs() -> list:
    response = stub.ListJobs(query)
    return response.jobs  # Can't serialize protobuf repeated field

# ✅ WORKS:
@mcp.tool()
def bats_list_jobs() -> dict:
    response = stub.ListJobs(query)
    jobs = []
    for job in response.jobs:
        jobs.append({
            "job_id": job.job_id,
            "status": job_pb2.JobStatus.Name(job.status),  # Convert enum to string
            # ... extract all fields ...
        })
    return {"jobs": jobs, "total": response.total_count}
```

Convert protobuf messages to plain dicts/lists.

### Lesson 5: Restart Required for Discovery

Claude Desktop caches tool schemas at startup. Adding new tools requires restart:

1. Add new `@mcp.tool()` to server.py
2. Quit Claude Desktop completely
3. Relaunch Claude Desktop
4. New tools are now discoverable

HTTP+SSE mode refreshes automatically, but stdio mode doesn't.

---

## What This Unlocks

### 1. Voice-Controlled Infrastructure

With Claude Desktop's voice input:

> "Submit 20 rock mesh processing jobs, priority 8, and tell me when they're done"

Claude translates speech → API calls → monitors completion → notifies you.

**Before:** Write script, run script, check logs.  
**After:** Speak intent, Claude executes.

### 2. Self-Healing Configurations

Claude can detect and fix configuration issues:

> **Me:** Jobs are failing with "Maya not found"

> **Claude:** [Calling `bats_get_orchestrator_config()`...]
>
> Issue: Maya executable path is incorrect.  
> Current: `C:/Program Files/Autodesk/Maya2025/bin/maya.exe`  
> Expected: `C:/Program Files/Autodesk/Maya2026/bin/maya.exe`
>
> [Calling `bats_add_dcc_path("maya", "C:/Program Files/Autodesk/Maya2026/bin/maya.exe")`...]  
> Updated Maya path to 2026.
>
> [Calling `bats_stop_orchestrator()`... then `bats_start_orchestrator()`...]  
> Restarted orchestrator.
>
> ✓ Fixed. Try resubmitting your jobs.

**Before:** Debug, edit JSON, restart manually.  
**After:** Report problem, Claude fixes.

### 3. Exploratory Workflows

Ask questions you don't know how to answer programmatically:

> **Me:** Which jobs have been running for more than 10 minutes?

> **Claude:** [Calling `bats_list_jobs(status_filter="RUNNING")`...]
>
> 3 jobs running over 10 minutes:
> - job_abc123: 15 min (Maya render)
> - job_def456: 12 min (Houdini fluid sim)
> - job_ghi789: 11 min (Maya texture bake)
>
> These are normal for their job types. Should I cancel any?

I didn't know how to query that programmatically off the top of my head. Claude just... figured it out.

### 4. Documentation-Free Operation

I don't remember all 20 tool signatures. But Claude does:

> **Me:** Submit a Houdini job for procedural rocks

> **Claude:** I'll need a few details:
> 1. Which Houdini job module? (I can list available modules)
> 2. Output directory?
> 3. Job priority (0-10)?

Claude knows what parameters are required and asks for missing ones.

---

## Architecture Patterns That Worked

### 1. Thin MCP Layer

MCP tools are thin wrappers around gRPC calls:

```python
@mcp.tool()
def bats_submit_job(...) -> dict:
    """[Rich docstring for AI]"""
    
    # 1. Convert MCP parameters to protobuf
    request = job_pb2.JobRequest(...)
    
    # 2. Call gRPC API
    response = stub.SubmitJob(request)
    
    # 3. Convert protobuf response to dict
    return {"job_id": response.job_id, ...}
```

No business logic in MCP layer. It's pure translation.

**Benefits:**
- MCP tools stay simple (easy to maintain)
- Business logic stays in orchestrator (single source of truth)
- Can add other interfaces (REST API, CLI) without duplicating logic

### 2. Consistent Error Format

All tools return errors in the same structure:

```python
return {
    "error": "Brief description",
    "details": str(exception),
    "suggestion": "What to try next"
}
```

Claude picks up on the "suggestion" field and turns it into actual next-step advice. Users never see raw error codes.

### 3. Environment-Based Configuration

Connection settings come from environment variables:

```json
{
  "mcpServers": {
    "bats-dev": {
      "env": {"BATS_ORCHESTRATOR_HOST": "localhost", "BATS_ORCHESTRATOR_PORT": "50051"}
    },
    "bats-staging": {
      "env": {"BATS_ORCHESTRATOR_HOST": "staging-server", "BATS_ORCHESTRATOR_PORT": "50051"}
    },
    "bats-prod": {
      "env": {"BATS_ORCHESTRATOR_HOST": "prod-server.example.com", "BATS_ORCHESTRATOR_PORT": "50051"}
    }
  }
}
```

Same MCP server code, different environments.

### 4. Tool Categories

I grouped tools into three categories so Claude has context for intent:

- **Job Management** - Day-to-day operations (submit, monitor, cancel)
- **Orchestrator Control** - Admin operations (start, stop, configure)
- **Worker Configuration** - Infrastructure setup (add DCCs, scale pools)

When I say "Submit a job"... Claude doesn't have to guess. It knows where to look.

---

## Limitations and Trade-offs

### What MCP is NOT Good For

**1. Streaming Real-Time Updates**

MCP tools are request/response. You can't stream job progress in real-time:

```python
# ❌ CAN'T DO THIS:
@mcp.tool()
def bats_monitor_job_realtime(job_id: str):
    for update in stub.StreamJobStatus(job_id):
        yield update  # MCP doesn't support streaming responses
```

**Workaround:** Poll with `bats_get_job_result()` — it handles the wait loop for you.

**2. Complex Visualizations**

AI can't render charts or graphs. You get text/JSON:

> **Claude:** Job completion rate over last 24 hours:
> - 00:00-06:00: 45 jobs (90% success)
> - 06:00-12:00: 67 jobs (85% success)
> - 12:00-18:00: 89 jobs (92% success)
> - 18:00-24:00: 23 jobs (78% success)

For visual dashboards, use traditional UI (web dashboard, system tray monitor).

**3. File Operations**

MCP tools can't directly open/edit files. Claude can suggest changes, but you execute:

> **Claude:** To fix the Houdini path issue, edit this file:
> `job_orchestrator/config/orchestrator_config.json`
>
> Change:
> `"houdini": "C:/Program Files/SideFX/Houdini 20.0.688/bin/hython.exe"`
>
> To:
> `"houdini": "C:/Program Files/SideFX/Houdini 21.0.123/bin/hython.exe"`

You still make the edit manually (or Claude can write the file if you have file access tools).

### The Learning Curve

**For developers:**
- Learn MCP concepts (20 minutes)
- Learn FastMCP library (30 minutes)
- Debug stdio transport issues (1-2 hours, honestly)

**For users:**
- Learn nothing. Just talk to Claude.

All the complexity stays on my side of the wall. That's the point.

---

## Production Results

### Metrics (March 2026, 2 weeks of use)

**Job submission:**
- Before MCP: ~2 minutes per batch (write script, run, monitor)
- After MCP: ~30 seconds (natural language request)
- Time saved: 75%

**Configuration changes:**
- Before MCP: ~5 minutes (edit JSON, restart, verify)
- After MCP: ~1 minute (tell Claude, it handles it)
- Time saved: 80%

**Troubleshooting:**
- Before MCP: ~10 minutes (read logs, check pool status, correlate issues)
- After MCP: ~2 minutes (ask Claude, it diagnoses)
- Time saved: 80%

**Most common operations:**

1. Batch job submission (used 150+ times)
2. Pool status checks (used 80+ times)
3. Failed job investigation (used 40+ times)
4. Worker scaling (used 15+ times)

**Unexpected benefits:**

- **Onboarding:** New team member could submit jobs without reading documentation
- **Remote work:** Voice commands while away from keyboard
- **Context switching:** No need to open VS Code for quick job submissions

---

## Lessons Learned

### 1. **Natural Language != Imprecise**

I expected NL commands to be ambiguous:

> "Submit some hero sword jobs"

But Claude asks clarifying questions:

> How many jobs? What blade lengths? Which output directory? Priority level?

Natural language can be as precise as code, just more conversational.

### 2. **AI Understands Intent Better Than Code**

When I say:

> "Restart the orchestrator to pick up the new configuration"

Claude knows:
1. Call `bats_stop_orchestrator()` (graceful shutdown)
2. Call `bats_start_orchestrator()` once stopped
3. Call `bats_get_orchestrator_status()` to verify it's running

It infers the multi-step workflow from a single sentence.

### 3. **Documentation Lives in Docstrings**

I used to write tools, then write docs separately. Docs always drifted — a renamed parameter here, a changed return shape there, and suddenly the docs are lying to you.

With MCP the docstring IS the documentation. AI reads it directly... so if I update the docstring when I change the code, docs are automatically current. No separate doc site to maintain. No drift.

**Result:** Documentation can't drift when it's the same text the AI is calling.

### 4. **Error Messages Matter More**

When code fails, developers read stack traces. When AI calls tools, users see error messages:

```python
# ❌ BAD:
return {"error": "GRPC_ERR_CONNECTION_FAILED"}

# ✅ GOOD:
return {
    "error": "Failed to connect to orchestrator",
    "details": "Connection refused to localhost:50051",
    "suggestion": "Check if orchestrator is running with: bats_get_orchestrator_status()"
}
```

AI translates the "suggestion" into actionable advice for users.

### 5. **MCP is Infrastructure as Conversation**

Before MCP: Infrastructure = code you write against  
After MCP: Infrastructure = system you talk to

It's not AI replacing developers. It's AI making infrastructure accessible to more people (artists, designers, QA, producers).

---

## Conclusion: Conversational Infrastructure

Going from raw gRPC APIs (Part 3) to MCP tools (Part 4) taught me something I didn't expect: **infrastructure doesn't have to be code-first**.

> **Traditional model:** Write code → Call APIs → Infrastructure does work  
> **MCP model:** Speak intent → AI calls APIs → Infrastructure does work

### The Four-Part Arc

**Part 1 ([Tool Logging](/blog/tool-logging-with-python/)):**  
Built observability. Can't fix what you can't see.

**Part 2 ([Threading Anti-patterns](/blog/threading-antipatterns-qt-async/)):**  
Simplified architecture. Don't add complexity without benefit.

**Part 3 ([Distributed Orchestration](/blog/distributed-orchestration-bats/)):**  
Scaled with parallelism. Built BATS for batch processing.

**Part 4 (This post):**  
Made it conversational. Exposed BATS through natural language.

**Each step builds on the previous:**
- Logging showed what was happening
- Simplifying removed false complexity
- Scaling added real parallelism
- MCP removed interface complexity

### Key Takeaways

1. **MCP is a protocol, not magic** - It's JSON-RPC over stdio/HTTP with tool schemas

2. **Tools are thin wrappers** - Keep business logic in your infrastructure, MCP translates

3. **Docstrings are documentation** - AI reads them, so write for AI (then humans benefit too)

4. **Errors need context** - Include suggestions for what to try next

5. **Connection lifecycle matters** - Reuse channels, handle reconnection gracefully

6. **Natural language is precise** - When AI asks clarifying questions

7. **Infrastructure becomes accessible** - Non-developers can operate complex systems

### What I Achieved

- ✅ 20 BATS MCP tools across 3 categories
- ✅ 75-80% time savings on common operations
- ✅ Voice-controlled job submission
- ✅ Self-healing configuration workflows
- ✅ Zero documentation required for users
- ✅ Onboarding time: minutes instead of days

### The Bigger Picture

MCP represents a shift in how I think about infrastructure:

**Before MCP:**

- My infrastructure exposed gRPC APIs
- I wrote Python to call them
- Artists asked me to submit their batch jobs

**After MCP:**

- My infrastructure exposes tools
- Claude calls them from natural language
- Artists just... ask

It's not replacing me. It's removing me as the bottleneck.

### The Golden Rule

> **"If a human can describe what they want in a sentence, AI should be able to execute it."**

That's the MCP promise. And with 20 BATS tools, it works.

**What's next?** Expanding MCP tools to other infrastructure:
- Source control operations (commit, merge, deploy)
- Cloud resource management (EC2, S3, Lambda)
- Monitoring and alerting (query metrics, acknowledge alerts)
- Build systems (trigger builds, check status)

Any system with an API can become conversational through MCP.

### Want to Learn More?

**MCP Resources:**
- [Model Context Protocol Specification](https://modelcontextprotocol.io/) - **Official docs:** Protocol details, transport modes, best practices.
- [FastMCP Library](https://github.com/jlowin/fastmcp) - **GitHub:** Python library for building MCP servers, examples included.
- [Claude Desktop](https://claude.ai/desktop) - **Download:** AI assistant with MCP support built-in.

**Related Topics:**
- [gRPC + MCP Integration](https://grpc.io/docs/) - Combining distributed systems with AI interfaces
- [Tool Use Best Practices](https://docs.anthropic.com/claude/docs/tool-use) - How Claude decides when to call tools

**Final thought:** Infrastructure should be accessible to everyone who needs it. MCP makes that possible.

---

_This post is Part 4 of a series on building maintainable game development tools:_
- _[Part 1: Tool Logging with Python](/blog/tool-logging-with-python/)_
- _[Part 2: Don't Thread What You Can't Parallelize](/blog/threading-antipatterns-qt-async/)_
- _[Part 3: When Parallelization IS the Answer](/blog/distributed-orchestration-bats/)_
- _Part 4: Natural Language Infrastructure (this post)_

_Have you built MCP tools? Made infrastructure conversational? Integrated AI with production systems? Let me know in the comments or reach out on [Twitter](https://twitter.com/hogjonny) or [LinkedIn](https://www.linkedin.com/in/hogjonny). Want to see the BATS MCP implementation? Check the [BATS repository](https://github.com/HogJonny-AMZN/BATS) (coming soon)._

---

```python
import logging as _logging
_MODULENAME = 'co3dex.posts.natural_language_infrastructure_mcp'
_LOGGER = _logging.getLogger(_MODULENAME)
_LOGGER.info(f'Initializing: {_MODULENAME} ... infrastructure: from code to conversation')
```

---
