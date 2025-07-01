# Niya Sales Agent - GitHub Setup Script
# This script helps you set up and push to GitHub

Write-Host "🚀 Niya Sales Agent - GitHub Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if git is configured
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitUser -or -not $gitEmail) {
    Write-Host "⚠️  Git is not configured. Please set up your Git identity:" -ForegroundColor Yellow
    $userName = Read-Host "Enter your name"
    $userEmail = Read-Host "Enter your email"
    
    git config --global user.name $userName
    git config --global user.email $userEmail
    
    Write-Host "✅ Git configured successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Git configured: $gitUser <$gitEmail>" -ForegroundColor Green
}

# Check if we have commits
$commitCount = git rev-list --count HEAD 2>$null
if ($commitCount -eq 0) {
    Write-Host "❌ No commits found. Please run the deployment script first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found $commitCount commit(s)" -ForegroundColor Green

# Get GitHub username
Write-Host ""
Write-Host "📋 GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

Write-Host "Please follow these steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/new" -ForegroundColor White
Write-Host "2. Create a new repository named 'niya-sales-agent'" -ForegroundColor White
Write-Host "3. DO NOT initialize with README, .gitignore, or license" -ForegroundColor White
Write-Host "4. Copy the repository URL" -ForegroundColor White

$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/niya-sales-agent.git)"

if ($repoUrl -match "https://github\.com/[^/]+/[^/]+\.git") {
    Write-Host "✅ Valid GitHub URL detected" -ForegroundColor Green
    
    # Add remote origin
    Write-Host "🔗 Adding remote origin..." -ForegroundColor Yellow
    git remote add origin $repoUrl
    
    # Rename branch to main
    Write-Host "🔄 Renaming branch to main..." -ForegroundColor Yellow
    git branch -M main
    
    # Push to GitHub
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Visit your repository to verify all files are uploaded" -ForegroundColor White
        Write-Host "2. Check that README.md displays correctly" -ForegroundColor White
        Write-Host "3. Set up GitHub Actions (optional)" -ForegroundColor White
        Write-Host "4. Add collaborators if needed" -ForegroundColor White
    } else {
        Write-Host "❌ Failed to push to GitHub. Please check your credentials." -ForegroundColor Red
    }
} else {
    Write-Host "❌ Invalid GitHub URL format" -ForegroundColor Red
    Write-Host "Expected format: https://github.com/username/repository-name.git" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 