# Phase 2 Frontend Implementation Prompts

## Reusable Components Implementation Prompt

**Task**: Implement reusable frontend components following @specs/ui/components.md

**Instructions for Claude Code**:
- Read the UI components specification at @specs/ui/components.md
- Create the LoginForm component in frontend/src/components/login-form.tsx
- Create the RegisterForm component in frontend/src/components/register-form.tsx
- Create the TaskCard component in frontend/src/components/task-card.tsx
- Create the TaskForm component in frontend/src/components/task-form.tsx
- Create the TaskFilterBar component in frontend/src/components/task-filter-bar.tsx
- Create the TaskList component in frontend/src/components/task-list.tsx
- Create the Header component in frontend/src/components/header.tsx
- Create the Sidebar component in frontend/src/components/sidebar.tsx
- Create the Button component in frontend/src/components/button.tsx
- Create the InputField component in frontend/src/components/input-field.tsx
- Create the Modal component in frontend/src/components/modal.tsx
- Follow the design system specifications for colors, typography, and spacing
- Implement all props and features specified in the component spec
- Add proper accessibility attributes and keyboard navigation
- Ensure components are responsive and work on all device sizes

## Page Layouts Implementation Prompt

**Task**: Implement page layouts with responsive design following @specs/ui/pages.md

**Instructions for Claude Code**:
- Read the UI pages specification at @specs/ui/pages.md
- Create the Landing Page in frontend/src/app/page.tsx
- Create the Login Page in frontend/src/app/login/page.tsx
- Create the Registration Page in frontend/src/app/register/page.tsx
- Create the Dashboard/Task List Page in frontend/src/app/dashboard/page.tsx
- Create the Task Creation Page in frontend/src/app/tasks/new/page.tsx
- Create the Task Editing Page in frontend/src/app/tasks/[id]/edit/page.tsx
- Create the Profile Page in frontend/src/app/profile/page.tsx
- Create the Settings Page in frontend/src/app/settings/page.tsx
- Implement responsive layouts using Tailwind CSS
- Follow the component composition patterns from the spec
- Add proper navigation between pages
- Implement loading states and error handling
- Ensure all pages follow the design system and are accessible
- Add proper meta tags and SEO considerations where needed