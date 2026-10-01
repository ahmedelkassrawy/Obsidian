"""Apply the vault's graph-view color groups and hub filter.

Run with Obsidian CLOSED (an open Obsidian keeps its own copy and overwrites this file):
  python _scripts/graph_colors.py
"""
import json, os

p = os.path.join(os.path.dirname(__file__), '..', '.obsidian', 'graph.json')
g = json.load(open(p, encoding='utf8'))

def c(h): return {"a": 1, "rgb": int(h, 16)}

g["search"] = "-path:_hubs -path:_MOC -path:_templates -path:_scripts -path:Excalidraw -path:tmp"
g["colorGroups"] = [
    {"query": "path:Concepts", "color": c("F2B705")},
    {"query": 'path:"Ai & ML" OR path:GenAi OR path:LLM OR path:DEPI OR path:MiniRAG OR path:"Claude Code Learning"', "color": c("9B5DE5")},
    {"query": "path:Database OR path:SQL", "color": c("2EC4B6")},
    {"query": "path:Backend OR path:API OR path:Deployment OR path:Linux", "color": c("3A86FF")},
    {"query": 'path:DSA OR path:CPP OR path:STL OR path:"Problem Solving" OR path:OOP OR path:Python OR path:JS', "color": c("FB5607")},
]
g["showOrphans"] = False
json.dump(g, open(p, "w", encoding='utf8'), indent=2)
print("graph colors applied")
