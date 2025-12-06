---
id: 002
title: Implementation Plan for Physical AI & Humanoid Robotics Textbook
stage: plan
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: physical-ai-robotics-textbook
branch: 001-physical-ai-robotics-textbook
user: User
command: /sp.plan
labels: ["plan","architecture"]
links:
  spec: specs/001-physical-ai-robotics-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-robotics-textbook/plan.md
tests:

---

## Prompt

FRONTEND ARCHITECTURE:

Docusaurus Configuration:
- Use Docusaurus v3 with TypeScript
- Custom theme with chatbot integration
- Sidebar organized by modules and weeks
- Search plugin enabled
- Dark mode support

File Structure:
```   docs/
├── intro.md
├── weeks-1-2-physical-ai/
│   ├── introduction.md
│   ├── embodied-intelligence.md
│   └── sensor-systems.md
├── module-01-ros2/
│   ├── _category_.json
│   ├── architecture.md
│   ├── nodes-topics.md
│   ├── python-rclpy.md
│   └── urdf-basics.md
├── module-02-digital-twin/
├── module-03-nvidia-isaac/
├── module-04-vla/
├── capstone/
└── hardware/
``` Custom React Components:
1. ChatBot component (src/components/ChatBot/)
   - Floating button bottom-right
   - Expandable chat window
   - Text selection listener for contextual Q&A
   - Message history
2. PersonalizeButton component
   - Fetches user background from API
   - Toggles content sections based on skill level

3. TranslateButton component
   - Calls translation API
   - Caches translations

4. AuthProvider wrapper
   - Better Auth React SDK integration
   - User session management
BACKEND ARCHITECTURE:

FastAPI Application (backend/main.py):
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # Routes:
# POST /api/chat - RAG chatbot endpoint
# POST /api/chat/selection - Text selection Q&A
# POST /api/auth/signup - User registration
# POST /api/auth/signin - User login
# GET /api/user/profile - Get user background
# POST /api/personalize - Get personalized content
# POST /api/translate - Translate to Urdu
```  RAG Engine (backend/rag_engine.py):
- Load all Docusaurus markdown files
- Split into chunks (500 tokens, 50 overlap)
- Generate embeddings using OpenAI text-embedding-3-small
- Store in Qdrant Cloud collection
- Query with user questions
- Return top 5 relevant chunks
- Feed to OpenAI Agents SDK for response   Database Schema (Neon Postgres):
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    name VARCHAR,
    software_level VARCHAR,
    hardware_level VARCHAR,
    languages TEXT[],
    robotics_experience VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    message TEXT,
    response TEXT,
    context TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    personalization_enabled BOOLEAN DEFAULT false,
    preferred_language VARCHAR DEFAULT 'en'
);
``` Qdrant Setup:
- Collection name: "physical-ai-textbook"
- Vector size: 1536 (OpenAI embedding dimension)
- Distance metric: Cosine
- Payload includes: {text, source_file, module, week}

DEPLOYMENT:

Frontend (GitHub Pages):
- Build: npm run build
- Deploy: gh-pages branch
- Custom domain support Backend (Railway/Vercel):
- Environment variables for API keys
- Auto-scaling enabled
- CORS configured for frontend domain

INTEGRATION POINTS:

1. Docusaurus ↔ ChatBot:
   - ChatBot component injected in theme layout
   - API calls to FastAPI backend
2. Better Auth Integration:
   - Auth endpoints in FastAPI
   - React context for user session
   - Protected routes for personalization

3. Content Personalization:
   - Dynamic imports based on user level
   - CSS classes to show/hide sections
4. Translation:
   - API call to translation service
   - LocalStorage caching
   - Preserve markdown formatting
```

### 6. **What Happens Next**
After you run these three commands, Claude Code will:
1. ✅ Set up the complete file structure
2. ✅ Generate all the markdown content for the book
3. ✅ Create React components (ChatBot, Auth, etc.)
4. ✅ Build the FastAPI backend
5. ✅ Set up database schemas
6. ✅ Configure Qdrant and embeddings
7. ✅ Wire everything together

### 7. **Then Run Implementation**

## Response snapshot

Successfully generated the implementation plan for the Physical AI & Humanoid Robotics Textbook. The plan covers frontend and backend architecture, database schemas, Qdrant setup, deployment strategies, and integration points. All constitution checks passed, and the project structure is defined.

## Outcome

- ✅ Impact: Implementation plan generated and saved.
- 🧪 Tests: N/A
- 📁 Files: specs/001-physical-ai-robotics-textbook/plan.md updated.
- 🔁 Next prompts: Proceed with implementation based on this plan, or further refine with `/sp.tasks`.
- 🧠 Reflection: The plan successfully integrates user requirements with technical architecture and adheres to constitutional principles. The temporary file approach resolved the previous write conflicts.

## Evaluation notes (flywheel)

- Failure modes observed: Repeated `Edit` tool failure due to external file modification, resolved by temporary file strategy.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
