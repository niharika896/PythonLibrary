# OceanMaster Bot Programming Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

OceanMaster is a strategy-based bot programming platform where you design **autonomous bots** that explore, harvest, fight, and survive in a grid-based world. This Python library provides the framework for creating intelligent bot strategies that operate independently once spawned.

## What the Project Does

This library enables developers to program bots for the OceanMaster game, a competitive environment where bots must navigate a grid, collect resources (algae), defend against enemies, and manage energy efficiently. Bots are defined by strategies implemented as Python classes, and the game engine handles execution autonomously.

## Why the Project is Useful

- **Strategic Programming**: Learn and practice algorithmic thinking through bot strategy development
- **Autonomous AI**: Create bots that make decisions independently based on game state
- **Competitive Gaming**: Compete with other players' bots in tournaments
- **Educational Tool**: Understand game theory, pathfinding, and resource management
- **Extensible Framework**: Build upon existing bot templates or create custom strategies

Key features include:
- Pre-built bot templates (Forager, HeatSeeker, Lurker, etc.)
- Comprehensive game API for sensing environment
- Ability system for bot customization
- Strategy inheritance for fine-tuning behaviors

## How Users Can Get Started

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/niharika896/PythonLibrary.git
   cd PythonLibrary
   ```

2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

1. **Define Your Bot Strategy**: Edit `User.py` to create custom bot classes that inherit from `BotController`.

2. **Implement the `act` Method**: Define how your bot behaves each turn.

3. **Set Spawn Policy**: Decide when and which bots to spawn in the `spawn_policy` function.

4. **Run the Game**: Integrate with the OceanMaster game engine (contact maintainers for engine access).

### Example: Creating a Simple Forager Bot

```python
from controllers.BotBase import BotController
from Constants import Direction

class MyForager(BotController):
    TEMPLATE = "MyForager"

    def act(self):
        ctx = self.ctx

        # If carrying algae, head to bank
        if ctx.getAlgaeHeld() > 0:
            bank = ctx.getNearestBank()
            direction = ctx.moveTarget(ctx.getLocation(), bank)
            if direction:
                return ctx.move(direction)

        # Otherwise, look for algae
        algae = ctx.senseAlgae()
        if algae:
            return ctx.harvestAlgae(algae.direction)

        # Move randomly if nothing found
        return ctx.move(Direction.NORTH)
```

### Advanced Example: Custom Spawn Policy

```python
def spawn_policy(api):
    actions = []
    if api.view.bot_count < api.view.max_bots:
        # Spawn a custom bot with extra abilities
        abilities = [
            Ability.HARVEST.value,
            Ability.SCOUT.value,
            Ability.SPEED.value,
        ]
        if can_afford(api, abilities):
            actions.append(spawn("MyForager", abilities))
    return actions
```

## Bot Inheritance and Fine-Tuning

You can inherit from existing bot templates to create specialized versions with modified behavior. This allows you to build upon proven strategies while adding your own tweaks.

### Example: Creating a Cautious Forager

```python
from templates.Forager import Forager
from controllers.BotBase import BotController

class CautiousForager(Forager):
    """
    A safer version of the built-in Forager.
    Deposits algae earlier to avoid losing it in combat.
    """

    def act(self):
        ctx = self.ctx

        # Deposit earlier than base Forager (which waits for 5 algae)
        if ctx.getAlgaeHeld() >= 3:
            bank = ctx.getNearestBank()
            direction = ctx.moveTarget(ctx.getLocation(), bank)
            if direction:
                return ctx.move(direction)

        # Otherwise, reuse base Forager behavior
        return super().act()
```

This example inherits from the `Forager` template and overrides the `act` method to deposit algae at 3 units instead of 5, making it more conservative.

## Bot Functionality Overview

Bots interact with the game world through the `BotContext` class, which provides a comprehensive set of methods for:

- **Status Monitoring**: Get bot ID, energy level, location, carried algae, and equipped abilities
- **Environmental Sensing**: Detect nearby enemies, friendly bots, algae, scraps, walls, and static objects like banks and energy pads
- **Pathfinding & Movement**: Calculate paths, check for obstacles, and execute safe movements toward targets
- **Resource Management**: Harvest algae, calculate ability costs, and locate nearest resources
- **Combat Actions**: Defend against attacks or self-destruct when necessary
- **Strategic Helpers**: Find nearest banks, energy pads, enemies, or resources for efficient decision-making

These methods enable bots to make intelligent, autonomous decisions based on the current game state.

```
PythonLibrary/
├── API.py                 # GameAPI class for accessing game state
├── BotContext.py          # Context methods for bot actions
├── Constants.py           # Enums for abilities, directions, etc.
├── User.py                # User-defined strategies and spawn policy
├── Wrapper.py             # Engine integration wrapper
├── controllers/           # Bot controller base classes
├── models/                # Game entity models
└── templates/             # Pre-built bot strategy templates
```

## Where Users Can Get Help

- **GitHub Issues**: Report bugs or request features at [https://github.com/niharika896/PythonLibrary/issues](https://github.com/niharika896/PythonLibrary/issues)
- **Documentation**: See inline code comments and docstrings for API details
- **Community**: Join discussions in the repository's discussions section

## Who Maintains and Contributes

**Maintainer**: [niharika896](https://github.com/niharika896)

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Reporting issues
- Submitting pull requests
- Code style and standards

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.