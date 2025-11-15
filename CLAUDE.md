# CLAUDE.md - Radio Player Project Guide

## Project Overview

**Radio Player** is a digital radio streaming application. This document serves as a comprehensive guide for AI assistants working on this codebase.

**Last Updated:** 2025-11-15
**Repository:** Radio-player
**Current State:** Initial project setup

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Technology Stack](#technology-stack)
3. [Development Workflow](#development-workflow)
4. [Code Conventions](#code-conventions)
5. [Git Workflow](#git-workflow)
6. [Testing Guidelines](#testing-guidelines)
7. [Common Tasks](#common-tasks)
8. [Architecture Overview](#architecture-overview)
9. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## Project Structure

```
Radio-player/
├── src/                    # Source code
│   ├── components/         # UI components
│   ├── services/          # Business logic & API services
│   ├── utils/             # Utility functions
│   ├── hooks/             # Custom React hooks (if React)
│   ├── stores/            # State management
│   ├── types/             # TypeScript type definitions
│   └── assets/            # Images, icons, audio files
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── public/                # Static assets
├── docs/                  # Documentation
├── scripts/               # Build and deployment scripts
├── config/                # Configuration files
└── CLAUDE.md             # This file
```

---

## Technology Stack

### Recommended Stack (to be confirmed)

**Frontend:**
- Framework: React/Vue/Svelte (TBD)
- Language: TypeScript
- Styling: CSS Modules/Tailwind/Styled Components
- State Management: Redux/Zustand/Context API

**Audio Playback:**
- HTML5 Audio API
- Web Audio API for advanced features
- HLS.js for streaming support

**Build Tools:**
- Vite/Webpack
- ESLint + Prettier
- TypeScript compiler

**Testing:**
- Jest/Vitest for unit tests
- Testing Library for component tests
- Playwright/Cypress for E2E tests

---

## Development Workflow

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd Radio-player

# Install dependencies
npm install  # or yarn/pnpm

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Branch Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature branches (e.g., `feature/playlist-ui`)
- **bugfix/**: Bug fix branches (e.g., `bugfix/audio-sync`)
- **hotfix/**: Critical production fixes
- **claude/**: AI-assisted development branches

### Development Process

1. **Create feature branch** from develop
2. **Implement changes** with tests
3. **Run linters and tests** locally
4. **Commit with clear messages**
5. **Push and create PR**
6. **Code review** and merge

---

## Code Conventions

### File Naming

- **Components**: PascalCase (e.g., `RadioPlayer.tsx`, `PlaylistItem.tsx`)
- **Utilities**: camelCase (e.g., `formatTime.ts`, `audioUtils.ts`)
- **Constants**: UPPER_SNAKE_CASE in files (e.g., `API_ENDPOINTS.ts`)
- **Tests**: Match source file with `.test` or `.spec` suffix

### Code Style

```typescript
// Use named exports for better refactoring
export const RadioPlayer = () => { ... }

// Type everything in TypeScript
interface RadioStation {
  id: string;
  name: string;
  streamUrl: string;
  genre: string;
  imageUrl?: string;
}

// Use async/await over promises
const fetchStations = async (): Promise<RadioStation[]> => {
  const response = await fetch('/api/stations');
  return response.json();
}

// Prefer const over let, never use var
const stations = await fetchStations();

// Use descriptive variable names
const currentStation = stations.find(s => s.id === activeStationId);
```

### Component Structure

```typescript
// 1. Imports
import { useState, useEffect } from 'react';
import { RadioStation } from '@/types';

// 2. Types/Interfaces
interface Props {
  station: RadioStation;
  onPlay: (id: string) => void;
}

// 3. Component
export const StationCard = ({ station, onPlay }: Props) => {
  // 4. Hooks
  const [isPlaying, setIsPlaying] = useState(false);

  // 5. Effects
  useEffect(() => {
    // ...
  }, []);

  // 6. Handlers
  const handlePlay = () => {
    onPlay(station.id);
    setIsPlaying(true);
  };

  // 7. Render
  return (
    <div className="station-card">
      {/* ... */}
    </div>
  );
};
```

### Comments

```typescript
// Use JSDoc for public APIs
/**
 * Plays a radio station from the given URL
 * @param url - The streaming URL of the radio station
 * @param options - Playback options
 * @returns Promise that resolves when playback starts
 */
export async function playStation(
  url: string,
  options?: PlaybackOptions
): Promise<void> {
  // Implementation
}

// Use inline comments sparingly, prefer self-documenting code
// Only comment the "why", not the "what"
```

---

## Git Workflow

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add playlist management feature
fix: resolve audio playback sync issue
docs: update API documentation
style: format code with prettier
refactor: simplify station loading logic
test: add unit tests for audio service
chore: update dependencies
perf: optimize station search algorithm
```

### Commit Best Practices

- One logical change per commit
- Write clear, descriptive messages
- Reference issues when applicable (e.g., `fixes #123`)
- Keep commits atomic and reversible

### Example Workflow

```bash
# Create feature branch
git checkout -b feature/station-search

# Make changes and commit
git add src/components/StationSearch.tsx
git commit -m "feat: implement station search with debouncing"

# Push to remote
git push -u origin feature/station-search

# Create pull request via GitHub
```

---

## Testing Guidelines

### Test Structure

```typescript
describe('RadioPlayer', () => {
  it('should play station when play button is clicked', async () => {
    // Arrange
    const station = createMockStation();
    const { getByRole } = render(<RadioPlayer station={station} />);

    // Act
    const playButton = getByRole('button', { name: /play/i });
    await userEvent.click(playButton);

    // Assert
    expect(audioService.play).toHaveBeenCalledWith(station.streamUrl);
  });
});
```

### Testing Priorities

1. **Critical paths**: Audio playback, station loading
2. **User interactions**: Play/pause, volume control, station selection
3. **Error handling**: Network failures, invalid URLs
4. **Edge cases**: Empty playlists, unsupported formats

### Coverage Goals

- Aim for 80%+ code coverage
- 100% coverage for critical audio services
- All user-facing features should have integration tests

---

## Common Tasks

### Adding a New Radio Station

1. Update station data source (API/JSON)
2. Verify stream URL is valid
3. Add station metadata (name, genre, image)
4. Test playback functionality
5. Update documentation if needed

### Implementing New Features

1. **Plan**: Break down feature into tasks
2. **Design**: Consider UI/UX implications
3. **Implement**: Write code with tests
4. **Test**: Manual and automated testing
5. **Document**: Update README and CLAUDE.md
6. **Review**: Get code review before merging

### Debugging Audio Issues

1. Check browser console for errors
2. Verify stream URL is accessible
3. Test with different audio formats
4. Check CORS headers for streaming URLs
5. Use browser DevTools Network tab
6. Test across different browsers

---

## Architecture Overview

### Audio Service Layer

The audio service abstracts audio playback logic:

```typescript
interface AudioService {
  play(url: string): Promise<void>;
  pause(): void;
  stop(): void;
  setVolume(level: number): void;
  getCurrentTime(): number;
  onStateChange(callback: (state: PlaybackState) => void): void;
}
```

### State Management

Recommended state structure:

```typescript
interface AppState {
  // Current playback
  currentStation: RadioStation | null;
  isPlaying: boolean;
  volume: number;

  // Station data
  stations: RadioStation[];
  favorites: string[];
  recentlyPlayed: string[];

  // UI state
  isLoading: boolean;
  error: Error | null;
}
```

### API Integration

```typescript
// services/api.ts
export const api = {
  fetchStations: () => fetch('/api/stations').then(r => r.json()),
  searchStations: (query: string) => fetch(`/api/search?q=${query}`).then(r => r.json()),
  getStation: (id: string) => fetch(`/api/stations/${id}`).then(r => r.json()),
};
```

---

## AI Assistant Guidelines

### When Working on This Project

1. **Always Read First**
   - Check existing files before creating new ones
   - Understand current architecture before making changes
   - Review recent commits to understand context

2. **Follow Conventions**
   - Match existing code style and patterns
   - Use established file naming conventions
   - Maintain consistency with current architecture

3. **Be Security-Conscious**
   - Validate all external URLs before playback
   - Sanitize user inputs
   - Be cautious with eval() or innerHTML
   - Implement CSP headers for production

4. **Test Everything**
   - Write tests for new features
   - Run existing tests before committing
   - Test across different browsers
   - Verify audio playback on different devices

5. **Document Changes**
   - Update README.md for user-facing changes
   - Update this CLAUDE.md for architectural changes
   - Add JSDoc comments for public APIs
   - Include migration notes for breaking changes

6. **Git Best Practices**
   - Create feature branches from develop
   - Write meaningful commit messages
   - Keep commits focused and atomic
   - Push to claude/* branches for AI-assisted work

7. **Performance Considerations**
   - Optimize audio buffer management
   - Lazy load station lists
   - Debounce search inputs
   - Use memoization where appropriate
   - Minimize re-renders

8. **Accessibility**
   - Provide keyboard controls for playback
   - Add ARIA labels to controls
   - Ensure sufficient color contrast
   - Support screen readers
   - Test with keyboard-only navigation

9. **Error Handling**
   - Always handle network failures gracefully
   - Provide user-friendly error messages
   - Log errors for debugging
   - Implement retry logic for transient failures
   - Never let the app crash

10. **Communication**
    - Ask clarifying questions when requirements are unclear
    - Explain trade-offs when making architectural decisions
    - Suggest improvements when you see opportunities
    - Keep the user informed of progress

### Common Pitfalls to Avoid

- ❌ Don't commit sensitive data (API keys, credentials)
- ❌ Don't ignore TypeScript errors
- ❌ Don't skip writing tests
- ❌ Don't create unnecessary files
- ❌ Don't use deprecated APIs
- ❌ Don't hardcode URLs or configuration
- ❌ Don't ignore browser compatibility
- ❌ Don't bypass CORS with insecure methods

### Recommended Tools & Libraries

**Audio:**
- `howler.js` - Cross-browser audio library
- `hls.js` - HLS streaming support
- `wavesurfer.js` - Audio visualization

**HTTP:**
- `axios` - Promise-based HTTP client
- `react-query` or `swr` - Data fetching & caching

**UI:**
- `radix-ui` - Accessible component primitives
- `framer-motion` - Animations
- `react-icons` - Icon library

**Utilities:**
- `date-fns` - Date manipulation
- `lodash-es` - Utility functions
- `zod` - Runtime type validation

---

## Quick Reference

### File Locations

- **Main app entry**: `src/main.tsx` or `src/index.tsx`
- **Types**: `src/types/index.ts`
- **API service**: `src/services/api.ts`
- **Audio service**: `src/services/audio.ts`
- **Configuration**: `config/` or root level
- **Tests**: Co-located with source or in `tests/`

### Important Commands

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run all tests
npm run test:watch   # Run tests in watch mode
npm run lint         # Run ESLint
npm run lint:fix     # Fix linting issues
npm run type-check   # Run TypeScript compiler check
npm run format       # Format code with Prettier
```

### Environment Variables

```bash
VITE_API_BASE_URL=    # API endpoint
VITE_STREAM_TIMEOUT=  # Stream timeout in ms
VITE_MAX_VOLUME=      # Maximum volume level
```

---

## Resources

### Documentation
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [HTML Audio Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio)
- [HLS Specification](https://datatracker.ietf.org/doc/html/rfc8216)

### Inspiration
- Radio Garden - https://radio.garden
- TuneIn Radio - https://tunein.com
- Radio Paradise - https://radioparadise.com

---

## Contributing

When adding new features or making significant changes:

1. Update this CLAUDE.md file
2. Document in README.md if user-facing
3. Add or update tests
4. Update TypeScript types
5. Consider backward compatibility

---

## Change Log

### 2025-11-15
- Initial CLAUDE.md creation
- Established project structure guidelines
- Defined code conventions and workflows

---

**For AI Assistants**: This document should be your first reference when working on this project. When in doubt, ask the user for clarification. Always prioritize code quality, security, and user experience.
