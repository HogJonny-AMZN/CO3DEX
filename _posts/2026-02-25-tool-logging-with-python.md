---
layout: post
title: "Tool Logging with Python"
summary: "Lessons learned from transforming a fragile prototype into a maintainable production tool through defensive logging strategies"
author: hogjonny
date: "2026-02-25 12:00:00 -0600"
category: python
thumbnail: /assets/img/generic_post_banner.png
keywords: python,logging,tools,debugging,qt,pyside,architecture
permalink: /blog/tool-logging-with-python/
usemathjax: false
---

# Welcome to the Co3deX

Hello and welcome to the CO3DEX, a blog of my Journey's in Real-time 3D Graphics and Technical Art. My name is Jonny Galloway, I am a polymath technical art leader who bridges art, tools, engine, and product.  I work as a Principal Technical Artist and tools/engine specialist with 30+ years in AAA game development, working across content, design, production, and technology.

# Tool Logging with Python: A Case Study in Defensive Programming

## Introduction: Inheriting the "Working Prototype"

We've all been there. You inherit a tool from a departed colleague—someone who had just enough knowledge to make something functional, but not enough experience with established patterns and practices to make it maintainable. The tool works, sort of. Users are using it. But when something goes wrong, you're left staring at code that feels like a puzzle with half the pieces missing.

This is the story of one such tool, and how proper logging transformed it from a brittle prototype into a debuggable, maintainable production asset.

### The Problem

The tool in question was a Python/PySide application for processing game assets through a multi-stage pipeline: Houdini for geometry reduction, Substance Designer for texture baking, and Maya for final export. The workflow itself was sound. The implementation? Not so much.

Here's what I walked into:

**The User Experience:**

- Main window with asset selection and a "Run" button
- Clicking "Run" spawned a second progress window with a simple console widget
- The console would display... something. Sometimes. When it felt like it.
- Users had no real visibility into what was happening or why things failed

**The Implementation Nightmare:**

- Three separate subprocess stages (Houdini, Substance, Maya)
- Each wrapped in threading code attempting "non-blocking UI"
- No actual parallelization—each stage had to wait for the previous one
- Threading made debugging nearly impossible
- Single monolithic script with cryptic variable names and convoluted flow
- Houdini would write a log file, which the tool would read _after completion_ and dump to the console
- No technical logging, no validation, no error context
- No way to troubleshoot failures without re-running the entire 5-8 minute pipeline

When something went wrong (and it often did), users would send screenshots of the console showing "Process failed" with no context. Developers would have to read through Houdini's log files manually (but there was nothing there but pass or fail), a desire to cross-reference with substance logs (but they didn't exist), check Maya's output (which wasn't logging either), and try to reconstruct what happened. It was a forensic investigation every single time.

### The Transformation

Rather than rewrite everything from scratch, I took an incremental approach, starting with the foundation every debugging session relies on: **logging**.

Here's what changed:

**1. Hierarchical Logging Architecture**
I implemented Python's logging hierarchy with separate concerns:

- **Module loggers** for technical/developer logging (full debug traces, stack traces, internal state)
- **Console loggers** for user-facing messages (clean, actionable feedback)
- **File handlers** capturing everything at DEBUG level for post-mortem analysis
- Separate log levels per handler, not per logger (developers get everything, users get clarity)

**2. Real-Time Process Monitoring**
Instead of reading log files after completion:

- Captured stdout/stderr from all subprocesses in real-time
- Routed subprocess output through the logging system
- Eventually migrated to QProcess for true async subprocess handling (ripping out all the threading code)
- Console handler displayed live progress with proper formatting

**3. Defensive Logging from the Start**
This wasn't just about fixing bugs—it was about _preventing_ them:

- Validation logging before expensive operations
- Entry/exit logging for major functions
- Error context (what was being processed, what stage, what parameters)
- Performance logging (timing each stage)
- File path logging (exactly which assets passed/failed)

**4. Integrated Console in Main Window**

- Removed the separate progress dialog entirely
- Added a proper console widget to the main window using a custom log handler
- Users could see real-time progress without window management
- Console stayed visible for copy/paste of error messages
- Debug mode toggle for power users who wanted technical details
- The UI was never blocked, and users had confidence the tool was working

### The Impact

The results were immediate and dramatic:

**For Users:**

- Clear, actionable error messages ("Asset X failed validation: missing UV set") instead of "Process failed"
- Real-time progress visibility (no more "is it frozen or just slow?")
- Ability to copy/paste log output for bug reports
- Confidence that the tool was actually working

**For Developers:**

- Full debug traces in log files for every run
- Ability to reproduce issues from log files alone
- Entry/exit logging revealed execution flow without a debugger
- Validation logging caught errors _before_ expensive 3-minute Houdini cooks
- Reduced troubleshooting time from hours to minutes

**For the Codebase:**

- Logging forced better error handling (can't log what you don't catch)
- Module separation became natural (each module has its own logger)
- Threading issues became obvious (race conditions showed up in logs)
- Eventually led to complete architecture refactor (because we could now debug it)

### The Philosophy: Defensive Logging

I call this approach **defensive logging**—setting up comprehensive logging infrastructure from day one, not as an afterthought. It's the same philosophy as defensive programming: assume things will go wrong, and build the safety nets before you need them.

The beautiful part? Defensive logging is _cheap_. Once you have the patterns down, it takes minutes to set up:

- Boilerplate logger configuration
- Standard module logger + console logger pattern
- Reusable custom handlers
- Consistent formatting

The payoff is enormous. Every hour spent setting up proper logging saves days of debugging down the line.

---

## Why This Matters: The Case for Proper Logging

Before we dive into implementation details, let's talk about why logging often gets treated as an afterthought, and why that's a mistake.

### Print Statements vs Proper Logging

We've all done it. Quick debugging session? Throw in a `print()`. Need to see variable state? Another `print()`. Before you know it, your codebase is littered with `print()` statements that:

- **Can't be turned off** without editing code
- **All go to stdout** (no separation of concerns)
- **Lack context** (what module? what time? what severity?)
- **Block execution** (stdout writes can be slow)
- **Pollute production output** (good luck parsing JSON when "DEBUG: x=5" is mixed in)
- **Can't be filtered** (see everything or nothing)
- **Don't persist** (terminal scrolls away, logs are gone)

Here's the reality: `print()` is not a debugging tool, it's a crutch. It works for tiny scripts, but the moment your code grows beyond a single file or needs to run unattended, print statements become a liability.

**The Hidden Cost:** Every `print()` you add is **technical debt**. You'll either leave it in (polluting output) or delete it (losing debugging context). Next time you need to debug that code path, you'll add the prints back. This cycle wastes hours.

### What Proper Logging Gives You

Python's `logging` module provides what print statements never can:

**1. Granular Control**

```python
# Development: See everything
logger.setLevel(logging.DEBUG)

# Production: Only errors and critical issues
logger.setLevel(logging.ERROR)

# No code changes needed - configure once, control globally
```

**2. Multiple Destinations**

```python
# Same log message goes to multiple places simultaneously
logger.debug("Processing asset X")
# → Console (for developer watching)
# → File (for post-mortem analysis)
# → Network (for centralized monitoring)
# → UI widget (for user feedback)
```

**3. Rich Context**

```python
# Automatic metadata
[2026-02-25 14:32:15,123] [DEBUG] [high_to_game_ready.tool:245] Processing asset X
#  ^timestamp              ^level    ^module:line             ^your message

# Compare to print():
Processing asset X  # What? When? Where? Why?
```

**4. Structured Output**

```python
# JSON logging for machine parsing
{"timestamp": "2026-02-25T14:32:15.123", "level": "DEBUG",
 "module": "high_to_game_ready.tool", "message": "Processing asset X"}

# Try that with print statements
```

**5. Performance**

```python
# Logging is lazy - expensive operations only happen if the level is enabled
logger.debug("Expensive data: %s", expensive_function())  # Only called if DEBUG enabled

# Print always executes
print(f"Data: {expensive_function()}")  # Always called, always slow
```

**6. Thread Safety**
Logging module is thread-safe by design. Print statements? Not guaranteed. In multithreaded applications, print output can interleave:

```
Thread 1: Start
Thread 2: StartThread 1:  processingThread 2:  processing
# Good luck reading that
```

### The Cost of Poor Logging

Let's do the math. In the tool I inherited:

**Before Proper Logging:**

- **Bug report:** "It failed" (screenshot of "Process failed")
- **Investigation:** 30 minutes reading code to understand flow
- **Reproduction attempt:** 8 minutes (asset processing time)
- **Still not enough info:** Add print statements, rebuild
- **Another reproduction:** 8 minutes
- **Root cause found:** 1 hour in
- **Fix applied:** 5 minutes
- **Verify fix:** 8 minutes

**Total time per bug:** ~90 minutes minimum, often much longer for complex issues.

**After Proper Logging:**

- **Bug report:** "It failed" (but now with log file attached)
- **Read log file:** 2 minutes
- **Root cause identified:** In the logs (asset missing UV set, line 342)
- **Fix applied:** 5 minutes
- **Verify fix:** 8 minutes

**Total time per bug:** ~15 minutes.

Over a project lifecycle with dozens of issues, this is the difference between **days of developer time vs hours**. And that's not counting the user frustration saved when they get clear error messages instead of mysterious failures.

### When to Log

A common mistake: logging too little (typical of beginners) or logging too much (typical after one debug session from hell). Here's a framework:

**Always Log:**

- **Entry points** - Application/tool startup, script entry
- **External operations** - File I/O, network requests, subprocess execution
- **State changes** - Mode switches, configuration changes
- **Validation failures** - Why did validation reject this input?
- **Errors and exceptions** - Always log exceptions with full context
- **Performance milestones** - Start/end of expensive operations

**Log Selectively:**

- **Loop iterations** - Only on errors or every N iterations
- **Intermediate calculations** - Only when debugging algorithms
- **Function entry/exit** - Only for major functions or when debugging
- **Variable state** - Only when relevant to logic flow

**Never Log:**

- **Secrets** - Passwords, API keys, tokens (seriously, never)
- **PII** - Personally identifiable information (check compliance requirements)
- **Binary data** - Unless hex-encoded and you have a reason
- **Excessive loops** - Don't log every iteration of processing 10,000 items

**The Decision Tree:**

```
Does this help diagnose failures? → Yes → Log it
Does this provide user-actionable info? → Yes → Log it (to console logger)
Is this a state change? → Yes → Log it
Is this just "code is running"? → No → Don't log it
Would I want this in a log file when investigating a bug? → Yes → Log it
```

### What to Log

The format matters as much as the content. Good log messages have:

**1. Context**

```python
# Bad
logger.error("File not found")

# Good
logger.error(f"Failed to load config file: {config_path} (working dir: {os.getcwd()})")
```

**2. Actionability**

```python
# Bad
logger.error("Asset validation failed")

# Good
logger.error(f"Asset '{asset_name}' missing required UV set 'UVChannel_0'. "
             f"Ensure asset is unwrapped before export.")
```

**3. Values and State**

```python
# Bad
logger.debug("Processing asset")

# Good
logger.debug(f"Processing asset {asset_index}/{total_assets}: {asset_path} "
             f"(resolution={resolution}, quality={quality})")
```

**4. Boundaries**

```python
# Entry
logger.info(f"Starting texture bake: {len(assets)} assets, output={output_dir}")

# Progress (for long operations)
logger.info(f"Texture bake progress: {completed}/{total} ({percent:.1f}%)")

# Exit with result
logger.info(f"Texture bake completed: {success_count} succeeded, {fail_count} failed "
            f"(duration={elapsed:.2f}s)")
```

### Python Logging Standards: Why They Matter

Now that we understand _why_ to log, let's talk about _how_. Python has a mature, well-designed logging system outlined in **PEP 282** (2002) and refined over two decades. Following these standards isn't just about being "proper"—it's about leveraging a battle-tested architecture.

**The Core Principles:**

**1. Hierarchical Loggers**
Loggers form a tree structure using dot-notation:

```python
root_logger = logging.getLogger()  # Root
app_logger = logging.getLogger("myapp")  # Top-level
module_logger = logging.getLogger("myapp.module")  # Child
submodule_logger = logging.getLogger("myapp.module.submodule")  # Grandchild
```

Messages flow upward: `myapp.module.submodule` → `myapp.module` → `myapp` → `root`

This means you can:

- Configure once at the root
- Override for specific subtrees
- Filter by hierarchy
- Zero coupling between modules

**2. Singleton Access by Name**

```python
# Module A
logger = logging.getLogger("myapp.moduleA")

# Module B (different file, no import needed)
logger = logging.getLogger("myapp.moduleA")  # Gets same logger instance

# They're the same object
```

This is **not** object-oriented design—it's a registry pattern. Loggers are singletons accessed by name, which enables:

- No dependencies between modules
- Global configuration changes
- Thread-safe access
- Easy mocking in tests

**3. Handlers Separate Output from Logic**
Your code emits log records. Handlers decide what to do with them:

```python
logger = logging.getLogger("myapp")
logger.addHandler(logging.FileHandler("app.log"))  # To file
logger.addHandler(logging.StreamHandler())  # To console
logger.addHandler(custom_ui_handler)  # To UI widget

# One log call, multiple destinations
logger.info("Started")  # Goes to all three handlers
```

**4. Formatters Separate Presentation from Content**

```python
# Same log record, different formatting
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
# → 2026-02-25 14:32:15 - myapp.module - INFO - Started

console_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))
# → [INFO] Started
```

**5. Levels Indicate Severity**

```python
logger.debug("Detailed diagnostic")    # DEBUG (10)
logger.info("Normal operation")        # INFO (20)
logger.warning("Something unexpected") # WARNING (30)
logger.error("Operation failed")       # ERROR (40)
logger.critical("System unstable")     # CRITICAL (50)
```

Filters work on numeric levels: set level to WARNING, get WARNING + ERROR + CRITICAL.

### Why Standards Matter

Following these standards ensures:

1. **Maintainability** - Other Python developers immediately understand your code
2. **Scalability** - Hierarchy grows naturally without refactoring
3. **Debuggability** - Standard tools (log analyzers, filters) work as expected
4. **Thread Safety** - Logger singletons are thread-safe by design
5. **Testability** - Easy to mock/intercept in tests without tight coupling
6. **Future-Proof** - Aligned with Python ecosystem evolution
7. **Integration** - Third-party libraries use the same system (automatic consistency)

The tool I inherited violated many of these principles. The refactor wasn't about being pedantic—it was about unlocking the power of the logging system's design.

---

## Python Logging Best Practices & Anti-Patterns

Now that we understand the fundamentals, let's look at how to apply them correctly—and how NOT to. These patterns apply to any Python project, not just my specific tool.

### Best Practice #1: Use `getLogger(name)` for Singleton Access

**The Right Way:**

```python
import logging

# Module-level logger
logger = logging.getLogger(__name__)  # Or explicit name
logger.info("Module loaded")

# Get same logger instance elsewhere
same_logger = logging.getLogger("myapp.module")  # Same object
```

**Why This Works:**

- Loggers are singletons accessed by name (registry pattern)
- No imports between modules needed
- Thread-safe by design
- Can reconfigure globally
- Automatic hierarchy

**What to Avoid:**

```python
# ❌ WRONG - Don't instantiate directly
logger = logging.Logger("mylogger")  # Breaks singleton pattern
```

### Best Practice #2: Use Module-Level Logger Names

**Standard Approach:**

```python
import logging

logger = logging.getLogger(__name__)  # Automatic module path
```

**Why `__name__` is Recommended:**

- Automatically gets the full module path (`package.subpackage.module`)
- DRY principle (don't repeat the module path)
- Standard practice everyone recognizes

**When to Use Explicit Names:**

There are valid reasons to deviate from `__name__`:

```python
import logging as _logging  # Avoid namespace collisions

_MODULE_NAME = "myapp.module"
_LOGGER = _logging.getLogger(_MODULE_NAME)
```

**Valid reasons for explicit names:**

1. **Entry point safety** - `__name__` becomes `"__main__"` in entry scripts
2. **DCC environment quirks** - Maya/Houdini userSetup.py can break with certain import patterns
3. **Metadata proximity** - Module name near `__version__`, `__author__` metadata
4. **Self-documenting** - Full path visible without guessing
5. **Import aliasing** - Using `import logging as _logging` to prevent variable name collisions

**The key:** Follow the **spirit** of hierarchical naming. Whether you use `__name__` or explicit strings, maintain the hierarchy structure.

| Context                                   | `__name__`           | Explicit Name       | Winner               |
| ----------------------------------------- | -------------------- | ------------------- | -------------------- |
| Normal module                             | ✅ Works perfectly    | ✅ Works perfectly   | `__name__` (simpler) |
| Entry point (`if __name__ == "__main__"`) | ❌ Gets `"__main__"`  | ✅ Gets correct path | Explicit             |
| DCC userSetup.py                          | ⚠️ May break         | ✅ Safer             | Explicit             |
| Dynamic imports                           | ⚠️ Context-dependent | ✅ Always correct    | Explicit             |

**My recommendation:** Use `__name__` by default. Switch to explicit names if you're in a complex environment (DCCs, entry points, multi-workspace).

### Best Practice #3: Configure Handlers at Entry Point Only

**The Rule:** Library code emits log messages. Application code configures handlers.

**Library Code (No Handler Setup):**

```python
# mylib/module.py
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug("Processing data")  # Just emit, don't configure
    # ... do work ...
    logger.info("Processing complete")
```

**Application Code (Configure Handlers):**

```python
# app.py
import logging
import mylib.module

# Configure logging at application entry point
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Now library logs go to configured handlers
mylib.module.process_data([1, 2, 3])
```

**Why This Matters:**

- Library doesn't dictate output format
- Application controls all logging config
- No duplicate handlers
- Easy to change output without touching library code

**What NOT to Do:**

```python
# ❌ WRONG - Don't configure in library code
# mylib/module.py
import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler('mylib.log')  # BAD!
logger.addHandler(handler)  # BAD!

def process_data(data):
    logger.info("Processing")  # Now library controls its own output
```

This creates problems:

- Application can't control library logging
- Multiple imports = multiple handlers (duplicate messages)
- Hard-coded file paths
- Pollution of application logging config

### Best Practice #4: Use Hierarchy Propagation

**How It Works:**

```python
import logging

# Create parent logger with handler
parent = logging.getLogger("myapp")
parent.setLevel(logging.DEBUG)
parent.addHandler(logging.StreamHandler())

# Create child loggers (no handlers needed)
module_logger = logging.getLogger("myapp.module")
submodule_logger = logging.getLogger("myapp.module.submodule")

# Messages automatically propagate up the hierarchy
submodule_logger.info("Hello")  # Goes to parent's StreamHandler
module_logger.warning("Warning")  # Also goes to parent's StreamHandler
```

**The Hierarchy:**

```
root
└── myapp (has StreamHandler)
    ├── myapp.module (inherits parent's handler)
    └── myapp.module.submodule (inherits parent's handler)
```

**Why This is Powerful:**

- Configure once at the root
- All children inherit automatically
- Zero coupling between modules
- Easy to add/remove handlers globally

**Controlling Propagation:**

```python
# Sometimes you want to isolate a hierarchy
tool_logger = logging.getLogger("mytool")
tool_logger.propagate = False  # Don't leak to root logger

# Useful for:
# - Separate UI console logging
# - Isolated subsystems
# - Preventing library logs from polluting your output
```

### Best Practice #5: Set Levels on Handlers, Not Loggers

**Flexible Approach:**

```python
import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)  # Logger accepts all levels

# Different handlers filter differently
file_handler = logging.FileHandler("debug.log")
file_handler.setLevel(logging.DEBUG)  # File gets everything

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Console gets INFO and above

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Now one log call goes to multiple destinations with different filtering
logger.debug("Detailed trace")  # Only to file
logger.info("User message")     # To both file and console
logger.error("Something broke")  # To both file and console
```

**Why This is Better:**

```python
# ❌ Less flexible - logger level filters for ALL handlers
logger.setLevel(logging.INFO)  # Can't get DEBUG anywhere now
```

**Pattern:**

- Set logger to DEBUG (accept everything)
- Let handlers decide what they want
- Flexibility to add new handlers with different levels

### Anti-Pattern #1: Passing Logger Instances

**The Wrong Way:**

```python
# ❌ WRONG - Passing loggers creates tight coupling
class DataProcessor:
    def __init__(self, logger):
        self.logger = logger  # Dependency on caller

class DataValidator:
    def __init__(self, logger):
        self.logger = logger  # More dependencies

# Caller must provide loggers
processor = DataProcessor(logger=some_logger)
validator = DataValidator(logger=some_logger)
```

**Problems:**

- Tight coupling (classes depend on logger being passed)
- Fragile (breaks if you forget to pass logger)
- Hard to refactor
- Breaks hierarchy benefits
- Not following Python logging design

**The Right Way:**

```python
# ✅ CORRECT - Each module gets its own logger by name
import logging

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)  # No dependency

class DataValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)  # No dependency

# Just works, no logger passing needed
processor = DataProcessor()
validator = DataValidator()
```

**The Exception: Framework Infrastructure**

There is ONE valid case for passing a logger: when framework code needs to attach handlers to a specific logger.

```python
# Framework base class
class BaseWindow:
    def __init__(self, logger=None):
        if logger:
            # Framework attaches UI console handler to specified logger
            console_handler = QTextEditHandler(self.console_widget)
            logger.addHandler(console_handler)

# Application tells framework which logger to enhance
class MyWindow(BaseWindow):
    def __init__(self):
        tool_root_logger = logging.getLogger("mytool")
        super().__init__(logger=tool_root_logger)  # Tell framework where to attach handler
```

**Why this exception is valid:**

1. **Infrastructure responsibility** - Framework owns the UI widget, must attach handler
2. **Single integration point** - Only happens once at initialization
3. **Explicit control** - Application explicitly tells framework which logger to enhance
4. **Not business logic** - This is plumbing, not application code

**Key difference:**

- ❌ **Anti-pattern**: Business logic passing loggers around between modules
- ✅ **Valid exception**: Application telling framework infrastructure which logger to enhance with UI handlers

### Anti-Pattern #2: Logger-Per-Instance

**The Wrong Way:**

```python
# ❌ WRONG - Creating logger for each instance
class AssetProcessor:
    def __init__(self, asset_name):
        # Creates a new logger for EVERY instance
        self.logger = logging.getLogger(f"processor.{asset_name}")
        self.asset_name = asset_name

# Creates 1000 separate loggers!
processors = [AssetProcessor(f"asset_{i}") for i in range(1000)]
```

**Problems:**

- Memory waste (thousands of logger objects)
- Hard to configure (can't predict instance names)
- Pollutes logger namespace
- Makes hierarchy meaningless

**The Right Way:**

```python
# ✅ CORRECT - One logger per module
import logging

class AssetProcessor:
    # Class-level logger (shared by all instances)
    logger = logging.getLogger(__name__)

    def __init__(self, asset_name):
        self.asset_name = asset_name

    def process(self):
        # Include instance context in message, not logger name
        self.logger.info(f"Processing asset: {self.asset_name}")
```

**Why This is Better:**

- One logger per class/module (efficient)
- Easy to configure
- Instance context goes in the message, not the logger name
- Follows Python logging design

### Anti-Pattern #3: Using Root Logger Directly

**The Wrong Way:**

```python
# ❌ WRONG - Using root logger
import logging

logging.debug("Processing started")  # Goes to root logger
logging.info("Step complete")        # Goes to root logger
logging.error("Failed")              # Goes to root logger
```

**Problems:**

- Pollutes global namespace
- Can't filter by module
- No hierarchy benefits
- Can't easily find source of logs
- Other libraries using root logger create confusion

**The Right Way:**

```python
# ✅ CORRECT - Named logger
import logging

logger = logging.getLogger(__name__)

logger.debug("Processing started")
logger.info("Step complete")
logger.error("Failed")
```

**Why This is Better:**

- Clear module attribution
- Can filter by hierarchy
- Isolated from other code
- Professional and maintainable

**The Exception: Early Bootstrap/Initialization**

There IS one valid case for using the root logger: very early initialization code before your logging infrastructure is set up.

```python
# ✅ ACCEPTABLE - Early bootstrap logging
import logging

# Very early initialization - before custom logging is configured
logging.info("Application starting...")
logging.debug("Python version: %s", sys.version)

try:
    # Now set up proper logging infrastructure
    configure_logging()

    # From here on, use named loggers
    logger = logging.getLogger(__name__)
    logger.info("Logging infrastructure initialized")

except Exception as e:
    # Logging setup failed - root logger is all we have
    logging.critical("Failed to configure logging", exc_info=True)
    sys.exit(1)
```

**When root logger is acceptable:**

1. **Early bootstrapping** - Before your logging config is established
2. **Logging setup failures** - When your logging infrastructure itself fails
3. **Critical initialization** - Very early startup before imports complete
4. **One-off scripts** - Quick debugging scripts (though named loggers are still better)

**Key principle:** Use root logger only when you can't use a named logger yet. Once your logging infrastructure is ready, switch to named loggers immediately.

### Anti-Pattern #4: Logging Secrets and Sensitive Data

**The Wrong Way:**

```python
# ❌ WRONG - Logging sensitive data
logger.debug(f"Connecting to database with password: {password}")
logger.info(f"API key: {api_key}")
logger.debug(f"User SSN: {ssn}")
logger.debug(f"Credit card: {card_number}")
```

**Why This is Dangerous:**

- Log files persist (security breach if exposed)
- Often sent to monitoring systems (data leak)
- May violate compliance (GDPR, PCI-DSS, HIPAA)
- Difficult to redact after the fact

**The Right Way:**

```python
# ✅ CORRECT - Log safely
logger.debug(f"Connecting to database at {host}:{port}")  # No password
logger.info(f"API authentication successful")  # No key
logger.debug(f"Processing user record ID: {user_id}")  # No PII

# If you must log something sensitive for debugging
import hashlib
logger.debug(f"Password hash: {hashlib.sha256(password.encode()).hexdigest()[:8]}...")
```

**What NOT to Log:**

- Passwords, API keys, tokens, secrets
- Social security numbers, credit cards
- Personally identifiable information (PII)
- Session tokens, authentication cookies
- Private encryption keys

**What's Safe to Log:**

- User IDs (not usernames if they're considered PII)
- Resource identifiers (file paths, database IDs)
- Timings and performance metrics
- Status codes and error codes
- Configuration (non-sensitive parts)

### Anti-Pattern #5: Excessive Logging in Loops

**The Wrong Way:**

```python
# ❌ WRONG - Logging every iteration
for i, item in enumerate(10000):
    logger.debug(f"Processing item {i}: {item}")  # 10,000 log messages!
    process(item)
```

**Problems:**

- Log files become enormous
- Performance impact (I/O is slow)
- Hard to find actual issues in noise
- May fill disk space

**The Right Way:**

```python
# ✅ CORRECT - Log milestones and errors
items = list(range(10000))
logger.info(f"Starting batch processing: {len(items)} items")

for i, item in enumerate(items):
    try:
        process(item)
        # Log every 1000 items
        if (i + 1) % 1000 == 0:
            logger.info(f"Progress: {i + 1}/{len(items)} items processed")
    except Exception as e:
        logger.error(f"Failed to process item {i}: {item}", exc_info=True)

logger.info(f"Batch processing complete: {len(items)} items")
```

**Another Right Way: Collect, Then Emit**

For debug logging where you want detailed information without spamming the log file, use the "collect, then emit" pattern:

```python
# ✅ ALSO CORRECT - Collect during loop, emit summary after
items = list(range(10000))
logger.info(f"Starting batch processing: {len(items)} items")

# Collect information during processing
processed_items = []
failed_items = []
timings = []

for i, item in enumerate(items):
    start_time = time.time()
    try:
        result = process(item)
        elapsed = time.time() - start_time

        # Collect, don't log
        processed_items.append(item)
        timings.append(elapsed)

    except Exception as e:
        # Immediate logging for errors still makes sense
        logger.error(f"Failed to process item {i}: {item}", exc_info=True)
        failed_items.append((item, str(e)))

# Now emit collected information as summary
logger.info(f"Batch processing complete: {len(processed_items)}/{len(items)} succeeded")
logger.debug(f"Average processing time: {sum(timings)/len(timings):.3f}s")
logger.debug(f"Min/Max time: {min(timings):.3f}s / {max(timings):.3f}s")

if failed_items:
    logger.warning(f"Failed items: {len(failed_items)}")
    for item, error in failed_items[:5]:  # Log first 5 failures
        logger.debug(f"  - {item}: {error}")
    if len(failed_items) > 5:
        logger.debug(f"  ... and {len(failed_items) - 5} more")
```

**When to use "collect, then emit":**

- Debug logging where you want statistics, not every event
- Performance analysis (collect timings, emit summary)
- Validation results (collect failures, emit grouped report)
- When you need to see patterns across all iterations

**Benefits:**

- Single, information-rich log message instead of thousands
- Can compute statistics (average, min/max, percentiles)
- Better signal-to-noise ratio
- Easier to parse programmatically
- Still get error details immediately when they happen

**Guidelines:**

- Log entry/exit of batch operations
- Log every N iterations (1000, 10%, etc.)
- Always log errors in loops
- Log summary statistics at the end

### Summary: The Golden Rules

**DO:**

- ✅ Use `logging.getLogger(__name__)` or explicit names
- ✅ Configure handlers at application entry point
- ✅ Use hierarchy propagation
- ✅ Set levels on handlers for flexibility
- ✅ Include context in log messages
- ✅ Log exceptions with `exc_info=True`
- ✅ Use appropriate log levels
- ✅ One logger per module/class

**DON'T:**

- ❌ Pass logger instances between modules
- ❌ Create logger per instance
- ❌ Use root logger directly
- ❌ Log secrets or PII
- ❌ Log every loop iteration
- ❌ Add handlers in library code
- ❌ Block execution with synchronous I/O logging

**Remember:** Python's logging system is powerful when used correctly. Following these patterns ensures your code is maintainable, debuggable, and professional.

### Anti-Pattern #6: Using f-strings Instead of Lazy Evaluation

**The Wrong Way:**

```python
# ❌ WRONG - f-strings always evaluate
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # DEBUG is disabled

# This ALWAYS calls expensive_function(), even when DEBUG is disabled!
for i in range(10000):
    logger.debug(f"Processing item {i}: {expensive_function(i)}")  # EXPENSIVE!
```

**Why This is Bad:**

- f-strings evaluate immediately, before checking log level
- Expensive operations run even when logging is disabled
- In hot loops, this can kill performance
- The string formatting happens regardless of whether it will be logged

**The Right Way:**

```python
# ✅ CORRECT - Lazy evaluation with old-style formatting
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # DEBUG is disabled

# expensive_function() only called if DEBUG level is enabled
for i in range(10000):
    logger.debug("Processing item %s: %s", i, expensive_function(i))  # FAST!
```

**Performance Comparison:**

```python
import time
import logging

def expensive_function(x):
    sum(range(1000))  # Simulate work
    return x * 2

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # DEBUG disabled

# Test 1: f-strings (always evaluate)
start = time.time()
for i in range(10000):
    logger.debug(f"Item {i}: {expensive_function(i)}")
print(f"f-string time: {time.time() - start:.2f}s")  # ~5 seconds

# Test 2: Lazy evaluation
start = time.time()
for i in range(10000):
    logger.debug("Item %s: %s", i, expensive_function(i))
print(f"Lazy eval time: {time.time() - start:.2f}s")  # ~0.01 seconds
```

**When f-strings are OK:**

```python
# Fine - simple, cheap operations
logger.info(f"Processing {asset_name}")  # Just a variable
logger.error(f"Failed after {attempts} attempts")  # Simple formatting

# Avoid - expensive operations
logger.debug(f"State: {serialize_entire_state()}")  # BAD!
logger.debug("State: %s", serialize_entire_state())  # GOOD (only if enabled)
```

**Rule of Thumb:**

- **Use f-strings:** For INFO/WARNING/ERROR messages (always logged)
- **Use lazy eval:** For DEBUG messages or when calling expensive functions
- **In hot loops:** Always use lazy evaluation

### Anti-Pattern #7: Handler Accumulation (Memory Leaks)

**The Problem:**
In long-running applications (especially DCCs like Maya/Houdini), tools get loaded, unloaded, and reloaded. If you don't remove handlers, they accumulate:

```python
# ❌ WRONG - Handler accumulation
class MyTool:
    def __init__(self):
        self.logger = logging.getLogger("mytool")
        handler = logging.FileHandler("tool.log")
        self.logger.addHandler(handler)  # Added every time tool loads!

# User loads tool, unloads it, loads it again...
# Each time: another handler added
# Result: Same log message appears 2x, 3x, 4x...
```

**Symptoms:**

- Duplicate log messages
- Log files grow exponentially
- Memory leaks (handlers hold file handles)
- In Maya: "Too many open files" errors after repeated tool loads

**The Right Way - Clean Up Handlers:**

```python
# ✅ CORRECT - Remove handlers on cleanup
import logging

class MyTool:
    def __init__(self):
        self.logger = logging.getLogger("mytool")
        self.handler = logging.FileHandler("tool.log")
        self.logger.addHandler(self.handler)

    def cleanup(self):
        """Call this when tool is closed/unloaded"""
        # Remove and close handler
        self.logger.removeHandler(self.handler)
        self.handler.close()
        self.handler = None

    def __del__(self):
        """Fallback cleanup (not always reliable)"""
        if hasattr(self, 'handler') and self.handler:
            try:
                self.logger.removeHandler(self.handler)
                self.handler.close()
            except:
                pass  # Might be called during shutdown
```

**For Qt Tools - Use closeEvent:**

```python
class MyToolWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("mytool")
        self.file_handler = logging.FileHandler("tool.log")
        self.logger.addHandler(self.file_handler)

        self.console_handler = QTextEditLogger(self.console_widget)
        self.logger.addHandler(self.console_handler)

    def closeEvent(self, event):
        """Qt calls this when window closes"""
        # Clean up handlers
        for handler in [self.file_handler, self.console_handler]:
            try:
                self.logger.removeHandler(handler)
                handler.close()
            except Exception as e:
                print(f"Handler cleanup error: {e}")

        super().closeEvent(event)
```

**Defensive Pattern - Clear All Handlers:**

```python
def setup_logging():
    """Set up logging, clearing any existing handlers first"""
    logger = logging.getLogger("mytool")

    # Clear existing handlers (prevents accumulation)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    # Now add fresh handlers
    logger.addHandler(logging.FileHandler("tool.log"))
    logger.setLevel(logging.DEBUG)
```

**Why This Matters in DCCs:**
Maya/Houdini sessions run for hours or days. Users load/reload tools constantly during development. Without handler cleanup:

- Day 1: 1 handler, logs work fine
- Day 2: 50 handlers, same message logged 50 times
- Day 3: 500 handlers, file system quota exceeded, Maya crashes

**Always clean up handlers in DCC tools.**

### Best Practice #6: Capture Python Warnings

Python's `warnings` module is separate from `logging`. Libraries emit deprecation warnings, user warnings, etc. that go to stderr by default. Capture them:

```python
import logging
import warnings

# Redirect warnings to logging system
logging.captureWarnings(True)

# Configure the py.warnings logger
warnings_logger = logging.getLogger('py.warnings')
warnings_logger.setLevel(logging.WARNING)

# Now warnings go through your logging infrastructure
import numpy as np
np.array([1, 2, 3], dtype=np.int)  # Deprecated dtype
# → [WARNING] [py.warnings] DeprecationWarning: np.int is deprecated...
```

**Why This Matters:**

- Third-party libraries generate warnings (PySide6, numpy, etc.)
- Warnings clutter stderr/console output
- Unifying all diagnostic output makes debugging easier
- Can filter/route warnings like any other log message
- Warnings become part of log files (persistent record)

**Complete Setup:**

```python
import logging
import warnings

def setup_logging():
    # Basic config
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

    # Capture warnings
    logging.captureWarnings(True)

    # Optional: Set warnings logger level
    logging.getLogger('py.warnings').setLevel(logging.WARNING)

    # Optional: Control which warnings are shown
    warnings.filterwarnings('default')  # Show all
    # warnings.filterwarnings('ignore', category=DeprecationWarning)  # Hide deprecations
```

---

## The Three-Logger Pattern: Separating Concerns

Now we get to the implementation that solved my inherited tool's problems. The key insight: **users and developers need different information from the same events**.

### The Problem: One Size Doesn't Fit All

When I looked at the original tool, logging was an afterthought. A few print statements here and there, maybe a log file from Houdini. No structure, no separation of concerns.

But here's the thing: **the information a user needs to see is fundamentally different from what a developer needs to debug.**

**Users need:**

- "Asset validation failed - missing UV set" (actionable)
- "Processing 5/10 assets..." (progress)
- "Houdini export complete" (confirmation)
- Clear error messages they can report

**Users DON'T need:**

- "Method: \_gather_assets() entry" (internal)
- "Debug: subprocess return code = 0" (technical)
- "Loading config from C:\..." (backend detail)
- Stack traces for normal operations

**Developers need:**

- ALL of the above, plus...
- Entry/exit logging for execution flow
- Variable state at key points
- Full stack traces on exceptions
- Timing information
- Configuration details

**The solution?** Separate logger hierarchies for separate audiences.

### The Three-Logger Architecture

Here's the pattern I implemented, which I now use across all my tools:

```
Root Logger (Python's global)
│
├── Technical Hierarchy (developer logging)
│   └── high_to_game_ready.tool (module logger)
│       └── FILE HANDLER (all DEBUG+ messages)
│       └── STREAM HANDLER (terminal output)
│
└── Console Hierarchy (user-facing logging)
    └── high_to_game_ready (tool root logger) [propagate=False]
        └── UI CONSOLE HANDLER (clean user messages)
        ├── high_to_game_ready.tool (tool module logger)
        ├── high_to_game_ready.view (tool module logger)
        └── high_to_game_ready.controller (tool module logger)
```

**Key Components:**

**1. Module Logger** (`_LOGGER`)

- **Purpose:** Technical/developer logging
- **Namespace:** `high_to_game_ready.tool` (full module path)
- **Destination:** File log + terminal
- **Level:** DEBUG (captures everything)
- **Audience:** Developers debugging issues

**2. Tool Root Logger** (`_TOOL_ROOT_LOGGER`)

- **Purpose:** Infrastructure - attachment point for UI console handler
- **Namespace:** `high_to_game_ready` (short, tool-specific)
- **Destination:** None (doesn't log directly)
- **Propagate:** `False` (isolates from root logger)
- **Audience:** N/A (infrastructure only)

**3. Tool Module Logger** (`_TOOL_LOGGER`)

- **Purpose:** User-facing console messages
- **Namespace:** `high_to_game_ready.tool` (child of tool root)
- **Destination:** UI console widget (via propagation to parent)
- **Level:** INFO (meaningful messages only)
- **Audience:** End users

### Implementation: Setting Up the Loggers

Here's how this looks in practice (simplified from the real tool):

**In the tool module (`tool.py`):**

```python
import logging as _logging

# Module metadata
_MODULE_NAME = "high_to_game_ready.tool"
_TOOL_NAME = "high_to_game_ready"
__version__ = "1.0"
__author__ = ["jGalloway"]

# 1. Module logger - technical logging for developers
_LOGGER = _logging.getLogger(_MODULE_NAME)
_LOGGER.setLevel(_logging.DEBUG)

# 2. Tool module logger - user-facing console messages
#    This automatically becomes a child of "high_to_game_ready" root logger
_TOOL_LOGGER = _logging.getLogger(f"{_TOOL_NAME}.tool")
_TOOL_LOGGER.setLevel(_logging.INFO)

class BP_HighToGameReadyTool(BP_BaseToolWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(
            parent=parent,
            logger=_TOOL_LOGGER,  # Pass tool logger to base class
            log_console=True,     # Enable UI console widget
            *args,
            **kwargs
        )

    def process_assets(self):
        # Technical logging - goes to file/terminal only
        _LOGGER.debug("Method: process_assets() entry")
        _LOGGER.debug(f"Asset list: {self.asset_list}")

        # User-facing logging - goes to UI console
        _TOOL_LOGGER.info("Starting asset processing...")

        try:
            result = self._run_houdini()

            # Technical
            _LOGGER.debug(f"Houdini subprocess exit code: {result}")

            # User-facing
            _TOOL_LOGGER.info("Houdini processing complete")

        except Exception as e:
            # Technical - full stack trace
            _LOGGER.exception("Houdini processing failed")

            # User-facing - actionable message
            _TOOL_LOGGER.error(f"Houdini failed: {e}. Check log file for details.")

        _LOGGER.debug("Method: process_assets() exit")
```

**Key observations:**

- Two separate loggers in the same module
- Module logger (`_LOGGER`) captures everything
- Tool logger (`_TOOL_LOGGER`) only gets user-relevant messages
- Zero coupling - both accessed by name, no passing between modules

### The Custom Console Handler

To route logs to a Qt UI widget, I created a custom handler (this is reusable across all Qt tools):

```python
# bp_py/lib/bp_logging/ui_console_handler.py
import logging
from PySide6 import QtCore, QtWidgets

class QTextEditLogger(logging.Handler):
    """Custom handler that routes log messages to a Qt text widget"""

    class Emitter(QtCore.QObject):
        # Signal for thread-safe logging
        log = QtCore.Signal(str)

    def __init__(self, text_widget):
        super().__init__()

        if not isinstance(text_widget, (QtWidgets.QPlainTextEdit,
                                       QtWidgets.QTextBrowser)):
            raise TypeError("text_widget must be a Qt text widget")

        self.widget = text_widget
        self.widget.setReadOnly(True)

        # Emitter provides thread-safe signal-based logging
        self.emitter = QTextEditLogger.Emitter()
        self.emitter.log.connect(self.append_log)

    def append_log(self, msg):
        """Append log message to widget (runs in main thread)"""
        if self.widget is None:
            return

        try:
            # Limit buffer to prevent memory bloat in long-running sessions
            # Keep last 5000 lines, remove oldest 500 when limit reached
            if self.widget.document().blockCount() > 5000:
                cursor = self.widget.textCursor()
                cursor.movePosition(cursor.Start)
                # Select and remove first 500 lines
                for _ in range(500):
                    cursor.select(cursor.BlockUnderCursor)
                    cursor.removeSelectedText()
                    cursor.deleteChar()  # Remove the newline

            self.widget.appendPlainText(msg)
        except RuntimeError:
            # C++ widget deleted, nullify reference
            self.widget = None

    def emit(self, record):
        """Handler's emit method - formats and signals message"""
        try:
            msg = self.format(record)
            self.emitter.log.emit(msg)  # Thread-safe via Qt signal
        except Exception:
            self.handleError(record)  # Standard logging error handling
```

**What makes this handler special:**

1. **Thread-safe** - Uses Qt signals for cross-thread logging
2. **Widget-agnostic** - Works with QPlainTextEdit, QTextBrowser, QTextEdit
3. **Safe cleanup** - Handles widget deletion gracefully
4. **Standard handler** - Inherits from `logging.Handler`, follows Python conventions

### Integration: Hooking Up the Console

Here's how the console handler gets attached to the tool root logger:

**In the base window class:**

```python
class BP_BaseToolWindow(QtWidgets.QMainWindow):
    def __init__(self, logger=None, log_console=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if log_console:
            # Create console widget
            self.console_widget = QtWidgets.QPlainTextEdit()
            self.console_widget.setReadOnly(True)

            # Set monospace font
            font = QtGui.QFont("Courier New", 9)
            self.console_widget.setFont(font)

            # Add to UI layout
            self.layout.addWidget(self.console_widget)

            # Attach console handler to provided logger
            if logger:
                self._console_handler = QTextEditLogger(self.console_widget)

                # Format: [LEVEL][logger.name] >> message
                formatter = logging.Formatter(
                    '[%(levelname)s][%(name)s] >> %(message)s'
                )
                self._console_handler.setFormatter(formatter)
                self._console_handler.setLevel(logging.INFO)

                # Attach handler to the provided logger
                logger.addHandler(self._console_handler)
```

**In the tool window:**

```python
class BP_HighToGameReadyTool(BP_BaseToolWindow):
    def __init__(self, *args, **kwargs):
        # Get tool root logger
        tool_root_logger = logging.getLogger("high_to_game_ready")
        tool_root_logger.setLevel(logging.DEBUG)
        tool_root_logger.propagate = False  # Isolate from root logger

        # Pass to base class - it will attach console handler
        super().__init__(
            logger=tool_root_logger,  # Base class attaches handler here
            log_console=True,
            *args,
            **kwargs
        )
```

**What happens:**

1. Tool creates/gets the root logger for its hierarchy
2. Passes it to base class during `__init__`
3. Base class creates console widget and attaches handler
4. All child loggers (`high_to_game_ready.tool`, etc.) automatically propagate up
5. Console handler receives user-facing messages, file handler gets technical logging

### Hierarchy in Action

Here's what actually happens when code runs:

**Code:**

```python
def validate_assets(self):
    _LOGGER.debug("Method: validate_assets() entry")  # Technical
    _TOOL_LOGGER.info("Validating assets...")         # User-facing

    if not self.asset_list:
        _LOGGER.warning("Asset list is empty (internal)")  # Technical
        _TOOL_LOGGER.error("No assets selected!")          # User-facing
        return False

    _LOGGER.debug(f"Validating {len(self.asset_list)} assets")  # Technical

    for asset in self.asset_list:
        _LOGGER.debug(f"Checking asset: {asset.path}")  # Technical

        if not asset.has_uv_set():
            msg = f"Asset '{asset.name}' missing UV set"
            _LOGGER.error(msg)           # Technical - with context
            _TOOL_LOGGER.error(msg)      # User-facing - same message
            return False

    _LOGGER.debug("All assets valid, returning True")  # Technical
    _TOOL_LOGGER.info("Asset validation successful")   # User-facing
    return True
```

**File log output (technical - everything):**

```
[2026-02-25 15:30:42,123] [DEBUG] [high_to_game_ready.tool:245] Method: validate_assets() entry
[2026-02-25 15:30:42,124] [INFO] [high_to_game_ready.tool:246] Validating assets...
[2026-02-25 15:30:42,125] [DEBUG] [high_to_game_ready.tool:251] Validating 3 assets
[2026-02-25 15:30:42,126] [DEBUG] [high_to_game_ready.tool:254] Checking asset: C:\assets\rock_01_high.fbx
[2026-02-25 15:30:42,130] [DEBUG] [high_to_game_ready.tool:254] Checking asset: C:\assets\rock_02_high.fbx
[2026-02-25 15:30:42,135] [DEBUG] [high_to_game_ready.tool:254] Checking asset: C:\assets\rock_03_high.fbx
[2026-02-25 15:30:42,140] [DEBUG] [high_to_game_ready.tool:263] All assets valid, returning True
[2026-02-25 15:30:42,141] [INFO] [high_to_game_ready.tool:264] Asset validation successful
```

**UI console output (user-facing - clean):**

```
[INFO][high_to_game_ready.tool] >> Validating assets...
[INFO][high_to_game_ready.tool] >> Asset validation successful
```

**See the difference?** The file log has timestamps, full paths, internal state. The UI console shows only what matters to the user.

### Error Case Example

**Code:**

```python
def process_houdini(self):
    _LOGGER.info("Starting Houdini subprocess")  # Technical
    _TOOL_LOGGER.info("Starting Houdini processing...")  # User-facing

    try:
        _LOGGER.debug(f"Houdini executable: {self.houdini_path}")
        _LOGGER.debug(f"Hip file: {self.hip_file}")
        _LOGGER.debug(f"Asset count: {len(self.asset_list)}")

        result = subprocess.run([self.houdini_path, self.hip_file])

        _LOGGER.debug(f"Subprocess exit code: {result.returncode}")

        if result.returncode != 0:
            raise RuntimeError(f"Houdini failed with code {result.returncode}")

        _TOOL_LOGGER.info("Houdini processing complete")

    except Exception as e:
        # Technical log - full context
        _LOGGER.exception("Houdini subprocess failed")
        _LOGGER.error(f"Houdini path: {self.houdini_path}")
        _LOGGER.error(f"Hip file: {self.hip_file}")
        _LOGGER.error(f"Working directory: {os.getcwd()}")

        # User-facing log - actionable message
        _TOOL_LOGGER.error(
            f"Houdini processing failed: {e}\n"
            f"Check log file: {self.log_file_path}"
        )
        raise
```

**File log (technical - full context):**

```
[2026-02-25 15:31:15,234] [INFO] [high_to_game_ready.tool:312] Starting Houdini subprocess
[2026-02-25 15:31:15,235] [DEBUG] [high_to_game_ready.tool:315] Houdini executable: C:\Program Files\Side Effects Software\Houdini 19.5\bin\hython.exe
[2026-02-25 15:31:15,236] [DEBUG] [high_to_game_ready.tool:316] Hip file: C:\tools\rock_batch.hip
[2026-02-25 15:31:15,237] [DEBUG] [high_to_game_ready.tool:317] Asset count: 3
[2026-02-25 15:33:22,541] [DEBUG] [high_to_game_ready.tool:321] Subprocess exit code: 1
[2026-02-25 15:33:22,542] [ERROR] [high_to_game_ready.tool:328] Houdini subprocess failed
Traceback (most recent call last):
  File "tool.py", line 323, in process_houdini
    raise RuntimeError(f"Houdini failed with code {result.returncode}")
RuntimeError: Houdini failed with code 1
[2026-02-25 15:33:22,543] [ERROR] [high_to_game_ready.tool:329] Houdini path: C:\Program Files\Side Effects Software\Houdini 19.5\bin\hython.exe
[2026-02-25 15:33:22,544] [ERROR] [high_to_game_ready.tool:330] Hip file: C:\tools\rock_batch.hip
[2026-02-25 15:33:22,545] [ERROR] [high_to_game_ready.tool:331] Working directory: C:\assets\rocks
```

**UI console (user-facing - clean error):**

```
[INFO][high_to_game_ready.tool] >> Starting Houdini processing...
[ERROR][high_to_game_ready.tool] >> Houdini processing failed: Houdini failed with code 1
Check log file: C:\logs\high_to_game_ready_20260225_153115.log
```

User gets a clear error message and knows where to find details. Developer gets full diagnostic information.

### Benefits in Practice

After implementing this pattern, here's what changed:

**Before (Print Statements):**

- User sees: "Process failed"
- Developer sees: Nothing (have to add prints and re-run)
- Troubleshooting time: 90+ minutes per bug

**After (Three-Logger Pattern):**

- User sees: Clear error with log file path
- Developer sees: Full trace in timestamped log file
- Troubleshooting time: 15 minutes per bug

**Additional Benefits:**

1. **Zero coupling** - No logger passing between modules
2. **Easy debugging** - Toggle console to DEBUG level for verbose output
3. **Professional UX** - Users get clean, actionable messages
4. **Post-mortem analysis** - Every run captured in timestamped log files
5. **Reusable** - Pattern works for any Qt tool
6. **Standards-compliant** - Uses Python logging properly
7. **Thread-safe** - Qt signal-based logging works across threads

### Debug Mode Toggle

One nice addition: let power users see technical logging if they want:

```python
class BP_HighToGameReadyTool(BP_BaseToolWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add debug mode checkbox
        self.debug_checkbox = QtWidgets.QCheckBox("Debug Mode")
        self.debug_checkbox.stateChanged.connect(self.toggle_debug_mode)
        self.toolbar.addWidget(self.debug_checkbox)

    def toggle_debug_mode(self, state):
        if state == QtCore.Qt.Checked:
            # Show technical logging in console
            self._console_handler.setLevel(logging.DEBUG)
            _TOOL_LOGGER.info("Debug mode enabled")
        else:
            # Back to user-facing only
            self._console_handler.setLevel(logging.INFO)
            _TOOL_LOGGER.info("Debug mode disabled")
```

Now users can toggle verbose output without code changes!

### The Pattern is Reusable

Once I had this working, I templated it. Every new tool now starts with:

```python
# Tool module template
import logging as _logging
from logging.handlers import RotatingFileHandler
import os

_MODULE_NAME = "my_tool.module"
_TOOL_NAME = "my_tool"
_LOGGER = _logging.getLogger(_MODULE_NAME)          # Technical
_TOOL_LOGGER = _logging.getLogger(f"{_TOOL_NAME}.module")  # Console

class MyTool(BP_BaseToolWindow):
    def __init__(self, *args, **kwargs):
        # Set up tool root logger with file handler
        tool_root = _logging.getLogger(_TOOL_NAME)
        tool_root.propagate = False
        tool_root.setLevel(_logging.DEBUG)

        # Clear any existing handlers (prevents accumulation)
        for handler in tool_root.handlers[:]:
            handler.close()
            tool_root.removeHandler(handler)

        # Add rotating file handler (10MB max, keep 5 old logs)
        log_dir = os.path.join(os.path.expanduser("~"), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{_TOOL_NAME}.log")

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(_logging.DEBUG)
        file_handler.setFormatter(_logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s'
        ))
        tool_root.addHandler(file_handler)

        # Capture Python warnings
        _logging.captureWarnings(True)

        # Pass to base class for console handler attachment
        super().__init__(logger=tool_root, log_console=True, *args, **kwargs)

        # Log startup
        _TOOL_LOGGER.info(f"{_TOOL_NAME} initialized")
        _LOGGER.debug(f"Log file: {log_file}")

    def closeEvent(self, event):
        """Clean up handlers when tool closes"""
        _LOGGER.debug("Tool closing, cleaning up handlers")

        tool_root = _logging.getLogger(_TOOL_NAME)
        for handler in tool_root.handlers[:]:
            try:
                handler.close()
                tool_root.removeHandler(handler)
            except Exception as e:
                print(f"Error cleaning up handler: {e}")

        super().closeEvent(event)
```

**Result:** Production-ready logging with rotation, cleanup, and ~40 lines of boilerplate (most of it comments).

---

## Wrapping Up: Defensive Logging in Practice

We've covered a lot of ground - from basic logging principles to a multi-hierarchy pattern for Qt tools. Let's bring it all together with practical guidance on when and how to apply these patterns.

### Key Takeaways

**1. Logging is Defensive Programming**

Logging isn't just for debugging - it's insurance. The time you spend setting up proper logging pays dividends the first time something breaks in production. My inherited tool went from 90+ minutes per bug to 15 minutes because I could see what actually happened instead of guessing.

**2. Separation of Concerns is Critical**

Users and developers need different information from the same events. Don't force your users to read stack traces, and don't deprive your developers of technical context. The three-logger pattern solves this by routing different information to different destinations.

**3. Python's Logging System is Powerful When Used Correctly**

The logging module has been part of Python since 2003 (PEP 282). It's battle-tested, thread-safe, and flexible. But you have to use it correctly:

- Named loggers, not root logger
- Configure at application entry, not in libraries
- Hierarchy propagation, not logger passing
- Handler-level filtering for flexibility

**4. Small Upfront Investment, Huge Long-term Payoff**

Setting up the three-logger pattern takes ~30 minutes the first time. After that, it's ~10 lines of boilerplate per new tool. Compare that to hours (or days) spent debugging tools without proper logging.

### When to Use This Pattern

**Use the Three-Logger Pattern When:**

- **Building Qt/GUI tools** - Users need UI feedback separate from technical logs
- **Long-running processes** - Users need progress updates, developers need execution traces
- **Production tools** - When failures need to be investigated after the fact
- **Multi-user tools** - When users report issues, you need their log files
- **Complex workflows** - When execution path isn't obvious from code alone

**Use Simpler Approaches When:**

- **One-off scripts** - Quick automation that won't be maintained
- **Personal utilities** - Tools only you will use
- **Prototype/POC** - Code that won't reach production
- **Simple CLIs** - Tools with straightforward, linear execution

**Rule of thumb:** If more than one person will use it, or if it will run unattended, invest in proper logging.

### Choosing the Right Level of Logging

**Minimal (Quick Scripts):**

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Just use the logger
logger.info("Script complete")
```

**Standard (Most Python Projects):**

```python
import logging

_LOGGER = logging.getLogger(__name__)

# Configure at application entry point
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
```

**Advanced (GUI Tools with Three-Logger Pattern):**

```python
import logging

_MODULE_NAME = "mytool.module"
_TOOL_NAME = "mytool"
_LOGGER = logging.getLogger(_MODULE_NAME)
_TOOL_LOGGER = logging.getLogger(f"{_TOOL_NAME}.module")

class MyTool(BaseWindow):
    def __init__(self):
        tool_root = logging.getLogger(_TOOL_NAME)
        tool_root.propagate = False
        super().__init__(logger=tool_root, log_console=True)
```

**Expert (Production Systems with Complex Requirements):**

- Multiple handlers with different formatters
- Rotating file handlers (size/time-based)
- Remote logging (syslog, network handlers)
- Custom handlers (database, cloud services)
- Dynamic reconfiguration (without restarts)
- Structured logging (JSON format for parsing)

### Common Pitfalls to Avoid

**1. Not Logging Early Enough**

Don't wait until something breaks to add logging. Build it in from the start. Retrofitting logging is painful and you'll miss critical paths.

**2. Too Much or Too Little**

- **Too much:** Logging every variable assignment, every loop iteration, every function entry
- **Too little:** Only logging exceptions (no execution flow context)
- **Just right:** Entry/exit of major operations, state changes, decisions, errors

**3. Forgetting About Log File Size**

Logs grow. Without rotation or cleanup, they'll fill your disk. Use `RotatingFileHandler` or `TimedRotatingFileHandler`:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5            # Keep 5 old logs
)
```

**4. Not Testing Error Paths**

Your logging is useless if it only works in the happy path. Test your error handling and verify that logs capture what you need:

```python
# Test error paths explicitly
try:
    result = risky_operation()
except ExpectedError as e:
    logger.error("Expected failure case", exc_info=True)
    # Verify: Does log have stack trace? Context? Error details?
except UnexpectedError as e:
    logger.critical("Unexpected failure!", exc_info=True)
    # Verify: Is this loud enough? Will I notice?
```

**5. Blocking the Main Thread**

File I/O is slow. In GUI applications, synchronous logging can freeze the UI. Solutions:

- Use `QueueHandler` (Python 3.2+) for async logging
- Set handler to non-blocking mode
- Use Qt signals (like our `QTextEditLogger`)
- For heavy logging, route to background thread

**6. Not Documenting Your Logging Strategy**

Six months from now, you (or your teammate) won't remember why there are three loggers. Document your pattern:

```python
"""
Logging Architecture:
- _LOGGER: Technical logging for developers (DEBUG+, file + terminal)
- _TOOL_LOGGER: User-facing console (INFO+, UI widget only)
- Tool root: Infrastructure attachment point for console handler

See docs/logging.md for details.
"""
```

### Testing Your Logging

Logging code is code - it should be tested. Here's how to verify your logging works correctly:

**Test 1: Basic Log Output**

```python
import logging
import unittest

class TestLogging(unittest.TestCase):
    def test_error_logged(self):
        """Verify error messages are logged"""
        with self.assertLogs('myapp', level='ERROR') as cm:
            logger = logging.getLogger('myapp')
            logger.error('Something went wrong')

        # Check log was captured
        self.assertEqual(len(cm.output), 1)
        self.assertIn('Something went wrong', cm.output[0])
        self.assertIn('ERROR', cm.output[0])
```

**Test 2: Log Levels**

```python
def test_log_levels(self):
    """Verify only appropriate levels are logged"""
    with self.assertLogs('myapp', level='WARNING') as cm:
        logger = logging.getLogger('myapp')
        logger.setLevel(logging.WARNING)

        logger.debug('Debug message')    # Should not appear
        logger.info('Info message')      # Should not appear
        logger.warning('Warning message') # Should appear
        logger.error('Error message')    # Should appear

    self.assertEqual(len(cm.output), 2)  # Only WARNING and ERROR
    self.assertIn('Warning message', cm.output[0])
    self.assertIn('Error message', cm.output[1])
```

**Test 3: Exception Logging**

```python
def test_exception_logging(self):
    """Verify exceptions are logged with tracebacks"""
    with self.assertLogs('myapp', level='ERROR') as cm:
        logger = logging.getLogger('myapp')

        try:
            raise ValueError("Test error")
        except ValueError:
            logger.exception("Caught error")

    # Should have exception info
    output = ''.join(cm.output)
    self.assertIn('ValueError', output)
    self.assertIn('Test error', output)
    self.assertIn('Traceback', output)
```

**Test 4: Custom Handler**

```python
import io

def test_custom_handler_output(self):
    """Verify custom handler formats correctly"""
    logger = logging.getLogger('test_handler')
    logger.setLevel(logging.DEBUG)

    # Capture to buffer
    buffer = io.StringIO()
    handler = logging.StreamHandler(buffer)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)

    try:
        logger.info('Test message')
        output = buffer.getvalue()
        self.assertEqual(output.strip(), 'INFO: Test message')
    finally:
        logger.removeHandler(handler)
        handler.close()
```

**Test 5: Qt Handler (Integration Test)**

```python
from PySide6 import QtWidgets, QtCore
import sys

class TestQtHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create QApplication (needed for Qt widgets)"""
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)

    def test_qt_logger_appends_text(self):
        """Verify QTextEditLogger writes to widget"""
        widget = QtWidgets.QPlainTextEdit()
        handler = QTextEditLogger(widget)

        logger = logging.getLogger('qt_test')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        try:
            logger.info('Test message')

            # Process Qt events (signal delivery)
            QtCore.QCoreApplication.processEvents()

            # Check widget has text
            text = widget.toPlainText()
            self.assertIn('Test message', text)
        finally:
            logger.removeHandler(handler)
            handler.close()
```

**Mock-Based Testing (Verify Logging Calls):**

```python
from unittest.mock import patch, MagicMock

def process_data(data):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing {len(data)} items")
    # ... process data ...
    logger.info("Processing complete")

def test_process_data_logging(self):
    """Verify process_data logs expected messages"""
    with patch('__main__.logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        process_data([1, 2, 3])

        # Verify logging calls
        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_any_call('Processing 3 items')
        mock_logger.info.assert_any_call('Processing complete')
```

**Testing Best Practices:**

- Always clean up handlers in test teardown
- Use `assertLogs()` context manager (Python 3.4+)
- Test both success and error paths
- Verify log messages contain expected context
- For Qt handlers, process events before assertions
- Mock external dependencies that shouldn't affect logging tests

### Logging in DCC Environments: Special Considerations

Maya, Houdini, and other DCCs have unique quirks that affect logging:

**1. Script Editor Logging - Use Native Handler**

Maya provides `maya.utils.MayaGuiLogHandler()` for Script Editor integration. **This is the preferred approach** - don't write a custom handler:

```python
import logging
import maya.utils

def setup_maya_logging(logger_name='mytool', log_level=logging.INFO):
    """Configure logging to Maya Script Editor (preferred method)."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Clear existing Maya GUI handlers (prevents accumulation on module reload)
    for handler in logger.handlers[:]:
        if isinstance(handler, maya.utils.MayaGuiLogHandler):
            logger.removeHandler(handler)
            handler.close()

    # Use Maya's native handler - respects Script Editor colors, tabs, preferences
    gui_handler = maya.utils.MayaGuiLogHandler()
    gui_handler.setLevel(log_level)
    gui_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] [%(name)s] %(message)s'
    ))
    logger.addHandler(gui_handler)

    # Prevent double-logging to Script Editor
    logger.propagate = False

    return logger

# Usage
logger = setup_maya_logging('mytool')
logger.info("Tool initialized")  # Appears in Script Editor with proper formatting
logger.error("Something failed")  # Appears in red
```

**Why MayaGuiLogHandler wins:**

- Native integration with Script Editor (colors, tabs, filtering)
- Thread-safe by design (Maya handles the complexity)
- ~10 lines vs ~40 lines for custom Qt handler
- Battle-tested against Maya's execution model

**When to use custom Qt handler instead:**

- Building a tool with its own console widget (not Script Editor)
- Need more control over formatting/buffer management
- Cross-DCC library (Houdini doesn't have equivalent)

**2. Houdini TOPnet Subprocess Logging - Dual Log Pattern**

When running Houdini via subprocess from a Qt tool, you need **two logs**: one for developers, one for the GUI to read:

```python
# --- htgr/globals.py - Initialization module ---
import logging
import sys
from pathlib import Path

_INITIALIZED = False
_TOPNET_NAME = "high_to_game_ready"

def _initialize_module():
    """Initialize logging once for all TOP nodes"""
    global _INITIALIZED, HOUDINI_PROCESS_LOG_FILE

    if _INITIALIZED:
        return

    # 1. Set up root logger with console handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.__stdout__)
    console_formatter = logging.Formatter(
        '[%(levelname)s][%(name)s] >> %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(console_handler)

    # 2. Debug log file (for developers)
    debug_log = Path.home() / 'logs' / f'{_TOPNET_NAME}_debug.log'
    debug_log.parent.mkdir(parents=True, exist_ok=True)

    debug_handler = logging.FileHandler(debug_log, mode='w')
    debug_handler.setFormatter(logging.Formatter(
        '%(asctime)s :: [%(levelname)s][%(name)s] >> %(message)s'
    ))
    root_logger.addHandler(debug_handler)

    # 3. Process log file (for GUI to read - live progress)
    HOUDINI_PROCESS_LOG_FILE = Path.home() / 'logs' / f'{_TOPNET_NAME}_process.log'
    HOUDINI_PROCESS_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Clear process log at start (GUI reads this for progress)
    HOUDINI_PROCESS_LOG_FILE.write_text('', encoding='utf-8')

    _INITIALIZED = True

# Initialize on import
_initialize_module()


# --- htgr/validate.py - TOP node that validates ---
import logging
import htgr.globals as htgr_globals

_LOGGER = logging.getLogger(f"{htgr_globals._TOPNET_NAME}.validate")

def check_parsed_values(work_item):
    """Validate work item attributes"""
    success = True

    # Validation logic with logging
    filename = work_item.stringAttribValue('filename')
    _LOGGER.info(f"Validating: {filename}")

    if not filename:
        _LOGGER.error("Missing filename attribute")
        success = False

    if success:
        _LOGGER.info(f"{filename} PASSED")
    else:
        _LOGGER.error(f"{filename} FAILED")

    return success


# --- htgr/finish.py - Final TOP node ---
import logging
import htgr.globals as htgr_globals

_LOGGER = logging.getLogger(f"{htgr_globals._TOPNET_NAME}.finish")

# Add process log handler to this specific logger (GUI reads this)
for handler in _LOGGER.handlers[:]:
    _LOGGER.removeHandler(handler)
    handler.close()

process_handler = logging.FileHandler(htgr_globals.HOUDINI_PROCESS_LOG_FILE)
process_handler.setFormatter(htgr_globals.console_formatter)
_LOGGER.addHandler(process_handler)

def validate_work_item(work_item):
    """Final validation and result logging"""
    filename = work_item.stringAttribValue('filename')

    if work_item.isCooked:
        _LOGGER.info(f"{filename} processing complete")  # GUI sees this
        return True
    else:
        _LOGGER.error(f"{filename} processing failed")  # GUI sees this
        return False
```

**Why this pattern works:**

1. **Single initialization** - `_initialize_module()` guard prevents duplicate handlers in TOP graph
2. **Hierarchical loggers** - Each node gets its own logger (`mytool.validate`, `mytool.finish`)
3. **Dual output** - Debug log captures everything, process log only gets essential progress messages
4. **GUI integration** - Qt tool reads process log in real-time to show Houdini progress
5. **Handler per purpose** - Console for terminal, debug file for post-mortem, process file for live GUI

**Qt GUI side (reading the process log):**

```python
# In your Qt tool that launches Houdini
class HighToGameReadyTool(QMainWindow):
    def monitor_houdini_progress(self):
        """Read process log and update UI"""
        process_log = Path.home() / 'logs' / 'high_to_game_ready_process.log'

        if process_log.exists():
            with open(process_log, 'r') as f:
                content = f.read()
                self.console_widget.setPlainText(content)  # Show in UI
```

This is the pattern that solved the "90 minutes → 15 minutes" debugging problem from the article intro.

**3. Headless Subprocess Logging - Consolidating Output for Parent Capture**

When launching a DCC as a headless subprocess (mayapy, hython) from a Qt tool, you face a coordination problem: the subprocess might have multiple modules logging independently (your tool code, utility libraries, DCC APIs), and you need **all of it** to reach the parent GUI.

Here's the pattern that solves it - consolidate everything to a single stdout stream:

```python
# --- maya_export.py - Headless Maya subprocess ---
import logging
import sys

_MODULE_NAME = "high_to_game_ready.jobs.maya_export"
_LOGGER = logging.getLogger(_MODULE_NAME)
_LOGGER.setLevel(logging.DEBUG)

# Custom formatter optimized for subprocess context
_MODULE_LOG_FORMATTER = logging.Formatter(
    fmt="[%(levelname)s][%(name)s] >> %(message)s ::(%(filename)s:%(lineno)d)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Single StreamHandler for subprocess → stdout
_TEMP_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
_TEMP_CONSOLE_HANDLER.setLevel(logging.DEBUG)
_TEMP_CONSOLE_HANDLER.setFormatter(_MODULE_LOG_FORMATTER)

# Get root logger and child package loggers
__ROOT_LOGGER = logging.getLogger()
__ROOT_LOGGER.setLevel(logging.DEBUG)

_BPMPY_LOGGER = logging.getLogger("BP_mPy")  # Maya utility library
_BPPY_LOGGER = logging.getLogger("bp_py")    # Studio library

# CRITICAL: Remove StreamHandlers from child loggers to prevent duplicate output
# (They might have handlers from initialization or previous runs)
for logger in [_BPMPY_LOGGER, _BPPY_LOGGER, _LOGGER]:
    for handler in list(logger.handlers):
        if isinstance(handler, logging.StreamHandler):
            logger.removeHandler(handler)
            handler.close()

# Attach single StreamHandler to root logger to collect everything
if not any(isinstance(h, logging.StreamHandler) for h in __ROOT_LOGGER.handlers):
    __ROOT_LOGGER.addHandler(_TEMP_CONSOLE_HANDLER)

_LOGGER.debug(f"Boot initialization complete for: {_MODULE_NAME}")


# --- Subprocess execution function ---
def execute(config=None):
    """Main execution function for Maya subprocess"""
    _LOGGER.info(f"Running: {__name__} execute()")

    # All logging from any module now goes to stdout via root logger
    _LOGGER.debug("Loading Maya scene...")

    # Even third-party code logs are captured
    from BP_mPy.lib.export.modelExport import exportBpModels
    exportBpModels()  # Its logging goes to stdout too

    cleanup()
    return 0  # Success


# --- Cleanup function (called on subprocess exit) ---
def cleanup():
    """Remove handler to prevent accumulation"""
    _LOGGER.info(f"Cleaning up {_MODULE_NAME} module.")

    if _TEMP_CONSOLE_HANDLER:
        __ROOT_LOGGER.removeHandler(_TEMP_CONSOLE_HANDLER)
        _TEMP_CONSOLE_HANDLER.close()

    _LOGGER.debug("Cleanup complete")


if __name__ == "__main__":
    try:
        exit_code = execute()
    except Exception as e:
        _LOGGER.exception(f"Fatal error: {e}")
        exit_code = 1

    cleanup()
    sys.exit(exit_code)
```

**Parent side - Qt tool launches subprocess and captures output:**

```python
# --- tool.py - Qt GUI that launches Maya subprocess ---
from PySide6.QtCore import QProcess, Slot

class HighToGameReadyTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self._maya_process = None

        # Console widget using QTextEditLogger from earlier pattern
        self.console = QTextEdit()
        self.console_logger = logging.getLogger("high_to_game_ready")  # Tool root

        handler = QTextEditLogger(self.console)
        handler.setLevel(logging.INFO)
        self.console_logger.addHandler(handler)

    def start_maya_subprocess(self):
        """Launch mayapy.exe as subprocess"""
        self._maya_process = QProcess(self)

        # Connect signals to capture subprocess output
        self._maya_process.readyReadStandardOutput.connect(self._on_maya_stdout)
        self._maya_process.readyReadStandardError.connect(self._on_maya_stderr)
        self._maya_process.finished.connect(self._on_maya_finished)

        # Launch subprocess
        mayapy_path = "C:/Program Files/Autodesk/Maya2024/bin/mayapy.exe"
        script_path = "d:/tools/high_to_game_ready/jobs/maya_export.py"

        self._maya_process.start(mayapy_path, [script_path, "--json-data", config])
        self.console_logger.info("Maya subprocess started...")

    @Slot()
    def _on_maya_stdout(self):
        """Capture subprocess stdout and display in GUI"""
        if self._maya_process:
            data = self._maya_process.readAllStandardOutput()
            text = bytes(data).decode('utf-8', errors='replace')

            # Parse subprocess log lines and route through console logger
            for line in text.strip().split('\n'):
                if line:
                    # Subprocess formatter already includes level/module
                    # Display directly in console (already formatted)
                    self.console.append(line)

    @Slot()
    def _on_maya_stderr(self):
        """Capture subprocess stderr (Maya's native errors)"""
        if self._maya_process:
            data = self._maya_process.readAllStandardError()
            text = bytes(data).decode('utf-8', errors='replace')

            if text.strip():
                self.console_logger.error(f"[Maya stderr]: {text}")

    @Slot(int, QProcess.ExitStatus)
    def _on_maya_finished(self, exit_code, exit_status):
        """Handle subprocess completion"""
        if exit_code == 0:
            self.console_logger.info("Maya processing complete!")
        else:
            self.console_logger.error(f"Maya process failed (exit code: {exit_code})")
```

**Why this pattern works:**

1. **Single stdout stream** - All logs route through root logger → one StreamHandler → stdout
2. **No duplicate output** - Child logger handlers removed, eliminating echo/duplicate messages
3. **Parent captures everything** - QProcess `readyReadStandardOutput` signal gets complete log stream
4. **Context preserved** - Custom formatter includes module/file/line even when routing through root
5. **Clean startup/shutdown** - Handler cleanup prevents accumulation across multiple subprocess runs

**What you get:**

Before this pattern:

```
Process started...
[Process finished]  ← Zero visibility into what happened
```

After this pattern:

```
[INFO][high_to_game_ready.jobs.maya_export] >> Running: maya_export execute() ::(maya_export.py:465)
[DEBUG][high_to_game_ready.jobs.maya_export] >> Loading Maya scene... ::(maya_export.py:520)
[INFO][BP_mPy.lib.export.createModelExportNodes] >> Creating BP export nodes ::(createModelExportNodes.py:89)
[DEBUG][BP_mPy.lib.export.createModelExportNodes] >> Found 3 mesh nodes ::(createModelExportNodes.py:112)
[INFO][BP_mPy.lib.export.modelExport] >> Exporting: rock_01_low.model ::(modelExport.py:245)
[INFO][BP_mPy.lib.export.modelExport] >> Export successful ::(modelExport.py:289)
[INFO][high_to_game_ready.jobs.maya_export] >> Cleaning up module ::(maya_export.py:447)
```

**The difference:**

- **Houdini dual-log pattern** (previous section): Two separate files - one for developers (debug.log), one for GUI (process.log)
- **This pattern**: Single stdout consolidation - ALL logs from subprocess → parent GUI in real-time

**When to use this:**

- Launching DCC as headless subprocess (mayapy, hython, blender --python)
- Parent is Qt/GUI tool that needs to display subprocess activity
- Multiple libraries/modules all logging independently in subprocess
- Need comprehensive visibility (not just "Process succeeded/failed")

This is the complete solution to the problem from the article intro: **inherited tool with subprocess that showed "Process failed" with zero context** → comprehensive real-time logging visible in parent GUI.

---

**Variation: Adding File Logging for Third-Party Tool Integration**

When working with **Substance Automation Toolkit (SAT)** or similar third-party toolkits that spawn their own subprocess executables (sbsbaker, sbscooker, etc.), you often need both real-time parent capture AND persistent file logs for post-mortem debugging.

This is the pattern I used for the Substance texture baking stage of the pipeline:

```python
# --- substance_bake.py - Subprocess wrapper for SAT operations ---
import logging
import sys
from pathlib import Path

_MODULE_NAME = "high_to_game_ready.jobs.substance_bake"
_LOGGER = logging.getLogger(_MODULE_NAME)
_LOGGER.setLevel(logging.DEBUG)

# 1. Console handler for parent QProcess capture (same as Maya pattern)
_TEMP_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
_TEMP_CONSOLE_HANDLER.setLevel(logging.DEBUG)
_TEMP_CONSOLE_HANDLER.setFormatter(logging.Formatter(
    "[%(levelname)s][%(name)s] >> %(message)s ::(%(filename)s:%(lineno)d)"
))

# 2. File handler for persistent debugging (NEW - for SAT integration)
_TOOL_ROOT = Path(__file__).parents[1]  # high_to_game_ready/
_MODULE_FILE_LOG_PATH = (_TOOL_ROOT / ".temp" / "logs" / "substance_bake.log").resolve()
_MODULE_FILE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

_MODULE_FILE_HANDLER = logging.FileHandler(_MODULE_FILE_LOG_PATH, mode='w')
_MODULE_FILE_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s :: [%(levelname)s][%(name)s] >> %(message)s'
))
_MODULE_FILE_HANDLER.setLevel(logging.DEBUG)

# Get root logger
__ROOT_LOGGER = logging.getLogger()
__ROOT_LOGGER.setLevel(logging.DEBUG)

# Remove StreamHandlers from child loggers (prevent duplicates)
for logger in [_LOGGER]:
    for handler in list(logger.handlers):
        if isinstance(handler, logging.StreamHandler):
            logger.removeHandler(handler)

# Attach BOTH handlers to root logger
if not any(isinstance(h, logging.StreamHandler) for h in __ROOT_LOGGER.handlers):
    __ROOT_LOGGER.addHandler(_TEMP_CONSOLE_HANDLER)  # Stdout → parent GUI

if not any(isinstance(h, logging.FileHandler) and h.baseFilename == str(_MODULE_FILE_LOG_PATH)
           for h in __ROOT_LOGGER.handlers):
    __ROOT_LOGGER.addHandler(_MODULE_FILE_HANDLER)  # File → persistent debug log

_LOGGER.debug(f"Boot initialization complete for: {_MODULE_NAME}")


# --- Main execution wrapping SAT operations ---
def main():
    """Substance texture baking workflow"""
    _LOGGER.info("Starting Substance texture baking process...")

    # Import SAT Python API (pysbs)
    from pysbs import batchtools, context, substance

    # Your SAT operations here
    _LOGGER.debug(f"Loading Substance baker settings from: {settings_path}")

    # Launch SAT subprocess applet (sbsbaker)
    # SAT applet stdout/stderr is captured and logged
    process = subprocess.Popen(
        [sat_executable, "--input", mesh_path, "--output", texture_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Route SAT applet output through your logging
    for line in process.stdout:
        _LOGGER.info(f"[sbsbaker] {line.strip()}")  # SAT output visible in parent GUI

    for line in process.stderr:
        _LOGGER.error(f"[sbsbaker stderr] {line.strip()}")

    process.wait()

    if process.returncode == 0:
        _LOGGER.info("Substance baking completed successfully")
    else:
        _LOGGER.error(f"Substance baking failed (exit code: {process.returncode})")

    cleanup()
    return process.returncode


# --- Cleanup removes BOTH handlers ---
def cleanup():
    """Remove handlers to prevent accumulation"""
    _LOGGER.info(f"Cleaning up {_MODULE_NAME} module.")

    if _MODULE_FILE_HANDLER:
        __ROOT_LOGGER.removeHandler(_MODULE_FILE_HANDLER)
        _MODULE_FILE_HANDLER.close()

    if _TEMP_CONSOLE_HANDLER:
        __ROOT_LOGGER.removeHandler(_TEMP_CONSOLE_HANDLER)
        _TEMP_CONSOLE_HANDLER.close()


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception as e:
        _LOGGER.exception(f"Fatal error: {e}")
        exit_code = 1

    cleanup()
    sys.exit(exit_code)
```

**Why this hybrid pattern for SAT:**

1. **Third-party tool integration** - SAT spawns its own executables (sbsbaker, sbscooker), need to capture their output
2. **Multiple output destinations** - Console handler → parent GUI (real-time), file handler → persistent debug log
3. **Complex workflows** - Texture baking involves multiple SAT operations, file log helps reconstruct sequence
4. **Subprocess within subprocess** - Python wrapper launches SAT applets, both layers need logging
5. **Developer convenience** - File log can be auto-opened in editor if `BP_GLOBAL_DEBUG` enabled

**Output destinations:**

```python
# Console (stdout) → Parent QProcess → GUI console widget
[INFO][high_to_game_ready.jobs.substance_bake] >> Starting Substance texture baking...
[INFO][high_to_game_ready.jobs.substance_bake] >> [sbsbaker] Processing rock_01_low.fbx
[INFO][high_to_game_ready.jobs.substance_bake] >> [sbsbaker] Baking normal map...
[INFO][high_to_game_ready.jobs.substance_bake] >> Baking completed successfully

# File (.temp/logs/substance_bake.log) → Post-mortem debugging
2026-02-25 15:45:10,123 :: [INFO][high_to_game_ready.jobs.substance_bake] >> Starting Substance texture baking...
2026-02-25 15:45:10,456 :: [DEBUG][high_to_game_ready.jobs.substance_bake] >> Loading settings: bp_designer_smm_baker.json
2026-02-25 15:45:11,789 :: [INFO][high_to_game_ready.jobs.substance_bake] >> [sbsbaker] Processing rock_01_low.fbx
2026-02-25 15:45:15,234 :: [INFO][high_to_game_ready.jobs.substance_bake] >> [sbsbaker] Baking normal map...
2026-02-25 15:45:18,567 :: [INFO][high_to_game_ready.jobs.substance_bake] >> Baking completed successfully
```

**Pattern comparison:**

| Pattern                              | Console (stdout) | File Log          | Use Case                                              |
| ------------------------------------ | ---------------- | ----------------- | ----------------------------------------------------- |
| **Maya headless** (previous section) | ✅ Yes            | ❌ No              | Simple DCC subprocess, parent capture sufficient      |
| **Substance/SAT** (this variation)   | ✅ Yes            | ✅ Yes             | Third-party tool integration, complex workflows       |
| **Houdini TOPnet** (earlier section) | ✅ Yes (via file) | ✅ Yes (dual logs) | Long-running distributed processing, GUI coordination |

**When to use this hybrid pattern:**

- Wrapping third-party tools with their own executables (SAT, FFmpeg, ImageMagick, etc.)
- Complex multi-stage workflows where reconstructing sequence matters
- Need both real-time GUI feedback AND post-mortem analysis
- Developer debugging of subprocess coordination issues
- Long-running operations where you might need to review logs after completion

This is what I ended up doing for the **Substance Automation Toolkit integration** in the High to Game Ready pipeline. The file log was invaluable when SAT applets failed mysteriously - I could see exactly which baker preset was loaded, what parameters were passed, and where the process died.

---

**4. Module Reloading During Development**

Developers reload modules constantly in DCCs. Logger singletons persist:

```python
# Problem: Handlers accumulate on reload
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('tool.log'))  # Added every reload!

# Solution: Always clear handlers first
def setup_logger():
    logger = logging.getLogger(__name__)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    # Add fresh handler
    logger.addHandler(logging.FileHandler('tool.log'))
    return logger

logger = setup_logger()
```

**5. Long-Running Sessions (Memory Management)**

DCC sessions run for days. Log files and UI buffers grow unbounded:

```python
from logging.handlers import RotatingFileHandler

# Automatic log rotation
handler = RotatingFileHandler(
    'maya_tool.log',
    maxBytes=10*1024*1024,  # 10MB per file
    backupCount=3           # Keep 3 old files
)

# For UI console widgets - limit buffer (see QTextEditLogger.append_log example)
```

**6. Threading/Async in Houdini**

Houdini's Python environment has thread safety issues:

```python
# Python logging module is thread-safe
# But be careful with custom handlers that touch Houdini state

import logging
import hou

class HoudiniHandler(logging.Handler):
    def emit(self, record):
        # DON'T call hou.ui methods from non-main threads!
        # Use Qt signals or executeDeferred patterns
        pass
```

**7. Import Path Pollution**

DCCs modify `sys.path` aggressively. Use explicit module names:

```python
# Risky - might get wrong module in DCC
logger = logging.getLogger(__name__)

# Safer - explicit namespace
logger = logging.getLogger('mystudio.mytool.module')
```

**8. User Shutdown (Tool Stays Loaded)**

Users close tool UIs, but Python objects persist in DCC session:

```python
class MyToolWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        """Always cleanup handlers on close"""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
        super().closeEvent(event)
```

**9. Multiple Tool Instances**

Users might open multiple instances of your tool:

```python
import logging
import uuid

class MyTool:
    def __init__(self):
        # Unique logger per instance
        instance_id = str(uuid.uuid4())[:8]
        self.logger = logging.getLogger(f'mytool.{instance_id}')

        # Or: shared logger, instance context in messages
        self.logger = logging.getLogger('mytool')
        self.instance_id = instance_id
        self.logger.info(f"[{self.instance_id}] Tool initialized")
```

**10. DCC Version Differences**

Maya 2023 uses Python 3.9, Maya 2024 uses 3.10. Logging APIs changed:

```python
import sys
import logging

# Python 3.8+ has force kwarg for basicConfig
if sys.version_info >= (3, 8):
    logging.basicConfig(level=logging.DEBUG, force=True)
else:
    # Older Python: manually clear handlers
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG)
```

**DCC Logging Checklist:**

- ✅ Clear handlers before adding new ones
- ✅ Use rotating file handlers
- ✅ Clean up handlers in closeEvent/shutdown
- ✅ Test with multiple tool loads/unloads
- ✅ Verify thread safety for custom handlers
- ✅ Use absolute module names, not `__name__` if fragile
- ✅ Handle version differences gracefully
- ✅ Document log file locations for users

### Making It Stick: Building the Habit

**For New Projects:**

1. **Day 1:** Set up logging infrastructure before writing business logic
2. **Template it:** Create a project template with logging pre-configured
3. **Make it easy:** If logging is hard, you won't do it consistently

**For Existing Projects:**

1. **Start with entry points:** Add logging to main(), top-level functions
2. **Work inward:** Add logging as you touch code (don't refactor everything at once)
3. **Focus on pain points:** Log the parts that break most often first

**For Teams:**

1. **Code review:** Check for proper logging during reviews
2. **Standards doc:** Document your logging patterns (this post can be that doc!)
3. **Share wins:** When logging saves the day, share the story
4. **Make it visible:** Show examples of good logging in team meetings

### Resources and Further Reading

**Python Documentation:**

- [Logging HOWTO](https://docs.python.org/3/howto/logging.html) - Official Python logging guide
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html) - Advanced patterns and recipes
- [PEP 282](https://www.python.org/dev/peps/pep-0282/) - Original logging proposal (historical context)

**Best Practices:**

- [The Hitchhiker's Guide to Python: Logging](https://docs.python-guide.org/writing/logging/) - Practical advice
- [Real Python: Logging in Python](https://realpython.com/python-logging/) - Tutorial with examples
- [Python Logging: Best Practices](https://betterstack.com/community/guides/logging/python/python-logging-best-practices/) - Comprehensive guide

**Qt/GUI-Specific:**

- [Qt Signals and Slots](https://doc.qt.io/qt-6/signalsandslots.html) - Understanding thread-safe communication
- [QPlainTextEdit Documentation](https://doc.qt.io/qt-6/qplaintextedit.html) - Widget used in console handler

**Advanced Topics:**

- [Structured Logging in Python](https://www.structlog.org/) - JSON logging for parsing
- [Logging Performance](https://docs.python.org/3/howto/logging.html#optimization) - Making logging fast
- [Distributed Tracing](https://opentelemetry.io/docs/instrumentation/python/) - Logging in microservices

**Tools:**

- [Loguru](https://github.com/Delgan/loguru) - Simplified logging library (alternative to stdlib)
- [Python-json-logger](https://github.com/madzak/python-json-logger) - JSON formatting for logs
- [Sentry](https://sentry.io/) - Error tracking and logging SaaS

### Final Thoughts

I've been using Python's logging module for years across my own projects - it's been an evolution of practice, refinement, and pattern development. Every tool I built taught me something new about what works, what doesn't, and why defensive logging matters.

Often when I joined new teams, I found a different landscape. Logging existed, but it was scattered, inconsistent, and didn't follow industry standards. Some tools had it, others didn't. There was no unified approach, no shared patterns.

**More challenging than the technical work was the cultural resistance.**

I have heard all kinds of pushback, some of this probably sounds familiar to anyone who's tried to bring new practices to an established team:

_"If the code works, you don't need logging."_

Until it doesn't. Until a Maya version changes Python versions, or an API call changes, or a package dependency breaks, or someone deprecated a dependancy but miss this code. Then you're waiting for the bomb to go off before you can start triage. Something will break eventually for one reason or another ... Defensive logging means you have the data _when_ things break (not if - when).

_"Logging makes the module code harder to read."_

Actually, it _replaces_ comments and makes code self-documenting. When I see `logger.info("Validating UV sets...")` followed by validation logic, I know exactly what's happening. And the patterns enforce other beneficial habits - you can't log validation results if you don't validate in the first place.

_"My tools work fine without it."_

Do they though? Or do they work fine _for you_, after you've manually run code over and over, added print statements, debugged, then removed those print statements? How many hours do you spend stepping through code to find where things break? All it takes is that one missed edge case and silent failure.

_"I've looked at other studios' code - it's no more advanced than ours."_

That's not the flex you think it is. Yes, I've seen code at major studios - including many AAA team - and much of it is messy scripting, not professional software engineering. But that's the _problem_, not justification. Why should Technical Artists at companies building AAA games not be held to a professional baseline of standards?

**What is the "technical bar" in technical art when you're writing code?** Is it "good enough to ship once" or "good enough to maintain for years"? Is it "works on my machine" or "works for the team"? Is it "I can debug it" or "anyone can debug it"? Could another studio pick up your code and understand it, or debug it without you?

Maybe the real question is: **to make better games faster, don't we need better standards and reusable, enterprise-quality code across studios?** If everyone is writing the same messy scripts, we're all reinventing the same wheels, badly. That's not efficiency - that's institutional dysfunction.

I've encountered a lot of other situations and types of resitance, here are some: not upgrading to use pathlib, not updating to f-strings for more readable code, not using virtual environments, not using type hints, not writing tests, not branching/versioning python code bases, not using code reviews, not following actual PEP8 standards (like clear variable names), etc. The pattern is the same - resistance to change, comfort with the status quo, and a lack of vision for what better practices can do for everyone.

The fact that other studios have the same problems doesn't mean we should accept them. It means the entire industry needs to level up.

By all means I am not trying disparge anyone, any studio, or codebase - I know how hard it is to build tools in this environment when you have to move fast, and I know how much of the work is invisible, or frustratingly at times is seen as a second class citizen.  Sometimes you just gotta do what you need to, and if it ain't broken don't fix it. I'm just trying to strongman and share what I've learned about what works, and why it matters.  Longe term velocity and maintainability are the real wins here, and logging is a critical part of that.

**Here's what those objections really mean: "This is new to me. I'm uncomfortable."**

And I get it - change is uncomfortable. Learning new patterns takes time. But there's a cost to staying comfortable:

**Without logging:**

- Add print statements when something breaks
- Run code, read output, add more prints
- Repeat until you find the problem
- Clean up all the print statements
- Hope you don't need them again tomorrow
- Troubleshooting time: 1-2 hours of stepping through code

**With logging:**

- Read the last 20 lines of the log file
- See exactly where it failed and why
- See the full context leading up to failure
- Troubleshooting time: ~15 minutes, straight to the problem

The difference isn't just speed - it's _confidence_. I can hand my tools to artists knowing that when (not if) something breaks, they'll have a log file to send me. I can look at that log file and know exactly what happened, even if I wasn't there when it failed.

**The three-logger pattern isn't revolutionary** - it's just Python's logging system used thoughtfully. But that thoughtfulness makes the difference between:

- "The tool broke and we have no idea why"
- "The tool broke, here's exactly what happened, and here's the fix"

Between:

- "Let me add some print statements and we'll try again"
- "Here's the log file from when it failed, I see the problem at line 247"

Between:

- Manually reproducing bugs over and over
- Reading persistent records of exactly what happened

**If you're the first person on your team pushing for proper logging, expect resistance.** People will claim their tools work fine without it (while manually debugging for hours). They'll say logging makes code messy (while writing `print()` statements they'll delete later). They'll say it's overkill (until the bomb goes off and they have no data).

That's okay. Lead by example:

1. **Add logging to your own tools first** - Let results speak for themselves
2. **Document your patterns** - Make it easy for others to follow
3. **Share the wins** - "This log file saved me 90 minutes today"
4. **Be patient** - Cultural change takes time
5. **Make it template-driven** - Reduce friction to adoption

Over time, people will notice. They'll see you troubleshooting issues in 15 minutes that would have taken them 2 hours. They'll see users sending you informative error reports instead of "it broke, I don't know why." They'll see your code is self-documenting and easier to understand, not harder.

And slowly, the pattern will spread.

> **If you can't log it, you can't debug it. If you can't debug it, you can't trust it.**

That's the philosophy I've been refining for years. That's what I brought to Bluepoint. That's what I'm sharing with you today.

**Now go add logging to that project you've been putting off.** Your future self will thank you. And maybe, just maybe, you'll start changing your team's culture too.

---

*Have questions or improvements to this pattern? Did you find errors, omissions, inaccurate statements, or flaws in the code snippets? Open an issue on the [CO3DEX repository](https://github.com/HogJonny-AMZN/CO3DEX). Find me on the Discord (in O3DE).*

*Want to see the full implementation? Pester me to make some of my repos and tools public! (see my next blog post related to this tool, coming soon... )*

---

```python

import logging as _logging
_MODULENAME = 'co3dex.posts.python_tool_logging'
_LOGGER = _logging.getLogger(_MODULENAME)
_LOGGER.info(f'Initializing: {_MODULENAME} ... you only get half credit if you cannot show your work!')

```

---
