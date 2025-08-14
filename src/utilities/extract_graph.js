// extract_graph.js
// Usage: node extract_graph.js <input.sol> <output_graph.json>

const parser = require('solidity-parser-antlr');
const fs = require('fs');

if (process.argv.length < 4) {
  console.error("Usage: node extract_graph.js <input.sol> <output_graph.json>");
  process.exit(1);
}

const inFile = process.argv[2];
const outFile = process.argv[3];

const src = fs.readFileSync(inFile, 'utf8');

let ast;
try {
  ast = parser.parse(src, { range: true });
} catch (e) {
  console.error("Parse error:", e.message);
  process.exit(2);
}

// maps
const functions = {};
const calls = {};
const externalCalls = {};
const stateChange = {};

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

// 1) collect functions
const parserVisit = parser.visit || parser; // safety
parser.visit(ast, {
  FunctionDefinition(node) {
    const name = fnName(node);
    functions[name] = { name, visibility: node.visibility, node };
    calls[name] = new Set();
    externalCalls[name] = [];
    stateChange[name] = false;
  }
});

// 2) collect calls / state changes
let currentFunc = null;
parser.visit(ast, {
  FunctionDefinition(node) {
    const name = fnName(node);
    const prev = currentFunc;
    currentFunc = name;

    parser.visit(node, {
      FunctionCall(callNode) {
        if (!currentFunc) return;
        if (callNode.expression.type === 'Identifier') {
          calls[currentFunc].add(callNode.expression.name);
        } else if (callNode.expression.type === 'MemberAccess') {
          const member = callNode.expression.memberName;
          if (member) calls[currentFunc].add(member);
          const lowLevel = ['call','delegatecall','staticcall','callcode','transfer','send'];
          if (lowLevel.includes(member)) {
            externalCalls[currentFunc].push({ type: member });
          }
        }
      },
      Assignment() {
        if (currentFunc) stateChange[currentFunc] = true;
      },
      AssignmentExpression() {
        if (currentFunc) stateChange[currentFunc] = true;
      }
    }, true);

    currentFunc = prev;
  }
}, true);

// 3) build nodes/edges
const nodes = Object.keys(functions).map(n => ({
  id: n,
  visibility: functions[n].visibility || null,
  stateChange: !!stateChange[n],
  extCalls: (externalCalls[n] || []).length
}));

const edges = [];
for (const [srcName, setCalls] of Object.entries(calls)) {
  for (const tgt of setCalls) {
    const internal = !!functions[tgt];
    edges.push({ source: srcName, target: tgt, internal });
  }
}

// 4) add external nodes (if any edge points to unknown target)
const ids = new Set(nodes.map(n => n.id));
for (const e of edges) {
  if (!ids.has(e.target)) {
    nodes.push({ id: e.target, external: true, visibility: null, stateChange: false, extCalls: 0 });
    ids.add(e.target);
  }
}

const out = { nodes, edges };
fs.writeFileSync(outFile, JSON.stringify(out, null, 2));
console.log(`Wrote graph: ${outFile}   (nodes: ${nodes.length}, edges: ${edges.length})`);
