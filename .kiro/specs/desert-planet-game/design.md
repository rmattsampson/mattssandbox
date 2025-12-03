# Design Document

## Overview

The Desert Planet Game is a web-based 8-bit style exploration game built with a Python backend and HTML5 Canvas frontend. The architecture follows a client-server model where the Python backend manages game state, world logic, and persistence, while the frontend handles rendering, input, and user interface. The game features a tile-based 2D world with free-range exploration, NPC interactions, and a credit-based progression system.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────┐
│         Web Browser (Client)        │
│  ┌───────────────────────────────┐  │
│  │   HTML5 Canvas Renderer       │  │
│  │   - 8-bit sprite rendering    │  │
│  │   - Tile-based world display  │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Input Handler               │  │
│  │   - Cursor key events         │  │
│  │   - Multiple choice selection │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   API Client                  │  │
│  │   - WebSocket/HTTP requests   │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
              │
              │ JSON over HTTP/WebSocket
              │
┌─────────────────────────────────────┐
│      Python Backend (Server)        │
│  ┌───────────────────────────────┐  │
│  │   Game Engine                 │  │
│  │   - Movement logic            │  │
│  │   - Collision detection       │  │
│  │   - NPC interaction           │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   World Manager               │  │
│  │   - Tile map management       │  │
│  │   - NPC positioning           │  │
│  │   - Work task generation      │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Save System                 │  │
│  │   - JSON serialization        │  │
│  │   - File-based persistence    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Technology Stack

- **Frontend**: HTML5, Canvas API, JavaScript
- **Backend**: Python 3.10+, Flask/FastAPI for REST API
- **Data Format**: JSON for state serialization and API communication
- **Storage**: File-based JSON storage for save games

## Components and Interfaces

### Frontend Components

#### Canvas Renderer
- Renders the game world using tile-based drawing
- Displays player character, NPCs, and environment tiles
- Implements 8-bit style sprite rendering with limited color palette
- Handles viewport scrolling to keep player centered

#### Input Handler
- Captures cursor key events (up, down, left, right)
- Manages multiple choice prompt selection
- Sends player actions to backend via API

#### UI Manager
- Displays credit balance
- Renders multiple choice prompts
- Shows interaction indicators near NPCs
- Manages save/load menu interface

### Backend Components

#### Game Engine
- Processes player movement requests
- Validates movement against world boundaries
- Handles collision detection with NPCs and objects
- Manages game state transitions

#### World Manager
- Maintains the tile map representing the game world
- Tracks NPC positions and states
- Generates work task opportunities
- Determines when player enters desert border region

#### NPC System
- Stores NPC dialogue trees
- Manages conversation state
- Provides multiple choice dialogue options
- Tracks NPC-specific quest/task states

#### Economy System
- Tracks player credit balance
- Defines work tasks and their credit rewards
- Validates task completion
- Updates credit totals

#### Save System
- Serializes complete game state to JSON
- Writes save files to disk
- Loads and validates save data
- Handles save file corruption gracefully

### API Endpoints

```
POST /api/game/new
- Creates a new game session
- Returns: Initial game state

POST /api/game/load
- Body: { save_id: string }
- Returns: Loaded game state

POST /api/game/save
- Body: { game_state: GameState }
- Returns: Save confirmation

POST /api/player/move
- Body: { direction: "up"|"down"|"left"|"right" }
- Returns: Updated game state

POST /api/player/interact
- Body: { target_id: string }
- Returns: Interaction options (dialogue/work tasks)

POST /api/player/choose
- Body: { choice_id: string }
- Returns: Updated game state after choice
```

## Data Models

### GameState
```python
{
  "player": {
    "x": int,
    "y": int,
    "credits": int,
    "sprite_id": string
  },
  "world": {
    "width": int,
    "height": int,
    "tiles": [[tile_id, ...], ...],
    "npcs": [
      {
        "id": string,
        "x": int,
        "y": int,
        "sprite_id": string,
        "dialogue_state": string
      }
    ],
    "work_tasks": [
      {
        "id": string,
        "x": int,
        "y": int,
        "reward": int,
        "completed": bool
      }
    ]
  },
  "metadata": {
    "save_id": string,
    "timestamp": string,
    "play_time": int
  }
}
```

### Tile
```python
{
  "id": string,
  "type": "ground"|"desert"|"structure",
  "walkable": bool,
  "sprite_index": int
}
```

### DialogueNode
```python
{
  "id": string,
  "text": string,
  "choices": [
    {
      "id": string,
      "text": string,
      "next_node_id": string,
      "action": Optional[string]
    }
  ]
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Movement updates position correctly
*For any* valid player position and movement direction (up, down, left, right), executing that movement should update the player coordinates in the expected direction: up decreases y, down increases y, left decreases x, right increases x.
**Validates: Requirements 1.1, 1.2, 1.3, 1.4**

### Property 2: In-bounds positions return world terrain
*For any* position within the game world boundaries, querying the tile at that position should return a non-desert terrain type with the appropriate world data.
**Validates: Requirements 1.5**

### Property 3: Out-of-bounds positions return desert terrain
*For any* position outside the game world boundaries, querying the tile at that position should return desert terrain type.
**Validates: Requirements 2.1**

### Property 4: Desert border has no interactive elements
*For any* position in the desert border region, querying for NPCs or work tasks at that position should return empty results.
**Validates: Requirements 2.2**

### Property 5: Border transition preserves world terrain
*For any* player position, moving out of bounds into the desert border and then moving back to the original position should result in the same terrain type as initially present.
**Validates: Requirements 2.3**

### Property 6: Adjacent positions trigger interaction availability
*For any* NPC position and player position that are adjacent (Manhattan distance of 1), the interaction check should return true indicating interaction is available.
**Validates: Requirements 3.1**

### Property 7: NPC interaction returns dialogue choices
*For any* NPC, initiating interaction should return a non-empty list of dialogue choice options.
**Validates: Requirements 3.2**

### Property 8: Dialogue choice advances conversation state
*For any* valid dialogue choice selection, the conversation state should transition to a new state (or end state) and not remain unchanged.
**Validates: Requirements 3.3**

### Property 9: Conversation end clears dialogue state
*For any* conversation that reaches a terminal dialogue node, the player's active dialogue state should be cleared (set to null/none).
**Validates: Requirements 3.4**

### Property 10: Work task locations provide work options
*For any* work task position where the player is located, querying available actions should return work-related choice options.
**Validates: Requirements 4.1**

### Property 11: Completing work tasks increases credits
*For any* work task with a defined reward value, completing that task should increase the player's credit balance by exactly the reward amount.
**Validates: Requirements 4.2, 4.3**

### Property 12: Completed tasks are marked as completed
*For any* work task, after the player completes it, the task's completed flag should be set to true in the game state.
**Validates: Requirements 4.4**

### Property 13: Save and load preserves game state
*For any* valid game state, saving it and then loading it should produce an equivalent game state with the same player position, credits, NPC states, and task completion status.
**Validates: Requirements 5.1, 5.2**

### Property 14: Saved states pass validation
*For any* game state that is successfully saved, loading that save data should pass all validation checks without errors.
**Validates: Requirements 5.3**

### Property 15: Corrupted save data is rejected
*For any* save data with invalid or corrupted fields (missing required keys, invalid types, out-of-range values), the load operation should fail gracefully and return an error without corrupting the current game state.
**Validates: Requirements 5.4**

### Property 16: All interactions use choice-based responses
*For any* player interaction request (NPC dialogue, work tasks, menu actions), the response should contain a list of predefined choices and not require free text input.
**Validates: Requirements 7.1**

### Property 17: Choice selection requires only choice ID
*For any* choice selection action, the request should only require a choice identifier and should not accept or require text input from the player.
**Validates: Requirements 7.3**

### Property 18: Action requests are properly formatted
*For any* player action sent to the backend, the request should conform to the defined API schema with required fields present and correctly typed.
**Validates: Requirements 8.2**

### Property 19: Backend responses include valid game state
*For any* backend response to a game action, the response should include a complete and valid game state object that passes schema validation.
**Validates: Requirements 8.3**

### Property 20: Deterministic actions produce consistent state
*For any* sequence of player actions applied to the same initial game state, executing that sequence should always produce the same final game state (deterministic behavior).
**Validates: Requirements 8.4**

## Error Handling

### Movement Errors
- Invalid direction inputs are rejected with clear error messages
- Attempts to move into non-walkable tiles are prevented
- Out-of-bounds movements transition to desert border rather than failing

### Interaction Errors
- Interaction attempts when not adjacent to NPCs return "not in range" error
- Invalid choice IDs return "invalid choice" error with available options
- Interaction attempts with non-existent entities return "entity not found" error

### Save/Load Errors
- Save failures (disk full, permissions) return specific error codes
- Corrupted save data triggers validation errors with details
- Missing save files return "save not found" error
- Load failures preserve current game state without corruption

### API Errors
- Malformed requests return 400 Bad Request with validation details
- Server errors return 500 with generic message (no sensitive data)
- Timeout handling with retry logic for transient failures

## Testing Strategy

### Unit Testing
The game will use pytest for Python backend unit tests. Unit tests will cover:

- Individual game logic functions (movement validation, credit calculations)
- Tile map queries and boundary detection
- NPC dialogue tree traversal
- Save/load serialization edge cases (empty states, maximum values)
- API endpoint request/response formatting

### Property-Based Testing
The game will use Hypothesis for Python to implement property-based tests. Each correctness property defined above will be implemented as a property-based test:

- Each property-based test will run a minimum of 100 iterations
- Tests will use Hypothesis strategies to generate random game states, positions, and actions
- Each test will be tagged with a comment referencing the specific correctness property from this design document
- Tag format: `# Feature: desert-planet-game, Property {number}: {property_text}`

Property-based tests will focus on:
- Movement properties across random positions and directions
- Boundary behavior with random out-of-bounds positions
- Interaction logic with randomly generated NPC positions
- Save/load round-trip with randomly generated game states
- State consistency with random action sequences

### Integration Testing
- End-to-end tests simulating complete player sessions
- Frontend-backend communication tests
- Save file persistence tests with actual file I/O

### Test Organization
```
tests/
  unit/
    test_movement.py
    test_world.py
    test_npcs.py
    test_economy.py
    test_save_system.py
  property/
    test_movement_properties.py
    test_world_properties.py
    test_interaction_properties.py
    test_save_properties.py
    test_state_properties.py
  integration/
    test_game_session.py
    test_api.py
```

## Implementation Notes

### World Generation
- The game world will be defined as a 2D tile array (e.g., 50x50 tiles)
- Tiles will be loaded from a JSON configuration file
- NPC and work task positions will be defined in the world configuration

### 8-Bit Rendering
- Sprites will be 16x16 pixel images
- Color palette limited to 256 colors (8-bit)
- Tile-based rendering with viewport scrolling

### Performance Considerations
- Client-side rendering at 30 FPS
- Backend state updates should complete within 100ms
- Save operations should complete within 500ms
- World size kept small (50x50) to ensure fast rendering

### Future Extensibility
- Dialogue system designed to support branching conversations
- Economy system can be extended with items and inventory
- World manager can support multiple world maps
- Save system supports versioning for future schema changes
