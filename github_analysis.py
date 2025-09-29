#!/usr/bin/env python3
"""
GitHub API-based Link Analysis Tool for dev-ai-enable Repository
Uses GitHub API to analyze all branches without needing to checkout locally
"""

import re
import json
import urllib.parse
import urllib.request
import base64
import time
from typing import Dict, List, Set, Tuple
from pathlib import Path

class GitHubLinkAnalyzer:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.branches = []
        
    def get_branches(self) -> List[Dict]:
        """Get all branches using GitHub API"""
        try:
            url = f"{self.base_url}/branches"
            print(f"Fetching branches from: {url}")
            
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Link-Analyzer/1.0')
            
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode())
                return data
        except Exception as e:
            print(f"Error getting branches: {e}")
            return []
    
    def get_tree(self, branch: str, recursive: bool = True) -> Dict:
        """Get file tree for a branch"""
        try:
            url = f"{self.base_url}/git/trees/{branch}"
            if recursive:
                url += "?recursive=1"
            
            print(f"Fetching tree for branch {branch}")
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Link-Analyzer/1.0')
            
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error getting tree for branch {branch}: {e}")
            return {}
    
    def get_file_content(self, sha: str) -> str:
        """Get file content by SHA"""
        try:
            url = f"{self.base_url}/git/blobs/{sha}"
            
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Link-Analyzer/1.0')
            
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode())
                
                if data.get('encoding') == 'base64':
                    content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                    return content
                else:
                    return data.get('content', '')
        except Exception as e:
            print(f"Error getting file content for SHA {sha}: {e}")
            return ""
    
    def is_documentation_file(self, path: str) -> bool:
        """Check if file is a documentation file"""
        doc_extensions = ['.md', '.txt', '.rst', '.html', '.json', '.yaml', '.yml']
        return any(path.lower().endswith(ext) for ext in doc_extensions)
    
    def extract_links(self, content: str) -> List[Tuple[str, int]]:
        """Extract all links from content with line numbers"""
        links = []
        
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
            
        # Relative file references - src and href attributes
        file_refs = re.finditer(r'(?:src|href)=["\']([^"\']+)["\']', content)
        for match in file_refs:
            line_num = content[:match.start()].count('\n') + 1
            ref = match.group(1)
            if not ref.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                links.append((ref, line_num))
        
        # File paths in markdown (like images and relative links)
        file_path_refs = re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', content)  # Images
        for match in file_path_refs:
            line_num = content[:match.start()].count('\n') + 1
            ref = match.group(1)
            if not ref.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                links.append((ref, line_num))
                
        return links
    
    def is_external_link(self, url: str) -> bool:
        """Check if URL is external"""
        return url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'ftp://'))
    
    def check_internal_link(self, link: str, current_file_path: str, files_in_branch: Set[str]) -> bool:
        """Check if internal link exists in the branch"""
        try:
            # Remove anchor/fragment
            link = link.split('#')[0]
            if not link:  # Just an anchor
                return True
            
            # Handle different types of internal links
            if link.startswith('/'):
                # Absolute path from repo root
                target_path = link.lstrip('/')
            else:
                # Relative path from current file
                current_dir = '/'.join(current_file_path.split('/')[:-1])
                if current_dir:
                    target_path = f"{current_dir}/{link}"
                else:
                    target_path = link
            
            # Normalize path (remove ./ and ../)
            path_parts = []
            for part in target_path.split('/'):
                if part == '.' or part == '':
                    continue
                elif part == '..':
                    if path_parts:
                        path_parts.pop()
                else:
                    path_parts.append(part)
            
            normalized_path = '/'.join(path_parts)
            
            # Check if file exists in branch
            return normalized_path in files_in_branch
            
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
            # Don't print every external link failure to reduce noise
            return False
    
    def analyze_branch(self, branch_name: str, branch_sha: str) -> Dict:
        """Analyze all files in a specific branch"""
        print(f"\nAnalyzing branch: {branch_name}")
        
        branch_analysis = {
            "branch": branch_name,
            "sha": branch_sha,
            "files_analyzed": 0,
            "total_links": 0,
            "broken_internal": [],
            "broken_external": [],
            "valid_internal": [],
            "valid_external": [],
            "file_details": {}
        }
        
        # Get file tree
        tree = self.get_tree(branch_sha)
        if not tree or 'tree' not in tree:
            return {"error": f"Could not get tree for branch {branch_name}"}
        
        # Get all file paths in branch for internal link checking
        files_in_branch = set()
        doc_files = []
        
        for item in tree['tree']:
            if item['type'] == 'blob':
                files_in_branch.add(item['path'])
                if self.is_documentation_file(item['path']):
                    doc_files.append(item)
        
        print(f"  Found {len(doc_files)} documentation files")
        branch_analysis["files_analyzed"] = len(doc_files)
        
        for file_item in doc_files:
            file_path = file_item['path']
            print(f"  Analyzing: {file_path}")
            
            # Get file content
            content = self.get_file_content(file_item['sha'])
            if not content:
                continue
            
            # Extract links
            links = self.extract_links(content)
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
                    time.sleep(0.3)  # Rate limiting
                    if self.check_external_link(link):
                        file_analysis["valid_external"].append({"url": link, "line": line_num})
                        branch_analysis["valid_external"].append({
                            "file": file_path,
                            "url": link,
                            "line": line_num
                        })
                    else:
                        file_analysis["broken_external"].append({"url": link, "line": line_num})
                        branch_analysis["broken_external"].append({
                            "file": file_path,
                            "url": link,
                            "line": line_num
                        })
                else:
                    # Check internal link
                    if self.check_internal_link(link, file_path, files_in_branch):
                        file_analysis["valid_internal"].append({"url": link, "line": line_num})
                        branch_analysis["valid_internal"].append({
                            "file": file_path,
                            "url": link,
                            "line": line_num
                        })
                    else:
                        file_analysis["broken_internal"].append({"url": link, "line": line_num})
                        branch_analysis["broken_internal"].append({
                            "file": file_path,
                            "url": link,
                            "line": line_num
                        })
            
            branch_analysis["file_details"][file_path] = file_analysis
        
        return branch_analysis
    
    def analyze_all_branches(self) -> Dict:
        """Analyze all branches in the repository"""
        branches = self.get_branches()
        print(f"Found {len(branches)} branches")
        
        full_analysis = {
            "repository": f"{self.owner}/{self.repo}",
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
        
        for branch_info in branches:
            branch_name = branch_info['name']
            branch_sha = branch_info['commit']['sha']
            
            try:
                analysis = self.analyze_branch(branch_name, branch_sha)
                full_analysis["branches"][branch_name] = analysis
                
                # Update summary
                if "error" not in analysis:
                    full_analysis["summary"]["total_files"] += analysis["files_analyzed"]
                    full_analysis["summary"]["total_links"] += analysis["total_links"]
                    full_analysis["summary"]["total_broken_internal"] += len(analysis["broken_internal"])
                    full_analysis["summary"]["total_broken_external"] += len(analysis["broken_external"])
                    
                    if analysis["broken_internal"] or analysis["broken_external"]:
                        full_analysis["summary"]["branches_with_issues"].append(branch_name)
                        
            except Exception as e:
                print(f"Error analyzing branch {branch_name}: {e}")
                full_analysis["branches"][branch_name] = {"error": str(e)}
        
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
        
        if summary['branches_with_issues']:
            report.append("### Branches with Issues:")
            for branch in summary['branches_with_issues']:
                report.append(f"- {branch}")
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
            report.append(f"- **SHA**: `{branch_data.get('sha', 'N/A')}`")
            report.append(f"- **Files Analyzed**: {branch_data['files_analyzed']}")
            report.append(f"- **Total Links**: {branch_data['total_links']}")
            report.append(f"- **Broken Internal**: {len(branch_data['broken_internal'])}")
            report.append(f"- **Broken External**: {len(branch_data['broken_external'])}")
            report.append("")
            
            # List broken internal links
            if branch_data["broken_internal"]:
                report.append("#### Broken Internal Links")
                for link in branch_data["broken_internal"][:10]:  # Limit to first 10
                    report.append(f"- `{link['file']}:{link['line']}` → `{link['url']}`")
                if len(branch_data["broken_internal"]) > 10:
                    report.append(f"- ... and {len(branch_data['broken_internal']) - 10} more")
                report.append("")
            
            # List broken external links
            if branch_data["broken_external"]:
                report.append("#### Broken External Links")
                for link in branch_data["broken_external"][:10]:  # Limit to first 10
                    report.append(f"- `{link['file']}:{link['line']}` → `{link['url']}`")
                if len(branch_data["broken_external"]) > 10:
                    report.append(f"- ... and {len(branch_data['broken_external']) - 10} more")
                report.append("")
        
        return "\n".join(report)


def main():
    owner = "adamsalah13"
    repo = "dev-ai-enable"
    
    analyzer = GitHubLinkAnalyzer(owner, repo)
    
    print("Starting comprehensive GitHub API-based link analysis...")
    analysis = analyzer.analyze_all_branches()
    
    # Save detailed JSON report
    json_report_path = Path("github_broken_links_analysis.json")
    with open(json_report_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"Detailed JSON report saved to: {json_report_path}")
    
    # Generate and save markdown report
    report = analyzer.generate_report(analysis)
    md_report_path = Path("GITHUB_BROKEN_LINKS_REPORT.md")
    with open(md_report_path, 'w') as f:
        f.write(report)
    print(f"Markdown report saved to: {md_report_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("GITHUB API ANALYSIS COMPLETE")
    print("="*60)
    print(f"Repository: {analysis['repository']}")
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