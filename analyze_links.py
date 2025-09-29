#!/usr/bin/env python3
"""
Comprehensive Link Analysis Tool for dev-ai-enable Repository
Analyzes all branches, files, personas, and documentation for broken links
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

class LinkAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.branches = []
        self.broken_links = {}
        self.missing_files = {}
        self.valid_links = {}
        self.internal_links = {}
        self.external_links = {}
        
    def get_branches(self) -> List[str]:
        """Get all remote branches"""
        try:
            result = subprocess.run(
                ['git', 'branch', '-r'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            branches = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and not line.startswith('origin/HEAD'):
                    branch = line.replace('origin/', '')
                    branches.append(branch)
            return branches
        except Exception as e:
            print(f"Error getting branches: {e}")
            return []
    
    def checkout_branch(self, branch: str) -> bool:
        """Checkout a specific branch"""
        try:
            # Try to checkout existing branch
            result = subprocess.run(
                ['git', 'checkout', branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                # Try to checkout remote branch
                result = subprocess.run(
                    ['git', 'checkout', '-b', branch, f'origin/{branch}'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
            return result.returncode == 0
        except Exception as e:
            print(f"Error checking out branch {branch}: {e}")
            return False
    
    def find_markdown_files(self) -> List[Path]:
        """Find all markdown and documentation files"""
        patterns = ['*.md', '*.txt', '*.rst', '*.html', '*.json', '*.yaml', '*.yml']
        files = []
        
        for pattern in patterns:
            files.extend(self.repo_path.rglob(pattern))
        
        # Filter out .git directory
        files = [f for f in files if '.git' not in str(f)]
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
                
            # Relative file references
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
            print(f"Error checking internal link {link}: {e}")
            return False
    
    def check_external_link(self, url: str) -> bool:
        """Check if external URL is accessible (with simple timeout)"""
        try:
            # Skip some problematic URLs
            if any(domain in url.lower() for domain in ['localhost', '127.0.0.1', 'example.com']):
                return True
                
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Link-Checker/1.0')
            
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status < 400
                
        except Exception as e:
            print(f"External link check failed for {url}: {e}")
            return False
    
    def analyze_branch(self, branch: str) -> Dict:
        """Analyze all files in a specific branch"""
        print(f"Analyzing branch: {branch}")
        
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
        
        files = self.find_markdown_files()
        branch_analysis["files_analyzed"] = len(files)
        
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
            
            for link, line_num in links:
                branch_analysis["total_links"] += 1
                
                if self.is_external_link(link):
                    # Check external link (with rate limiting)
                    time.sleep(0.5)  # Rate limiting
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
            
            branch_analysis["file_details"][str(relative_path)] = file_analysis
        
        return branch_analysis
    
    def analyze_all_branches(self) -> Dict:
        """Analyze all branches in the repository"""
        self.branches = self.get_branches()
        print(f"Found {len(self.branches)} branches: {self.branches}")
        
        full_analysis = {
            "repository": str(self.repo_path),
            "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_branches": len(self.branches),
            "branches": {},
            "summary": {
                "total_files": 0,
                "total_links": 0,
                "total_broken_internal": 0,
                "total_broken_external": 0,
                "branches_with_issues": []
            }
        }
        
        for branch in self.branches:
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
        """Generate a human-readable report"""
        report = []
        report.append("# Comprehensive Link Analysis Report")
        report.append(f"**Repository**: {analysis['repository']}")
        report.append(f"**Analysis Date**: {analysis['analysis_timestamp']}")
        report.append("")
        
        # Summary
        summary = analysis["summary"]
        report.append("## Summary")
        report.append(f"- **Total Branches Analyzed**: {analysis['total_branches']}")
        report.append(f"- **Total Files Analyzed**: {summary['total_files']}")
        report.append(f"- **Total Links Found**: {summary['total_links']}")
        report.append(f"- **Broken Internal Links**: {summary['total_broken_internal']}")
        report.append(f"- **Broken External Links**: {summary['total_broken_external']}")
        report.append(f"- **Branches with Issues**: {len(summary['branches_with_issues'])}")
        report.append("")
        
        # Branch-by-branch analysis
        report.append("## Branch Analysis")
        
        for branch_name, branch_data in analysis["branches"].items():
            if "error" in branch_data:
                report.append(f"### {branch_name} ❌")
                report.append(f"**Error**: {branch_data['error']}")
                report.append("")
                continue
                
            broken_count = len(branch_data["broken_internal"]) + len(branch_data["broken_external"])
            status = "✅" if broken_count == 0 else "⚠️"
            
            report.append(f"### {branch_name} {status}")
            report.append(f"- **Files Analyzed**: {branch_data['files_analyzed']}")
            report.append(f"- **Total Links**: {branch_data['total_links']}")
            report.append(f"- **Broken Internal**: {len(branch_data['broken_internal'])}")
            report.append(f"- **Broken External**: {len(branch_data['broken_external'])}")
            report.append("")
            
            # List broken internal links
            if branch_data["broken_internal"]:
                report.append("#### Broken Internal Links")
                for link in branch_data["broken_internal"]:
                    report.append(f"- `{link['file']}:{link['line']}` → `{link['url']}`")
                report.append("")
            
            # List broken external links
            if branch_data["broken_external"]:
                report.append("#### Broken External Links")
                for link in branch_data["broken_external"]:
                    report.append(f"- `{link['file']}:{link['line']}` → `{link['url']}`")
                report.append("")
        
        return "\n".join(report)


def main():
    repo_path = "/home/runner/work/dev-ai-enable/dev-ai-enable"
    analyzer = LinkAnalyzer(repo_path)
    
    print("Starting comprehensive link analysis...")
    analysis = analyzer.analyze_all_branches()
    
    # Save detailed JSON report
    json_report_path = Path(repo_path) / "broken_links_analysis.json"
    with open(json_report_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"Detailed JSON report saved to: {json_report_path}")
    
    # Generate and save markdown report
    report = analyzer.generate_report(analysis)
    md_report_path = Path(repo_path) / "BROKEN_LINKS_REPORT.md"
    with open(md_report_path, 'w') as f:
        f.write(report)
    print(f"Markdown report saved to: {md_report_path}")
    
    # Print summary
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
    print(f"Branches analyzed: {analysis['total_branches']}")
    print(f"Files analyzed: {analysis['summary']['total_files']}")
    print(f"Total links: {analysis['summary']['total_links']}")
    print(f"Broken internal links: {analysis['summary']['total_broken_internal']}")
    print(f"Broken external links: {analysis['summary']['total_broken_external']}")
    
    if analysis['summary']['branches_with_issues']:
        print(f"\nBranches with issues:")
        for branch in analysis['summary']['branches_with_issues']:
            print(f"  - {branch}")
    else:
        print("\n✅ No broken links found!")


if __name__ == "__main__":
    main()