#!/usr/bin/env python3
"""
Manual Analysis Based on Known Repository Content
Using information gathered from GitHub MCP server calls
"""

import json
import time
from pathlib import Path

# Known content from GitHub MCP server exploration
BRANCH_ANALYSIS = {
    "main": {
        "sha": "179f209bbee86f9cb59510040a1e6347dc154b7b",
        "files": ["LICENSE", "README.md"],
        "structure": {
            "README.md": {
                "size": 39,
                "content": "# dev-ai-enable\nfintech-ai-enable labs\n",
                "links": []
            },
            "LICENSE": {
                "size": 1067,
                "content": "MIT License\n\nCopyright (c) 2025 Adam Salah\n...",
                "links": []
            }
        }
    },
    "copilot/fix-3ff8626e-54ce-4208-be9a-f3dfbd339e4c": {
        "sha": "5053712f4458f32f9744c16c50be1a674c4617b6",
        "files": [
            ".github/", ".gitignore", "LICENSE", "README.md", 
            "docs/", "personas/", "sample-app/", "templates/"
        ],
        "docs_files": [
            "docs/assessment-criteria.md",
            "docs/collaboration-workflows.md", 
            "docs/course-setup.md",
            "docs/cursor-ai-guide.md",
            "docs/deployment/",
            "docs/fintech/",
            "docs/github-copilot-guide.md",
            "docs/prompting-guide.md",
            "docs/testing/"
        ],
        "personas": [
            "personas/business-analyst/",
            "personas/developer/",
            "personas/devops/",
            "personas/documentation/",
            "personas/qa/"
        ],
        "sample_app": [
            "sample-app/.env.example",
            "sample-app/README.md",
            "sample-app/backend/",
            "sample-app/database/",
            "sample-app/docker-compose.yml",
            "sample-app/frontend/",
            "sample-app/package.json"
        ],
        "readme_content": """# AI-Driven End-to-End CI/CD Course

A comprehensive hands-on course for development teams to learn AI-driven CI/CD processes from Business Analysis to Quality Assurance and Documentation.

## 🎯 Course Overview

This course introduces development teams to modern AI-powered workflows that span the entire software development lifecycle. Participants will learn to leverage AI tools like GitHub Copilot, Cursor AI, and VSCode extensions to streamline processes from requirements gathering to deployment and documentation.

## 👥 Target Personas

This course is designed for cross-functional development teams including:

- **Business Analysts (BA)** - Requirements gathering and user story creation
- **Product Owners** - Feature planning and backlog management
- **Developers** - Code implementation and testing
- **DevOps Engineers** - CI/CD pipeline management
- **Quality Assurance (QA)** - Testing strategy and automation
- **Technical Writers** - Documentation and knowledge management

## 🏗️ Course Structure

### Module 1: Foundation Setup
- Repository setup and collaboration workflows
- VSCode/Cursor AI agent configuration
- GitHub Copilot integration
- Fork and contribution workflows

### Module 2: Persona-Specific AI Workflows
- BA: AI-assisted requirements analysis
- Developer: AI-powered code generation
- QA: AI-driven test automation
- Documentation: AI-enhanced technical writing

### Module 3: End-to-End Integration
- Connecting AI workflows across personas
- Automated CI/CD with AI assistance
- Quality gates and automated reviews
- Deployment and monitoring

### Module 4: Fintech-Specific Applications
- Compliance and security considerations
- Financial data handling
- Regulatory documentation
- Risk management workflows

## 🚀 Getting Started

1. **Fork this repository** to your GitHub account
2. **Clone your fork** locally
3. **Follow the setup guides** in each persona directory
4. **Complete the exercises** in sequence
5. **Submit pull requests** for review

## 📁 Repository Structure

```
├── personas/                    # Persona-specific guides and exercises
│   ├── business-analyst/       # BA workflows and tools
│   ├── developer/              # Development workflows
│   ├── devops/                 # CI/CD and infrastructure
│   ├── qa/                     # Testing and quality assurance
│   └── documentation/          # Technical writing workflows
├── sample-app/                  # Fintech sample application
├── templates/                   # AI prompt templates
├── workflows/                   # GitHub Actions examples
└── docs/                       # Course documentation
```

## 🛠️ Prerequisites

- GitHub account
- Git basics knowledge
- VSCode or Cursor IDE
- Basic understanding of software development lifecycle
- Interest in AI-powered development workflows

## 📚 Learning Outcomes

By the end of this course, participants will be able to:

- ✅ Set up and configure AI development environments
- ✅ Use AI tools effectively for their specific role
- ✅ Collaborate across personas using AI-enhanced workflows
- ✅ Implement end-to-end CI/CD pipelines with AI assistance
- ✅ Apply fintech-specific considerations to AI workflows
- ✅ Create and maintain AI-generated documentation
- ✅ Establish quality gates and automated review processes

## 🤝 Contributing

This is a collaborative learning environment. Please:
1. Fork the repository
2. Create feature branches for exercises
3. Submit pull requests for review
4. Participate in code reviews
5. Share learnings with the team

## 📄 License

MIT License - See [LICENSE](LICENSE) for details."""
    },
    "copilot/fix-25a990a4-640b-43e6-ab17-9d88ac37e6cf": {
        "sha": "d91af0cd544cded24aa0d0268723e2d4d8ba71dc",
        "files": [
            ".github/", ".gitignore", "LICENSE", "README.md",
            "docs/", "personas/", "sample-app/", "templates/"
        ],
        "note": "Similar structure to fix-3ff8626e but with different SHA - likely has variations"
    },
    "copilot/fix-32e1de2b-3b2f-4ba5-9c7a-aafbfced55fd": {
        "sha": "09c1fca12a039b9632a655907f574bf18e8b9cf3",
        "files": ["LICENSE", "README.md"],
        "note": "Minimal branch - similar to main"
    }
}

def analyze_links_in_content(content: str, file_path: str) -> dict:
    """Analyze links in content"""
    import re
    
    links = {
        "markdown_links": [],
        "direct_urls": [],
        "file_references": [],
        "broken_links": []
    }
    
    # Markdown links: [text](url)
    markdown_links = re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', content)
    for match in markdown_links:
        line_num = content[:match.start()].count('\n') + 1
        url = match.group(2)
        links["markdown_links"].append({
            "text": match.group(1),
            "url": url,
            "line": line_num
        })
        
        # Check if it's a broken internal reference
        if not url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            # This is an internal reference
            if url in ["LICENSE"]:  # Known to exist in most branches
                pass  # Valid
            else:
                links["broken_links"].append({
                    "url": url,
                    "line": line_num,
                    "reason": "Internal file reference may not exist",
                    "type": "internal"
                })
    
    # Direct URLs
    url_pattern = re.compile(r'https?://[^\s<>"\']+')
    for match in re.finditer(url_pattern, content):
        line_num = content[:match.start()].count('\n') + 1
        url = match.group(0)
        url = re.sub(r'[.,;:!?)]+$', '', url)  # Clean trailing punctuation
        links["direct_urls"].append({
            "url": url,
            "line": line_num
        })
    
    return links

def generate_comprehensive_analysis():
    """Generate comprehensive analysis from known data"""
    
    analysis = {
        "repository": "adamsalah13/dev-ai-enable",
        "analysis_method": "Manual analysis based on GitHub MCP server exploration",
        "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "branches_analyzed": len(BRANCH_ANALYSIS),
        "branches": {}
    }
    
    summary = {
        "total_files": 0,
        "total_doc_files": 0,
        "total_links": 0,
        "broken_links": 0,
        "personas_found": set(),
        "richest_branch": None,
        "recommended_base": None
    }
    
    for branch_name, branch_data in BRANCH_ANALYSIS.items():
        print(f"Analyzing {branch_name}...")
        
        branch_analysis = {
            "sha": branch_data["sha"],
            "total_files": len(branch_data["files"]),
            "documentation_files": [],
            "personas": [],
            "structure": {},
            "links_analysis": {},
            "issues_found": []
        }
        
        # Count documentation files
        doc_files = [f for f in branch_data["files"] if any(f.endswith(ext) for ext in ['.md', '.txt', '.rst'])]
        branch_analysis["documentation_files"] = doc_files
        
        # Extract personas if present
        if "personas" in branch_data:
            personas = []
            for persona_path in branch_data["personas"]:
                persona_name = persona_path.replace("personas/", "").replace("/", "")
                personas.append(persona_name)
            branch_analysis["personas"] = personas
            summary["personas_found"].update(personas)
        
        # Analyze README content if available
        if "readme_content" in branch_data:
            content = branch_data["readme_content"]
            links_analysis = analyze_links_in_content(content, "README.md")
            branch_analysis["links_analysis"]["README.md"] = links_analysis
            
            # Count links
            total_links = (len(links_analysis["markdown_links"]) + 
                          len(links_analysis["direct_urls"]))
            branch_analysis["total_links"] = total_links
            branch_analysis["broken_links"] = len(links_analysis["broken_links"])
            
            summary["total_links"] += total_links
            summary["broken_links"] += len(links_analysis["broken_links"])
            
            # Check for specific issues
            if links_analysis["broken_links"]:
                for broken_link in links_analysis["broken_links"]:
                    branch_analysis["issues_found"].append({
                        "type": "broken_link",
                        "file": "README.md",
                        "details": broken_link
                    })
        
        # Special analysis for rich branches
        if "docs_files" in branch_data:
            branch_analysis["has_comprehensive_docs"] = True
            branch_analysis["docs_structure"] = branch_data["docs_files"]
            
        if "sample_app" in branch_data:
            branch_analysis["has_sample_app"] = True
            branch_analysis["sample_app_structure"] = branch_data["sample_app"]
        
        summary["total_files"] += branch_analysis["total_files"]
        summary["total_doc_files"] += len(branch_analysis["documentation_files"])
        
        analysis["branches"][branch_name] = branch_analysis
    
    # Determine the richest branch
    richest_score = 0
    for branch_name, branch_data in analysis["branches"].items():
        score = (len(branch_data.get("personas", [])) * 10 +
                len(branch_data.get("documentation_files", [])) * 5 +
                (10 if branch_data.get("has_comprehensive_docs") else 0) +
                (10 if branch_data.get("has_sample_app") else 0) -
                branch_data.get("broken_links", 0) * 2)
        
        if score > richest_score:
            richest_score = score
            summary["richest_branch"] = branch_name
            summary["recommended_base"] = branch_name
    
    analysis["summary"] = {
        "total_files": summary["total_files"],
        "total_doc_files": summary["total_doc_files"],
        "total_links": summary["total_links"],
        "broken_links": summary["broken_links"],
        "personas_found": list(summary["personas_found"]),
        "richest_branch": summary["richest_branch"],
        "recommended_base_branch": summary["recommended_base"]
    }
    
    return analysis

def generate_report(analysis):
    """Generate markdown report"""
    report = []
    
    report.append("# 🔍 Comprehensive Repository Analysis Report")
    report.append("## dev-ai-enable Repository - Cross-Branch Content Analysis")
    report.append("")
    report.append(f"**Repository**: `{analysis['repository']}`")
    report.append(f"**Analysis Date**: {analysis['analysis_timestamp']}")
    report.append(f"**Analysis Method**: {analysis['analysis_method']}")
    report.append("")
    
    # Executive Summary
    summary = analysis["summary"]
    report.append("## 📊 Executive Summary")
    report.append("")
    report.append(f"| Metric | Value |")
    report.append(f"|--------|-------|")
    report.append(f"| Branches Analyzed | {analysis['branches_analyzed']} |")
    report.append(f"| Total Files | {summary['total_files']} |")
    report.append(f"| Documentation Files | {summary['total_doc_files']} |")
    report.append(f"| Links Analyzed | {summary['total_links']} |")
    report.append(f"| Potential Issues | {summary['broken_links']} |")
    report.append(f"| Personas Found | {len(summary['personas_found'])} |")
    report.append("")
    
    if summary["personas_found"]:
        report.append("### 🎭 Personas Discovered:")
        for persona in sorted(summary["personas_found"]):
            report.append(f"- **{persona.title()}**")
        report.append("")
    
    # Branch Comparison
    report.append("## 🌳 Branch Comparison & Analysis")
    report.append("")
    
    for branch_name, branch_data in analysis["branches"].items():
        if branch_name == summary["recommended_base_branch"]:
            icon = "🥇"
            status = "RECOMMENDED BASE"
        elif branch_data.get("has_comprehensive_docs"):
            icon = "⭐"
            status = "RICH CONTENT"
        elif len(branch_data.get("personas", [])) > 0:
            icon = "🎭"
            status = "HAS PERSONAS"
        else:
            icon = "📝"
            status = "BASIC"
        
        report.append(f"### {icon} `{branch_name}` - {status}")
        report.append("")
        report.append(f"**SHA**: `{branch_data['sha']}`")
        report.append("")
        
        # Structure overview
        report.append("| Aspect | Details |")
        report.append("|--------|---------|")
        report.append(f"| Total Files | {branch_data['total_files']} |")
        report.append(f"| Documentation | {len(branch_data['documentation_files'])} files |")
        report.append(f"| Personas | {len(branch_data.get('personas', []))} |")
        report.append(f"| Has Docs Structure | {'✅' if branch_data.get('has_comprehensive_docs') else '❌'} |")
        report.append(f"| Has Sample App | {'✅' if branch_data.get('has_sample_app') else '❌'} |")
        report.append(f"| Link Issues | {branch_data.get('broken_links', 0)} |")
        report.append("")
        
        # Show personas if available
        if branch_data.get("personas"):
            report.append("**🎭 Personas in this branch:**")
            for persona in branch_data["personas"]:
                report.append(f"- {persona}")
            report.append("")
        
        # Show docs structure if available
        if branch_data.get("docs_structure"):
            report.append("**📚 Documentation structure:**")
            for doc in sorted(branch_data["docs_structure"][:10]):  # First 10
                report.append(f"- `{doc}`")
            if len(branch_data["docs_structure"]) > 10:
                report.append(f"- ... and {len(branch_data['docs_structure']) - 10} more")
            report.append("")
        
        # Show issues if any
        if branch_data.get("issues_found"):
            report.append("**⚠️ Issues found:**")
            for issue in branch_data["issues_found"][:5]:  # First 5
                report.append(f"- {issue['type'].title()}: {issue['details'].get('reason', 'Unknown issue')}")
            report.append("")
        
        report.append("---")
        report.append("")
    
    # Consolidation Recommendations
    report.append("## 💡 Dev-AI Repository Consolidation Plan")
    report.append("")
    
    recommended = summary["recommended_base_branch"]
    if recommended:
        report.append(f"### 🎯 Recommended Strategy")
        report.append("")
        report.append(f"**Base Branch**: `{recommended}`")
        
        recommended_data = analysis["branches"][recommended]
        report.append("")
        report.append("**Why this branch?**")
        report.append(f"- ✅ Most comprehensive content ({recommended_data['total_files']} files)")
        if recommended_data.get("has_comprehensive_docs"):
            report.append("- ✅ Complete documentation structure")
        if recommended_data.get("has_sample_app"):
            report.append("- ✅ Sample application included")
        if recommended_data.get("personas"):
            report.append(f"- ✅ {len(recommended_data['personas'])} personas defined")
        report.append("")
    
    report.append("### 📋 Step-by-Step Consolidation Plan")
    report.append("")
    report.append("1. **🎯 Create new dev-ai repository**")
    report.append(f"   - Use `{recommended}` as the foundation")
    report.append("   - Copy complete file structure")
    report.append("")
    
    report.append("2. **🔧 Fix identified issues**")
    if summary["broken_links"] > 0:
        report.append(f"   - Address {summary['broken_links']} potential link issues")
        report.append("   - Update file references to match new structure")
    else:
        report.append("   - No major link issues detected")
    report.append("")
    
    report.append("3. **📚 Merge unique content from other branches**")
    for branch_name, branch_data in analysis["branches"].items():
        if branch_name != recommended and branch_data["total_files"] > 2:  # More than just LICENSE + README
            report.append(f"   - Review `{branch_name}` for unique content")
    report.append("")
    
    report.append("4. **🎭 Organize persona content**")
    if summary["personas_found"]:
        report.append("   - Ensure all personas are properly documented:")
        for persona in sorted(summary["personas_found"]):
            report.append(f"     - {persona}")
    report.append("")
    
    report.append("5. **🔍 Implement quality assurance**")
    report.append("   - Add link validation CI/CD pipeline")
    report.append("   - Create documentation standards")
    report.append("   - Set up automated testing for sample applications")
    report.append("")
    
    # File manifest
    report.append("## 📦 Complete File Manifest")
    report.append("")
    
    all_files = set()
    for branch_data in analysis["branches"].values():
        all_files.update(branch_data["documentation_files"])
        if branch_data.get("docs_structure"):
            all_files.update(branch_data["docs_structure"])
        if branch_data.get("sample_app_structure"):
            all_files.update(branch_data["sample_app_structure"])
    
    report.append("### 📁 Files to consolidate:")
    for file_path in sorted(all_files):
        report.append(f"- `{file_path}`")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("## 🎯 Next Steps")
    report.append("")
    report.append("1. **Create dev-ai repository** with the recommended base structure")
    report.append("2. **Copy and organize** all identified content")
    report.append("3. **Fix broken links** and update references")
    report.append("4. **Test sample applications** and documentation")
    report.append("5. **Implement CI/CD** for ongoing quality assurance")
    report.append("")
    report.append("*This analysis provides a roadmap for successful repository consolidation.*")
    
    return "\n".join(report)

def main():
    print("🚀 Starting manual comprehensive analysis...")
    print("Using data gathered from GitHub MCP server exploration")
    print("")
    
    # Generate analysis
    analysis = generate_comprehensive_analysis()
    
    # Generate report
    report = generate_report(analysis)
    
    # Save files
    json_path = Path("FINAL_COMPREHENSIVE_ANALYSIS.json")
    with open(json_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    md_path = Path("FINAL_COMPREHENSIVE_ANALYSIS.md")
    with open(md_path, 'w') as f:
        f.write(report)
    
    print(f"{'='*80}")
    print("🎯 COMPREHENSIVE ANALYSIS COMPLETE")
    print(f"{'='*80}")
    
    summary = analysis["summary"]
    print(f"📊 Final Summary:")
    print(f"   - Repository: {analysis['repository']}")
    print(f"   - Branches analyzed: {analysis['branches_analyzed']}")
    print(f"   - Total files: {summary['total_files']}")
    print(f"   - Documentation files: {summary['total_doc_files']}")
    print(f"   - Personas found: {len(summary['personas_found'])}")
    print(f"   - Recommended base: {summary['recommended_base_branch']}")
    
    if summary["personas_found"]:
        print(f"\n🎭 Personas discovered:")
        for persona in sorted(summary["personas_found"]):
            print(f"   - {persona}")
    
    print(f"\n📄 Reports generated:")
    print(f"   - JSON: {json_path}")
    print(f"   - Markdown: {md_path}")
    
    print(f"\n✅ Ready for dev-ai repository creation and consolidation!")

if __name__ == "__main__":
    main()