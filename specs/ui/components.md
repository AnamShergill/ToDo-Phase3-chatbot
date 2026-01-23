# UI Components Specification

## Overview

The Todo application UI consists of reusable components designed to create a cohesive, accessible, and responsive user experience. All components follow modern design principles and are built with accessibility in mind.

## Component Categories

### Authentication Components

#### LoginForm
- **Purpose**: Handles user login functionality
- **Props**:
  - `onLogin`: Function called when login is successful
  - `onForgotPassword`: Function called when user clicks forgot password
- **Features**:
  - Email and password input fields
  - Form validation for email format and password length
  - Loading state during authentication
  - Error display for authentication failures
  - "Remember me" checkbox option
- **Accessibility**: Proper labels, ARIA attributes, keyboard navigation
- **Responsiveness**: Adapts to mobile and desktop layouts

#### RegisterForm
- **Purpose**: Handles new user registration
- **Props**:
  - `onRegister`: Function called when registration is successful
- **Features**:
  - Email, password, and name input fields
  - Password strength validation
  - Form validation for all required fields
  - Loading state during registration
  - Error display for registration failures
- **Accessibility**: Proper labels, ARIA attributes, keyboard navigation
- **Responsiveness**: Adapts to mobile and desktop layouts

### Task Management Components

#### TaskCard
- **Purpose**: Displays individual task information and actions
- **Props**:
  - `task`: Task object with all relevant properties
  - `onCompleteToggle`: Function to handle completion status toggle
  - `onEdit`: Function to initiate task editing
  - `onDelete`: Function to handle task deletion
- **Features**:
  - Title display with strikethrough when completed
  - Description preview (truncated if too long)
  - Priority indicator with color coding
  - Due date display with overdue highlighting
  - Completion checkbox
  - Action buttons (edit, delete)
- **Accessibility**: Keyboard navigable, proper ARIA labels
- **States**: Normal, completed, overdue, editing

#### TaskForm
- **Purpose**: Creates or updates task information
- **Props**:
  - `task`: Existing task object for editing (optional)
  - `onSubmit`: Function called when form is submitted
  - `onCancel`: Function called when form is cancelled
- **Features**:
  - Title input field (required)
  - Description textarea (optional)
  - Priority selection dropdown
  - Due date picker
  - Submit and cancel buttons
  - Form validation for required fields
- **Accessibility**: Proper labels, ARIA attributes, keyboard navigation
- **States**: Create mode, edit mode

#### TaskFilterBar
- **Purpose**: Provides filtering and sorting options for task lists
- **Props**:
  - `filters`: Current filter state
  - `onFilterChange`: Function to update filters
- **Features**:
  - Status filter (all, completed, pending)
  - Priority filter (all, low, medium, high)
  - Sort options (due date, priority, creation date)
  - Search input for task titles
- **Accessibility**: Proper labels, keyboard navigation
- **Responsiveness**: Collapses to compact view on mobile

#### TaskList
- **Purpose**: Displays multiple tasks with pagination
- **Props**:
  - `tasks`: Array of task objects to display
  - `onTaskAction`: Function to handle task-specific actions
  - `pagination`: Pagination information
  - `onPageChange`: Function to handle page changes
- **Features**:
  - Renders multiple TaskCard components
  - Pagination controls
  - Empty state display
  - Loading state during data fetch
- **Accessibility**: Proper list semantics, keyboard navigation
- **States**: Loading, empty, populated

### Navigation Components

#### Header
- **Purpose**: Main application header with navigation and user controls
- **Props**:
  - `user`: User object for display
  - `onLogout`: Function to handle user logout
- **Features**:
  - Logo and brand display
  - Navigation links
  - User profile dropdown
  - Logout button
  - Mobile menu toggle
- **Accessibility**: Proper landmark roles, keyboard navigation
- **Responsiveness**: Desktop navigation vs mobile hamburger menu

#### Sidebar
- **Purpose**: Secondary navigation and quick actions
- **Props**:
  - `activePage`: Current active page for highlighting
  - `onNavigate`: Function to handle navigation
- **Features**:
  - Navigation links
  - Active state indication
  - Quick action buttons
  - Collapsible on mobile
- **Accessibility**: Proper navigation landmarks
- **Responsiveness**: Collapses to icons only on smaller screens

### Utility Components

#### Button
- **Purpose**: Reusable button component with consistent styling
- **Props**:
  - `variant`: Style variant (primary, secondary, danger, etc.)
  - `size`: Size variant (small, medium, large)
  - `disabled`: Whether button is disabled
  - `loading`: Whether button is in loading state
  - `onClick`: Click handler function
- **Features**:
  - Multiple style variants
  - Loading state with spinner
  - Disabled state styling
  - Consistent padding and typography
- **Accessibility**: Proper button semantics, keyboard activation

#### InputField
- **Purpose**: Reusable input field with consistent styling
- **Props**:
  - `label`: Label text
  - `type`: Input type (text, password, email, etc.)
  - `placeholder`: Placeholder text
  - `value`: Current value
  - `onChange`: Change handler
  - `error`: Error message to display
  - `required`: Whether field is required
- **Features**:
  - Associated label with proper htmlFor
  - Error message display
  - Required field indicator
  - Consistent styling
- **Accessibility**: Proper label association, ARIA attributes

#### Modal
- **Purpose**: Overlay component for dialogs and popups
- **Props**:
  - `isOpen`: Whether modal is open
  - `onClose`: Function to close modal
  - `title`: Modal title
  - `children`: Content to display in modal
- **Features**:
  - Overlay backdrop
  - Close button
  - Click outside to close
  - Keyboard ESC to close
  - Focus trap for accessibility
- **Accessibility**: Proper ARIA roles, focus management

## Design System

### Color Palette
- **Primary**: #3B82F6 (Blue for primary actions)
- **Secondary**: #6B7280 (Gray for secondary elements)
- **Success**: #10B981 (Green for positive actions)
- **Danger**: #EF4444 (Red for destructive actions)
- **Warning**: #F59E0B (Yellow for warnings)
- **Background**: #FFFFFF (White background)
- **Surface**: #F9FAFB (Light gray for surfaces)
- **Text Primary**: #1F2937 (Dark gray for primary text)
- **Text Secondary**: #6B7280 (Medium gray for secondary text)

### Typography
- **Font Family**: Tailwind's default sans-serif stack
- **Heading 1**: 2rem, bold, leading-tight
- **Heading 2**: 1.5rem, bold, leading-snug
- **Heading 3**: 1.25rem, bold, leading-normal
- **Body**: 1rem, normal, leading-normal
- **Small**: 0.875rem, normal, leading-normal

### Spacing
- **Base Unit**: 0.25rem (4px)
- **Scale**: Multiples of base unit (1, 2, 3, 4, 5, 6, 8, 10, 12, 16)

### Component States
- **Default**: Standard appearance
- **Hover**: Subtle color/opacity change
- **Active**: Pressed/down state
- **Focus**: Visible focus ring for keyboard navigation
- **Disabled**: Reduced opacity, no interaction
- **Loading**: Spinner indicator with disabled state

## Cross-Spec References

- Authentication flows are detailed in @specs/features/authentication.md
- Task CRUD operations are specified in @specs/features/task-crud.md
- UI pages are outlined in @specs/ui/pages.md