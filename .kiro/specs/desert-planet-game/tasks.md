# Implementation Plan

- [ ] 1. Set up project structure and dependencies
  - Create Python backend directory structure with Flask/FastAPI
  - Create frontend directory with HTML/CSS/JS files
  - Set up pytest and Hypothesis for testing
  - Create requirements.txt with dependencies
  - _Requirements: 8.1_

- [ ] 2. Implement core data models and validation
  - [ ] 2.1 Create GameState, Player, World, NPC, and WorkTask data classes
    - Define Python dataclasses or Pydantic models for all game entities
    - Implement JSON serialization methods
    - _Requirements: 5.1, 5.2_
  
  - [ ]* 2.2 Write property test for save/load round-trip
    - **Property 13: Save and load preserves game state**
    - **Validates: Requirements 5.1, 5.2**
  
  - [ ]* 2.3 Write property test for save validation
    - **Property 14: Saved states pass validation**
    - **Validates: Requirements 5.3**
  
  - [ ]* 2.4 Write property test for corrupted save rejection
    - **Property 15: Corrupted save data is rejected**
    - **Validates: Requirements 5.4**

- [ ] 3. Implement world management system
  - [ ] 3.1 Create tile map data structure and world configuration loader
    - Implement 2D tile array with tile type definitions
    - Load world configuration from JSON file
    - Define desert border logic for out-of-bounds positions
    - _Requirements: 1.5, 2.1, 2.2, 9.1, 9.2_
  
  - [ ]* 3.2 Write property test for in-bounds terrain
    - **Property 2: In-bounds positions return world terrain**
    - **Validates: Requirements 1.5**
  
  - [ ]* 3.3 Write property test for out-of-bounds desert
    - **Property 3: Out-of-bounds positions return desert terrain**
    - **Validates: Requirements 2.1**
  
  - [ ]* 3.4 Write property test for desert border emptiness
    - **Property 4: Desert border has no interactive elements**
    - **Validates: Requirements 2.2**
  
  - [ ]* 3.5 Write property test for border transition
    - **Property 5: Border transition preserves world terrain**
    - **Validates: Requirements 2.3**

- [ ] 4. Implement player movement system
  - [ ] 4.1 Create movement logic with direction handling
    - Implement move function that updates player x, y coordinates
    - Add boundary checking and desert border transitions
    - Validate movement against walkable tiles
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.3_
  
  - [ ]* 4.2 Write property test for movement direction correctness
    - **Property 1: Movement updates position correctly**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**

- [ ] 5. Implement NPC interaction system
  - [ ] 5.1 Create NPC data structures and dialogue tree system
    - Define NPC class with position and dialogue state
    - Implement dialogue tree with nodes and choices
    - Create dialogue traversal logic
    - _Requirements: 3.2, 3.3, 3.4, 9.3_
  
  - [ ] 5.2 Implement interaction detection and dialogue flow
    - Create adjacency checking function (Manhattan distance)
    - Implement interaction initiation logic
    - Add conversation state management
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ]* 5.3 Write property test for adjacency detection
    - **Property 6: Adjacent positions trigger interaction availability**
    - **Validates: Requirements 3.1**
  
  - [ ]* 5.4 Write property test for dialogue choice availability
    - **Property 7: NPC interaction returns dialogue choices**
    - **Validates: Requirements 3.2**
  
  - [ ]* 5.5 Write property test for dialogue state transitions
    - **Property 8: Dialogue choice advances conversation state**
    - **Validates: Requirements 3.3**
  
  - [ ]* 5.6 Write property test for conversation end cleanup
    - **Property 9: Conversation end clears dialogue state**
    - **Validates: Requirements 3.4**

- [ ] 6. Implement economy and work task system
  - [ ] 6.1 Create work task definitions and credit management
    - Define WorkTask class with position, reward, and completion status
    - Implement credit balance tracking
    - Create task completion logic
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [ ]* 6.2 Write property test for work task options
    - **Property 10: Work task locations provide work options**
    - **Validates: Requirements 4.1**
  
  - [ ]* 6.3 Write property test for credit rewards
    - **Property 11: Completing work tasks increases credits**
    - **Validates: Requirements 4.2, 4.3**
  
  - [ ]* 6.4 Write property test for task completion marking
    - **Property 12: Completed tasks are marked as completed**
    - **Validates: Requirements 4.4**

- [ ] 7. Implement save system
  - [ ] 7.1 Create save and load functions with file I/O
    - Implement JSON serialization of game state
    - Write save file to disk with error handling
    - Load save file with validation
    - Handle corrupted data gracefully
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 8. Implement game engine and state management
  - [ ] 8.1 Create main game engine class that coordinates all systems
    - Integrate movement, world, NPC, and economy systems
    - Implement game state update logic
    - Add action processing pipeline
    - _Requirements: 8.2, 8.3, 8.4_
  
  - [ ]* 8.2 Write property test for choice-based interactions
    - **Property 16: All interactions use choice-based responses**
    - **Validates: Requirements 7.1**
  
  - [ ]* 8.3 Write property test for choice ID requirements
    - **Property 17: Choice selection requires only choice ID**
    - **Validates: Requirements 7.3**
  
  - [ ]* 8.4 Write property test for deterministic state updates
    - **Property 20: Deterministic actions produce consistent state**
    - **Validates: Requirements 8.4**

- [ ] 9. Implement backend API endpoints
  - [ ] 9.1 Create Flask/FastAPI application with REST endpoints
    - Implement POST /api/game/new endpoint
    - Implement POST /api/game/load endpoint
    - Implement POST /api/game/save endpoint
    - Implement POST /api/player/move endpoint
    - Implement POST /api/player/interact endpoint
    - Implement POST /api/player/choose endpoint
    - Add request validation and error handling
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [ ]* 9.2 Write property test for API request formatting
    - **Property 18: Action requests are properly formatted**
    - **Validates: Requirements 8.2**
  
  - [ ]* 9.3 Write property test for API response validity
    - **Property 19: Backend responses include valid game state**
    - **Validates: Requirements 8.3**

- [ ] 10. Checkpoint - Ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Create frontend HTML structure and styling
  - [ ] 11.1 Build HTML page with canvas and UI elements
    - Create index.html with canvas element
    - Add UI containers for credit display and prompts
    - Style with 8-bit aesthetic CSS
    - _Requirements: 6.1, 6.2, 7.2_

- [ ] 12. Implement frontend canvas renderer
  - [ ] 12.1 Create tile-based rendering system
    - Implement canvas drawing functions for tiles
    - Create sprite loading and rendering
    - Add viewport scrolling to center player
    - Implement 8-bit color palette constraints
    - _Requirements: 6.1, 6.2, 6.3, 9.1, 9.2, 9.3_

- [ ] 13. Implement frontend input handling
  - [ ] 13.1 Create keyboard event handlers for cursor keys
    - Capture arrow key events
    - Send movement requests to backend API
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [ ] 13.2 Create multiple choice prompt UI and selection handling
    - Display choice prompts with keyboard/mouse selection
    - Send choice selections to backend API
    - _Requirements: 3.2, 4.1, 7.1, 7.2, 7.3_

- [ ] 14. Implement frontend API client
  - [ ] 14.1 Create API communication layer
    - Implement fetch calls to all backend endpoints
    - Handle API responses and update game state
    - Add error handling for network failures
    - _Requirements: 8.1, 8.2, 8.3_

- [ ] 15. Implement frontend UI manager
  - [ ] 15.1 Create UI update logic for game state changes
    - Display credit balance
    - Show interaction indicators near NPCs
    - Render multiple choice prompts
    - Add save/load menu interface
    - _Requirements: 3.1, 4.3, 5.1, 5.2_

- [ ] 16. Create game content and assets
  - [ ] 16.1 Design and create sprite assets
    - Create player character sprite (16x16 pixels)
    - Create NPC sprites with sci-fi designs
    - Create tile sprites (ground, desert, structures)
    - _Requirements: 6.1, 9.1, 9.2, 9.3_
  
  - [ ] 16.2 Create world configuration and dialogue content
    - Define world tile map in JSON
    - Write NPC dialogue trees
    - Define work task locations and rewards
    - _Requirements: 3.2, 4.1, 9.1, 9.2_

- [ ] 17. Integrate frontend and backend
  - [ ] 17.1 Connect all frontend components to backend API
    - Wire up movement to API calls
    - Connect interaction system to backend
    - Integrate save/load functionality
    - Test complete game flow
    - _Requirements: 8.1, 8.4_

- [ ] 18. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
