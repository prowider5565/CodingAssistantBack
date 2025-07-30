# Database Schema Overview

## Core Entities

### 1. User Management
- `User`: Core user model with authentication and profile information
- `Interests`: User interests (many-to-one relationship with User)

### 2. Testing System
- `Tests`: Container for test instances
- `Questions`: Questions within tests (with types: FreeText/MultipleChoice)
- `Answers`: Possible answers for multiple-choice questions
- `Submissions`: User test submissions with scores

### 3. Coding Tasks
- `CodingTasks`: Coding challenges with time limits
- `CodingTaskSubmissions`: User submissions for coding tasks with performance metrics

### 4. Chat System
- `ChatSession`: Chat conversation sessions
- `ChatMessages`: Individual messages within a chat session
- `GeneralMemory`: Persistent memory storage for chat context

## Enums
- `QuestionType`: FreeText, MultipleChoice
- `Author`: User, ChatBot (for message attribution)

## Relationships
- Users can have multiple interests, test submissions, coding tasks, and chat sessions
- Tests contain multiple questions
- Questions can have multiple answers (for multiple-choice)
- Chat sessions contain multiple messages
- Coding tasks can have multiple submissions
