#!/bin/bash

# Development Loop Helper
# Quick commands for common development tasks

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

case "$1" in
    start)
        print_info "Starting development server..."
        source venv/bin/activate
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
        
    test)
        print_info "Running all tests..."
        npm test
        ;;
        
    test-ui)
        print_info "Opening Playwright UI..."
        npx playwright test --ui
        ;;
        
    lint)
        print_info "Running linter..."
        source venv/bin/activate
        ruff check app/
        ;;
        
    fix)
        print_info "Auto-fixing code issues..."
        source venv/bin/activate
        ruff check app/ --fix
        ruff format app/
        print_success "Code fixed and formatted!"
        ;;
        
    quality)
        print_info "Running complete quality check..."
        source venv/bin/activate
        
        echo "1. Linting..."
        ruff check app/
        
        echo "2. Formatting..."
        ruff format app/ --check
        
        echo "3. Tests..."
        npm test
        
        print_success "All quality checks passed!"
        ;;
        
    deploy-check)
        print_info "Checking if ready to deploy..."
        
        # Check if on develop or feature branch
        BRANCH=$(git branch --show-current)
        if [[ $BRANCH == "main" ]]; then
            print_warning "You're on main branch!"
            exit 1
        fi
        
        # Check for uncommitted changes
        if [[ -n $(git status -s) ]]; then
            print_warning "You have uncommitted changes!"
            git status -s
            exit 1
        fi
        
        # Run quality checks
        source venv/bin/activate
        ruff check app/ && ruff format app/ --check
        
        # Run tests
        npm test
        
        print_success "Ready to deploy!"
        ;;
        
    prod-verify)
        print_info "Verifying production deployment..."
        
        echo "Checking health endpoint..."
        curl -s https://job-fit-ai-1.onrender.com/health | jq
        
        echo ""
        echo "Production URL: https://job-fit-ai-1.onrender.com/"
        
        print_success "Production is healthy!"
        ;;
        
    sync)
        print_info "Syncing branches..."
        
        git fetch origin
        
        CURRENT=$(git branch --show-current)
        
        git checkout develop
        git pull origin develop
        
        git checkout main
        git pull origin main
        
        git checkout $CURRENT
        
        print_success "All branches synced!"
        ;;
        
    status)
        print_info "Development status:"
        echo ""
        
        echo "📂 Current branch:"
        git branch --show-current
        echo ""
        
        echo "📝 Uncommitted changes:"
        git status -s || echo "  (none)"
        echo ""
        
        echo "🌿 Local branches:"
        git branch
        echo ""
        
        echo "🔄 Remote status:"
        git fetch origin --dry-run
        echo ""
        
        echo "🌐 Production:"
        curl -s https://job-fit-ai-1.onrender.com/health | jq
        ;;
        
    *)
        echo "Development Loop Helper"
        echo ""
        echo "Usage: ./scripts/dev.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start          - Start local development server"
        echo "  test           - Run all Playwright tests"
        echo "  test-ui        - Run tests with Playwright UI"
        echo "  lint           - Run linter (ruff check)"
        echo "  fix            - Auto-fix linting and formatting"
        echo "  quality        - Run complete quality check (lint + format + test)"
        echo "  deploy-check   - Check if code is ready to deploy"
        echo "  prod-verify    - Verify production deployment"
        echo "  sync           - Sync all branches with remote"
        echo "  status         - Show current development status"
        echo ""
        echo "Examples:"
        echo "  ./scripts/dev.sh start       # Start dev server"
        echo "  ./scripts/dev.sh fix         # Fix all issues"
        echo "  ./scripts/dev.sh quality     # Run all checks"
        echo "  ./scripts/dev.sh prod-verify # Check production"
        exit 1
        ;;
esac
