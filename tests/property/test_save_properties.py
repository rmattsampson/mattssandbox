"""
Property-based tests for save/load functionality.

Tests the correctness properties related to game state persistence.
"""

import pytest
from hypothesis import given, strategies as st
from datetime import datetime
import json

from backend.models import (
    GameState, Player, World, NPC, WorkTask, GameMetadata
)


# Hypothesis strategies for generating test data

@st.composite
def player_strategy(draw):
    """Generate random Player instances."""
    return Player(
        x=draw(st.integers(min_value=-100, max_value=100)),
        y=draw(st.integers(min_value=-100, max_value=100)),
        credits=draw(st.integers(min_value=0, max_value=10000)),
        sprite_id=draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_')))
    )


@st.composite
def npc_strategy(draw):
    """Generate random NPC instances."""
    return NPC(
        id=draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_'))),
        x=draw(st.integers(min_value=0, max_value=50)),
        y=draw(st.integers(min_value=0, max_value=50)),
        sprite_id=draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_'))),
        dialogue_state=draw(st.one_of(st.none(), st.text(min_size=1, max_size=20)))
    )


@st.composite
def work_task_strategy(draw):
    """Generate random WorkTask instances."""
    return WorkTask(
        id=draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_'))),
        x=draw(st.integers(min_value=0, max_value=50)),
        y=draw(st.integers(min_value=0, max_value=50)),
        reward=draw(st.integers(min_value=1, max_value=1000)),
        completed=draw(st.booleans())
    )


@st.composite
def world_strategy(draw):
    """Generate random World instances."""
    width = draw(st.integers(min_value=5, max_value=20))
    height = draw(st.integers(min_value=5, max_value=20))
    
    # Generate tile map
    tiles = []
    tile_ids = ['ground', 'desert', 'structure', 'rock', 'sand']
    for _ in range(height):
        row = [draw(st.sampled_from(tile_ids)) for _ in range(width)]
        tiles.append(row)
    
    npcs = draw(st.lists(npc_strategy(), min_size=0, max_size=5))
    work_tasks = draw(st.lists(work_task_strategy(), min_size=0, max_size=5))
    
    return World(
        width=width,
        height=height,
        tiles=tiles,
        npcs=npcs,
        work_tasks=work_tasks
    )


@st.composite
def game_metadata_strategy(draw):
    """Generate random GameMetadata instances."""
    return GameMetadata(
        save_id=draw(st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_-'))),
        timestamp=datetime.now().isoformat(),
        play_time=draw(st.integers(min_value=0, max_value=100000))
    )


@st.composite
def game_state_strategy(draw):
    """Generate random GameState instances."""
    return GameState(
        player=draw(player_strategy()),
        world=draw(world_strategy()),
        metadata=draw(game_metadata_strategy())
    )


# Property-based tests

@given(game_state_strategy())
def test_save_load_round_trip(game_state):
    """
    Feature: desert-planet-game, Property 13: Save and load preserves game state
    
    For any valid game state, saving it and then loading it should produce 
    an equivalent game state with the same player position, credits, NPC states, 
    and task completion status.
    
    Validates: Requirements 5.1, 5.2
    """
    # Serialize to JSON
    json_str = game_state.to_json()
    
    # Deserialize from JSON
    loaded_state = GameState.from_json(json_str)
    
    # Verify player state is preserved
    assert loaded_state.player.x == game_state.player.x
    assert loaded_state.player.y == game_state.player.y
    assert loaded_state.player.credits == game_state.player.credits
    assert loaded_state.player.sprite_id == game_state.player.sprite_id
    
    # Verify world dimensions are preserved
    assert loaded_state.world.width == game_state.world.width
    assert loaded_state.world.height == game_state.world.height
    
    # Verify tile map is preserved
    assert loaded_state.world.tiles == game_state.world.tiles
    
    # Verify NPCs are preserved
    assert len(loaded_state.world.npcs) == len(game_state.world.npcs)
    for loaded_npc, original_npc in zip(loaded_state.world.npcs, game_state.world.npcs):
        assert loaded_npc.id == original_npc.id
        assert loaded_npc.x == original_npc.x
        assert loaded_npc.y == original_npc.y
        assert loaded_npc.sprite_id == original_npc.sprite_id
        assert loaded_npc.dialogue_state == original_npc.dialogue_state
    
    # Verify work tasks are preserved
    assert len(loaded_state.world.work_tasks) == len(game_state.world.work_tasks)
    for loaded_task, original_task in zip(loaded_state.world.work_tasks, game_state.world.work_tasks):
        assert loaded_task.id == original_task.id
        assert loaded_task.x == original_task.x
        assert loaded_task.y == original_task.y
        assert loaded_task.reward == original_task.reward
        assert loaded_task.completed == original_task.completed
    
    # Verify metadata is preserved
    assert loaded_state.metadata.save_id == game_state.metadata.save_id
    assert loaded_state.metadata.timestamp == game_state.metadata.timestamp
    assert loaded_state.metadata.play_time == game_state.metadata.play_time
