// extract_graph.js
// npm i solidity-parser-antlr
//node extract_graph.js contract.sol

const parser = require('solidity-parser-antlr');
const fs = require('fs');
const path = require('path');

if (process.argv.length < 3) {
  console.error("Usage: node extract_graph.js <contract.sol>");
  process.exit(1);
}

const filename = process.argv[2];
const src = fs.readFileSync(filename, 'utf8');

let ast;
try {
  ast = parser.parse(src, { range: true });
} catch (e) {
  console.error("Parse error:", e.message);
  process.exit(2);
}

// maps
const functions = {};    // name -> node info {name, visibility, node}
const calls = {};        // name -> Set(calledNames)
const externalCalls = {}; // name -> array of external call descriptions
const stateChange = {};  // name -> boolean (assignment to state var)

function fnName(node) {
  if (!node) return "<unknown>";
  if (node.type === 'FunctionDefinition') {
    if (node.name) return node.name;
    if (node.isConstructor) return "constructor";
    if (node.isFallback) return "fallback";
    if (node.isReceive) return "receive";
    return "<anon_fn@" + (node.range ? node.range[0] : "?") + ">";
  }
  return "<node>";
}

// 1) Collect functions
parser.visit(ast, {
  FunctionDefinition(node) {
    const name = fnName(node);
    functions[name] = {
      name,
      visibility: node.visibility,
      node
    };
    calls[name] = new Set();
    externalCalls[name] = [];
    stateChange[name] = false;
  }
});

// helper: current function stack for nested visits
let currentFunc = null;
parser.visit(ast, {
  FunctionDefinition(node) {
    const name = fnName(node);
    const prev = currentFunc;
    currentFunc = name;
    // visit body manually to detect calls/assignments
    parser.visit(node, {
      FunctionCall(callNode) {
        if (!currentFunc) return;
        // direct identifier e.g., foo()
        if (callNode.expression.type === 'Identifier') {
          calls[currentFunc].add(callNode.expression.name);
        } else if (callNode.expression.type === 'MemberAccess') {
          // something.foo() or externalContract.foo()
          const member = callNode.expression.memberName;
          // consider internal member names as possible functions too
          if (member) {
            calls[currentFunc].add(member);
          }
          // detect low-level external calls
          const lowLevel = ['call','delegatecall','staticcall','callcode','transfer','send'];
          if (lowLevel.includes(member)) {
            externalCalls[currentFunc].push({
              type: member,
              raw: parser.visit(callNode, {}) || null
            });
          }
        }
      },
      Assignment(left, right) {
        // any assignment in function body -> mark possible state change
        if (currentFunc) stateChange[currentFunc] = true;
      },
      AssignmentExpression(node) {
        if (currentFunc) stateChange[currentFunc] = true;
      },
      StateVariableDeclaration(node) {
        // ignore: declarations
      }
    }, true);
    currentFunc = prev;
  }
}, true);

// Build nodes and links for graph.json
const nodes = Object.keys(functions).map(n => ({ id: n, visibility: functions[n].visibility || null, stateChange: stateChange[n], extCalls: externalCalls[n].length }));
const links = [];
for (const [srcName, setCalls] of Object.entries(calls)) {
  for (const tgt of setCalls) {
    // only add link if target is known function, otherwise still add as external node
    const exists = functions[tgt] ? true : false;
    links.push({ source: srcName, target: tgt, internal: exists });
  }
}

// Add external nodes for calls which are not functions in the same contract
const existingIds = new Set(nodes.map(n => n.id));
for (const l of links) {
  if (!existingIds.has(l.target)) {
    nodes.push({ id: l.target, external: true, visibility: null, stateChange: false, extCalls: 0 });
    existingIds.add(l.target);
  }
}

// helper: detect cycles via DFS
function detectCycles() {
  const visited = {};
  const stack = {};
  const cycles = [];

  function dfs(u, path) {
    visited[u] = true;
    stack[u] = true;
    path.push(u);
    const outs = (calls[u] ? Array.from(calls[u]) : []);
    for (const v of outs) {
      if (!visited[v]) {
        dfs(v, path);
      } else if (stack[v]) {
        // found cycle: slice path from v to end
        const idx = path.indexOf(v);
        if (idx >= 0) cycles.push(path.slice(idx).concat(v));
      }
    }
    stack[u] = false;
    path.pop();
  }

  for (const u of Object.keys(calls)) {
    if (!visited[u]) dfs(u, []);
  }
  return cycles;
}

const cycles = detectCycles();

// simple critical paths: all paths from public/external functions that end in an external call or state-change
const criticalPaths = [];
function findPaths(start, visited = new Set(), path = []) {
  visited.add(start);
  path.push(start);
  // if this function does external low-level call or stateChange -> record path
  if ((externalCalls[start] && externalCalls[start].length > 0) || stateChange[start]) {
    criticalPaths.push([...path]);
  }
  for (const nxt of (calls[start] ? Array.from(calls[start]) : [])) {
    if (!visited.has(nxt)) {
      findPaths(nxt, visited, path);
    } else {
      // allow revisiting external unknown nodes but skip cycles
    }
  }
  path.pop();
  visited.delete(start);
}

// start from public or external functions
for (const [fname, meta] of Object.entries(functions)) {
  if (meta.visibility === 'public' || meta.visibility === 'external') {
    findPaths(fname);
  }
}

// write graph.json
const out = { nodes, links, cycles, criticalPaths };
fs.writeFileSync('graph.json', JSON.stringify(out, null, 2));
console.log("Wrote graph.json");
console.log(`Functions: ${Object.keys(functions).length}, nodes: ${nodes.length}, links: ${links.length}`);
console.log(`Cycles found: ${cycles.length}, Critical paths found: ${criticalPaths.length}`);
