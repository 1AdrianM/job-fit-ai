# Contributing to Job Fit AI

Thanks for your interest in contributing! 🎉

## Development Setup

1. **Fork and clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/job-fit-ai.git
   cd job-fit-ai
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY
   ```

4. **Run tests**
   ```bash
   npm test
   ```

## Development Workflow

1. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests locally
   ```bash
   npm test
   ```

4. Commit with conventional commits
   ```bash
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: fix bug in analysis"
   ```

5. Push and open a PR
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes (formatting)
- `chore:` Build/tooling changes

## Testing

- All PRs must pass CI tests
- Add tests for new features
- Run `npm test` before pushing
- Run `npm run test:ui` for interactive testing

## Code Style

- Python: Follow PEP 8
- JavaScript: Follow Airbnb style guide
- Use descriptive variable names
- Add comments for complex logic

## Questions?

Open an issue or reach out to [@1AdrianM](https://github.com/1AdrianM)
