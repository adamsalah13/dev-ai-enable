#!/usr/bin/env python3
"""
Local Git-based Link Analysis Tool for dev-ai-enable Repository
Analyzes all local and remote branches by checking them out locally
"""

import os
import re
import json
import urllib.parse
import urllib.request
from typing import Dict, List, Set, Tuple
from pathlib import Path
import subprocess
import time

class LocalGitLinkAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.branches = []
        
    def get_remote_branches(self) -> List[str]:
        """Get all remote branches"""
        try:
            # First fetch all remote branches
            subprocess.run(['git', 'fetch', '--all'], cwd=self.repo_path, capture_output=True)
            
            result = subprocess.run(
                ['git', 'ls-remote', '--heads', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            branches = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and 'refs/heads/' in line:
                    branch = line.split('refs/heads/')[-1]
                    branches.append(branch)
            
            print(f"Found remote branches: {branches}")
            return branches
            
        except Exception as e:
            print(f"Error getting remote branches: {e}")
            return []
    
    def checkout_branch(self, branch: str) -> bool:
        """Checkout a specific branch"""
        try:
            # First try to delete any existing local branch
            subprocess.run(
                ['git', 'branch', '-D', branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Checkout remote branch as new local branch
            result = subprocess.run(
                ['git', 'checkout', '-b', branch, f'origin/{branch}'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            success = result.returncode == 0
            if not success:
                print(f"Failed to checkout {branch}: {result.stderr}")
            else:
                print(f"Successfully checked out branch: {branch}")
            
            return success
            
        except Exception as e:
            print(f"Error checking out branch {branch}: {e}")
            return False
    
    def find_documentation_files(self) -> List[Path]:
        """Find all documentation files in current checkout"""
        patterns = ['*.md', '*.txt', '*.rst', '*.html', '*.json', '*.yaml', '*.yml']
        files = []
        
        for pattern in patterns:
            files.extend(self.repo_path.rglob(pattern))
        
        # Filter out .git directory and common build/dependency directories
        exclude_dirs = {'.git', 'node_modules', '.venv', '__pycache__', '.pytest_cache'}
        files = [f for f in files if not any(part in exclude_dirs for part in f.parts)]
        
        return files
    
    def extract_links(self, file_path: Path) -> List[Tuple[str, int]]:
        """Extract all links from a file with line numbers"""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Markdown links: [text](url)
            markdown_links = re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', content)
            for match in markdown_links:
                line_num = content[:match.start()].count('\n') + 1
                links.append((match.group(2), line_num))
            
            # HTML links: href="url"
            html_links = re.finditer(r'href=["\']([^"\']+)["\']', content)
            for match in html_links:
                line_num = content[:match.start()].count('\n') + 1
                links.append((match.group(1), line_num))
            
            # Direct URLs: http(s)://...
            url_pattern = re.compile(r'https?://[^\s<>"\']+')
            url_matches = re.finditer(url_pattern, content)
            for match in url_matches:
                line_num = content[:match.start()].count('\n') + 1
                url = match.group(0)
                # Clean up URL (remove trailing punctuation)
                url = re.sub(r'[.,;:!?)]+$', '', url)
                links.append((url, line_num))
                
            # Image references: ![alt](src)
            img_refs = re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', content)
            for match in img_refs:
                line_num = content[:match.start()].count('\n') + 1
                ref = match.group(1)
                if not ref.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                    links.append((ref, line_num))
            
            # File references in HTML-like tags
            file_refs = re.finditer(r'(?:src|href)=["\']([^"\']+)["\']', content)
            for match in file_refs:
                line_num = content[:match.start()].count('\n') + 1
                ref = match.group(1)
                if not ref.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                    links.append((ref, line_num))
                    
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            
        return links
    
    def is_external_link(self, url: str) -> bool:
        """Check if URL is external"""
        return url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'ftp://'))
    
    def check_internal_link(self, link: str, current_file: Path) -> bool:
        """Check if internal link exists"""
        try:
            # Remove anchor/fragment
            link = link.split('#')[0]
            if not link:  # Just an anchor
                return True
                
            # Resolve relative path
            if link.startswith('/'):
                # Absolute path from repo root
                target_path = self.repo_path / link.lstrip('/')
            else:
                # Relative path from current file
                target_path = current_file.parent / link
                
            # Normalize path
            target_path = target_path.resolve()
            
            # Check if file/directory exists
            return target_path.exists()
            
        except Exception as e:
            return False
    
    def check_external_link(self, url: str) -> bool:
        """Check if external URL is accessible (with simple timeout)"""
        try:
            # Skip some problematic URLs
            if any(domain in url.lower() for domain in ['localhost', '127.0.0.1', 'example.com']):
                return True
                
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Link-Checker/1.0')
            
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status < 400
                
        except Exception:
            return False
    
    def analyze_branch(self, branch: str) -> Dict:
        """Analyze all files in a specific branch"""
        print(f"\n{'='*50}")
        print(f"Analyzing branch: {branch}")
        print(f"{'='*50}")
        
        if not self.checkout_branch(branch):
            return {"error": f"Could not checkout branch {branch}"}
        
        branch_analysis = {
            "branch": branch,
            "files_analyzed": 0,
            "total_links": 0,
            "broken_internal": [],
            "broken_external": [],
            "valid_internal": [],
            "valid_external": [],
            "file_details": {}
        }
        
        files = self.find_documentation_files()
        branch_analysis["files_analyzed"] = len(files)
        print(f"Found {len(files)} documentation files")
        
        for file_path in files:
            relative_path = file_path.relative_to(self.repo_path)
            print(f"  Analyzing: {relative_path}")
            
            links = self.extract_links(file_path)
            file_analysis = {
                "total_links": len(links),
                "broken_internal": [],
                "broken_external": [],
                "valid_internal": [],
                "valid_external": []
            }
            
            print(f"    Found {len(links)} links")
            
            for link, line_num in links:
                branch_analysis["total_links"] += 1
                
                if self.is_external_link(link):
                    # Check external link (with rate limiting)
                    time.sleep(0.2)  # Rate limiting
                    if self.check_external_link(link):
                        file_analysis["valid_external"].append({"url": link, "line": line_num})
                        branch_analysis["valid_external"].append({
                            "file": str(relative_path),
                            "url": link,
                            "line": line_num
                        })
                    else:
                        file_analysis["broken_external"].append({"url": link, "line": line_num})
                        branch_analysis["broken_external"].append({
                            "file": str(relative_path),
                            "url": link,
                            "line": line_num
                        })
                        print(f"    BROKEN EXTERNAL: {link}")
                else:
                    # Check internal link
                    if self.check_internal_link(link, file_path):
                        file_analysis["valid_internal"].append({"url": link, "line": line_num})
                        branch_analysis["valid_internal"].append({
                            "file": str(relative_path),
                            "url": link,
                            "line": line_num
                        })
                    else:
                        file_analysis["broken_internal"].append({"url": link, "line": line_num})
                        branch_analysis["broken_internal"].append({
                            "file": str(relative_path),
                            "url": link,
                            "line": line_num
                        })
                        print(f"    BROKEN INTERNAL: {link}")
            
            branch_analysis["file_details"][str(relative_path)] = file_analysis
        
        # Summary for this branch
        broken_total = len(branch_analysis["broken_internal"]) + len(branch_analysis["broken_external"])
        print(f"\nBranch {branch} summary:")
        print(f"  - Files: {branch_analysis['files_analyzed']}")
        print(f"  - Total links: {branch_analysis['total_links']}")
        print(f"  - Broken internal: {len(branch_analysis['broken_internal'])}")
        print(f"  - Broken external: {len(branch_analysis['broken_external'])}")
        print(f"  - Status: {'❌ HAS ISSUES' if broken_total > 0 else '✅ ALL GOOD'}")
        
        return branch_analysis
    
    def analyze_all_branches(self) -> Dict:
        """Analyze all branches in the repository"""
        branches = self.get_remote_branches()
        
        if not branches:
            print("No branches found!")
            return {}
        
        print(f"Will analyze {len(branches)} branches: {branches}")
        
        full_analysis = {
            "repository": str(self.repo_path),
            "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_branches": len(branches),
            "branches": {},
            "summary": {
                "total_files": 0,
                "total_links": 0,
                "total_broken_internal": 0,
                "total_broken_external": 0,
                "branches_with_issues": []
            }
        }
        
        for branch in branches:
            try:
                analysis = self.analyze_branch(branch)
                full_analysis["branches"][branch] = analysis
                
                # Update summary
                if "error" not in analysis:
                    full_analysis["summary"]["total_files"] += analysis["files_analyzed"]
                    full_analysis["summary"]["total_links"] += analysis["total_links"]
                    full_analysis["summary"]["total_broken_internal"] += len(analysis["broken_internal"])
                    full_analysis["summary"]["total_broken_external"] += len(analysis["broken_external"])
                    
                    if analysis["broken_internal"] or analysis["broken_external"]:
                        full_analysis["summary"]["branches_with_issues"].append(branch)
                        
            except Exception as e:
                print(f"Error analyzing branch {branch}: {e}")
                full_analysis["branches"][branch] = {"error": str(e)}
        
        return full_analysis
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a comprehensive human-readable report"""
        if not analysis:
            return "# Error: No analysis data available"
            
        report = []
        report.append("# Comprehensive Link Analysis Report")
        report.append("## dev-ai-enable Repository - All Branches Analysis")
        report.append("")
        report.append(f"**Repository Path**: `{analysis['repository']}`")
        report.append(f"**Analysis Date**: {analysis['analysis_timestamp']}")
        report.append("")
        
        # Executive Summary
        summary = analysis["summary"]
        report.append("## 📊 Executive Summary")
        report.append("")
        report.append(f"| Metric | Count |")
        report.append(f"|--------|-------|")
        report.append(f"| Branches Analyzed | {analysis['total_branches']} |")
        report.append(f"| Documentation Files | {summary['total_files']} |")
        report.append(f"| Total Links Found | {summary['total_links']} |")
        report.append(f"| 🔴 Broken Internal Links | {summary['total_broken_internal']} |")
        report.append(f"| 🔴 Broken External Links | {summary['total_broken_external']} |")
        report.append(f"| ⚠️ Branches with Issues | {len(summary['branches_with_issues'])} |")
        report.append("")
        
        if summary['branches_with_issues']:
            report.append("### 🚨 Branches with Link Issues:")
            for branch in summary['branches_with_issues']:
                report.append(f"- `{branch}`")
            report.append("")
        else:
            report.append("### ✅ All branches have clean links!")
            report.append("")
        
        # Detailed Branch Analysis
        report.append("## 📋 Detailed Branch Analysis")
        report.append("")
        
        for branch_name, branch_data in analysis["branches"].items():
            if "error" in branch_data:
                report.append(f"### 🔴 {branch_name}")
                report.append(f"**Status**: ERROR")
                report.append(f"**Error**: {branch_data['error']}")
                report.append("")
                continue
                
            broken_count = len(branch_data["broken_internal"]) + len(branch_data["broken_external"])
            status_icon = "✅" if broken_count == 0 else "🔴"
            
            report.append(f"### {status_icon} {branch_name}")
            report.append("")
            report.append(f"| Metric | Count |")
            report.append(f"|--------|-------|")
            report.append(f"| Files Analyzed | {branch_data['files_analyzed']} |")
            report.append(f"| Total Links | {branch_data['total_links']} |")
            report.append(f"| Valid Internal | {len(branch_data['valid_internal'])} |")
            report.append(f"| Valid External | {len(branch_data['valid_external'])} |")
            report.append(f"| 🔴 Broken Internal | {len(branch_data['broken_internal'])} |")
            report.append(f"| 🔴 Broken External | {len(branch_data['broken_external'])} |")
            report.append("")
            
            # Show file structure for this branch
            if branch_data["file_details"]:
                report.append("#### 📁 Files in this branch:")
                for file_path in sorted(branch_data["file_details"].keys()):
                    file_data = branch_data["file_details"][file_path]
                    broken_in_file = len(file_data["broken_internal"]) + len(file_data["broken_external"])
                    file_icon = "🔴" if broken_in_file > 0 else "✅"
                    report.append(f"- {file_icon} `{file_path}` ({file_data['total_links']} links)")
                report.append("")
            
            # List broken internal links
            if branch_data["broken_internal"]:
                report.append("#### 🔗 Broken Internal Links")
                report.append("")
                for i, link in enumerate(branch_data["broken_internal"]):
                    if i >= 20:  # Limit to first 20
                        report.append(f"... and {len(branch_data['broken_internal']) - 20} more broken internal links")
                        break
                    report.append(f"- **File**: `{link['file']}`")
                    report.append(f"  - **Line**: {link['line']}")
                    report.append(f"  - **Link**: `{link['url']}`")
                    report.append("")
            
            # List broken external links
            if branch_data["broken_external"]:
                report.append("#### 🌐 Broken External Links")
                report.append("")
                for i, link in enumerate(branch_data["broken_external"]):
                    if i >= 20:  # Limit to first 20
                        report.append(f"... and {len(branch_data['broken_external']) - 20} more broken external links")
                        break
                    report.append(f"- **File**: `{link['file']}`")
                    report.append(f"  - **Line**: {link['line']}")
                    report.append(f"  - **URL**: `{link['url']}`")
                    report.append("")
            
            report.append("---")
            report.append("")
        
        # Recommendations
        report.append("## 💡 Recommendations for dev-ai Repository")
        report.append("")
        
        if summary['total_broken_internal'] > 0 or summary['total_broken_external'] > 0:
            report.append("### Priority Actions:")
            report.append("")
            
            if summary['total_broken_internal'] > 0:
                report.append(f"1. **Fix {summary['total_broken_internal']} broken internal links**")
                report.append("   - Review file paths and ensure referenced files exist")
                report.append("   - Update relative paths to match new repository structure")
                report.append("   - Consider using absolute paths from repository root")
                report.append("")
            
            if summary['total_broken_external'] > 0:
                report.append(f"2. **Review {summary['total_broken_external']} external links**")
                report.append("   - Check if external resources have moved")
                report.append("   - Update to new URLs or find alternative resources")
                report.append("   - Consider archiving important external content locally")
                report.append("")
            
            report.append("3. **Choose the best branch for consolidation**")
            
            # Find the branch with the most content and fewest issues
            best_branches = []
            for branch_name, branch_data in analysis["branches"].items():
                if "error" not in branch_data:
                    files = branch_data['files_analyzed']
                    links = branch_data['total_links']
                    broken = len(branch_data['broken_internal']) + len(branch_data['broken_external'])
                    score = files + links - (broken * 2)  # Penalize broken links
                    best_branches.append((branch_name, score, files, links, broken))
            
            best_branches.sort(key=lambda x: x[1], reverse=True)
            
            if best_branches:
                report.append("   - **Recommended base branch for consolidation**:")
                for i, (branch, score, files, links, broken) in enumerate(best_branches[:3]):
                    rank = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
                    report.append(f"     - {rank} `{branch}` ({files} files, {links} links, {broken} broken)")
                report.append("")
        else:
            report.append("### ✅ All links are working!")
            report.append("All branches have clean documentation with no broken links.")
            report.append("")
        
        # Branch consolidation recommendations
        report.append("4. **Consolidation Strategy**")
        report.append("   - Merge content from multiple branches")
        report.append("   - Standardize file structure across all documentation")
        report.append("   - Create a unified navigation structure")
        report.append("   - Implement link validation in CI/CD pipeline")
        report.append("")
        
        report.append("---")
        report.append("")
        report.append("*This report was generated automatically. Please review and validate findings.*")
        
        return "\n".join(report)


def main():
    repo_path = "/home/runner/work/dev-ai-enable/dev-ai-enable"
    analyzer = LocalGitLinkAnalyzer(repo_path)
    
    print("Starting comprehensive local git-based link analysis...")
    print("This will checkout each branch and analyze all documentation files.")
    print("This may take several minutes...")
    print("")
    
    analysis = analyzer.analyze_all_branches()
    
    if not analysis:
        print("❌ Analysis failed!")
        return
    
    # Save detailed JSON report
    json_report_path = Path(repo_path) / "comprehensive_link_analysis.json"
    with open(json_report_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"\n📄 Detailed JSON report saved to: {json_report_path}")
    
    # Generate and save markdown report
    report = analyzer.generate_report(analysis)
    md_report_path = Path(repo_path) / "COMPREHENSIVE_LINK_ANALYSIS.md"
    with open(md_report_path, 'w') as f:
        f.write(report)
    print(f"📄 Comprehensive markdown report saved to: {md_report_path}")
    
    # Print final summary
    print(f"\n{'='*80}")
    print("🎯 FINAL ANALYSIS SUMMARY")
    print(f"{'='*80}")
    print(f"Repository: dev-ai-enable")
    print(f"Branches analyzed: {analysis['total_branches']}")
    print(f"Documentation files: {analysis['summary']['total_files']}")
    print(f"Total links found: {analysis['summary']['total_links']}")
    print(f"🔴 Broken internal links: {analysis['summary']['total_broken_internal']}")
    print(f"🔴 Broken external links: {analysis['summary']['total_broken_external']}")
    
    if analysis['summary']['branches_with_issues']:
        print(f"\n⚠️  Branches with issues:")
        for branch in analysis['summary']['branches_with_issues']:
            branch_data = analysis['branches'][branch]
            broken = len(branch_data['broken_internal']) + len(branch_data['broken_external'])
            print(f"   - {branch}: {broken} broken links")
    else:
        print("\n✅ All branches have clean links!")
    
    print(f"\n📊 Reports generated:")
    print(f"   - JSON: {json_report_path}")
    print(f"   - Markdown: {md_report_path}")
    print(f"\n🎯 Ready for dev-ai repository consolidation!")


if __name__ == "__main__":
    main()