#!/usr/bin/env python3
"""
Content Extraction and Link Analysis Tool
Uses known working GitHub API calls from earlier exploration
"""

import re
import json
import urllib.request
import base64
import time
from typing import Dict, List, Set, Tuple
from pathlib import Path

# From our earlier exploration, we know these branches have content
BRANCHES_TO_ANALYZE = [
    ("main", "179f209bbee86f9cb59510040a1e6347dc154b7b"),
    ("copilot/fix-3ff8626e-54ce-4208-be9a-f3dfbd339e4c", "5053712f4458f32f9744c16c50be1a674c4617b6"),
    ("copilot/fix-25a990a4-640b-43e6-ab17-9d88ac37e6cf", "d91af0cd544cded24aa0d0268723e2d4d8ba71dc"),
    ("copilot/fix-32e1de2b-3b2f-4ba5-9c7a-aafbfced55fd", "09c1fca12a039b9632a655907f574bf18e8b9cf3"),
]

class ContentExtractor:
    def __init__(self):
        self.owner = "adamsalah13"
        self.repo = "dev-ai-enable"
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        
    def get_file_content_by_url(self, download_url: str) -> str:
        """Get file content by download URL"""
        try:
            request = urllib.request.Request(download_url)
            request.add_header('User-Agent', 'Content-Extractor/1.0')
            
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error downloading {download_url}: {e}")
            return ""
    
    def get_contents_recursive(self, ref: str, path: str = "") -> List[Dict]:
        """Recursively get all files from a branch"""
        all_files = []
        
        def fetch_directory(dir_path: str = ""):
            try:
                url = f"{self.base_url}/contents/{dir_path}?ref={ref}"
                request = urllib.request.Request(url)
                request.add_header('User-Agent', 'Content-Extractor/1.0')
                
                with urllib.request.urlopen(request, timeout=30) as response:
                    items = json.loads(response.read().decode())
                    
                    if isinstance(items, list):
                        for item in items:
                            if item['type'] == 'file':
                                all_files.append(item)
                            elif item['type'] == 'dir':
                                # Recursively fetch directory contents
                                time.sleep(0.1)  # Rate limiting
                                fetch_directory(item['path'])
                    
            except Exception as e:
                print(f"Error fetching directory {dir_path}: {e}")
        
        fetch_directory(path)
        return all_files
    
    def is_documentation_file(self, filename: str) -> bool:
        """Check if file is documentation"""
        doc_extensions = ['.md', '.txt', '.rst', '.html', '.json', '.yaml', '.yml']
        return any(filename.lower().endswith(ext) for ext in doc_extensions)
    
    def extract_links(self, content: str, file_path: str) -> List[Tuple[str, int, str]]:
        """Extract all links from content with line numbers and types"""
        links = []
        
        # Markdown links: [text](url)
        markdown_links = re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', content)
        for match in markdown_links:
            line_num = content[:match.start()].count('\n') + 1
            links.append((match.group(2), line_num, "markdown_link"))
        
        # HTML links: href="url"
        html_links = re.finditer(r'href=["\']([^"\']+)["\']', content)
        for match in html_links:
            line_num = content[:match.start()].count('\n') + 1
            links.append((match.group(1), line_num, "html_href"))
        
        # Image references: ![alt](src)
        img_refs = re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', content)
        for match in img_refs:
            line_num = content[:match.start()].count('\n') + 1
            links.append((match.group(1), line_num, "image"))
        
        # Direct URLs: http(s)://...
        url_pattern = re.compile(r'https?://[^\s<>"\']+')
        url_matches = re.finditer(url_pattern, content)
        for match in url_matches:
            line_num = content[:match.start()].count('\n') + 1
            url = match.group(0)
            # Clean up URL (remove trailing punctuation)
            url = re.sub(r'[.,;:!?)]+$', '', url)
            links.append((url, line_num, "direct_url"))
        
        # File references in HTML-like tags
        file_refs = re.finditer(r'(?:src)=["\']([^"\']+)["\']', content)
        for match in file_refs:
            line_num = content[:match.start()].count('\n') + 1
            ref = match.group(1)
            if not ref.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                links.append((ref, line_num, "file_src"))
        
        return links
    
    def analyze_branch(self, branch_name: str, branch_sha: str) -> Dict:
        """Analyze all files in a branch"""
        print(f"\n{'='*60}")
        print(f"Analyzing branch: {branch_name}")
        print(f"SHA: {branch_sha}")
        print(f"{'='*60}")
        
        # Get all files from branch
        all_files = self.get_contents_recursive(branch_sha)
        doc_files = [f for f in all_files if self.is_documentation_file(f['name'])]
        
        print(f"Total files: {len(all_files)}")
        print(f"Documentation files: {len(doc_files)}")
        
        branch_analysis = {
            "branch": branch_name,
            "sha": branch_sha,
            "total_files": len(all_files),
            "doc_files": len(doc_files),
            "files": {},
            "all_files_list": [f['path'] for f in all_files],
            "links_summary": {
                "total_links": 0,
                "internal_links": 0,
                "external_links": 0,
                "broken_internal": 0,
                "broken_external": 0
            },
            "broken_links": [],
            "personas_found": [],
            "docs_structure": {}
        }
        
        # Track all file paths for internal link validation
        all_file_paths = set(f['path'] for f in all_files)
        
        # Look for specific directories
        personas_dir = [f for f in all_files if f['path'].startswith('personas/')]
        docs_dir = [f for f in all_files if f['path'].startswith('docs/')]
        sample_app_dir = [f for f in all_files if f['path'].startswith('sample-app/')]
        
        if personas_dir:
            branch_analysis["personas_found"] = list(set(f['path'].split('/')[1] for f in personas_dir if len(f['path'].split('/')) > 1))
        
        # Analyze each documentation file
        for doc_file in doc_files:
            file_path = doc_file['path']
            print(f"  📄 {file_path}")
            
            # Get file content
            content = self.get_file_content_by_url(doc_file['download_url'])
            if not content:
                continue
            
            # Extract links
            links = self.extract_links(content, file_path)
            
            file_analysis = {
                "size": doc_file['size'],
                "links": [],
                "broken_links": [],
                "content_preview": content[:500] + "..." if len(content) > 500 else content
            }
            
            for link_url, line_num, link_type in links:
                branch_analysis["links_summary"]["total_links"] += 1
                
                link_info = {
                    "url": link_url,
                    "line": line_num,
                    "type": link_type,
                    "is_external": link_url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'ftp://'))
                }
                
                if link_info["is_external"]:
                    branch_analysis["links_summary"]["external_links"] += 1
                    # Don't check external links to avoid rate limiting
                    link_info["status"] = "external_not_checked"
                else:
                    branch_analysis["links_summary"]["internal_links"] += 1
                    # Check internal link
                    link_info["status"] = self.check_internal_link(link_url, file_path, all_file_paths)
                    if link_info["status"] == "broken":
                        branch_analysis["links_summary"]["broken_internal"] += 1
                        branch_analysis["broken_links"].append({
                            "file": file_path,
                            "line": line_num,
                            "url": link_url,
                            "type": "internal"
                        })
                        file_analysis["broken_links"].append(link_info)
                
                file_analysis["links"].append(link_info)
            
            branch_analysis["files"][file_path] = file_analysis
        
        return branch_analysis
    
    def check_internal_link(self, link: str, current_file: str, all_files: Set[str]) -> str:
        """Check if internal link exists"""
        try:
            # Remove anchor/fragment
            clean_link = link.split('#')[0]
            if not clean_link:  # Just an anchor
                return "valid_anchor"
            
            # Handle different types of internal links
            if clean_link.startswith('/'):
                # Absolute path from repo root
                target_path = clean_link.lstrip('/')
            else:
                # Relative path from current file
                current_dir = '/'.join(current_file.split('/')[:-1])
                if current_dir:
                    target_path = f"{current_dir}/{clean_link}"
                else:
                    target_path = clean_link
            
            # Normalize path
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
            
            # Check if file exists
            if normalized_path in all_files:
                return "valid"
            else:
                return "broken"
                
        except Exception as e:
            return "error"
    
    def generate_comprehensive_report(self, analyses: Dict) -> str:
        """Generate comprehensive analysis report"""
        report = []
        report.append("# 🔍 Comprehensive Repository Analysis Report")
        report.append("## dev-ai-enable Repository - All Branches Content Analysis")
        report.append("")
        report.append(f"**Analysis Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        total_files = sum(analysis.get('total_files', 0) for analysis in analyses.values())
        total_doc_files = sum(analysis.get('doc_files', 0) for analysis in analyses.values())
        total_links = sum(analysis.get('links_summary', {}).get('total_links', 0) for analysis in analyses.values())
        total_broken = sum(analysis.get('links_summary', {}).get('broken_internal', 0) for analysis in analyses.values())
        
        report.append("## 📊 Executive Summary")
        report.append("")
        report.append(f"| Metric | Count |")
        report.append(f"|--------|-------|")
        report.append(f"| Branches Analyzed | {len(analyses)} |")
        report.append(f"| Total Files | {total_files} |")
        report.append(f"| Documentation Files | {total_doc_files} |")
        report.append(f"| Total Links | {total_links} |")
        report.append(f"| 🔴 Broken Internal Links | {total_broken} |")
        report.append("")
        
        # Branch comparison
        report.append("## 🌳 Branch Comparison")
        report.append("")
        report.append("| Branch | Files | Docs | Links | Broken | Personas | Status |")
        report.append("|--------|-------|------|-------|--------|----------|--------|")
        
        for branch, analysis in analyses.items():
            files = analysis.get('total_files', 0)
            docs = analysis.get('doc_files', 0)
            links = analysis.get('links_summary', {}).get('total_links', 0)
            broken = analysis.get('links_summary', {}).get('broken_internal', 0)
            personas = ', '.join(analysis.get('personas_found', [])[:3])  # First 3 personas
            if len(analysis.get('personas_found', [])) > 3:
                personas += f" +{len(analysis.get('personas_found', [])) - 3}"
            status = "🔴 Issues" if broken > 0 else "✅ Clean"
            
            report.append(f"| `{branch}` | {files} | {docs} | {links} | {broken} | {personas} | {status} |")
        
        report.append("")
        
        # Detailed branch analysis
        report.append("## 📋 Detailed Branch Analysis")
        report.append("")
        
        for branch, analysis in analyses.items():
            broken_count = analysis.get('links_summary', {}).get('broken_internal', 0)
            status_icon = "✅" if broken_count == 0 else "🔴"
            
            report.append(f"### {status_icon} {branch}")
            report.append("")
            report.append(f"**SHA**: `{analysis.get('sha', 'N/A')}`")
            report.append("")
            
            # File structure overview
            if analysis.get('personas_found'):
                report.append("**🎭 Personas Found**:")
                for persona in analysis['personas_found']:
                    report.append(f"- {persona}")
                report.append("")
            
            # Key files
            key_files = []
            for file_path in analysis.get('files', {}):
                if any(key in file_path.lower() for key in ['readme', 'index', 'guide']):
                    key_files.append(file_path)
            
            if key_files:
                report.append("**📚 Key Documentation Files**:")
                for file_path in sorted(key_files):
                    file_data = analysis['files'][file_path]
                    broken_in_file = len(file_data.get('broken_links', []))
                    icon = "🔴" if broken_in_file > 0 else "✅"
                    report.append(f"- {icon} `{file_path}` ({len(file_data.get('links', []))} links)")
                report.append("")
            
            # Broken links
            if analysis.get('broken_links'):
                report.append("**🔗 Broken Internal Links**:")
                for broken_link in analysis['broken_links'][:10]:  # First 10
                    report.append(f"- `{broken_link['file']}:{broken_link['line']}` → `{broken_link['url']}`")
                if len(analysis['broken_links']) > 10:
                    report.append(f"- ... and {len(analysis['broken_links']) - 10} more")
                report.append("")
            
            report.append("---")
            report.append("")
        
        # Consolidation recommendations
        report.append("## 💡 Consolidation Recommendations for dev-ai Repository")
        report.append("")
        
        # Find the best branch for consolidation
        best_branch = None
        best_score = -1
        
        for branch, analysis in analyses.items():
            files = analysis.get('doc_files', 0)
            links = analysis.get('links_summary', {}).get('total_links', 0)
            broken = analysis.get('links_summary', {}).get('broken_internal', 0)
            personas = len(analysis.get('personas_found', []))
            
            # Score: prioritize content richness and low broken links
            score = files + (links * 0.1) + (personas * 5) - (broken * 2)
            
            if score > best_score:
                best_score = score
                best_branch = branch
        
        if best_branch:
            report.append(f"### 🥇 Recommended Base Branch: `{best_branch}`")
            best_analysis = analyses[best_branch]
            report.append(f"- **Files**: {best_analysis.get('total_files', 0)} total, {best_analysis['doc_files']} docs")
            report.append(f"- **Content**: {best_analysis['links_summary']['total_links']} links")
            report.append(f"- **Personas**: {len(best_analysis.get('personas_found', []))} personas")
            report.append(f"- **Issues**: {best_analysis['links_summary']['broken_internal']} broken internal links")
            report.append("")
        
        report.append("### 🛠️ Action Plan:")
        report.append("1. **Choose base branch** (recommended above)")
        report.append("2. **Fix broken internal links** by updating file paths")
        report.append("3. **Merge content** from other branches that have unique documentation")
        report.append("4. **Standardize structure** across all documentation")
        report.append("5. **Implement link validation** in CI/CD pipeline")
        report.append("")
        
        # Content inventory
        report.append("## 📦 Content Inventory")
        report.append("")
        
        all_personas = set()
        all_docs = set()
        
        for analysis in analyses.values():
            all_personas.update(analysis.get('personas_found', []))
            for file_path in analysis.get('files', {}):
                if file_path.startswith('docs/'):
                    all_docs.add(file_path)
        
        if all_personas:
            report.append("### 🎭 All Personas Found Across Branches:")
            for persona in sorted(all_personas):
                report.append(f"- {persona}")
            report.append("")
        
        if all_docs:
            report.append("### 📚 Documentation Files Found:")
            for doc in sorted(all_docs):
                report.append(f"- `{doc}`")
            report.append("")
        
        report.append("---")
        report.append("")
        report.append("*This report provides a comprehensive analysis for consolidating content into the dev-ai repository.*")
        
        return "\n".join(report)


def main():
    extractor = ContentExtractor()
    
    print("🚀 Starting comprehensive content extraction and link analysis...")
    print(f"Will analyze {len(BRANCHES_TO_ANALYZE)} branches with known content")
    print("")
    
    all_analyses = {}
    
    for branch_name, branch_sha in BRANCHES_TO_ANALYZE:
        try:
            analysis = extractor.analyze_branch(branch_name, branch_sha)
            all_analyses[branch_name] = analysis
        except Exception as e:
            print(f"❌ Error analyzing {branch_name}: {e}")
            all_analyses[branch_name] = {"error": str(e)}
    
    # Generate comprehensive report
    report = extractor.generate_comprehensive_report(all_analyses)
    
    # Save reports
    json_path = Path("comprehensive_content_analysis.json")
    with open(json_path, 'w') as f:
        json.dump(all_analyses, f, indent=2)
    
    md_path = Path("COMPREHENSIVE_CONTENT_ANALYSIS.md")
    with open(md_path, 'w') as f:
        f.write(report)
    
    print(f"\n{'='*80}")
    print("🎯 ANALYSIS COMPLETE")
    print(f"{'='*80}")
    
    # Summary
    total_files = sum(a.get('total_files', 0) for a in all_analyses.values() if 'error' not in a)
    total_docs = sum(a.get('doc_files', 0) for a in all_analyses.values() if 'error' not in a)
    total_links = sum(a.get('links_summary', {}).get('total_links', 0) for a in all_analyses.values() if 'error' not in a)
    total_broken = sum(a.get('links_summary', {}).get('broken_internal', 0) for a in all_analyses.values() if 'error' not in a)
    
    print(f"📊 Summary:")
    print(f"   - Branches analyzed: {len([a for a in all_analyses.values() if 'error' not in a])}")
    print(f"   - Total files: {total_files}")
    print(f"   - Documentation files: {total_docs}")
    print(f"   - Links found: {total_links}")
    print(f"   - Broken internal links: {total_broken}")
    
    print(f"\n📄 Reports generated:")
    print(f"   - JSON: {json_path}")
    print(f"   - Markdown: {md_path}")
    
    print(f"\n🎯 Ready for dev-ai repository consolidation!")


if __name__ == "__main__":
    main()