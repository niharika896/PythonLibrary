# OceanMaster Bot Programming – User Guide

OceanMaster is a strategy-based bot programming platform where you design **autonomous bots** that explore, harvest, fight, and survive in a grid-based world.

> **Key Mindset**  
> You do **not** control bots every turn.  
> You **define strategies**, and bots follow them autonomously for their entire lifetime.

## Core Philosophy

> **A bot is born with a strategy.  
> It lives with that strategy.  
> It dies with that strategy.**

- You define **how a bot behaves**
- The engine decides **when that behavior runs**
- You never micromanage bots after spawning

---

## Architecture Overview

| Layer | Responsibility |
|------|----------------|
| **User (`user.py`)** | Strategy logic only |
| **BotContext** | Gives you methods to define your custom bot |
| **Helpers** | Create actions (`move`, `attack`, etc.) |

You only write **`user.py`**.

---

## Bots = Strategies

Each bot type is a **Python class**.

```python
class Forager(BotController):
    def act(self):
        ...
```
Define your complete bot strategy here and execute!
