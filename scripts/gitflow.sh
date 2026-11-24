#!/bin/bash

# Git Flow Helper Script
# Usage: ./scripts/gitflow.sh [command] [args]

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not a git repository"
    exit 1
fi

# Commands
case "$1" in
    feature)
        case "$2" in
            start)
                if [ -z "$3" ]; then
                    print_error "Usage: ./scripts/gitflow.sh feature start <feature-name>"
                    exit 1
                fi
                
                FEATURE_NAME="feature/$3"
                
                print_info "Starting new feature: $FEATURE_NAME"
                git checkout develop
                git pull origin develop
                git checkout -b "$FEATURE_NAME"
                
                print_success "Feature branch created: $FEATURE_NAME"
                print_info "Start coding! When done, run: ./scripts/gitflow.sh feature finish"
                ;;
                
            finish)
                CURRENT_BRANCH=$(git branch --show-current)
                
                if [[ ! $CURRENT_BRANCH == feature/* ]]; then
                    print_error "Not on a feature branch. Current: $CURRENT_BRANCH"
                    exit 1
                fi
                
                print_info "Finishing feature: $CURRENT_BRANCH"
                git push origin "$CURRENT_BRANCH"
                
                print_success "Feature branch pushed to remote"
                echo ""
                print_info "Next steps:"
                echo "  1. Go to: https://github.com/1AdrianM/job-fit-ai/compare/develop...$CURRENT_BRANCH"
                echo "  2. Click 'Create Pull Request'"
                echo "  3. Fill in PR details"
                echo "  4. Wait for CI tests to pass"
                echo "  5. Merge PR"
                echo "  6. Delete branch after merge"
                ;;
                
            *)
                print_error "Unknown feature command: $2"
                echo "Usage:"
                echo "  ./scripts/gitflow.sh feature start <name>"
                echo "  ./scripts/gitflow.sh feature finish"
                exit 1
                ;;
        esac
        ;;
        
    release)
        case "$2" in
            start)
                if [ -z "$3" ]; then
                    print_error "Usage: ./scripts/gitflow.sh release start <version>"
                    exit 1
                fi
                
                VERSION="$3"
                RELEASE_BRANCH="release/v$VERSION"
                
                print_info "Starting release: $RELEASE_BRANCH"
                git checkout develop
                git pull origin develop
                git checkout -b "$RELEASE_BRANCH"
                
                print_success "Release branch created: $RELEASE_BRANCH"
                print_info "Update version numbers, changelog, etc."
                print_info "When ready, push and create PRs to main and develop"
                ;;
                
            finish)
                CURRENT_BRANCH=$(git branch --show-current)
                
                if [[ ! $CURRENT_BRANCH == release/* ]]; then
                    print_error "Not on a release branch. Current: $CURRENT_BRANCH"
                    exit 1
                fi
                
                print_info "Finishing release: $CURRENT_BRANCH"
                git push origin "$CURRENT_BRANCH"
                
                print_success "Release branch pushed"
                echo ""
                print_warning "IMPORTANT: Create TWO Pull Requests:"
                echo "  PR 1: $CURRENT_BRANCH → main (production)"
                echo "        https://github.com/1AdrianM/job-fit-ai/compare/main...$CURRENT_BRANCH"
                echo ""
                echo "  PR 2: $CURRENT_BRANCH → develop (merge back)"
                echo "        https://github.com/1AdrianM/job-fit-ai/compare/develop...$CURRENT_BRANCH"
                ;;
                
            *)
                print_error "Unknown release command: $2"
                echo "Usage:"
                echo "  ./scripts/gitflow.sh release start <version>"
                echo "  ./scripts/gitflow.sh release finish"
                exit 1
                ;;
        esac
        ;;
        
    hotfix)
        case "$2" in
            start)
                if [ -z "$3" ]; then
                    print_error "Usage: ./scripts/gitflow.sh hotfix start <bug-name>"
                    exit 1
                fi
                
                HOTFIX_NAME="hotfix/$3"
                
                print_info "Starting hotfix: $HOTFIX_NAME"
                git checkout main
                git pull origin main
                git checkout -b "$HOTFIX_NAME"
                
                print_success "Hotfix branch created: $HOTFIX_NAME"
                print_warning "Fix the critical bug ASAP!"
                ;;
                
            finish)
                CURRENT_BRANCH=$(git branch --show-current)
                
                if [[ ! $CURRENT_BRANCH == hotfix/* ]]; then
                    print_error "Not on a hotfix branch. Current: $CURRENT_BRANCH"
                    exit 1
                fi
                
                print_info "Finishing hotfix: $CURRENT_BRANCH"
                git push origin "$CURRENT_BRANCH"
                
                print_success "Hotfix branch pushed"
                echo ""
                print_warning "URGENT: Create TWO Pull Requests:"
                echo "  PR 1: $CURRENT_BRANCH → main (immediate production fix)"
                echo "        https://github.com/1AdrianM/job-fit-ai/compare/main...$CURRENT_BRANCH"
                echo ""
                echo "  PR 2: $CURRENT_BRANCH → develop (keep in sync)"
                echo "        https://github.com/1AdrianM/job-fit-ai/compare/develop...$CURRENT_BRANCH"
                ;;
                
            *)
                print_error "Unknown hotfix command: $2"
                echo "Usage:"
                echo "  ./scripts/gitflow.sh hotfix start <name>"
                echo "  ./scripts/gitflow.sh hotfix finish"
                exit 1
                ;;
        esac
        ;;
        
    sync)
        print_info "Syncing all branches..."
        
        git fetch origin
        
        print_info "Updating main..."
        git checkout main
        git pull origin main
        
        print_info "Updating develop..."
        git checkout develop
        git pull origin develop
        
        print_success "All branches synced!"
        ;;
        
    status)
        print_info "Git Flow Status"
        echo ""
        
        CURRENT=$(git branch --show-current)
        print_info "Current branch: $CURRENT"
        echo ""
        
        print_info "Feature branches:"
        git branch | grep "feature/" || echo "  (none)"
        echo ""
        
        print_info "Release branches:"
        git branch | grep "release/" || echo "  (none)"
        echo ""
        
        print_info "Hotfix branches:"
        git branch | grep "hotfix/" || echo "  (none)"
        ;;
        
    *)
        echo "Git Flow Helper Script"
        echo ""
        echo "Usage: ./scripts/gitflow.sh [command] [args]"
        echo ""
        echo "Commands:"
        echo "  feature start <name>   - Start a new feature"
        echo "  feature finish         - Finish current feature (push & show PR link)"
        echo ""
        echo "  release start <ver>    - Start a release (e.g., 1.0.0)"
        echo "  release finish         - Finish current release"
        echo ""
        echo "  hotfix start <name>    - Start a hotfix"
        echo "  hotfix finish          - Finish current hotfix"
        echo ""
        echo "  sync                   - Sync all branches with remote"
        echo "  status                 - Show current Git Flow status"
        echo ""
        echo "Examples:"
        echo "  ./scripts/gitflow.sh feature start cv-upload"
        echo "  ./scripts/gitflow.sh release start 1.0.0"
        echo "  ./scripts/gitflow.sh hotfix start api-timeout"
        exit 1
        ;;
esac
