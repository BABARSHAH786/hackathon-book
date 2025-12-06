# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/001-physical-ai-robotics-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/` (adjusting from plan.md structure)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Configure Docusaurus structure in `docusaurus.config.ts`
- [ ] T002 Set up custom Docusaurus theme with chatbot integration in `src/theme/`
- [ ] T003 Create sidebar navigation structure in `sidebars.ts`
- [ ] T004 Initialize FastAPI project structure in `backend/`
- [ ] T005 Set up CORS middleware in `backend/main.py`
- [ ] T006 Configure TypeScript for frontend development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Set up Neon Postgres database schema in `backend/schemas.sql`
- [ ] T008 [P] Create database interaction utility in `backend/database.py`
- [ ] T009 [P] Set up Qdrant Cloud connection in `backend/rag_engine.py`
- [ ] T010 [P] Implement Better Auth integration utilities in `backend/auth.py`
- [ ] T011 Configure environment variables for deployment in `.env` (frontend and backend)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Core Content Consumption (Priority: P1) 🎯 MVP

**Goal**: Access comprehensive content, progressing from basics to advanced, with practical code examples and a hardware guide.

**Independent Test**: A user can navigate through all 13 weeks of content, including the introduction, modules, advanced topics, and hardware guide, and view all text and code examples.

### Implementation for User Story 1

- [ ] T012 [US1] Write Introduction chapters (Weeks 1-2) in `docs/weeks-1-2-physical-ai/`
- [ ] T013 [US1] Write Module 1 - ROS 2 content in `docs/module-01-ros2/`
- [ ] T014 [US1] Write Module 2 - Gazebo & Unity content in `docs/module-02-digital-twin/`
- [ ] T015 [US1] Write Module 3 - NVIDIA Isaac content in `docs/module-03-nvidia-isaac/`
- [ ] T016 [US1] Write Module 4 - VLA content in `docs/module-04-vla/`
- [ ] T017 [US1] Write Capstone project guide in `docs/capstone/`
- [ ] T018 [US1] Write Hardware requirements guide in `docs/hardware/`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Interactive AI Assistant (Priority: P1)

**Goal**: An embedded interactive AI assistant that can answer contextual questions about the textbook content.

**Independent Test**: A user can ask a question about a displayed chapter via the AI assistant and receive a relevant answer. The user can also highlight text and a question specifically about that highlighted text.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement RAG engine with Langchain (loading, chunking, embeddings) in `backend/rag_engine.py`
- [ ] T020 [US2] Create API endpoint `POST /api/chat` for RAG chatbot in `backend/main.py`
- [ ] T021 [US2] Create API endpoint `POST /api/chat/selection` for text selection Q&A in `backend/main.py`
- [ ] T022 [P] [US2] Build FloatingButton component for chatbot in `src/components/ChatBot/FloatingButton.tsx`
- [ ] T023 [P] [US2] Build ChatWindow component for chatbot in `src/components/ChatBot/ChatWindow.tsx`
- [ ] T024 [US2] Implement text selection listener for contextual Q&A in `src/components/ChatBot/ChatBot.tsx`
- [ ] T025 [US2] Integrate ChatBot component into Docusaurus theme layout in `src/theme/Layout.tsx` (example path)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Personalized Learning Experience (Priority: P2)

**Goal**: Personalize textbook content based on user background.

**Independent Test**: A user can select "Personalize for Me" and observe changes in content detail (e.g., more explanations for beginners, optimization tips for advanced users).

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create `preferences` table in `backend/schemas.sql`
- [ ] T027 [US3] Implement API endpoint `POST /api/personalize` to save/retrieve preferences in `backend/main.py`
- [ ] T028 [P] [US3] Build PersonalizeButton component in `src/components/PersonalizeButton/PersonalizeButton.tsx`
- [ ] T029 [US3] Implement logic to adjust content based on user background (dynamic imports, CSS classes) in Docusaurus content pages and React components.

**Checkpoint**: All user stories should now be independently functional up to this point

---

## Phase 6: User Story 4 - User Authentication and Profile Management (Priority: P2)

**Goal**: Allow users to create accounts, sign in securely, and manage their profile.

**Independent Test**: A new user can successfully sign up, log in, and view their profile with the details they provided.

### Implementation for User Story 4

- [ ] T030 [P] [US4] Create `users` table in `backend/schemas.sql`
- [ ] T031 [US4] Create API endpoint `POST /api/auth/signup` for user registration in `backend/main.py`
- [ ] T032 [US4] Create API endpoint `POST /api/auth/signin` for user login in `backend/main.py`
- [ ] T033 [US4] Create API endpoint `GET /api/user/profile` to get user background in `backend/main.py`
- [ ] T034 [P] [US4] Create AuthProvider wrapper for Better Auth React SDK integration in `src/components/AuthProvider/AuthProvider.tsx`
- [ ] T035 [US4] Implement signup and signin forms in frontend React components (`src/pages/auth/Signup.tsx`, `src/pages/auth/Signin.tsx` - example paths)
- [ ] T036 [US4] Implement user profile management in frontend React components (`src/pages/user/Profile.tsx` - example path)

**Checkpoint**: All user stories should now be independently functional up to this point

---

## Phase 7: User Story 5 - Urdu Translation (Priority: P3)

**Goal**: Read textbook content translated into Urdu, preserving English code blocks and technical accuracy.

**Independent Test**: A user can click "اردو میں پڑھیں" and see the chapter content translated into Urdu, with code blocks remaining in English.

### Implementation for User Story 5

- [ ] T037 [P] [US5] Implement API endpoint `POST /api/translate` for Urdu translation in `backend/main.py`
- [ ] T038 [P] [US5] Build TranslateButton component in `src/components/TranslateButton/TranslateButton.tsx`
- [ ] T039 [US5] Implement logic to call translation API and cache translations in frontend components.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T040 Configure Docusaurus search plugin.
- [ ] T041 Implement Docusaurus dark mode support.
- [ ] T042 Ensure mobile-responsive design for all frontend components.
- [ ] T043 Implement comprehensive error handling across frontend and backend.
- [ ] T044 Implement performance monitoring for chatbot responses.
- [ ] T045 Conduct accessibility compliance review (WCAG 2.1).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1): Core Content Consumption
  - User Story 2 (P1): Interactive AI Assistant
  - User Story 3 (P2): Personalized Learning Experience
  - User Story 4 (P2): User Authentication and Profile Management
  - User Story 5 (P3): Urdu Translation
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Integrates with User Story 1 content.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 4 for user profile.
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Integrates with User Story 1 content.

### Within Each User Story

- Frontend components may depend on backend API endpoints.
- UI elements (buttons, chat windows) before their interaction logic.
- Core implementation before integration.

### Parallel Opportunities

- All tasks marked [P] can run in parallel (different files, no dependencies).
- Once Foundational phase completes, User Stories can be worked on in parallel by different team members (respecting story dependencies).
- Within each user story, tasks marked [P] can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Core Content)
4. Complete Phase 4: User Story 2 (Interactive AI Assistant)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 4 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Content)
   - Developer B: User Story 2 (AI Assistant)
   - Developer C: User Story 4 (Authentication)
   - Developer D: User Story 3 (Personalization - depends on Auth)
   - Developer E: User Story 5 (Translation - depends on Content)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
