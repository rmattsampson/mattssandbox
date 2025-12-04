"""
Data models for the Desert Planet Game.

This module defines the core data structures used throughout the game:
- Player: Player character state (position, credits)
- NPC: Non-player character data
- WorkTask: Work task definitions
- Tile: Tile type definitions
- DialogueChoice: Dialogue option structure
- DialogueNode: Dialogue tree node
- World: Game world state
- GameState: Complete game state
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class Player:
    """Player character state."""
    x: int
    y: int
    credits: int
    sprite_id: str = "player_default"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create Player from dictionary."""
        return cls(**data)


@dataclass
class NPC:
    """Non-player character."""
    id: str
    x: int
    y: int
    sprite_id: str
    dialogue_state: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NPC':
        """Create NPC from dictionary."""
        return cls(**data)


@dataclass
class WorkTask:
    """Work task that players can complete for credits."""
    id: str
    x: int
    y: int
    reward: int
    completed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkTask':
        """Create WorkTask from dictionary."""
        return cls(**data)


@dataclass
class Tile:
    """Tile definition."""
    id: str
    type: str  # "ground", "desert", "structure"
    walkable: bool
    sprite_index: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tile':
        """Create Tile from dictionary."""
        return cls(**data)


@dataclass
class DialogueChoice:
    """A dialogue choice option."""
    id: str
    text: str
    next_node_id: Optional[str]
    action: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogueChoice':
        """Create DialogueChoice from dictionary."""
        return cls(**data)


@dataclass
class DialogueNode:
    """A node in a dialogue tree."""
    id: str
    text: str
    choices: List[DialogueChoice] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'text': self.text,
            'choices': [choice.to_dict() for choice in self.choices]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogueNode':
        """Create DialogueNode from dictionary."""
        choices = [DialogueChoice.from_dict(c) for c in data.get('choices', [])]
        return cls(
            id=data['id'],
            text=data['text'],
            choices=choices
        )


@dataclass
class World:
    """Game world state."""
    width: int
    height: int
    tiles: List[List[str]]  # 2D array of tile IDs
    npcs: List[NPC] = field(default_factory=list)
    work_tasks: List[WorkTask] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'width': self.width,
            'height': self.height,
            'tiles': self.tiles,
            'npcs': [npc.to_dict() for npc in self.npcs],
            'work_tasks': [task.to_dict() for task in self.work_tasks]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'World':
        """Create World from dictionary."""
        npcs = [NPC.from_dict(n) for n in data.get('npcs', [])]
        work_tasks = [WorkTask.from_dict(t) for t in data.get('work_tasks', [])]
        return cls(
            width=data['width'],
            height=data['height'],
            tiles=data['tiles'],
            npcs=npcs,
            work_tasks=work_tasks
        )


@dataclass
class GameMetadata:
    """Metadata about the game save."""
    save_id: str
    timestamp: str
    play_time: int = 0  # in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameMetadata':
        """Create GameMetadata from dictionary."""
        return cls(**data)


@dataclass
class GameState:
    """Complete game state."""
    player: Player
    world: World
    metadata: GameMetadata
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'player': self.player.to_dict(),
            'world': self.world.to_dict(),
            'metadata': self.metadata.to_dict()
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create GameState from dictionary."""
        player = Player.from_dict(data['player'])
        world = World.from_dict(data['world'])
        metadata = GameMetadata.from_dict(data['metadata'])
        return cls(player=player, world=world, metadata=metadata)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'GameState':
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
