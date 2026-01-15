# OceanMaster Python SDK (`ocean_lib`)

A robust, strongly-typed Python library for building bots for **Ocean Master**.

## Core Philosophy

> **A bot is born with a strategy. It lives with that strategy. It dies with that strategy.**

In Ocean Master, you don't micromanage every unit every turn. Instead, you define **Strategies** (behaviors) and assign them to bots when they spawn. The library handles the rest.

## Quick Start

1.  **Inherit from `Game`**: This is your main engine.
2.  **Define a `BotStrategy`**: This is your bot's brain.
3.  **Run logic**: The library handles state parsing and action dispatch.

## Architecture

### `BotStrategy`
The brain of a single bot. Implement the abstract `act(self, ctx: BotContext)` method.
*   **Input**: `BotContext` (Your view of the world).
*   **Output**: `Action` (Move, Attack, Spawn, etc.) or `None`.

### `BotContext`
A helper class passed to `act()`. It wraps the raw `Bot` data and `GameState` to provide convenient method:
*   `ctx.move(direction, step=1)`
*   `ctx.attack(target_point)`
*   `ctx.get_enemies_in_radius(radius)`
*   `ctx.spawn(abilities, strategy)`

### `Game`
The central manager. It maintains persistence:
*   `self._strategies`: Maps `bot_id` -> `BotStrategy` instance.
*   **Spawning**: When you call `ctx.spawn()`, the `Game` generates a ID locally and maps the new strategy instance immediately.

## Spawning Bots

To spawn a new bot, you must provide the **Abilities** and the **Strategy Instance** that will control it.

```python
class MotherShip(BotStrategy):
    def act(self, ctx: BotContext):
        if ctx.scraps >= 50:
            # Spawn a new Scout with the FlashScout strategy
            return ctx.spawn(
                abilities=[Ability.SPEED, Ability.SCOUT],
                strategy=FlashScoutStrategy()
            )
```

## Included Templates

Check `ocean_lib/templates/` for reference implementations:
*   **Forager**: Harvests algae and returns to bank.
*   **FlashScout**: Uses speed to explore quickly.
*   **Lurker**: Stationary defender.
*   **Saboteur**: Hunts down specific enemies.
*   **HeatSeeker**: Logic to ram into targets.

## Data Structures
All models are strictly typed dataclasses found in `ocean_lib.models`:
*   `Point(x, y)`
*   `Bot`
*   `GameMap` / `GameState`
*   `Action` types (`MoveAction`, `SpawnAction`, etc.)