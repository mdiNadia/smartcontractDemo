// graph_to_steps.js
// تبدیل گراف (JSON) به لیست مراحل متنی

const fs = require("fs");

// گرفتن مسیر فایل‌های ورودی و خروجی از خط فرمان
const [inputPath, outputPath] = process.argv.slice(2);

if (!inputPath || !outputPath) {
    console.error("Usage: node graph_to_steps.js <input_graph.json> <output_steps.txt>");
    process.exit(1);
}

// خواندن و پارس کردن فایل JSON
let rawData, graphData;
try {
    rawData = fs.readFileSync(inputPath, "utf-8");
    graphData = JSON.parse(rawData);
} catch (err) {
    throw new Error(`❌ Error reading or parsing input file: ${err.message}`);
}

// تشخیص ساختار داده (nodes و edges)
let nodes = [];
let edges = [];

if (Array.isArray(graphData)) {
    nodes = graphData.filter(item => item.id);
    edges = graphData.filter(item => item.source && item.target);
} else if (graphData.nodes && graphData.edges) {
    nodes = graphData.nodes;
    edges = graphData.edges;
} else if (graphData.nodes && graphData.links) {
    nodes = graphData.nodes;
    edges = graphData.links;
} else {
    throw new Error("❌ Invalid graph structure: Expected nodes[] and edges[] or links[]");
}

if (!nodes.length) {
    throw new Error("❌ No nodes found in the input graph.");
}

// پیدا کردن گره‌های ریشه
const targetIds = new Set(edges.map(e => e.target));
let roots = nodes.filter(n => !targetIds.has(n.id));
if (!roots.length) roots = [...nodes];

// الگوریتم DFS برای ساخت لیست مراحل
let visited = new Set();
let steps = [];

function dfs(node, depth = 0) {
    if (visited.has(node.id)) return;
    visited.add(node.id);

    // توضیح کوتاه برای هر گره
    let description = `${" ".repeat(depth * 2)}[${node.label || node.name || node.id}]`;
    if (node.stateChanges) description += ` — State changes: ${JSON.stringify(node.stateChanges)}`;
    if (node.externalCalls && node.externalCalls.length) description += ` — External calls: ${node.externalCalls.length}`;
    steps.push(description);

    // رفتن به فرزندان
    edges
        .filter(e => e.source === node.id)
        .forEach(e => {
            const child = nodes.find(n => n.id === e.target);
            if (child) dfs(child, depth + 1);
        });
}

// اجرا از همه‌ی ریشه‌ها
roots.forEach(root => dfs(root));

// اضافه کردن گره‌های بی‌اتصال
nodes.forEach(n => {
    if (!visited.has(n.id)) {
        steps.push(`[${n.label || n.name || n.id}] — (Unconnected node)`);
    }
});

// نوشتن خروجی در فایل
try {
    fs.writeFileSync(outputPath, steps.join("\n"), "utf-8");
    console.log(` Wrote steps: ${outputPath}   (lines: ${steps.length})`);
} catch (err) {
    throw new Error(` Error writing output file: ${err.message}`);
}
